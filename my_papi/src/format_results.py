#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import locale

# 3rd party packages
from ctypes import *

# local source
import pandas as pd
import dash
import dash_html_components as html
import dash_table
# from dash_table import DataTable, FormatTemplate
from dash_table.Format import Format, Scheme
import dash_html_components as html

# --------------------------------------------------------------------------- #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria", "Pablo Abad", "Pablo Prieto"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# --------------------------------------------------------------------------- #


class format_results(object):
    """Permite realizar medidas de los eventos mediante el uso de la
    libreria libmy_papi.so, que a su vez se basa en el codigo de PAPI."""

    # Attributes
    # ----------
    # self.cores          # Array de cores logicos pertenecientes al mismo fisico
    # self.p_lib          # Con el se puede acceder a la liberia y sus func.
    # self.num_event_sets # numero de event_sets
    # self.event_sets     # lista con los event_setss

    def __init__(self):
        """Constructor de la clase my_papi que recibe por parametro la
        localizacion de la liberia libmy_papi.so."""

        super(format_results, self).__init__()
    # ----------------------------------------------------------------------- #

    def check_results(self, events_file, output_file):
        """Test the values in the file and check the total amount of each event
        """

        import pandas as pd

        # Setting the dict of event name and how many computations represent
        # each count
        computations_dict = {
            "fp_arith_inst_retired.128b_packed_double": 2,
            "fp_arith_inst_retired.128b_packed_single": 4,
            "fp_arith_inst_retired.256b_packed_double": 4,
            "fp_arith_inst_retired.256b_packed_single": 8,
            "fp_arith_inst_retired.512b_packed_double": 8,
            "fp_arith_inst_retired.512b_packed_single": 16,
            "fp_arith_inst_retired.scalar_double": 1,
            "fp_arith_inst_retired.scalar_single": 1,
            "fp_assist.any": 1
        }

        # Read events from file
        with open(events_file) as f:
            self.events = f.read().splitlines()

        # Read csv
        data = pd.read_csv(output_file, header=None, sep=":", names=range(4))

        # Assign new header
        header = ["CPU", "Value", "Unit", "Event Name"]
        data.columns = header

        # Sum of the same events
        events_sum = {}
        for e in self.events:
            sum = data.loc[data["Event Name"] == e, "Value"].sum()
            events_sum[e] = sum

        # Print the sum of the events
        locale.setlocale(locale.LC_ALL, '')
        total_fp_events = 0
        for k, v in events_sum.items():
            print("Sum [", k, "] =", locale.format_string('%.0f', v, True))
            if computations_dict.get(k) is not None:
                total_fp_events += computations_dict[k] * v
        print("Total fp measured =", locale.format_string('%.0f',
                                                          total_fp_events, True))
    # ----------------------------------------------------------------------- #

    def create_dash_table(self, csv_file):
        """Test the values in the file and check the total amount of each event
        """

        # Read csv
        header = ["CPU", "Value", "Unit", "Event Name"]
        df = pd.read_csv(csv_file, header=None, sep=":", names=header)

        # Pivot it
        df = df.pivot_table(index=["CPU"], columns=[
                            "Event Name"], values=["Value"]).fillna(0)

        # Drop the first multiindex
        df.columns = df.columns.droplevel()

        # Group params to pass them to plotly
        columns = []
        columns.insert(0, {"name": "CPU", "id": "CPU", "type": "numeric"})
        for i in df.columns:
            columns.append({"name": i, "id": i, "type": "numeric",
                           "format": Format().group(True)})

        data = df.to_dict('records')
        index = df.index.values.tolist()
        for i in range(0, len(data)):
            dictionary = data[i]
            dictionary["CPU"] = index[i]

        # Adding IPC
        columns.append({"name": "IPC", "id": "IPC", "type": "numeric",
                       "format": Format(precision=4, scheme=Scheme.fixed)})
        ipc = self.calculate_rate(df["instructions"], df["cycles"])
        for i in range(0, len(data)):
            data[i]["IPC"] = ipc[i]
        # Adding branch %
        columns.append({"name": "Branch acc.", "id": "Branch acc.", "type": "numeric",
                       "format": Format(precision=2, scheme=Scheme.percentage)})
        brnch = self.calculate_rate(
            df["branch-misses"], df["branch-instructions"])
        for i in range(0, len(data)):
            data[i]["Branch acc."] = brnch[i]

        # Create the app
        app = dash.Dash(__name__)
        app.layout = html.Div(children=[
            # Header
            html.H1(children=str(csv_file)),

            # Subtitle
            html.Div(children='''
                MyPapi: Events measured
            '''),

            # Table
            dash_table.DataTable(
                sort_action='native',
                id='table',
                columns=columns,
                data=data,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'height': 'auto',
                    'whiteSpace': 'normal',
                },
                style_header={
                    'backgroundColor': 'paleturquoise',
                    'fontWeight': 'bold'
                },
                # style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender")
            )
        ])

        app.run_server(debug=False)
    # ----------------------------------------------------------------------- #

    def create_plotly_table(self, csv_file, html_file):
        """Test the values in the file and check the total amount of each event
        """

        import plotly.graph_objects as go
        import pandas as pd

        # Read csv
        header = ["CPU", "Value", "Unit", "Event Name"]
        df = pd.read_csv(csv_file, header=None, sep=":", names=header)

        # Pivot it
        df = df.pivot_table(index=["CPU"], columns=[
                            "Event Name"], values=["Value"]).fillna(0)

        # Drop the first multiindex
        df.columns = df.columns.droplevel()

        # Group params to pass them to plotly
        df_T = df.transpose()
        hd = list(df.columns)
        hd.insert(0, "CPU")
        bd = list(df_T.values)
        bd.insert(0, df.index)

        fig = go.Figure(data=[go.Table(
            header=dict(values=hd, fill_color='paleturquoise', align='left'),
            cells=dict(values=bd, fill_color='lavender', align='left'))
        ])

        # Display it at the end of execution
        # fig.show()
        # Save it in a file and don't open it now
        fig.write_html(html_file)
    # ----------------------------------------------------------------------- #

    def calculate_rate(self, dividend, divisor):
        aux = []
        if len(dividend) != len(divisor):
            return

        for i in range(0, len(dividend)):
            aux.append(dividend[i] / divisor[i])

        return aux
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #


if __name__ == "__main__":

    from format_results import format_results

    # Creates a object
    fm = format_results()

    # CHECKING RESULTS!
    events_file = "conf/events_node.cfg"
    csv_file = "out/file_w_callbacks.csv"
    # html_file = "out/file_w_callbacks.html"
    # fm.create_plotly_table(csv_file, html_file)
    # fm.create_dash_table(csv_file)

    # csv_file = "out/main_file.csv"
    # html_file = "out/main_file.html"
    # fm.create_plotly_table(csv_file, html_file)
    # fm.create_dash_table(csv_file)


    fm.check_results(events_file, csv_file)