import matplotlib.pyplot as plt
import plotly.graph_objects as go
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden
    out_folder = "outputs/GF2050"
    r = Results(out_folder)
    capacity = r.get_total("capacity").reset_index()
    capacity['year_construction'] = 2049.0

    for tech in r.get_system().set_conversion_technologies:
        filepath = "GF2050_fix_df_forced/set_technologies/set_conversion_technologies/" + tech + "/"

        capacity_existing = capacity[capacity.technology == tech].loc[:,['location','year_construction',0]].copy()
        capacity_existing = capacity_existing.rename(columns={'location': 'node','year_construction':'year_construction', 0: 'capacity_existing'})
        capacity_existing.to_csv(filepath + "capacity_existing.csv", index=False)

    for tech in r.get_system().set_storage_technologies:
        filepath = "GF2050_fix_df_forced/set_technologies/set_storage_technologies/" + tech + "/"

        capacity_existing = capacity[(capacity.technology == tech) & (capacity.capacity_type == 'power')].loc[:, ['location', 'year_construction', 0]].copy()
        capacity_existing = capacity_existing.rename(columns={'location': 'node', 'year_construction': 'year_construction', 0: 'capacity_existing'})
        capacity_existing.to_csv(filepath + "capacity_existing.csv", index=False)

        capacity_existing_energy = capacity[(capacity.technology == tech) & (capacity.capacity_type == 'energy')].loc[:, ['location', 'year_construction', 0]].copy()
        capacity_existing_energy = capacity_existing_energy.rename(columns={'location': 'node', 'year_construction': 'year_construction', 0: 'capacity_existing_energy'})
        capacity_existing_energy.to_csv(filepath + "capacity_existing_energy.csv", index=False)

    for tech in r.get_system().set_transport_technologies:
        filepath = "GF2050_fix_df_forced/set_technologies/set_transport_technologies/" + tech + "/"

        capacity_existing = capacity[capacity.technology == tech].loc[:,['location','year_construction',0]].copy()
        capacity_existing = capacity_existing.rename(columns={'location': 'edge','year_construction':'year_construction', 0: 'capacity_existing'})
        capacity_existing.to_csv(filepath + "capacity_existing.csv", index=False)

    a=1

if __name__ == '__main__':
    main()