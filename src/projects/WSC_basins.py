'''
Created on Aug 27, 2016

This module contains meta data for all available WSC river basins in Canada. 

@author: Andre R. Erler, GPL v3
'''

from collections import OrderedDict
from datasets.common import addLoadFcts
from datasets.WSC import BasinSet, Basin

# dictionary with basin meta data
basin_list = OrderedDict() # maintain order
# meta data for specific basins

basin_list['AY']  = BasinSet(name='AY', long_name='Alaska and Yukon', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholeAY'])
basin_list['AO']  = BasinSet(name='AO', long_name='Arctic Ocean', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholeAO'])
basin_list['ARB'] = BasinSet(name='ARB', long_name='Athabasca River Basin', rivers=['Athabasca'], data_source='WSC',
                               stations=dict(Athabasca=['Embarras','McMurray']),
                               subbasins=['WholeARB','UpperARB','LowerARB'])
basin_list['CRB'] = BasinSet(name='CRB', long_name='Columbia River Basin', rivers=['Columbia'], data_source='WSC',
                               stations=dict(), subbasins=['WholeCRB'])
basin_list['FRB'] = BasinSet(name='FRB', long_name='Fraser River Basin', rivers=['Fraser'], data_source='WSC',
                               stations=dict(Fraser=['PortMann','Mission']),
                               subbasins=['WholeFRB','UpperFRB','LowerFRB'])
basin_list['GLB'] = BasinSet(name='GLB', long_name='Great Lakes Basin', rivers=['Upper Saint Lawrence'], data_source='WSC',
                              stations=dict(), subbasins=['WholeGLB'])
basin_list['GRW'] = BasinSet(name='GRW', long_name='Grand River Watershed', rivers=['Grand River'], data_source='Aquanty',
                               stations={'Grand River':['Brantford']}, subbasins=['WholeGRW','UpperGRW','LowerGRW','NorthernGRW','SouthernGRW','WesternGRW'])
basin_list['GSL'] = BasinSet(name='GSL', long_name='Great Slave Lake', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholeGSL'])
basin_list['LS']  = BasinSet(name='LS', long_name='Labrador Sea', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholeLS'])
basin_list['MKB'] = BasinSet(name='MKB', long_name='MacKenzie Basin', rivers=['MacKenzie'], data_source='',
                               stations=dict(), subbasins=['WholeMKB'])
basin_list['MRB'] = BasinSet(name='MRB', long_name='Missouri River Basin', rivers=['Missouri'], data_source='WSC',
                               stations=dict(), subbasins=['WholeMRB'])
basin_list['NRB'] = BasinSet(name='NRB', long_name='Nelson River Basin', rivers=['Nelson'], data_source='WSC',
                               stations=dict(), subbasins=['WholeNRB'])
basin_list['NHB'] = BasinSet(name='NHB', long_name='Northern Hudson Bay', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholeNHB'])
basin_list['NO']  = BasinSet(name='NO', long_name='Northern Ontario', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholeNO'])
basin_list['PO']  = BasinSet(name='PO', long_name='Pacific Ocean', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholePO'])
basin_list['PSB'] = BasinSet(name='PSB', long_name='Pacific Seaboard', rivers=[], data_source='WSC',
                               stations=dict(), subbasins=['WholePSB','NorthernPSB','SouthernPSB'])
basin_list['SLR'] = BasinSet(name='SLR', long_name='Saint Lawrence River', rivers=['Saint Lawrence'], data_source='WSC',
                               stations=dict(), subbasins=['WholeSLR'])
basin_list['SSR'] = BasinSet(name='SSR', long_name='South Sasketchewan River', rivers=['South Sasketchewan River'], data_source='Aquanty',
                               stations=dict(), subbasins=['WholeSSR'])

# N.B.: to add new gage stations add the name to the statins-dict and download the CSV files for monthly values and meta data
#       from the WSC historical archive (no missing days): http://wateroffice.ec.gc.ca/search/search_e.html?sType=h2oArc

# N.B.: all shapefiles from Water Survey of Canada

basin_sets = basin_list.copy() # dict that only contains basin sets
# dictionary of basins
basins = OrderedDict() # maintain order
for name,basin in basin_list.items():
  # add plain Basin instance of main basin under proper name
  basins[name] = basin.subbasins[basin.outline]
  # add all subbasins (including main basin with 'Whole' prefix)
  for subname,subbasin in basin.subbasins.iteritems():
    basins[subname] = subbasin # list with all Basin instances
    basin_list[subname] = subbasin # list with all basins, BasinSet and Basin instances

 
# get hydrographs from WSC here: https://wateroffice.ec.gc.ca/search/search_e.html?sType=h2oArc

## generate loadGageStation* versions with these basins
from datasets.WSC import loadGageStation
addLoadFcts(locals(), locals(), basins=basins, basin_list=basin_list)


if __name__ == '__main__':
    
  ## print basins
  for name,basin in basin_list.iteritems():
    s = '  {:3s}: '.format(name)
    if hasattr(basin, 'subbasins'):
      for subbasin in basin.subbasins: s += ' {:9s}'.format('{:s},'.format(subbasin))
    print(s)
    #print(basin.folder)