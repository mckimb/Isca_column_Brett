# NOTE: this script was created by combining aspects of run_column.py, gcm_testrrtm.py, and socrates_ape_aquaplanet.py
import os
import numpy as np
from isca import SocratesCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

NCORES = 16

# compile code
base_dir = os.path.dirname(os.path.realpath(__file__))
cb = SocratesCodeBase.from_directory(GFDL_BASE) # NOTE: column model uses SocColumnCodeBase
cb.compile()

# changeable parameters
S0_add = 0. # S0 =  1360
sst_pert = 0
co2_multiply = float(1) # PI = 280
# co2_string = '1'
# ml_depth = float(1e10)
# sst = 290.
# ml_temp = sst

# exp = Experiment('ape_soc_'+str(sst_pert)+'K_take5_atmos1440_rad7200_7bands', codebase=cb)
# exp = Experiment('soc_'+str(sst_pert)+'K'+'50Wm2'+'_take5_atmos1440_rad7200_7bands', codebase=cb)
exp = Experiment('ape_soc_testing_6_lowres_diffusivityra', codebase=cb)

exp.clear_rundir()
#Tell model how to write diagnostics
# NOTE: where will I store this data?
diag = DiagTable()
# diag.add_file('atmos_monthly', 30, 'days', time_units='days')
diag.add_file('atmos_yearly', 360, 'days', time_units='days')

#Tell model which diagnostics to write, NOTE: I'm not sure I need all of these. Some will need to be changed from column and I might need to add new ones for the gcm
# vertical grid
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('atmosphere', 'height', time_avg=True)
# surface variables
diag.add_field('mixed_layer', 't_surf', time_avg=True)
diag.add_field('mixed_layer', 'flux_lhe', time_avg=True)
diag.add_field('mixed_layer', 'flux_t', time_avg=True)
diag.add_field('atmosphere',   'flux_u', time_avg=True) #tauu - zonal component of stress
diag.add_field('atmosphere',   'flux_v', time_avg=True) #tauv
# # near surface variables
# diag.add_field('atmosphere', 'temp_2m', time_avg=True)
# diag.add_field('atmosphere', 'sphum_2m', time_avg=True)
# diag.add_field('atmosphere', 'u_10m', time_avg=True)
# diag.add_field('atmosphere', 'v_10m', time_avg=True)
# radiative fluxes and tendencies
diag.add_field('socrates', 'soc_tdt_lw', time_avg=True)
diag.add_field('socrates', 'soc_tdt_sw', time_avg=True)
diag.add_field('socrates', 'soc_tdt_rad', time_avg=True)
# diag.add_field('socrates', 'soc_surf_flux_lw', time_avg=True)
# diag.add_field('socrates', 'soc_surf_flux_sw', time_avg=True)
# diag.add_field('socrates', 'soc_surf_flux_lw_down', time_avg=True)
# diag.add_field('socrates', 'soc_surf_flux_sw_down', time_avg=True)
diag.add_field('socrates', 'soc_olr', time_avg=True)
diag.add_field('socrates', 'soc_toa_sw', time_avg=True)
# diag.add_field('socrates', 'soc_toa_sw_down', time_avg=True)
diag.add_field('socrates', 'soc_co2', time_avg=True)
# diag.add_field('socrates', 'soc_spectral_olr', time_avg=True)
# atmospheric variables and tendencies
diag.add_field('atmosphere', 'precipitation', time_avg=True)
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'vor', time_avg=True)
diag.add_field('dynamics', 'div', time_avg=True)
diag.add_field('atmosphere', 'dt_ug_diffusion', time_avg=True)
diag.add_field('atmosphere', 'dt_vg_diffusion', time_avg=True)
diag.add_field('atmosphere', 'dt_tg_diffusion', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_diffusion', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_convection', time_avg=True)
diag.add_field('atmosphere', 'dt_tg_convection', time_avg=True)
diag.add_field('atmosphere', 'dt_tg_condensation', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_condensation', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_total', time_avg=True)
diag.add_field('atmosphere', 'pbl_height', time_avg=True)
diag.add_field('atmosphere', 'rh', time_avg=True)
diag.add_field('atmosphere', 'convection_rain', time_avg=True)
diag.add_field('atmosphere', 'cape', time_avg=True)
diag.add_field('atmosphere', 'cin', time_avg=True)
diag.add_field('atmosphere', 'pLCL', time_avg=True)
diag.add_field('atmosphere', 'pLZB', time_avg=True)
diag.add_field('atmosphere', 'kLZB', time_avg=True)
diag.add_field('atmosphere', 'pshallow', time_avg=True)
diag.add_field('atmosphere', 'convflag', time_avg=True)
diag.add_field('atmosphere', 'shallower_flag', time_avg=True)
diag.add_field('atmosphere', 'deep_gorman_flag', time_avg=True)
diag.add_field('atmosphere', 'deep_frierson_flag', time_avg=True)
diag.add_field('atmosphere', 'noconvflag', time_avg=True)
diag.add_field('atmosphere', 'precip_level_DNE_flag', time_avg=True)
diag.add_field('atmosphere', 'precip_level_DNE_ktop_flag', time_avg=True)
diag.add_field('atmosphere', 'precip_both_negative_flag', time_avg=True)
#needed for eddy flux terms
diag.add_field('dynamics', 'ucomp_vcomp', time_avg=True)
diag.add_field('dynamics', 'sphum_v', time_avg=True)
diag.add_field('dynamics', 'vcomp_temp', time_avg=True)

exp.diag_table = diag

#Define values for the 'core' namelist
exp.namelist = namelist = Namelist({
    'main_nml':{
     'days'   : 360,
     'hours'  : 0,
     'minutes': 0,
     'seconds': 0,
     'dt_atmos': 1440, # the column model is 3600
     'current_date' : [1,1,1,0,0,0],
     'calendar' : 'thirty_day'
    },
    'socrates_rad_nml':{
        'stellar_constant': 1370.+S0_add,
        'lw_spectral_filename': '/home/links/bam218/Isca/src/atmos_param/socrates/src/trunk/data/spectra/ga7/sp_lw_ga7',
        'sw_spectral_filename': '/home/links/bam218/Isca/src/atmos_param/socrates/src/trunk/data/spectra/ga7/sp_sw_ga7',
        'dt_rad': 7200,
        'store_intermediate_rad': True,
        'chunk_size': NCORES,
        'do_read_ozone': False,
        # 'solday': 90., # turn off seasonal cycle - diurnal by default (NOTE: I'm not sure if I need this option or not)
        'inc_co2': True,
        'co2_ppmv': 280.*co2_multiply,
        'inc_o3': False,
        'inc_o2': False,
        'account_for_effect_of_ozone': False,
        'frierson_solar_rad': True, # NOTE: should I specify annual averag insolation?
        'store_intermediate_rad':True, # NOTE: I'm not sure if I need this option or not
        'tidally_locked': False,
        'use_pressure_interp_for_half_levels': False, # NOTE: I'm not sure if I need this option or not
    },
    'idealized_moist_phys_nml':{
        'do_damping': True, # NOTE: this is false in run_column.py
        'turb': True,
        'mixed_layer_bc': True,
        'do_virtual': False,
        'do_simple': True,
        'roughness_mom': 3.21e-05,
        'roughness_heat': 3.21e-05,
        'roughness_moist': 3.21e-05,
        'two_steam_gray': False,
        'do_rrtm_radiation': False,
        'do_socrates_radiation': True,
        'convection_scheme': 'SIMPLE_BETTS_MILLER',
    },
    'vert_turb_driver_nml':{
        'do_mellor_yamada': False,      # default: True
        'do_diffusivity': True,         # default: False
        'do_simple': True,              # default: False
        'constant_gust': 0.0,           # default: 1.0
        'use_tau': False,
    },
    'diffusivity_nml':{
        'fixed_depth': True, # default: False
        'do_entrain': False, # NOTE: this is not specified in run_column.py
        'do_simple': True, # NOTE: this is not specified in run_column.py
    },
    'surface_flux_nml':{
        'use_virtual_temp': False, # NOTE: this is True in run_column.py and says to use virtua temperature for BL stability
        'do_simple': True,
        'old_dtaudv': True,
    },
    'atmosphere_nml':{
        'idealized_moist_model': True
    },
    'mixed_layer_nml':{
        'tconst': 285., # NOTE: I set this to my specified SST in run_column.py
        'prescribe_initial_dist': False, # NOTE: this if false in run_column.py but I think I'm setting it true here because of _sst
        'evaporation': True,
        'depth': 2.5, # NOTE: I set this to 1e10 in run_column.py, but I don't think I need to do that here because of do_ape_sst
        'albedo_value': 0.2, # NOTE: run_column.py uses 0.20, but Jucker and Gerber 2017 uses 0.38,
        'do_ape_sst': True, # NOTE: this is obviously not set in run_column.py
        # NOTE: think about ways to modify the SSTs using do_sc_sst and sst_file, see: https://execlim.github.io/Isca/modules/mixedlayer.html
        'sst_pert': sst_pert # adds a constant amount to ape_sst formula
    },
    'qe_moist_convection_nml':{
        'rhbm': 0.7,  # rh criterion for convection
        'Tmin': 100., # min temperature for convection scheme look up tables
        'Tmax': 350., # max temperature for convection scheme look up tables
    },
    'lscale_cond_nml':{
        'do_simple': True, # only rain (no ice)
        'do_evap': True, # don't reevaporate falling precipitation, NOTE: ask Nadir about this one
    },
    'sat_vapor_pres_nml':{
        'do_simple': True,
        # 'construct_table_wrt_liq_and_ice': True, # NOTE: this option isn't specified in run_column.py
    },
    'damping_driver_nml':{ # NOTE: this namelist isn't necessary for run_column.py because damping is turned off there
        'do_rayleigh': True,
        'trayfric': -0.5, # neg value: time in days
        'sponge_pbottom': 50., # setting the lower pressure bounary (Pa) for the model sponge layer
        'do_conserve_energy': True,
    },
    # FMS Framework configuration
    'diag_manager_nml':{
        'mix_snapshot_average_fields': False # time avg fields are labelled with time in middle of window
    },
    'fms_nml':{
        'domains_stack_size': 600000 # default: 0
    },

    'fms_io_nml':{
        'threading_write': 'single',    # default: multi
        'fileset_write': 'single',      # default: multi
    },
    'spectral_dynamics_nml':{ # NOTE: this namelist isn't necessary in run_column.py because it's replaced by column_nml
        'damping_order': 4,
        'water_correction_limit': 200.e2,
        'reference_sea_level_press': 1.0e5,
        'num_levels': 25,
        'valid_range_t': [100., 800.],
        'initial_sphum': [1.e-3], # default is 1.e-6 for gcm
        'vert_coord_option': 'uneven_sigma',
        'surf_res': 0.2,
        'scale_heights': 11.0,
        'exponent': 7.0,
        'robert_coeff': 0.03, # NOTE: this is 0.0 in run_column.py because no leapfrog scheme is needed when there are no dynamics
        # 'make_symmetric': True, # Make model zonally symmetric
    },
    # 'astronomy_nml':{ NOTE: I'm not sure where to specify annual average insolation. Maybe in socrates, with frierson?
    #     'ecc': 0.0,
    #     'obliq': 0.0,
    #     'per': 0.0
    # },
})

# exp.namelist = namelist # NOTE: I'm not sure if I need this line, but it's in gcm_testrrtm.py

# Let's do a run!
if __name__ == '__main__':
    # cb.compile(debug=False) # NOTE: I'm not sure if I need this line
    exp.set_resolution('T21') # NOTE: I'm not sure if I need this line here
    exp.run(1, use_restart=False, num_cores=NCORES)

    for i in range(2,31): # NOTE: socrates_ape_aquaplanet.py suggests all runs should be 30 years + spinup, but maybe less is fine for now?
        exp.run(i, num_cores=NCORES)
