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
    out_folder = "outputs/GF2050_dunkeflaute_DE"
    r_df = Results(out_folder)


    start_date = pd.Timestamp('2050-01-01 00:00:00')
    end_date = pd.Timestamp('2050-12-31 23:00:00')
    datetime_index = pd.date_range(start=start_date, end=end_date, freq='H')

    country = 'DE'
    storage_techs = ['battery','hydrogen_storage','pumped_hydro']
    res_techs = ['photovoltaics', 'wind_onshore', 'wind_offshore', 'reservoir_hydro', 'nuclear', 'natural_gas_turbine']

    fig = go.Figure()
    for tech in storage_techs:
        fig.add_trace(go.Scatter(x=datetime_index, y=r.get_full_ts("storage_level").loc[tech, country],name=tech+" base", mode='lines'))
        fig.add_trace(go.Scatter(x=datetime_index, y=r_df.get_full_ts("storage_level").loc[tech, country], name=tech + " dunkeflaute",mode='lines'))
    fig.show()

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
        go.Bar(x=storage_capacity_df.index, y=storage_capacity_df[0].values, name='dunkeflaute', offsetgroup=0)
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

    storage_capacity_base = r.get_total("capacity").loc[storage_techs, 'energy', country].groupby(['technology']).sum()
    storage_capacity_df = r_df.get_total("capacity").loc[storage_techs, 'energy', country].groupby(['technology']).sum()
    fig = go.Figure(
        data = [
            go.Bar(x=storage_capacity_base.index, y=storage_capacity_base[0].values, name='base',offsetgroup=0),
            go.Bar(x=storage_capacity_df.index, y=storage_capacity_df[0].values, name='dunkeflaute', offsetgroup=1)
        ]
    )
    fig.update_layout(title="storage technology in " + country)
    fig.show()

    capacity_base = r.get_total("capacity").loc[:,:,country].groupby(["technology"]).sum()
    capacity_df = r_df.get_total("capacity").loc[:,:,country].groupby(["technology"]).sum()
    fig = go.Figure(
        data=[
            go.Bar(x=capacity_base.loc[res_techs].index, y=capacity_base[0].loc[res_techs].values, name='base',offsetgroup=0),
            go.Bar(x=capacity_df.loc[res_techs].index, y=capacity_df[0].loc[res_techs].values, name='dunkeflaute', offsetgroup=1)
        ]
    )
    fig.update_layout(title = "conversion technology in " + country)
    fig.show()

    a = 1


if __name__ == '__main__':
    main()