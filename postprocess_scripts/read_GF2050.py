import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden
    out_folder = "outputs/GF2050"
    r = Results(out_folder)
    out_folder = "outputs/GF2050_dunkelflaute"
    r_df = Results(out_folder)
    out_folder = "outputs/GF2050_drought"
    r_dr = Results(out_folder)


    start_date = pd.Timestamp('2050-01-01 00:00:00')
    end_date = pd.Timestamp('2050-12-31 23:00:00')
    datetime_index = pd.date_range(start=start_date, end=end_date, freq='h')

    country = 'CH'
    storage_techs = ['battery','hydrogen_storage','pumped_hydro']
    res_techs = ['photovoltaics', 'wind_onshore', 'wind_offshore', 'reservoir_hydro', 'run-of-river_hydro']

    country_list = r.get_system().set_nodes

    # Plot all storage level per country
    '''
    fig = make_subplots(rows=4, cols=7)
    row = 1
    col = 1
    for country in country_list:
        if col == 8:
            row = row+1
            col = 1
        for tech in storage_techs:
            fig.add_trace(go.Scatter(x=datetime_index, y=r.get_full_ts("storage_level").loc[tech, country],name=tech+" base", mode='lines',offsetgroup=0),row=row, col=col)
            fig.add_trace(go.Scatter(x=datetime_index, y=r_df.get_full_ts("storage_level").loc[tech, country], name=tech + " dunkeflaute",mode='lines',offsetgroup=1),row=row, col=col)

        col = col+1

    fig.show()
    '''
    fig = go.Figure()
    flow_electricity_base = r.get_full_ts("flow_conversion_output").loc[res_techs, "electricity", country].groupby(
        ['technology']).sum()
    flow_electricity_df = r_df.get_full_ts("flow_conversion_output").loc[res_techs, "electricity", country].groupby(
        ['technology']).sum()
    for tech in res_techs:
        fig.add_trace(
            go.Scatter(x=datetime_index, y=flow_electricity_base.loc[tech], name=tech+" base", mode='lines'))
        fig.add_trace(
            go.Scatter(x=datetime_index, y=flow_electricity_df.loc[tech], name=tech + " dunkeflaute", mode='lines'))
    fig.show()

    ## Plot storage and conversion capacity  for all Europe ##

    storage_capacity_base = r.get_total("capacity").loc[storage_techs, 'energy', :].groupby(['technology']).sum()
    storage_capacity_df = r_df.get_total("capacity").loc[storage_techs, 'energy', :].groupby(['technology']).sum()

    fig = go.Figure(
        data = [
        go.Bar(x=storage_capacity_base.index, y=storage_capacity_base[0].values,name='base',offsetgroup=0),
        go.Bar(x=storage_capacity_df.index, y=storage_capacity_df[0].values, name='dunkeflaute', offsetgroup=1)
        ]
    )
    fig.update_layout(title="storage technology in Europe")
    fig.show()


    capacity_base = r.get_total("capacity").groupby(["technology"]).sum()
    capacity_df = r_df.get_total("capacity").groupby(["technology"]).sum()

    fig = go.Figure(
        data=[
            go.Bar(x=capacity_base.loc[res_techs].index, y=capacity_base[0].loc[res_techs].values,name='base',offsetgroup=0),
            go.Bar(x=capacity_df.loc[res_techs].index, y=capacity_df[0].loc[res_techs], name='dunkeflaute', offsetgroup=1)
        ]
    )
    fig.update_layout(title="conversion technology in Europe")
    fig.show()


    ## Plot storage and conversion capacity but for one country ##

    fig = make_subplots(rows=4, cols=7)
    row = 1
    col = 1
    for i,country in enumerate(country_list):
        if col == 8:
            row = row + 1
            col = 1
        if i == 0:
            flag = True
        else:
            flag = False
        storage_capacity_base = r.get_total("capacity").loc[storage_techs, 'energy', country].groupby(['technology']).sum()
        storage_capacity_df = r_df.get_total("capacity").loc[storage_techs, 'energy', country].groupby(['technology']).sum()
        storage_capacity_dr = r_dr.get_total("capacity").loc[storage_techs, 'energy', country].groupby(
            ['technology']).sum()
        fig.add_trace(go.Bar(x=storage_capacity_base.index, y=storage_capacity_base[0].values, name='base',marker_color = 'green',showlegend=flag, offsetgroup=0), row=row, col=col)
        fig.add_trace(go.Bar(x=storage_capacity_df.index, y=storage_capacity_df[0].values, name='dunkeflaute',marker_color = 'blue',showlegend=flag,  offsetgroup=1),row=row, col=col)
        fig.add_trace(go.Bar(x=storage_capacity_dr.index, y=storage_capacity_dr[0].values, name='drought',
                             marker_color='red', showlegend=flag, offsetgroup=2), row=row, col=col)

        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>"+str(country)+"</b>", row=row, col=col)
        fig.update_yaxes(title_text='storage capacity (GWh)', row=row, col=col)
        col = col + 1
    fig.show()


    fig = make_subplots(rows=4, cols=7)
    row = 1
    col = 1
    for i,country in enumerate(country_list):
        if col == 8:
            row = row + 1
            col = 1
        if i == 0:
            flag = True
        else:
            flag = False
        capacity_base = r.get_total("capacity").loc[:, :, country].groupby(["technology"]).sum()
        capacity_df = r_df.get_total("capacity").loc[:, :, country].groupby(["technology"]).sum()
        capacity_dr = r_dr.get_total("capacity").loc[:, :, country].groupby(["technology"]).sum()
        fig.add_trace(go.Bar(x=capacity_base.loc[res_techs].index, y=capacity_base[0].loc[res_techs].values, name='base',marker_color = 'green',showlegend=flag, offsetgroup=0), row=row, col=col)
        fig.add_trace(go.Bar(x=capacity_df.loc[res_techs].index, y=capacity_df[0].loc[res_techs].values, name='dunkeflaute',marker_color = 'blue',showlegend=flag,  offsetgroup=1),row=row, col=col)
        fig.add_trace(go.Bar(x=capacity_dr.loc[res_techs].index, y=capacity_dr[0].loc[res_techs].values, name='drought',marker_color='red', showlegend=flag, offsetgroup=2), row=row, col=col)
        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>"+str(country)+"</b>", row=row, col=col)
        fig.update_yaxes(title_text='conversion capacity (GW)', row=row, col=col)
        col = col+1

    fig.show()



    transport = r.get_total("flow_transport").loc['power_line']
    transport_df = r_df.get_total("flow_transport").loc['power_line']
    transport_dr = r_dr.get_total("flow_transport").loc['power_line']

    fig = make_subplots(rows=4, cols=7)
    row = 1
    col = 1
    for i, country in enumerate(country_list):
        if col == 8:
            row = row + 1
            col = 1
        if i == 0:
            flag = True
        else:
            flag = False
        df = pd.DataFrame(index=['import', 'export'], data=[transport[transport.index.str.endswith(country)].sum().values,
                                                        transport[transport.index.str.startswith(country)].sum().values])
        df_df = pd.DataFrame(index=['import', 'export'],
                          data=[transport_df[transport_df.index.str.endswith(country)].sum().values,
                                transport_df[transport_df.index.str.startswith(country)].sum().values])
        df_dr = pd.DataFrame(index=['import', 'export'],
                          data=[transport_dr[transport_dr.index.str.endswith(country)].sum().values,
                                transport_dr[transport_dr.index.str.startswith(country)].sum().values])

        fig.add_trace(go.Bar(x=df.index, y=df[0], name='base', marker_color='green', showlegend=flag, offsetgroup=0),row=row, col=col)
        fig.add_trace(go.Bar(x=df_df.index, y=df_df[0], name='dunkelflaute', marker_color='blue', showlegend=flag, offsetgroup=1),row=row, col=col)
        fig.add_trace(go.Bar(x=df_dr.index, y=df_dr[0], name='drought', marker_color='red', showlegend=flag, offsetgroup=2),row=row, col=col)

        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>" + str(country) + "</b>", row=row, col=col)
        fig.update_yaxes(title_text='Total transport (GWh)', row=row, col=col)
        col = col + 1

    fig.show()

    df_cost = pd.DataFrame(index=['opex', 'capex'], columns= ['base','dunkelflaute','drought'])

    df_cost['base'] = [r.get_total('cost_opex_total')[0], r.get_total('cost_capex_total')[0]]
    df_cost['dunkelflaute'] = [r_df.get_total('cost_opex_total')[0], r_df.get_total('cost_capex_total')[0]]
    df_cost['drought'] = [r_dr.get_total('cost_opex_total')[0], r_dr.get_total('cost_capex_total')[0]]
    fig = go.Figure()
    colors = ['green','blue','red']
    for i, name in enumerate(['base','dunkelflaute','drought']):
        fig.add_trace(go.Bar(x=df_cost.index, y=df_cost[name],name=name, marker_color=colors[i], offsetgroup=i))
    fig.show()



    a = 1


if __name__ == '__main__':
    main()