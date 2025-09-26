import json
import numpy as np
import pyLCR

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def prepare_ts(lc):
    ts_list = []
    for met, ts in zip(lc.met, lc.ts):
        ts_list.append([int(met), ts])
    return ts_list

def prepare_flux(lc):
    flux_list = []
    for met, flux in zip(lc.met_detections, lc.flux):
        flux_list.append([int(met), flux])
    return flux_list

def prepare_flux_upper_limits(lc):
    flux_upper_limits_list = []
    for met, flux_upper_limit in zip(lc.met_upperlimits, lc.flux_upper_limits):
        flux_upper_limits_list.append([int(met), flux_upper_limit])
    return flux_upper_limits_list

def prepare_flux_error(lc):
    flux_error_list = []
    for met, flux_error in zip(lc.met_detections, lc.flux_error):
        flux_error_list.append([int(met)] + list(flux_error))
    return flux_error_list

def prepare_photon_index(lc):
    photon_index_list = []
    for met, photon_index in zip(lc.met_detections, lc.photon_index):
        photon_index_list.append([int(met), photon_index])
    return photon_index_list

def prepare_photon_index_interval(lc):
    photon_index_interval_list = []
    for met, photon_index_interval in zip(lc.met_detections, lc.photon_index_interval):
        photon_index_interval_list.append([int(met), photon_index_interval, photon_index_interval])
    return photon_index_interval_list

def prepare_fit_tolerance(lc):
    fit_tolerance_list = []
    for met, fit_tolerance in zip(lc.met, lc.fit_tolerance):
        fit_tolerance_list.append([int(met), fit_tolerance])
    return fit_tolerance_list

def prepare_fit_convergence(lc):
    fit_convergence_list = []
    for met, fit_convergence in zip(lc.met, lc.fit_convergence):
        fit_convergence_list.append([int(met), fit_convergence])
    return fit_convergence_list

def prepare_dlogl(lc):
    return list(lc.dlogl)

def prepare_EG(lc):
    return list(lc.EG)

def prepare_GAL(lc):
    return list(lc.GAL)

def prepare_bin_id(lc):
    return list(lc.bin_id)

def prepare_dict(lc):
    json_dict = {
        'ts': prepare_ts(lc),
        'flux': prepare_flux(lc),
        'flux_upper_limits': prepare_flux_upper_limits(lc),
        'flux_error': prepare_flux_error(lc),
        'photon_index': prepare_photon_index(lc),
        'photon_index_interval': prepare_photon_index_interval(lc),
        'fit_tolerance': prepare_fit_tolerance(lc),
        'fit_convergence': prepare_fit_convergence(lc),
        'dlogl': prepare_dlogl(lc),
        'EG': prepare_EG(lc),
        'GAL': prepare_GAL(lc),
        'bin_id': prepare_bin_id(lc)
    }
    return json_dict

def make_dict_for_source(
    source_name,
    cadence='monthly',
    flux_type='energy',
    index_type='fixed',
    ts_min=4,
):
    lc = pyLCR.getLightCurve(
        source_name,
        cadence=cadence,
        flux_type=flux_type,
        index_type=index_type,
        ts_min=ts_min
    )
    if lc is None:
        return dict()
    return prepare_dict(lc)

def save_json_for_source(
    source_name,
    cadence='monthly',
    flux_type='energy',
    index_type='fixed',
    ts_min=4,
    save_path="",
):
    json_dict = make_dict_for_source(
        source_name,
        cadence=cadence,
        flux_type=flux_type,
        index_type=index_type,
        ts_min=ts_min
    )
    if not json_dict:
        return
    source_name = source_name.split(" ")[0] + "_20" + source_name.split(" ")[-1]
    filename = f"{save_path}/{source_name}_{cadence}_{flux_type}_{index_type}_tsmin{ts_min}"
    
    with open(f'{filename}.json', 'w') as f:
        json.dump(json_dict, f, cls=NpEncoder)