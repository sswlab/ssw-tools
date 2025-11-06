"""
SDO/AIA Data Preparation Code for Machine Learning
@author: Mingyu Jeon (https://mgjeon.com, mgjeon@khu.ac.kr)
References:
1) https://github.com/RobertJaro/InstrumentToInstrument/
"""

import argparse
from pathlib import Path
import astropy.units as u
from astropy.table import QTable
from astropy.coordinates import SkyCoord
from aiapy.calibrate import update_pointing, degradation
from sunpy.map import Map
import numpy as np
import warnings; warnings.filterwarnings("ignore")
from tqdm import tqdm
from loguru import logger

def nan_to_num_clip(data, nan=0, a_min=0, a_max=None):
    data = np.nan_to_num(data, nan=nan)
    data = np.clip(data, a_min=a_min, a_max=a_max)
    return data

def register_ml(smap, *, resolution=2048, padding_factor=0.2):
    data = nan_to_num_clip(smap.data.astype(np.float32), nan=0, a_min=0)
    smap = Map(data, smap.meta)
    r_obs_pix = smap.rsun_obs / smap.scale[0]
    r_obs_pix = (1 + padding_factor) * r_obs_pix
    scale_factor = resolution / (2 * r_obs_pix.value)
    smap = smap.rotate(recenter=True, scale=scale_factor, missing=0, order=3, method='scipy')
    frame_arcsec = ((resolution / 2) * smap.scale[0].value) * u.arcsec
    smap = smap.submap(
        bottom_left = SkyCoord(-frame_arcsec, -frame_arcsec, frame=smap.coordinate_frame),
        top_right   = SkyCoord( frame_arcsec,  frame_arcsec, frame=smap.coordinate_frame)
    )
    excess_x = smap.data.shape[0] - resolution
    excess_y = smap.data.shape[1] - resolution
    smap = smap.submap(
        bottom_left = [excess_x // 2, excess_y // 2] * u.pix,
        top_right   = [excess_x // 2 + resolution - 1, excess_y // 2 + resolution - 1] * u.pix
    )
    if smap.data.shape[0] < resolution or smap.data.shape[1] < resolution:
        data = smap.data
        new_data = np.zeros((resolution, resolution))
        pad_x = (resolution - data.shape[0]) // 2
        pad_y = (resolution - data.shape[1]) // 2
        new_data[pad_x:pad_x + data.shape[0], pad_y:pad_y + data.shape[1]] = data
        smap = Map(new_data, smap.meta)
    smap.meta['BITPIX'] = -32
    smap.meta['LVL_NUM'] = 2.0
    smap.meta['R_SUN'] = smap.rsun_obs.value / smap.meta['CDELT1']
    smap.meta['CRPIX1'] = resolution // 2 + 0.5
    smap.meta['CRPIX2'] = resolution // 2 + 0.5
    smap.meta['CRVAL1'] = 0
    smap.meta['CRVAL2'] = 0
    smap.meta["PC1_1"] = 1
    smap.meta["PC1_2"] = 0
    smap.meta["PC2_1"] = 0
    smap.meta["PC2_2"] = 1
    smap.meta['CROTA'] = 0
    return smap


def degradation_correction(smap, *, correction_table):
    d = degradation(
        smap.wavelength,
        smap.date,
        correction_table=correction_table,
    )
    smap = smap / d
    smap.meta['deg_corr'] = d.item().value
    return smap


def aia_prep_ml(aia_map, *, pointing_table=None, correction_table=None,
                resolution=1024, padding_factor=0.1):
    """
    1. Pointing correction
    2. Registration
       NaN to 0, Negative to 0
       Cast to float 32
       Rotate Solar north up
       Image center = Solar center
       resolution/2 = (1 + padding_factor) R_sun
    3. Degradation correction
    4. Exposure normalization [DN/s]
    """
    # 1.
    if pointing_table is not None:
        aia_map = update_pointing(aia_map, pointing_table=pointing_table)
    # 2.
    aia_map = register_ml(aia_map, resolution=resolution, padding_factor=padding_factor)
    # 3.
    if correction_table is not None:
        aia_map = degradation_correction(aia_map, correction_table=correction_table)
    # 4.
    aia_map /= aia_map.exposure_time
    return aia_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_raw', default='F:/data/raw/sdo/aia', type=str, help='Path to raw data')
    parser.add_argument('--path_prep', default='F:/data/prep/sdo/aia', type=str, help='Path to prepared data')
    parser.add_argument('--resolution', default=1024, type=int, help='Resolution of the output image')
    parser.add_argument('--padding_factor', default=0.1, type=float, help='Padding factor for image registration')
    args = parser.parse_args()

    ROOT = Path(args.path_raw)
    ROOT_PREP = Path(args.path_prep)

    logger.remove()
    logger.add(ROOT_PREP / 'aia_prep.log')

    pointing_table = QTable.read(ROOT_PREP / 'pointing_table.ecsv', format='ascii.ecsv')
    correction_table = QTable.read(ROOT_PREP / 'correction_table.ecsv', format='ascii.ecsv')

    files = list(ROOT.glob('**/*.fits'))
    for f in tqdm(files):
        fn_prep = ROOT_PREP / f.relative_to(ROOT)
        if not fn_prep.exists():
            fn_prep.parent.mkdir(exist_ok=True, parents=True)
            logger.info(f'Processing {f} -> {fn_prep}')
            aia_map = Map(f)
            try:
                aia_map = aia_prep_ml(
                    aia_map, 
                    pointing_table=pointing_table, 
                    correction_table=correction_table,
                    resolution=args.resolution,
                    padding_factor=args.padding_factor,
                )
                aia_map.save(fn_prep)
            except Exception as e:
                logger.error(f"Error processing {fn_prep}: {e}")
                continue