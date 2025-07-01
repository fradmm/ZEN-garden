import matplotlib.pyplot as plt
import plotly.graph_objects as go
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden

    input_system_name = '20240603_GF'
    input_scenario = 'scenario_46'

    out_folder = "outputs/" + input_system_name
    r = Results(out_folder)

    operation_n = 9

    output_system_name = 'GF_46_LR_' + str(operation_n)



    if input_scenario == []:
        capacity = r.get_total("capacity").reset_index()
    else:
        capacity = r.get_total("capacity").loc[input_scenario].reset_index()

    capacity['year_construction'] = 2049.0

    ### set the operation scnario as the default one ###
    filepath = output_system_name + "/set_carriers/heat/"
    df_demand = pd.read_csv(filepath+'demand_'+str(operation_n)+'.csv')
    df_demand.to_csv(filepath+'demand.csv',index=False)

    techs_with_scenario = ['photovoltaics','wind_onshore','wind_offshore']
    for tech in techs_with_scenario:
        filepath = output_system_name + "/set_technologies/set_conversion_technologies/" + tech +"/"
        df_max_load = pd.read_csv(filepath + "max_load_"+str(operation_n)+".csv")
        df_max_load.to_csv(filepath + "max_load.csv")

    ### get the existing capacity from thput scenario and write the capacity_existing.csv files

    for tech in r.get_system().set_conversion_technologies:
        filepath = output_system_name + "/set_technologies/set_conversion_technologies/" + tech + "/"

        capacity_existing = capacity[capacity.technology == tech].loc[:,['location','year_construction',0]].copy()
        capacity_existing = capacity_existing.rename(columns={'location': 'node','year_construction':'year_construction', 0: 'capacity_existing'})
        capacity_existing.to_csv(filepath + "capacity_existing.csv", index=False)

    for tech in r.get_system().set_storage_technologies:
        filepath = output_system_name + "/set_technologies/set_storage_technologies/" + tech + "/"

        capacity_existing = capacity[(capacity.technology == tech) & (capacity.capacity_type == 'power')].loc[:, ['location', 'year_construction', 0]].copy()
        capacity_existing = capacity_existing.rename(columns={'location': 'node', 'year_construction': 'year_construction', 0: 'capacity_existing'})
        capacity_existing.to_csv(filepath + "capacity_existing.csv", index=False)

        capacity_existing_energy = capacity[(capacity.technology == tech) & (capacity.capacity_type == 'energy')].loc[:, ['location', 'year_construction', 0]].copy()
        capacity_existing_energy = capacity_existing_energy.rename(columns={'location': 'node', 'year_construction': 'year_construction', 0: 'capacity_existing_energy'})
        capacity_existing_energy.to_csv(filepath + "capacity_existing_energy.csv", index=False)

    for tech in r.get_system().set_transport_technologies:
        filepath = output_system_name + "/set_technologies/set_transport_technologies/" + tech + "/"

        capacity_existing = capacity[capacity.technology == tech].loc[:,['location','year_construction',0]].copy()
        capacity_existing = capacity_existing.rename(columns={'location': 'edge','year_construction':'year_construction', 0: 'capacity_existing'})
        capacity_existing.to_csv(filepath + "capacity_existing.csv", index=False)



    a=1

if __name__ == '__main__':
    main()