import matplotlib.pyplot as plt
import plotly.graph_objects as go
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden

    input_system_name = '20240614_GF_LR'
    out_folder = "outputs/" + input_system_name
    r = Results(out_folder)


    output_system_name = '20240625_GF_NE'


    scenarios = ['scenario_3_LR_9'] #r.get_total('cost_total').index.values[1:]
    scenario = '3_9'

    for input_scenario in scenarios:

        capacity = r.get_total("capacity").loc[input_scenario].reset_index()
        #scenario = input_scenario.split('_')[1]

        capacity['year_construction'] = 2049.0

    ### get the existing capacity from thput scenario and write the capacity_existing.csv files

        for tech in r.get_system().set_conversion_technologies:
            filepath = output_system_name + "/set_technologies/set_conversion_technologies/" + tech + "/"

            capacity_existing = capacity[capacity.technology == tech].loc[:,['location','year_construction',0]].copy()
            capacity_existing = capacity_existing.rename(columns={'location': 'node','year_construction':'year_construction', 0: 'capacity_existing'})
            capacity_existing.to_csv(filepath + "capacity_existing_"+scenario+".csv", index=False)

        for tech in r.get_system().set_storage_technologies:
            filepath = output_system_name + "/set_technologies/set_storage_technologies/" + tech + "/"

            capacity_existing = capacity[(capacity.technology == tech) & (capacity.capacity_type == 'power')].loc[:, ['location', 'year_construction', 0]].copy()
            capacity_existing = capacity_existing.rename(columns={'location': 'node', 'year_construction': 'year_construction', 0: 'capacity_existing'})
            capacity_existing.to_csv(filepath + "capacity_existing_"+scenario+".csv", index=False)

            capacity_existing_energy = capacity[(capacity.technology == tech) & (capacity.capacity_type == 'energy')].loc[:, ['location', 'year_construction', 0]].copy()
            capacity_existing_energy = capacity_existing_energy.rename(columns={'location': 'node', 'year_construction': 'year_construction', 0: 'capacity_existing_energy'})
            capacity_existing_energy.to_csv(filepath + "capacity_existing_energy_"+scenario+".csv", index=False)

        for tech in r.get_system().set_transport_technologies:
            filepath = output_system_name + "/set_technologies/set_transport_technologies/" + tech + "/"

            capacity_existing = capacity[capacity.technology == tech].loc[:,['location','year_construction',0]].copy()
            capacity_existing = capacity_existing.rename(columns={'location': 'edge','year_construction':'year_construction', 0: 'capacity_existing'})
            capacity_existing.to_csv(filepath + "capacity_existing_"+scenario+".csv", index=False)



    a=1

if __name__ == '__main__':
    main()