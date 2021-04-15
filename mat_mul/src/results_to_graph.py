#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library

# 3rd party packages

# local source


# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    """Programa principal"""

    import os
    import locale
    import pandas as pd
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots
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
                # Elimino los eventos que no se han ejecutado/contado
                if line[0] != '0':
                    newfile.write(line)

    df = pd.read_csv(file_name_out, header=None, sep=":", names=range(7))
    # ! Es necesario poner el mismo titulo que aparece en el fichero
    table_names = ["SEQ_512_MULTITHREAD_main_papi_NO",
                   "SEQ_512_MULTITHREAD_main_papi_YES",
                   "SEQ_512_MULTITHREAD_main_perf_NO",
                   "SEQ_512_MULTITHREAD_main_perf_YES",
                   "SEQ_512_TRANSPOSE_main_papi_NO",
                   "SEQ_512_TRANSPOSE_main_papi_YES",
                   "SEQ_512_TRANSPOSE_main_perf_NO",
                   "SEQ_512_TRANSPOSE_main_perf_YES"]
    groups = df[0].isin(table_names).cumsum()
    tables = {g.iloc[0, 0]: g.iloc[1:] for k, g in df.groupby(groups)}

    # The fields are in this order:
    # •   optional usec time stamp in fractions of second (with -I xxx)
    # •   optional CPU, core, or socket identifier
    # •   optional number of logical CPUs aggregated
    # •   counter value
    # •   unit of the counter value or empty
    # •   event name
    # •   run time of counter
    # •   percentage of measurement time the counter was running
    # •   optional variance if multiple values are collected with -r
    # •   optional metric value
    # •   optional unit of metric
    # Additional metrics may be printed with all earlier fields being empty.
    tables_header = ["Value", "Unit", "Event Name", "Run Time", "% Timer Running",
                     "opt. Metric Value", "opt. Unit Of Metric"]

    # Cambiando de header
    for k, v in tables.items():
        aux = v[1:]
        v.columns = tables_header

    # Time to create the tables needed
    for k, v in tables.items():
        for c in v.columns:
            if c != tables_header[0] and c != tables_header[2]:
                v = v.drop(c, axis=1)

    # ---------------- PLOTLY ----------------

    # Se crean dos figuras, 1 por cada método de ejecución:
    fig = make_subplots(
        rows=4, cols=2,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}, {"type": "table"}],
               [{"type": "table"}, {"type": "table"}],
               [{"type": "table"}, {"type": "table"}],
               [{"type": "table"}, {"type": "table"}]]
    )

    r = c = 1

    for k, v in tables.items():
        print(v)

    for key, value in tables.items():
        fig.add_trace(
            go.Table(
                header=dict(
                    values=list(v.columns),
                    fill_color='paleturquoise',
                    font=dict(size=15),
                    align="left"
                ),
                cells=dict(
                    values=[v[k].tolist() for k in v.columns],
                    fill_color='lavender',
                    align = "left")
            ),
            row=r, col=c
        )
        r = r + 1
        if r > 4:
            r = 1
            c = c + 1

    fig.update_yaxes(title_text="PAPI with TASKSET", row=1, col=1)
    fig.update_yaxes(title_text="PAPI without TASKSET", row=2, col=1)
    fig.update_yaxes(title_text="PERF with TASKSET", row=3, col=1)
    fig.update_yaxes(title_text="PERF without TASKSET", row=4, col=1)

    fig.update_yaxes(title_text="PAPI with TASKSET", row=1, col=2)
    fig.update_yaxes(title_text="PAPI without TASKSET", row=2, col=2)
    fig.update_yaxes(title_text="PERF with TASKSET", row=3, col=2)
    fig.update_yaxes(title_text="PERF without TASKSET", row=4, col=2)

    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(family="sans-serif",
                        size=12,
                        color="black"),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )

    # key_view = tables.keys()
    # dict_iter = iter(key_view)
    # first_key = next(dict_iter)


    # print(table_names[first_key])




# fig.add_trace(
#     go.Table(
#         header=dict(
#             values=["Date", "Number<br>Transactions", "Output<br>Volume (BTC)",
#                     "Market<br>Price", "Hash<br>Rate", "Cost per<br>trans-USD",
#                     "Mining<br>Revenue-USD", "Trasaction<br>fees-BTC"],
#             font=dict(size=10),
#             align="left"
#         ),
#         cells=dict(
#             values=[df[k].tolist() for k in df.columns[1:]],
#             align = "left")
#     ),
#     row=1, col=1
# )

    # for key, value in tables.items():
    #     fig.add_trace(go.Scatter(x="MULTITHREAD", y=value, name=key,
    #                             marker_color='blue'))

    # for key, value in dict_y2.items():
    #     fig.add_trace(go.Scatter(x=eje_x, y=value, name=key,
    #                             marker_color='red'))

    # for key, value in tables.items():
    #     data = [go.Table(
    #         header=dict(values=list(v.columns),
    #                     fill_color='paleturquoise',
    #                     align='left'),
    #         cells=dict(values=[v.Value, v.Unit, v.EventName, v.percenttimerunning,
    #                            v.Opt_metricvalue, v.Opt_unitofmetric],
    #                    fill_color='lavender',
    #                    align='left'))
    #             ]

    # Add table data
    # table_data = [['Team', 'Wins', 'Losses', 'Ties'],
    #             ['Montréal<br>Canadiens', 18, 4, 0],
    #             ['Dallas Stars', 18, 5, 0],
    #             ['NY Rangers', 16, 5, 0],
    #             ['Boston<br>Bruins', 13, 8, 0],
    #             ['Chicago<br>Blackhawks', 13, 8, 0],
    #             ['Ottawa<br>Senators', 12, 5, 0]]

    # # Initialize a fig with ff.create_table(table_data)
    # fig = ff.create_table(v)
    # for k, v in tables.items():
    #     fig.add_table(v)

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

    fig.show()

    # Se guarda la grafica
    # fig.write_html(name_html)
    # run(["mv", name_html, self.RESDIR])
