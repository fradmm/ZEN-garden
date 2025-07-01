import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden
    out_folder = "outputs/20240603_GF"
    r = Results(out_folder)

    jitter_plot_capacity(r, 'conversion')
    #jitter_plot_capacity(r,'storage','power')

    ##plot costs

    # jitter_plot_cost(r,['cost_capex_total','cost_opex_total','cost_carrier','cost_total'])

    '''
    Check variables

    Demand
    r.get_total("demand").groupby(level=[0,1]).sum()

    Max load
    r.get_total('max_load').loc[:,'wind_onshore',:].groupby(level=0).sum()

    Storage level
    r.get_full_ts('storage_level','scenario_10').loc['hydrogen_storage'].sum().plot()
    
    Dual variables - shadow price
    r.get_dual("constraint_nodal_energy_balance").loc['scenario_21','electricity',:].sum()
    '''
    r.get_total('cost_capex_total').groupby(level=0).sum().to_csv('cost_capex_total.csv',index=True)
    r.get_total('cost_opex_total').groupby(level=0).sum().to_csv('cost_opex_total.csv', index=True)
    r.get_total('cost_carrier').groupby(level=0).sum().to_csv('cost_carrier.csv', index=True)
    r.get_total('cost_total').groupby(level=0).sum().to_csv('cost_total.csv', index=True)
    r.get_total('capacity').to_csv('capacity.csv',index=True)
    r.get_full_ts('demand').loc[:,'heat',:].to_csv('df_heat_demand.csv',index=True)
    r.get_dual("constraint_nodal_energy_balance").loc[:,'heat',:].to_csv('df_dual_heat_all_nodes.csv',index=True)
    r.get_full_ts('demand').loc[:, 'electricity', :].to_csv('df_electricity_demand.csv', index=True)
    r.get_dual("constraint_nodal_energy_balance").loc[:, 'electricity', :].to_csv('df_dual_electricity_all_nodes.csv', index=True)
    r.get_total('max_load').loc[:, 'wind_onshore', :].to_csv('df_max_load_wind.csv', index=True)


    a = 1

def plot_heatmap():
    # Plot shadow price electricity

    # Plot shadow price heat
    scenario_list = r.get_total('capacity_addition').index.levels[0].tolist()[1:]
    component = 'electricity'
    df_dual = r.get_dual("constraint_nodal_energy_balance").loc[:,component,:].groupby(level=0).sum()

    ncols = 3
    nrows = len(scenario_list) // ncols

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(60, 30), sharex=True, gridspec_kw={'hspace': 0.5})
    i=0
    j=0
    for scenario in (scenario_list):
        if i==nrows:
            i=0
            j= j+1
        im = axs[i,j].imshow(np.log(df_dual.loc[scenario].values).reshape(1,-1), aspect='auto', cmap='coolwarm', interpolation='none')
        axs[i,j].set_ylabel(scenario, rotation=0, labelpad=80,fontsize=20)
        axs[i,j].yaxis.set_label_position("right")
        axs[i,j].set_yticks([])  # Hide y-axis ticks
        i = i+1

    fig.suptitle('Shadow price of '+component, fontsize=16)

    cbar = fig.colorbar(im, ax=axs, orientation='vertical', fraction=0.02, pad=0.1)
    cbar.set_label('Shadow price (EUR)')

    ticks_per_month = 8760 // 12
    for i in range(ncols):
        axs[-1,i].set_xticks(np.arange(0, 8760, ticks_per_month))
        axs[-1,i].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    plt.show()

def jitter_plot_capacity(r, tech_type,capacity_type='power'):

    if tech_type == 'conversion':
        techs = r.get_system().set_conversion_technologies
    elif tech_type == 'storage':
        techs = r.get_system().set_storage_technologies

    scenario_list = r.get_total('capacity_addition').index.levels[0]

    fig = go.Figure()
    jitter = 0.2  # Jitter magnitude
    jitter_delta = np.linspace(-jitter,jitter, len(scenario_list))

    for i, tech in enumerate(techs):
        x_jittered = i + jitter_delta               # np.random.uniform(-jitter, jitter, len(scenario_list))
        capacity = get(r,'capacity',tech,capacity_type=capacity_type)
        # Create a jitter plot using Plotly Go
        fig.add_trace(
            go.Scatter(x=x_jittered, y=capacity, mode='markers', text=scenario_list, hoverinfo='text+y', name=tech))

    # Update layout
    fig.update_layout(title=tech_type,
                      xaxis_title='Technology',
                      yaxis_title='Installed capacity (GWh)',
                      xaxis=dict(tickvals=list(range(len(techs))), ticktext=techs))

    # Show the plot
    fig.show()


def get(r,component,tech_type,capacity_type='power'):
    return r.get_total('capacity').loc[:,tech_type,capacity_type,:].groupby(level=0).sum().values[:, 0]



def jitter_plot_cost(r, components):

    scenario_list = r.get_total('capacity_addition').index.levels[0]

    fig = go.Figure()
    jitter = 0.2
    jitter_delta = np.linspace(-jitter,jitter, len(scenario_list))
    for i,component in enumerate(components):
        x_jittered = i + jitter_delta# np.random.uniform(-jitter, jitter, len(scenario_list))
        cost = r.get_total(component).groupby(level=0).sum().values[:,0]
    # Create a jitter plot using Plotly Go
        fig.add_trace(
            go.Scatter(x=x_jittered, y=cost, mode='markers', text=scenario_list, hoverinfo='text+y', name=component))

    fig.update_layout(title="System cost",
                      xaxis_title='Cost type',
                      yaxis_title='Cost (M EUR)',
                      xaxis=dict(tickvals=list(range(len(components))), ticktext=components))
    fig.show()





if __name__ == '__main__':
    main()

