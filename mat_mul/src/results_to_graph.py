#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import subprocess
import os
import plotly
import csv
from array import array
from subprocess import run       # para ejecutar un programa
from pathlib import Path
from sys import exit
from time import time
from io import StringIO

# 3rd party packages
import numpy as np
import plotly.graph_objects as go

# local source


# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    """Programa principal"""

    import os
    import locale
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.figure_factory as ff

    # ! Se ignoran los parametros de mat_type y mat_size

    # Define the locale format
    locale.setlocale(locale.LC_ALL, '')

    # Name of the input/output files
    file_name = os.path.os.getcwd() + "/out/results1.txt"
    file_name_out = os.path.os.getcwd() + "/out/results1.csv"

    # List of chars to be deleted/ignored
    bad_words = ["EOF"]

    # Se edita el fichero para que pueda ser leido con pandas
    with open(file_name, 'r') as oldfile, open(file_name_out, 'w') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in bad_words):
                # newfile.write(line[2:-2]+"\n")
                newfile.write(line)

    table_names = ["multi_papi_no", "multi_papi_yes",
                   "multi_perf_no", "multi_perf_no",
                   "transp_papi_no", "transp_papi_yes",
                   "transp_perf_no", "transp_perf_yes"]

    df = pd.read_csv(file_name_out, sep=":", names=range(3))

    groups = df[0].isin(table_names).cumsum()
    
    tables = {g.iloc[0,0]: g.iloc[1:] for k,g in df.groupby(groups)}

    for k,v in tables.items():
        print("table:", k)
        print(v)
        print()

    # print(df)

    # # Add table data
    # table_data = [['Team', 'Wins', 'Losses', 'Ties'],
    #             ['Montréal<br>Canadiens', 18, 4, 0],
    #             ['Dallas Stars', 18, 5, 0],
    #             ['NY Rangers', 16, 5, 0],
    #             ['Boston<br>Bruins', 13, 8, 0],
    #             ['Chicago<br>Blackhawks', 13, 8, 0],
    #             ['Ottawa<br>Senators', 12, 5, 0]]

    # # Initialize a fig with ff.create_table(table_data)
    # fig = ff.create_table(table_data, height_constant=60)

    # # Add graph data
    # teams = ['Montréal Canadiens', 'Dallas Stars', 'NY Rangers',
    #         'Boston Bruins', 'Chicago Blackhawks', 'Ottawa Senators']
    # GFPG = [3.54, 3.48, 3.0, 3.27, 2.83, 3.18]
    # GAPG = [2.17, 2.57, 2.0, 2.91, 2.57, 2.77]

    # fig.add_trace(go.Bar(x=teams, y=GFPG, xaxis='x2', yaxis='y2',
    #                 marker=dict(color='#0099ff'),
    #                 name='Goals For<br>Per Game'))

    # fig.add_trace(go.Bar(x=teams, y=GAPG, xaxis='x2', yaxis='y2',
    #                 marker=dict(color='#404040'),
    #                 name='Goals Against<br>Per Game'))

    # fig.update_layout(
    #     title_text = '2016 Hockey Stats',
    #     height = 800,
    #     margin = {'t':75, 'l':50},
    #     yaxis = {'domain': [0, .45]},
    #     xaxis2 = {'anchor': 'y2'},
    #     yaxis2 = {'domain': [.6, 1], 'anchor': 'x2', 'title': 'Goals'}
    # )

    # fig.show()

    # Se guarda la grafica
    # fig.write_html(name_html)
    # run(["mv", name_html, self.RESDIR])
