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
    out_folder = "outputs/GF2050_1"
    r_df = Results(out_folder)
    out_folder = "outputs/GF2050_2"
    r_dr = Results(out_folder)


    start_date = pd.Timestamp('2050-01-01 00:00:00')
    end_date = pd.Timestamp('2050-12-31 23:00:00')
    datetime_index = pd.date_range(start=start_date, end=end_date, freq='h')

    country = 'CH'
    storage_techs = ['battery','hydrogen_storage','pumped_hydro']
    res_techs = ['photovoltaics', 'wind_onshore', 'wind_offshore', 'reservoir_hydro', 'run-of-river_hydro']

    country_list_full = r.get_system().set_nodes

    # Plot all storage level per country

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





    transport = r.get_total("flow_transport").loc['power_line']
    transport_df = r_df.get_total("flow_transport").loc['power_line']
    transport_dr = r_dr.get_total("flow_transport").loc['power_line']

    fig = make_subplots(rows=4, cols=7)
    row = 1
    col = 1
    for i, country in enumerate(country_list_full):
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


    transport = r.get_full_ts("flow_transport").loc['power_line']
    transport_df = r_df.get_full_ts("flow_transport").loc['power_line']
    transport_dr = r_dr.get_full_ts("flow_transport").loc['power_line']

    #fig = make_subplots(rows=4, cols=7)
    fig = make_subplots(rows=1, cols=1)
    row = 1
    col = 1

    country_list = ['FR']

    for i, country in enumerate(country_list):
        if col == 8:
            row = row + 1
            col = 1
        if i == 0:
            flag = True
        else:
            flag = False
        imp = (transport[transport.index.str.endswith(country)].sum() - transport[transport.index.str.startswith(country)].sum())/r.get_full_ts("demand").loc['electricity',country]
        exp = transport[transport.index.str.startswith(country)].sum()
        imp_df = (transport_df[transport_df.index.str.endswith(country)].sum() - transport_df[transport_df.index.str.startswith(country)].sum()) /r_df.get_full_ts("demand").loc['electricity',country]
        imp_dr = (transport_dr[transport_dr.index.str.endswith(country)].sum() - transport_dr[transport_dr.index.str.startswith(country)].sum()) /r_dr.get_full_ts("demand").loc['electricity',country]

        fig.add_trace(go.Scatter(x=datetime_index, y=imp, name='Reference ', line=dict(width=4), marker_color='green', showlegend=flag),row=row, col=col)
        fig.add_trace(go.Scatter(x=datetime_index, y=imp_df, name='Dunkelflaute', line=dict(width=1), marker_color='blue', showlegend=flag),
                      row=row, col=col)
        fig.add_trace(go.Scatter(x=datetime_index, y=imp_dr, name='Drought', line=dict(width=1), marker_color='red', showlegend=flag),
            row=row, col=col)

        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>" + str(country) + "</b>", row=row, col=col)
        col = col + 1

    fig.update_layout(yaxis=dict(title='net import / demand (-)'))
    fig.show()


    # SHADOW PRICE OF TRANSPORT

    transport = r.get_dual("constraint_capacity_factor").loc['power_line',:,'power']

    # fig = make_subplots(rows=4, cols=7)
    fig = make_subplots(rows=1, cols=1)
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
        imp = (transport[transport.index.str.endswith(country)].sum())


        fig.add_trace(go.Scatter(x=datetime_index, y=imp, name='Reference ', line=dict(width=2), marker_color='green',
                                 showlegend=flag), row=row, col=col)

        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>" + str(country) + "</b>", row=row, col=col)
        col = col + 1

    fig.update_layout(yaxis=dict(title='import shadow price'))
    fig.show()



    ## SHADOW PRICE NODAL ENERGY BALANCE

    fig = make_subplots(rows=4, cols=7)
    # fig = make_subplots(rows=1, cols=1)
    row = 1
    col = 1

    for i, country in enumerate(country_list_full):
        if col == 8:
            row = row + 1
            col = 1
        if i == 0:
            flag = True
        else:
            flag = False
        imp = (transport[transport.index.str.endswith(country)].sum())

        fig.add_trace(go.Scatter(x=datetime_index, y=r.get_dual("constraint_nodal_energy_balance").loc['electricity',country], name='Reference ', line=dict(width=2), marker_color='green',
                                 showlegend=flag), row=row, col=col)

        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>" + str(country) + "</b>", row=row, col=col)
        col = col + 1

    fig.update_layout(yaxis=dict(title='Energy balance shadow price'))
    fig.show()






    # fig = make_subplots(rows=4, cols=7)
    fig = make_subplots(rows=1, cols=1)
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

        fig.add_trace(go.Scatter(x=datetime_index, y=r.get_full_ts("shed_demand").loc['electricity',country]/r.get_full_ts("demand").loc['electricity',country], name='Reference', line=dict(width=4), marker_color='green', showlegend=flag),
                      row=row, col=col)
        fig.add_trace(
            go.Scatter(x=datetime_index, y=r_df.get_full_ts("shed_demand").loc['electricity',country]/r_df.get_full_ts("demand").loc['electricity',country], name='Dunkelflaute', line=dict(width=1), marker_color='blue', showlegend=flag),
            row=row, col=col)
        fig.add_trace(
            go.Scatter(x=datetime_index, y=r_dr.get_full_ts("shed_demand").loc['electricity',country]/r_dr.get_full_ts("demand").loc['electricity',country], name='Drought', line=dict(width=1), marker_color='red', showlegend=flag),
            row=row, col=col)

        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>" + str(country) + "</b>", row=row, col=col)


        col = col + 1
    fig.update_layout( yaxis=dict(title='shed demand / demand (-)'))
    fig.show()

    #fig = make_subplots(rows=4, cols=7)
    fig = make_subplots(rows=1, cols=1)
    tech = 'hydrogen_storage'
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

        fig.add_trace(go.Scatter(x=datetime_index, y=r.get_full_ts('storage_level').loc[tech,country],
                                 name='Reference', line=dict(width=4), marker_color='green', showlegend=flag),
                      row=row, col=col)
        fig.add_trace(
            go.Scatter(x=datetime_index,
                       y=r_df.get_full_ts('storage_level').loc[tech,country], name='Dunkelflaute', line=dict(width=1), marker_color='blue',
                       showlegend=flag),
            row=row, col=col)
        fig.add_trace(
            go.Scatter(x=datetime_index,
                       y=r_dr.get_full_ts('storage_level').loc[tech,country], name='Drought', line=dict(width=1), marker_color='red',
                       showlegend=flag),
            row=row, col=col)

        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False,
                           text="Country = <b>" + str(country) + "</b>", row=row, col=col)

        col = col + 1
    fig.update_layout(yaxis=dict(title='storage level of '+tech+' (GWh)' ))
    fig.show()


    a = 1


if __name__ == '__main__':
    main()