import matplotlib.pyplot as plt
#import plotly.graph_objects as go
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden
    out_folder = "outputs/7_multiple_time_steps_per_year_1_inflow"

    r = Results("outputs/20240603_GF")

    r_0 = Results("outputs/7_multiple_time_steps_per_year_inflow")
    r_1 = Results("outputs/7_multiple_time_steps_per_year_1_inflow")
    r_N = Results("outputs/7_multiple_time_steps_per_year_inflow_no_spillage")

    r_0_PV = Results("outputs/7_multiple_time_steps_per_year_inflow_PV_opex")
    r_1_PV = Results("outputs/7_multiple_time_steps_per_year_1_inflow_PV_opex")
    r_10_PV = Results("outputs/7_multiple_time_steps_per_year_10_inflow_PV_opex")

    a=1

if __name__ == '__main__':
    main()