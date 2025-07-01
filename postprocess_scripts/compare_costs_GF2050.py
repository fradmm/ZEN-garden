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
    r_df = Results("outputs/GF2050_dunkeflaute_DE")
    r_fix_1 = Results("outputs/GF2050_fix_df_forced")

    plt.figure(1)
    plt.plot(r.get_full_ts('flow_conversion_output').loc['photovoltaics','electricity','DE'])
    plt.xlabel("time (h)")
    plt.ylabel("Power (MW)")
    plt.ylim([0, 160])
    plt.title("PV Electricity production in Germany - Design: BS, Operation: BS")

    plt.figure(2)
    plt.plot(r_fix_1.get_full_ts('flow_conversion_output').loc['photovoltaics', 'electricity', 'DE'])
    plt.xlabel("time (h)")
    plt.ylabel("Power (MW)")
    plt.ylim([0, 160])
    plt.title("PV Electricity production in Germany - Design: BS, Operation: DF")

    plt.show()




    a=1

if __name__ == '__main__':
    main()