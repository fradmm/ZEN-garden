import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden
    out_folder = "outputs/GF"
    r = Results(out_folder)

    A = r.get_total('capacity').loc[:, 'photovoltaics', :, :].copy()
    A.index.names = ['scenario', 'capacity_type', 'node']
    A.groupby('scenario').sum()

    a = 1


if __name__ == '__main__':
    main()