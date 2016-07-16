'''
Created on Jun 4, 2016

A module that provides various project specific definitions, mainly related to experiments and plotting. 

@author:  Andre R. Erler, GPL v3
'''

# external imports
import matplotlib as mpl
# internal imports
import clim.load as clim_load
import clim.plot as clim_plot
import eva.load as eva_load
import eva.plot as eva_plot
from geodata.misc import AttrDict
from plotting import figure
from WRF_experiments import WRF_ens, WRF_exps
from projects.CESM_experiments import CESM_ens, CESM_exps

# method to add defaults to specifics
def _mergeAnnotation(specifics, defaults):
  annotation = dict()
  for name,specs in specifics.iteritems():
    atts = defaults.copy()
    atts.update(specs)
    annotation[name] = atts 
  return annotation

# variable collections
wetday_extensions = clim_load.wetday_extensions[:3]
variables_rc = dict(); VL = clim_load.VL
# mostly for hydrological analysis
variables_rc['temp']            = VL(vars=('T2', 'Tmax', 'Tmin'), files=('srfc','xtrm',), label='2m Temperature')
# variables_rc['temp']          = VL(vars=('T2',), files=('srfc',), label='2m Temperature')
variables_rc['precip_obs']      = VL(vars=('precip', 'solprec', 'wetfrq_010'), files=('hydro',), label='Precipitation')
variables_rc['precip_xtrm_obs'] = VL(vars=('MaxPrecip_1d', 'MaxPrecip_5d', 'wetprec_010'), files=('hydro',), label='Precipitation')
variables_rc['precip']          = VL(vars=('precip', 'preccu', 'solprec'), files=('hydro',), label='Precipitation')
variables_rc['precip_xtrm']     = VL(vars=('MaxPrecip_1d', 'MaxPrecip_5d', 'MaxPreccu_1d'), files=('hydro',), label='Precipitation')
variables_rc['precip_cesm']     = VL(vars=('MaxPrecip_1d', 'MaxPreccu_1d', ), files=('hydro',), label='Precipitation')
variables_rc['precip_alt']      = VL(vars=('MaxPrecip_1d', 'MaxPrecnc_1d', 'MaxSolprec_1d'), files=('hydro',), label='Precipitation')
variables_rc['precip_types']    = VL(vars=('precip','preccu','precnc'), files=('hydro',), label='Water Flux')
variables_rc['precip_net']      = VL(vars=('precip','solprec','p-et'), files=('hydro',), label='Water Flux')
variables_rc['flux_snow']       = VL(vars=('precip','snwmlt','solprec'), files=('hydro',), label='Water Flux')
variables_rc['flux_days']       = VL(vars=('wetfrq_010','snwmlt','p-et'), files=('hydro',), label='Water Flux')
variables_rc['wetprec']         = VL(vars=['wetprec'+ext for ext in wetday_extensions], files=('hydro',), label='Wet-day Precip.')
variables_rc['wetdays']         = VL(vars=['wetfrq'+ext for ext in wetday_extensions], files=('hydro',), label='Wet-day Ratio')
variables_rc['CWD']             = VL(vars=['CWD'+ext for ext in wetday_extensions]+['CNWD'], files=('hydro',), label='Continuous Wet-days')
variables_rc['CDD']             = VL(vars=['CDD'+ext for ext in wetday_extensions[:-1]]+['CNDD'], files=('hydro',), label='Continuous Dry-days')
variables_rc['sfcflx']          = VL(vars=('p-et','snwmlt','waterflx',), files=('hydro',), label='Surface Flux')
variables_rc['runoff']          = VL(vars=('waterflx','sfroff','runoff'), files=('lsm','hydro'), label='Runoff')
variables_rc['runoff_flux']     = VL(vars=('runoff','snwmlt','p-et'), files=('lsm','hydro'), label='Water Flux')
variables_rc['heat']            = VL(vars=('hfx','lhfx','rSM'),files=('srfc','lsm'), label='Energy Flux')
variables_rc['evap']            = VL(vars=('p-et','evap','pet',), files=('hydro',), label='Water Flux')
variables_rc['spei']            = VL(vars=('precip','evap','pet',), files=('aux','hydro',), label='Water Flux')
variables_rc['Q2']              = VL(vars=('Q2',),files=('srfc',), label='2m Humidity')
variables_rc['aSM']             = VL(vars=('aSM',),files=('lsm',), label='Soil Moisture') 
variables_rc['rSM']             = VL(vars=('rSM',),files=('lsm',), label='Relative Soil Moisture')
# N.B.: Noah-MP does not have relative soil moisture and there is not much difference anyway
# mostly for extreme value analysis
variables_rc['hydro_eva']    = VL(vars=['precip', 'p-et', 'snwmlt', 'waterflx','sfroff','runoff','aSM'],
                                  files=['hydro','lsm'], label='')
variables_rc['precip_eva']   = VL(vars=['precip', 'MaxPrecip_1h', 'MaxPrecip_6h', 'MaxPrecip_1d', 'MaxPrecip_5d',
                                        'MaxWaterflx_5d', 'wetfrq', 'CDD', 'CWD'], files=['hydro','srfc'], label='Precipitation')
variables_rc['temp_eva']     = VL(vars=['T2', 'MaxT2', 'MaxTmax', 'MinTmin', 'MaxTmax_7d', 'MinTmin_7d', 
                                        'frzfrq', 'CFD', 'CDFD', 'CNFD'], files=['srfc','xtrm'], label='Temperature')                          
variables_rc['precip_short'] = VL(vars=['MaxPreccu_1h', 'MaxPrecnc_1h', 'MaxPrecip_6h', 'MaxPreccu_6h'], 
                                  files=['xtrm','srfc'], label='MaxPrecip')
variables_rc['precip_long']  = VL(vars=['MaxPrecip_1d', 'MaxPreccu_1d', 'MaxPrecip_5d',], 
                                  files=['hydro'], label='MaxPrecip')
variables_rc['precip_CDD']   = VL(vars=['CNDD','CNWD']+[var+threshold for threshold in wetday_extensions for var in 'CDD','CWD'], 
                                  files=['hydro'], label='CDD')


# station selection criteria
constraints_rc = dict()
constraints_rc['min_len'] = 15 # for valid climatology
constraints_rc['lat'] = (45,55) 
constraints_rc['max_zerr'] = 300 # can't use this, because we are loading EC data separately from WRF
constraints_rc['prov'] = ('BC','AB')
constraints_rc['end_after'] = 1980
                        
# dataset collections
exps_rc = dict(); EX = clim_load.EX
exps_rc['obs']       = EX(name='obs',exps=['CRU','WSC'], styles=['-','-.'], title='Observations', 
                          master='CRU', reference='CRU', target=None)
exps_rc['erai']      = EX(name='erai',exps=['erai-g','erai-t'], styles=['--','-',], 
                          title='ERA-I G & T',
                          master='erai-g', reference=None, target=None)
exps_rc['erai-3']      = EX(name='erai',exps=['erai-g','erai-t','erai-g3','erai-t3'], styles=['--','-','-.',':'], 
                          title='G & T (10km & 90km, ERA-I)',
                          master='erai-g', reference=None, target=None)
exps_rc['val-mod']   = EX(name='val-mod', exps=['g-ens', 'g-ens_d01', 'Ens','t-ens'],
                          master='g-ens', reference=None, target=None, title='Model Comparison')
exps_rc['cesm-all']  = EX(name='cesm-all', exps=['Observations', 'Ens','Ens-2050','Ens-2100'],  
                         master='Ens', reference='Observations', target='Ens', title='CESM Validation & Projection')
exps_rc['cesm-mal']  = EX(name='cesm-ensa', exps=['Observations', 'MEns','MEns-2050','MEns-2100'],  
                         master='MEns', reference='Observations', target='MEns', title='CESM Validation & Projection')
exps_rc['cesm-prj']  = EX(name='cesm-ens', exps=['MEns','MEns-2050','MEns-2100'],  
                         master='MEns', reference='MEns', target='MEns', title='CESM Projection')
# initial condition ensembles (including observations)
exps_rc['g-all']     = EX(name='g-all',exps=['Observations', 'g-ens','g-ens-2050','g-ens-2100'], 
                          styles=['-','-.','--'], title='G Ensemble Average (Hist., Mid-, End-Century)',
                          master='g-ens', reference='Observations', target='g-ens')
exps_rc['t-all']     = EX(name='t-all',exps=['Observations', 't-ens','t-ens-2050','t-ens-2100'], 
                          styles=['-','-.','--'], title='T Ensemble Average (Hist., Mid-, End-Century)',
                          master='t-ens', reference='Observations', target='g-ens')
exps_rc['g3-all']    = EX(name='g3-all',exps=['Observations', 'g3-ens','g3-ens-2050','g3-ens-2100'], 
                         styles=['-','-.','--'], title='G Ens. Avg. (90km, Hist., Mid-, End-Century)',
                         master='g3-ens', reference='Observations', target='g-ens')
exps_rc['t3-all']    = EX(name='t3-all',exps=['Observations', 't3-ens','t3-ens-2050','t3-ens-2100'], 
                         styles=['-','-.','--'], title='T Ens. Avg. (90km, Hist., Mid-, End-Century)',
                         master='t3-ens', reference='Observations', target='g-ens')
# initial condition ensembles (projection)
exps_rc['g-prj']     = EX(name='g-prj',exps=['g-ens','g-ens-2050','g-ens-2100'], 
                          styles=['-','-.','--'], title='G Ensemble Average (Hist., Mid-, End-Century)',
                          master='g-ens', reference=None, target=None)
exps_rc['t-prj']     = EX(name='t-prj',exps=['t-ens','t-ens-2050','t-ens-2100'], 
                          styles=['-','-.','--'], title='T Ensemble Average (Hist., Mid-, End-Century)',
                          master='t-ens', reference=None, target=None)
exps_rc['g3-prj']    = EX(name='g3-prj',exps=['g3-ens','g3-ens-2050','g3-ens-2100'], 
                         styles=['-','-.','--'], title='G Ens. Avg. (90km, Hist., Mid-, End-Century)',
                         master='g3-ens', reference=None, target=None)
exps_rc['t3-prj']    = EX(name='t3-prj',exps=['t3-ens','t3-ens-2050','t3-ens-2100'], 
                         styles=['-','-.','--'], title='T Ens. Avg. (90km, Hist., Mid-, End-Century)',
                         master='t3-ens', reference=None, target=None)
# G ensemble members
exps_rc['g-Z']       = EX(name='g-Z',exps=['g-ctrl','g-ctrl-2050','g-ctrl-2100'], 
                          styles=['-','-.','--'], title='WRF-Z (Hist., Mid-, End-Century)',
                          master='g-ctrl', reference=None, target=None)
exps_rc['g-A']       = EX(name='g-A',exps=['g-ens-A','g-ens-A-2050','g-ens-A-2100'], 
                          styles=['-','-.','--'], title='WRF-A (Hist., Mid-, End-Century)',
                          master='g-ens-A', reference=None, target=None)
exps_rc['g-B']       = EX(name='g-B',exps=['g-ens-B','g-ens-B-2050','g-ens-B-2100'], 
                          styles=['-','-.','--'], title='WRF-B (Hist., Mid-, End-Century)',
                          master='g-ens-B', reference=None, target=None)
exps_rc['g-C']       = EX(name='g-C',exps=['g-ens-C','g-ens-C-2050','g-ens-C-2100'], 
                          styles=['-','-.','--'], title='WRF-C (Hist., Mid-, End-Century)',
                          master='g-ens-C', reference=None, target=None)
# physics ensemble  (withand without Observations)
exps_rc['phys-all']  = EX(name='phys',exps=['phys-ens','phys-ens-2050','phys-ens-2100'], 
                        styles=['-','-.','--'], title='WRF Phys. Ens. (Hist., Mid-, End-Century)',
                        master='phys-ens', reference='Observations', target='phys-ens')
exps_rc['phys-prj']  = EX(name='phys',exps=['phys-ens','phys-ens-2050','phys-ens-2100'], 
                        styles=['-','-.','--'], title='WRF Phys. Ens. (Hist., Mid-, End-Century)',
                        master='phys-ens', reference='phys-ens', target='phys-ens')
# physics ensemble members (with Observations)
exps_rc['gg-ctrl'] = EX(name='gg-ctrl', exps=['Observations', 'g-ctrl','gg-ctrl', 'g-ctrl-2050','gg-ctrl-2050'],
                        styles=['-','-.','--'], master='Observations', reference='Observations', target=None, title='')  
exps_rc['m-ctrl']  = EX(name='m-ctrl',  exps=['Observations', 'm-ctrl', 'm-ctrl-2050'],   
                        styles=['-','-.','--'], master='Observations', reference='Observations', target=None, title='')
exps_rc['mm-ctrl'] = EX(name='mm-ctrl', exps=['Observations', 'mm-ctrl', 'mm-ctrl-2050'], 
                        styles=['-','-.','--'], master='Observations', reference='Observations', target=None, title='')
exps_rc['t-ctrl']  = EX(name='t-ctrl',  exps=['Observations', 't-ctrl', 't-ctrl-2050'],
                        styles=['-','-.','--'], master='Observations', reference='Observations', target=None, title='')
# physics ensemble members (projection only)
exps_rc['gg-ctrl'] = EX(name='gg-ctrl', exps=['g-ctrl','gg-ctrl', 'g-ctrl-2050','gg-ctrl-2050'],
                        styles=['-','-.','--'], master='g-ctrl', reference=None, target=None, title='')  
exps_rc['m-ctrl']  = EX(name='m-ctrl',  exps=['m-ctrl', 'm-ctrl-2050'],   
                        styles=['-','-.','--'], master='m-ctrl', reference=None, target=None, title='')
exps_rc['mm-ctrl'] = EX(name='mm-ctrl', exps=['mm-ctrl', 'mm-ctrl-2050'], 
                        styles=['-','-.','--'], master='mm-ctrl', reference=None, target=None, title='')
exps_rc['t-ctrl']  = EX(name='t-ctrl',  exps=['t-ctrl', 't-ctrl-2050'],
                        styles=['-','-.','--'], master='t-ctrl', reference=None, target=None, title='')
# sea-ice experiments
# exps_rc['seaice']  = EX(name='seaice',exps=['g-ens-2050','g-seaice-2050','g-ens-2100','g-seaice-2100'],
#                         styles=['-.','--','-','.--','.-'], title='WRF (Mid-, End-Century; Ens. Avg., Sea-ice)',
#                         master=['g-ens-2050','g-ens-2100'], reference=None, target=None)
# exps_rc['si25']    = EX(name='si25',exps=['g-ens','g-ens-2050','g-seaice-2050'], 
#                         styles=[':','--','-'], title='WRF (Hist., Mid-Century; Ens. Avg., Sea-ice)',
#                         master='g-ens-2050', reference=None, target=None)
# exps_rc['si21']    = EX(name='si21',exps=['g-ens','g-ens-2100','g-seaice-2100'], 
#                         styles=[':','--','-'], title='WRF (Hist., End-Century; Ens. Avg., Sea-ice)',
#                         master='g-ens-2100', reference=None, target=None)


# set default variable atts for load functions from clim_load
def loadShapeObservations(variable_list=None, **kwargs):
  ''' wrapper for clim.load.loadShapeObservations that sets variable lists '''
  if variable_list is None: variable_list = variables_rc
  return clim_load.loadShapeObservations(variable_list=variable_list, **kwargs)
def loadShapeEnsemble(variable_list=None, **kwargs):
  ''' wrapper for clim.load.loadShapeEnsemble that sets experiment and variable lists '''
  if variable_list is None: variable_list = variables_rc  
  return clim_load.loadShapeEnsemble(variable_list=variable_list, WRF_exps=WRF_exps, CESM_exps=CESM_exps, 
                                     WRF_ens=WRF_ens, CESM_ens=CESM_ens, **kwargs)
def loadStationEnsemble(variable_list=None, **kwargs):
  ''' wrapper for clim.load.loadStationEnsemble that sets experiment and variable lists '''
  if variable_list is None: variable_list = variables_rc  
  return clim_load.loadStationEnsemble(variable_list=variable_list, WRF_exps=WRF_exps, CESM_exps=CESM_exps, 
                                       WRF_ens=WRF_ens, CESM_ens=CESM_ens, **kwargs)
def loadShapeFit(variable_list=None, **kwargs):
  ''' wrapper for eva.load.loadShapeEnsemble that sets experiment and variable lists '''
  if variable_list is None: variable_list = variables_rc  
  return eva_load.loadShapeFit(variable_list=variable_list, WRF_exps=WRF_exps, CESM_exps=CESM_exps, 
                               WRF_ens=WRF_ens, CESM_ens=CESM_ens, **kwargs)
def loadStationFit(variable_list=None, default_constraints=None, **kwargs):
  ''' wrapper for eva.load.loadStationEnsemble that sets experiment and variable lists etc. '''
  if variable_list is None: variable_list = variables_rc  
  if default_constraints is None: default_constraints = constraints_rc    
  return eva_load.loadStationFit(variable_list=variable_list, default_constraints=default_constraints,
                                 WRF_exps=WRF_exps, CESM_exps=CESM_exps, WRF_ens=WRF_ens, 
                                 CESM_ens=CESM_ens, **kwargs)


## settings for plotting 

# plot labels: translate internal names to something more presentable
plot_labels_rc = dict()
# datasets
plot_labels_rc['Unity']           = 'Uni. Obs.'
plot_labels_rc['Observations']    = 'EC Obs.'
plot_labels_rc['EC_1935']         = 'EC (1935)'
plot_labels_rc['EC_1965']         = 'EC (1965)'
plot_labels_rc['EC_1995']         = 'EC (1995)'
plot_labels_rc['Ens']             = 'CESM'  
plot_labels_rc['Ens-2050']        = 'CESM 2050' 
plot_labels_rc['Ens-2100']        = 'CESM 2100' 
plot_labels_rc['MEns']            = 'CESM*'  
plot_labels_rc['MEns-2050']       = 'CESM* 2050' 
plot_labels_rc['MEns-2100']       = 'CESM* 2100' 
plot_labels_rc['phys-ens']        = 'Phy Ens.' 
plot_labels_rc['phys-ens-2050']   = 'Phy 2050' 
plot_labels_rc['phys-ens-2100']   = 'Phy 2100' 
plot_labels_rc['phys-ens_d01']    = 'Phy (D1)'
plot_labels_rc['g-ens']           = 'G Ens.'  
plot_labels_rc['g-ens-2050']      = 'G 2050' 
plot_labels_rc['g-ens-2100']      = 'G 2100' 
plot_labels_rc['g3-ens']           = 'G Ens. (90km)'  
plot_labels_rc['g3-ens-2050']      = 'G 2050 (90km)' 
plot_labels_rc['g3-ens-2100']      = 'G 2100 (90km)' 
# plot_labels_rc['g-ens']           = 'WRF Ens.'  
# plot_labels_rc['g-ens-2050']      = 'WRF 2050' 
# plot_labels_rc['g-ens-2100']      = 'WRF 2100' 
plot_labels_rc['erai-g']          = 'ERA-I G'  
plot_labels_rc['t-ens']           = 'T Ens.'
plot_labels_rc['t-ens-2050']      = 'T 2050'
plot_labels_rc['t-ens-2100']      = 'T 2100'
plot_labels_rc['t3-ens']           = 'T Ens. (90km)'
plot_labels_rc['t3-ens-2050']      = 'T 2050 (90km)'
plot_labels_rc['t3-ens-2100']      = 'T 2100 (90km)'
plot_labels_rc['erai-t']          = 'ERA-I T'   
# variables
plot_labels_rc['MaxPrecip_1d']    = 'Max Precip. (1d)'
plot_labels_rc['MaxPrecip_5d']    = 'Max Precip. (5d)'
plot_labels_rc['MaxPreccu_1d']    = 'Max Conv. (1d)'
plot_labels_rc['MaxSolprec_1d']   = 'Max Snow (1d)'
plot_labels_rc['MaxWaterFlx_1d']  = 'Max Flux (1d)'
plot_labels_rc['wetfrq_010']      = 'Wet-days'
plot_labels_rc['wetprec_010']     = 'Precip. Intensity'
plot_labels_rc['T2']              = 'T (2m)'   
plot_labels_rc['precip']          = 'Precip.'  
plot_labels_rc['liqprec']         = 'Liquid' 
plot_labels_rc['solprec']         = 'Snow' 
plot_labels_rc['dryprec']         = 'dryprec' 
plot_labels_rc['preccu']          = 'Conv.'  
plot_labels_rc['precnc']          = 'NC'  
plot_labels_rc['evap']            = 'ET'    
plot_labels_rc['p-et']            = 'Net Precip.'    
plot_labels_rc['pet']             = 'PET' 
plot_labels_rc['waterflx']        = 'Water Flux'
plot_labels_rc['snwmlt']          = 'Snow Melt' 
plot_labels_rc['runoff']          = 'Total Runoff' 
plot_labels_rc['ugroff']          = 'Undergr. R\'off' 
plot_labels_rc['sfroff']          = 'Surface Runoff' 
plot_labels_rc['Tmax']            = 'T (max)'    
plot_labels_rc['Tmin']            = 'T (min)'    
plot_labels_rc['hfx']             = 'Sens. Heat'     
plot_labels_rc['lhfx']            = 'Latent Heat'    
plot_labels_rc['Q2']              = 'Q (2m)'      
plot_labels_rc['aSM']             = 'aSM'     
plot_labels_rc['rSM']             = 'Soil Moist.'       

## plot styles for climatology plots
climds_plotargs_rc = dict()
# observational datasets
obs_args = AttrDict(marker='o', linestyle=' ') # 5*mpl.rcParams['lines.linewidth']
climds_plotargs_rc['Observations'] =  obs_args
climds_plotargs_rc['WSC']          =  obs_args
climds_plotargs_rc['Unity']        =  obs_args
climds_plotargs_rc['CRU']          =  obs_args
climds_plotargs_rc['GPCC']         =  obs_args
# reanalysis datasets
rea_args = AttrDict(marker='^', markersize=mpl.rcParams['lines.markersize'], linestyle=' ') # 'small'
climds_plotargs_rc['CFSR']         =  rea_args
climds_plotargs_rc['NARR']         =  rea_args
# variable settings
variable_plotargs_rc = dict()
variable_plotargs_rc['MaxPrecip_1d']   = AttrDict(color = 'green')
variable_plotargs_rc['MaxPrecip_5d']   = AttrDict(color = 'sienna')
variable_plotargs_rc['MaxPreccu_1d']   = AttrDict(color = 'magenta')
variable_plotargs_rc['MaxPrecnc_1d']   = AttrDict(color = 'grey')
variable_plotargs_rc['MaxSolprec_1d']  = AttrDict(color = 'blue')
variable_plotargs_rc['MaxWaterFlx_1d'] = AttrDict(color = 'blue')
variable_plotargs_rc['T2']             = AttrDict(color = 'green')
variable_plotargs_rc['precip']         = AttrDict(color = 'green')
variable_plotargs_rc['liqprec']        = AttrDict(color = 'cyan')
variable_plotargs_rc['solprec']        = AttrDict(color = 'blue')
variable_plotargs_rc['dryprec']        = AttrDict(color = 'green')
variable_plotargs_rc['preccu']         = AttrDict(color = 'magenta')
variable_plotargs_rc['precnc']         = AttrDict(color = 'coral')
variable_plotargs_rc['evap']           = AttrDict(color = 'red')
variable_plotargs_rc['p-et']           = AttrDict(color = 'red')
variable_plotargs_rc['pet']            = AttrDict(color = 'purple')
variable_plotargs_rc['waterflx']       = AttrDict(color = 'dodgerblue') # 'dodgerblue'
variable_plotargs_rc['snwmlt']         = AttrDict(color = 'orange')
variable_plotargs_rc['runoff']         = AttrDict(color = 'purple')
variable_plotargs_rc['ugroff']         = AttrDict(color = 'coral')
variable_plotargs_rc['sfroff']         = AttrDict(color = 'green')
variable_plotargs_rc['Tmax']           = AttrDict(color = 'red')
variable_plotargs_rc['Tmin']           = AttrDict(color = 'blue')
variable_plotargs_rc['hfx']            = AttrDict(color = 'red')
variable_plotargs_rc['lhfx']           = AttrDict(color = 'purple')
variable_plotargs_rc['Q2']             = AttrDict(color = 'blue')
variable_plotargs_rc['aSM']            = AttrDict(color = 'coral')
variable_plotargs_rc['rSM']            = AttrDict(color = 'green')
variable_plotargs_rc['CNWD']           = AttrDict(color = 'green')
variable_plotargs_rc['CNDD']           = AttrDict(color = 'green')
# add wet-day threshold dependent variables    
wetday_colors = ['steelblue', 'purple', 'crimson', 'orange']   
for wdext,color in zip(clim_load.wetday_extensions,wetday_colors):
  variable_plotargs_rc['wetprec'+wdext] = AttrDict(color = color)
  variable_plotargs_rc['wetfrq' +wdext] = AttrDict(color = color)
  variable_plotargs_rc['CWD'+wdext]     = AttrDict(color = color)
  variable_plotargs_rc['CDD' +wdext]    = AttrDict(color = color)

# wrapper with custom defaults to figure creator (plotargs and label positions)
def climFigAx(subplot, dataset_plotargs=None, variable_plotargs=None, plot_labels=None, xtop=None, yright=None, **kwargs):
  if dataset_plotargs is None: dataset_plotargs = climds_plotargs_rc 
  if variable_plotargs is None: variable_plotargs = variable_plotargs_rc
  if plot_labels is None: plot_labels = plot_labels_rc
  return figure.getFigAx(subplot, dataset_plotargs=dataset_plotargs, variable_plotargs=variable_plotargs,
                         plot_labels=plot_labels, xtop=xtop, yright=yright, **kwargs)

## annotation for climatology plot
# defaults
clim_defaults = AttrDict(heat=(-30,130), Q2=(0,20), aSM=(0.1,0.5), temp=(245,305), wetprec=(0,25), wetfrq=(0,100))
# specific settings
clim_specifics = dict()
clim_specifics['GLB']         = AttrDict(temp=(245,300), water=(-1.,5.), precip_net=(-0.5,5.5), precip_types=(-0.5,5.5), precip_xtrm=(-1.,29.),
                                         runoff=(-0.5,2.5), runoff_flux=(-0.5,3.5), flux=(-0.5,3.5), flux_snow=(-0.5,3.5), spei=(-1.5,5.5), evap=(-1.5,5.5))
clim_specifics['GRW']         = clim_specifics['GLB']
clim_specifics['NRB']         = AttrDict(temp=(245,305), water=(-1.4,2.2), precip=(-0.4,3.4), runoff=(-2.,2.), flux=(-2,5.5))
clim_specifics['Prairies']    = AttrDict(temp=(250,305), water=(-1.5,1.5), precip=(-0.5,3.5), precip_xtrm=(0,30), precip_cesm=(0,30), precip_alt=(0,30), wetprec=(0,30), wetdays=(0,80), CWD=(0,15), CDD=(0,25))
# add defaults to specifics
clim_annotation = _mergeAnnotation(clim_specifics, clim_defaults)
  
# wrapper with annotation defaults for climPlot
def climPlot(annotation=None, defaults=None, variable_list=None, **kwargs):
  if annotation is None: annotation = annotation
  if defaults is None: defaults = defaults
  if variable_list is None: variable_list = variables_rc
  return clim_plot.climPlot(annotation=clim_annotation, defaults=clim_defaults, 
                            variable_list=variable_list, **kwargs)

## plot styles for EVA plots
# dataset settings
evads_plotargs_rc = dict()
evads_plotargs_rc['EC']              = AttrDict(color='black')
evads_plotargs_rc['EC (1935)']       = AttrDict(color='blue')
# distribution plot defaults
                         MaxWaterflx_5d=(5,35), CWD=(0,30), CDD=(0,50), CNWD=(0,30), CNDD=(0,80), 
                         CWD_100=(0,15), CDD_100=(0,100), CWD_200=(0,10), CDD_200=(0,100),
                         MaxPrecip_1d=(0,120), MaxPreccu_1d=(0, 40), MaxPrecnc_1d=(0,120), 
                         MaxPrecnc_1h=(0,500), MaxPrecip_5d=(0,20),)
dist_specifics = dict() 
# basins (annual)
dist_specifics['plateau_summer']  = AttrDict(MaxPreccu_1h=(0,600), MaxPrecnc_1h=(0,600), MaxPrecip_6h=(0,180), MaxPrecnc_6h=(0,180), MaxPreccu_6h=(0,100), MaxPrecip_1d=(0, 60), MaxSolprec_1d=(0, 60), MaxPrecnc_1d=(0, 60), MaxPreccu_1d=(0,30), MaxPrecip_5d=(0,30), MaxSolprec_5d=(0,30), MaxWaterflx_5d=(-4,10), CWD_002=(0,30), CDD_002=(0,50), CWD_010=(0,45), CDD_010=(0,90), CNWD=(0,20), CNDD=(0,120))
dist_specifics['AB_summer']       = dist_specifics['prairies_summer'] 
dist_specifics['AB_winter']       = dist_specifics['prairies_winter']
# wrapper with custom annotation defaults for distPlot
def distPlot(annotation=None, defaults=None, variable_list=None, **kwargs):
  if annotation is None: annotation = dist_annotation
  if defaults is None: defaults = dist_defaults
  return eva_plot.distPlot(annotation=annotation, defaults=defaults, **kwargs)

# quantile plot defaults
quant_specifics['ARB'] = AttrDict(waterflx=(1.5,4.5), MaxWaterflx_5d = (5,15), aSM=(0.16,0.21))
# provinces (seasonal)
# clusters (seasonal)

# wrapper with custom annotation defaults for distPlot
def quantPlot(annotation=None, defaults=None, variable_list=None, **kwargs):
  if annotation is None: annotation = quant_annotation
  if defaults is None: defaults = quant_defaults
  return eva_plot.quantPlot(annotation=annotation, defaults=defaults, **kwargs)

if __name__ == '__main__':