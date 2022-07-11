import numpy as np
from isca import SocratesCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE
from isca.util import exp_progress
NCORES = 32
base_dir = os.path.dirname(os.path.realpath(__file__))
cb = SocratesCodeBase.from_directory(GFDL_BASE)
inputfiles = [os.path.join(GFDL_BASE,'input/land_masks/era_land_t42.nc'),os.path.join(GFDL_BASE,'input/rrtm_input_files/ozone_1990.nc'), '/scratch/mh920/experiments/ECS_peak/input/sphum_300ppm.nc','/scratch/mh920/experiments/ECS_peak/input/conv_300ppm.nc' ]
#Tell model how to write diagnostics
diag = DiagTable()
diag.add_file('atmos_monthly', 30, 'days', time_units='days')
#Tell model which diagnostics to write
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('atmosphere', 'precipitation', time_avg=True)
diag.add_field('mixed_layer', 't_surf', time_avg=True)
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'vor', time_avg=True)
diag.add_field('dynamics', 'div', time_avg=True)
diag.add_field('mixed_layer', 'flux_t', time_avg=True)
diag.add_field('mixed_layer', 'flux_lhe', time_avg=True)
diag.add_field('mixed_layer', 'ml_heat_cap', time_avg=True)
diag.add_field('atmosphere', 'dt_tg_convection', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_convection', time_avg=True)
diag.add_field('atmosphere', 'dt_tg_condensation', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_condensation', time_avg=True)
diag.add_field('atmosphere', 'dt_tg_diffusion', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_diffusion', time_avg=True)
diag.add_field('atmosphere', 'sphum_SW_in', time_avg=True)
diag.add_field('atmosphere', 'rh', time_avg=True)
#radiative tendencies
diag.add_field('socrates', 'soc_tdt_lw', time_avg=True)
diag.add_field('socrates', 'soc_tdt_sw', time_avg=True)
diag.add_field('socrates', 'soc_tdt_rad', time_avg=True)
#net (up) and down surface fluxes
diag.add_field('socrates', 'soc_surf_flux_lw', time_avg=True)
diag.add_field('socrates', 'soc_surf_flux_sw', time_avg=True)
diag.add_field('socrates', 'soc_surf_flux_lw_down', time_avg=True)
diag.add_field('socrates', 'soc_surf_flux_sw_down', time_avg=True)
#net (up) TOA and downard fluxes
diag.add_field('socrates', 'soc_olr', time_avg=True)
diag.add_field('socrates', 'soc_toa_sw', time_avg=True)
diag.add_field('socrates', 'soc_toa_sw_down', time_avg=True)
# additional output options commented out
diag.add_field('socrates', 'soc_flux_lw', time_avg=True)
diag.add_field('socrates', 'soc_flux_sw', time_avg=True)
diag.add_field('socrates', 'soc_co2', time_avg=True)
#diag.add_field('socrates', 'soc_ozone', time_avg=True)
#diag.add_field('socrates', 'soc_coszen', time_avg=True)
diag.add_field('socrates', 'soc_spectral_olr', time_avg=True)
diag.add_field('atmosphere', 'diss_heat_ray', time_avg=True)
diag.add_field('atmosphere', 'diss_heat', time_avg=True)
diag.add_field('damping', 'tdt_diss_rdamp', time_avg=True)
diag.add_field('dynamics', 'vcomp_temp', time_avg=True)
diag.add_field('dynamics', 'vcomp_height', time_avg=True)
diag.add_field('dynamics', 'sphum_v', time_avg=True)
diag.add_field('dynamics', 'ucomp_temp', time_avg=True)
diag.add_field('dynamics', 'ucomp_height', time_avg=True)
diag.add_field('dynamics', 'sphum_u', time_avg=True)
diag.add_field('dynamics', 'sphum_w', time_avg=True)
diag.add_field('dynamics', 'omega', time_avg=True)
diag.add_field('dynamics', 'omega_temp', time_avg=True)
diag.add_field('dynamics', 'omega_height', time_avg=True)
#Define values for the 'core' namelist
namelist = Namelist({
    'main_nml':{
     'days'   : 30,
     'hours'  : 0,
     'minutes': 0,
     'seconds': 0,
     'dt_atmos':600,
     'current_date' : [1,1,1,0,0,0],
     'calendar' : 'thirty_day'
    },
    'socrates_rad_nml': {
        'stellar_constant':1370.,
        'lw_spectral_filename':os.path.join(GFDL_BASE,'src/atmos_param/socrates/src/trunk/data/spectra/arcc/sp_lw_17_dsa_arcc'),
        'sw_spectral_filename':os.path.join(GFDL_BASE,'src/atmos_param/socrates/src/trunk/data/spectra/ga7/sp_sw_ga7'),
        'do_read_ozone': True,
        'ozone_file_name':'ozone_1990',
        'ozone_field_name':'ozone_1990',
        'dt_rad':3600,
        'store_intermediate_rad':True,
        'chunk_size': 16,
        'use_pressure_interp_for_half_levels':False,
        'tidally_locked':False,
        #'solday': 90
        'frierson_solar_rad':True,
    },
    'idealized_moist_phys_nml': {
        'do_damping': True,
        'turb':True,
        'mixed_layer_bc':True,
        'do_virtual' :False,
        'do_simple': True,
        'roughness_mom':3.21e-05,
        'roughness_heat':3.21e-05,
        'roughness_moist':3.21e-05,
        'two_stream_gray': False,     #Use the grey radiation scheme
        'do_socrates_radiation': True,
        'convection_scheme': 'SIMPLE_BETTS_MILLER', #Use simple Betts miller convection
        'do_sphum_SW_soc' : False,
        'sphum_SW_soc_field_name' : 'sphum',
        'sphum_SW_soc_file_name' : '/scratch/mh920/experiments/ECS_peak/input/sphum_300ppm_nozone.nc',
        'fixed_conv' : False,
        'conv_file_name' : '/scratch/mh920/experiments/ECS_peak/input/conv_300ppm.nc',
        'conv_dt_tg_field_name' : 'dt_tg_convection',
        'conv_dt_qg_field_name' : 'dt_qg_convection'
    },
    'vert_turb_driver_nml': {
        'do_mellor_yamada': False,     # default: True
        'do_diffusivity': True,        # default: False
        'do_simple': True,             # default: False
        'constant_gust': 0.0,          # default: 1.0
        'use_tau': False
    },
    'diffusivity_nml': {
        'do_entrain':False,
        'do_simple': True,
    },
    'surface_flux_nml': {
        'use_virtual_temp': False,
        'do_simple': True,
        'old_dtaudv': True
    },
    'atmosphere_nml': {
        'idealized_moist_model': True
    },
    #Use a large mixed-layer depth, and the Albedo of the CTRL case in Jucker & Gerber, 2017
    'mixed_layer_nml': {
        'tconst' : 285.,
        'prescribe_initial_dist':True,
        'evaporation':True,
        'depth': 2.5,                          #Depth of mixed layer used
        'albedo_value': 0.23,                  #Albedo value used
        'albedo_choice' : 1,
    },
    'qe_moist_convection_nml': {
        'rhbm':0.7,
        'Tmin':100.,
        'Tmax':550.
    },
    'lscale_cond_nml': {
        'do_simple':True,
        'do_evap':True
    },
    'sat_vapor_pres_nml': {
        'do_simple':True,
        'tcmax_simple':550,
        'tcmin_simple':-273
    },
    'damping_driver_nml': {
        'do_rayleigh': True,
        'trayfric': -0.5,              # neg. value: time in *days*
        'sponge_pbottom':  150., #Setting the lower pressure boundary for the model sponge layer in Pa.
        'do_conserve_energy': True,
    },
    # FMS Framework configuration
    'diag_manager_nml': {
        'mix_snapshot_average_fields': False  # time avg fields are labelled with time in middle of window
    },
    'fms_nml': {
        'domains_stack_size': 600000                        # default: 0
    },
    'fms_io_nml': {
        'threading_write': 'single',                         # default: multi
        'fileset_write': 'single',                           # default: multi
    },
    'spectral_dynamics_nml': {
        'damping_order': 4,
        'water_correction_limit': 200.e2,
        'reference_sea_level_press':1.0e5,
        'num_levels':40,      #How many model pressure levels to use
        'valid_range_t':[0.,1000.],
        'initial_sphum':[2.e-6],
        'vert_coord_option':'uneven_sigma',
        'surf_res':0.2, #Parameter that sets the vertical distribution of sigma levels
        'scale_heights' : 11.0,
        'exponent':7.0,
        'robert_coeff':0.03
    },
    # FMS Framework configuration
    'diag_manager_nml': {
        'mix_snapshot_average_fields': False  # time avg fields are labelled with time in middle of window
    },
    'fms_nml': {
        'domains_stack_size': 600000                        # default: 0
    },
    'fms_io_nml': {
        'threading_write': 'single',                         # default: multi
        'fileset_write': 'single',                           # default: multi
    },
    'constants_nml': {
        'es0' : 1.0,
    },
})
#Lets do a run!
if __name__=="__main__":
    cb.compile()
    init_arr = [9600,19200,38400]
    co2_arr = [19200,38400,76800]
    j=0
    for myCO2 in co2_arr:
        exp = Experiment('ECS_peaks_'+str(myCO2)+'ppm_0.15alb_diffinit', codebase=cb)
        exp.clear_rundir()
        exp.diag_table=diag
        exp.inputfiles=inputfiles
        exp.namelist = namelist.copy()
        exp.namelist['socrates_rad_nml']['do_read_ozone']=False
        exp.namelist['socrates_rad_nml']['co2_ppmv']=myCO2
        exp.namelist['mixed_layer_nml']['depth']=2
        exp.namelist['mixed_layer_nml']['albedo_value']=0.15 #ctl is 0.19
        exp.run(1, use_restart=True, restart_file= '/scratch/mh920/data_isca/ECS_peaks_'+str(init_arr[j])+'sqrt2ppm_0.15alb/restarts/res0099.tar.gz', num_cores=NCORES)
        for i in range(2,100):
            exp.run(i, num_cores=NCORES)
        j=j+1
