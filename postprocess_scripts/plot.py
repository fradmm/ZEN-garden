def jitter_plot_all(r):

    conversion_techs = r.get_system().set_conversion_technologies
      #  ['natural_gas_turbine', 'natural_gas_turbine_CCS', 'nuclear', 'photovoltaics',
       #                 'reservoir_hydro', 'run-of-river_hydro', 'waste_plant', 'wind_offshore', 'wind_onshore']

    scenario_list = r.get_total('capacity').index.levels[0]

    fig = go.Figure()
    jitter = 0.2  # Jitter magnitude

    for i,tech in enumerate(conversion_techs):

        x_jittered = i + np.random.uniform(-jitter, jitter, len(scenario_list))
        capacity = r.get_total('capacity').loc[(slice(None), tech), :].groupby('scenario').sum().values[:, 0]
    # Create a jitter plot using Plotly Go
        fig.add_trace(go.Scatter(x=x_jittered, y=capacity, mode='markers',text=scenario_list,hoverinfo='text',name=tech))

    # Update layout
    fig.update_layout(title='Jitter Plot',
                      xaxis_title='Technology',
                      yaxis_title='Installed capacity (GWh)',
                      xaxis=dict(tickvals=list(range(len(conversion_techs))), ticktext=conversion_techs))

    # Show the plot
    fig.show()