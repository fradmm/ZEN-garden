import matplotlib.pyplot as plt
#import plotly.graph_objects as go
#import plotly.express as px
import pandas as pd
#import numpy as np

from zen_garden.postprocess.results.results import Results

def main():
    #zen_garden
    out_folder = "outputs/20240617_GF_NE"

    r = Results(out_folder)
    r.get_total('capacity')


    a=1

if __name__ == '__main__':
    main()