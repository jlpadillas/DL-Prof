#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["University of Cantabria", "Pablo Abad", "Pablo Prieto"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# --------------------------------------------------------------------------- #

# Imports for the module
from ctypes import CDLL, c_int, c_char_p, POINTER
from locale import setlocale, format_string, LC_ALL


# Sets the locale for future prints
# setlocale(LC_ALL, '')
from os import environ
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash_table.DataTable import DataTable
from dash.dependencies import Input, Output
from dash_table.Format import Format, Scheme

# Forces the program to execute on CPU
environ['CUDA_VISIBLE_DEVICES'] = '0'
# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Last import or warnning will appear on screen (libcudart not found)
from tensorflow import keras
# --------------------------------------------------------------------------- #


class MyPapi(object):
    """
    Class that uses the libmy_papi.so library and perform measures of events.
    It is based on the Performance Application Programming Interface (PAPI).

    Attributes
    ----------
    self.p_lib : ctypes.CDLL
        Library of my_papi
    self.cpus : list
        List of int where the system will measure the events
    self.events_file : str
        Path where the file with the events is located
    self.output_file : str
        Path where the file with the results is located
    """

    def __init__(self, lib_path):
        """
        My_papi class constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        """

        super(MyPapi, self).__init__()

        # Loads the library path
        self.__set_my_lib(lib_path)
    # ----------------------------------------------------------------------- #

    def prepare_measure(self, events_file, cpus=None):
        """It performs the necessary adjustments before start measuring.

        A file path is passed as a parameter where the events to be measured
        are distributed one per line.

        If the argument `cpus` isn't passed in, then the default CPUs to be
        measured will be all the logical cores of the system.

        Parameters
        ----------
        events_file : str
            Path where the file is located
        cpus : list, optional
            List of integers which corresponds to the cpus where we have to
            measure the events (default is all)
        """

        if cpus is None:
            import multiprocessing
            cpus = list(range(0, multiprocessing.cpu_count()))

        # Saving the passed arguments
        self.events_file = events_file
        self.cpus = cpus

        # Now, we have to cast the data to pass them to the C library
        # 1. Encode the string
        # 2. Create a c_int type with the length of the cpu list
        # 3. Cast the cpu list to: int*
        len_cpus = len(cpus)
        self.p_lib.my_prepare_measure(events_file.encode('utf-8'),
                                      c_int(len_cpus),
                                      (c_int * len_cpus)(*cpus))
    # ----------------------------------------------------------------------- #

    def start_measure(self):
        """Calls the C function with the same name and start the measuring.

        Parameters
        ----------
        None
        """

        self.p_lib.my_start_measure()
    # ----------------------------------------------------------------------- #

    def stop_measure(self):
        """Calls the C function with the same name and stop the measuring.

        Parameters
        ----------
        None
        """

        self.p_lib.my_stop_measure()
    # ----------------------------------------------------------------------- #

    def print_measure(self, output_file=None):
        """Print the results to the screen or to a file.

        If the argument `output_file` isn't passed in, then the default output
        is the screen.

        Parameters
        ----------
        output_file : str, optional
            Path (and name) of the file where the results will be printed.
        """

        self.output_file = output_file
        if output_file is not None:
            output_file = output_file.encode('utf-8')

        self.p_lib.my_print_measure(output_file)
    # ----------------------------------------------------------------------- #

    def finalize_measure(self):
        """Calls the C function with the same name which will stop the my_papi
        library and free the memory used.

        Parameters
        ----------
        None
        """

        self.p_lib.my_finalize_measure()
    # ----------------------------------------------------------------------- #

    def __set_my_lib(self, lib_path):
        """
        Loads the library libmy_papi.so from the PATH passed by parameter and
        define the input/output of the main functions.

        Parameters
        ----------
        lib_path : Path
            Path to the library
        """

        _library_file = lib_path
        self.p_lib = CDLL(lib_path)

        # ------------------------------------------------------------------- #
        # int my_prepare_measure(char *input_file_name, int num_cpus,
        #                       int *cpus)
        # ------------------------------------------------------------------- #
        self.p_lib.my_prepare_measure.argtypes = [
            c_char_p, c_int, POINTER(c_int)]
        self.p_lib.my_prepare_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_start_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_start_measure.argtypes = None
        self.p_lib.my_start_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_stop_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_stop_measure.argtypes = None
        self.p_lib.my_stop_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_print_measure(char *output_file_name)
        # ------------------------------------------------------------------- #
        self.p_lib.my_print_measure.argtypes = [c_char_p]
        self.p_lib.my_print_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_finalize_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_finalize_measure.argtypes = None
        self.p_lib.my_finalize_measure.restype = c_int
    # ----------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #

    def dash_table_by_cpus(self, csv_file):
        """Create a dash app and prints several tables grouped by the CPU.
        """

        # Read csv with the following header
        header = ["CPU", "Value", "Unit", "Event Name"]
        df = pd.read_csv(csv_file, header=None, sep=":", names=header)

        # Get the list of CPUs measured
        available_cpus = df["CPU"].unique()
        # And the events
        events_measured = df["Event Name"].unique()

        # Add to the first column the # of measure
        num_measure = 0
        df.insert(0, "# Measure", num_measure)
        # We have to modify them depending on the number of measures and cpus
        len_per_df = len(events_measured) * len(available_cpus)
        for i in range(int(len(df.index) / len_per_df), 0, -1):
            df.loc[df.index[-i * len_per_df:], "# Measure"] = num_measure
            num_measure += 1

        df = df.pivot_table(index=["# Measure", "CPU"], columns=[
            "Event Name"], values=["Value"]).fillna(0)
        # Drop the first multiindex
        df.columns = df.columns.droplevel()

        df = self.get_rates_from_df(df)

        # cpu_value = 2
        # dfff = dff.query('CPU == @cpu_value')

        # Create the app
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


        # Create the html page
        app.layout = html.Div([
            # Header
            html.Div([
                html.H1("MyPapi measure")
            ]),
            # Options
            html.Div([
                html.Table(
                    [
                        html.Thead([
                            html.Tr([
                                html.Th("CPU", style={'width': 200}),
                                html.Th("Type of representation")
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                html.Td([
                                    dcc.Dropdown(
                                        id='cpu-dropdown',
                                        options=[{'label': i, 'value': i}
                                                 for i in available_cpus],
                                        value='0',
                                        style={'width': 200, 'align-items': 'center', 'justify-content': 'center'}
                                    )
                                ], style={'width': 200, 'align-items': 'center', 'justify-content': 'center'}),
                                html.Td([
                                    dcc.RadioItems(
                                        id='table-graph-radio-items',
                                        options=[{'label': i, 'value': i}
                                                 for i in ['Table', 'Graph']],
                                        value='Table'
                                    )
                                ])
                            ], style={'align-items': 'center', 'justify-content': 'center'})
                        ], style={'align-items': 'center', 'justify-content': 'center'})
                    ]
                )
            ]),
            # Separator
            html.Hr(),
            # Figures: table or graph
            html.Div([
                # dash_table.DataTable(id='datatable-upload-container')
                dash_table.DataTable(
                    sort_action='native',
                    id='datatable-upload-container',
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
                    style_data=dict(backgroundColor="lavender"),
                    export_format='xlsx',
                    export_headers='display',
                    css=[
                    {"selector": ".column-header--delete svg", "rule": 'display: "none"'},
                    {"selector": ".column-header--delete::before", "rule": 'content: "X"'}]
                )
                # ,
                # dcc.Graph(id='datatable-upload-graph')
            ])
        ])

        @app.callback(
            # Output(component_id='table-graph', component_property='figure'),
            Output(component_id='datatable-upload-container',
                   component_property='data'),
            Output(component_id='datatable-upload-container',
                   component_property='columns'),
            Input(component_id='cpu-dropdown', component_property='value')
            # ,
            # Input(component_id='table-graph-radio-items', component_property='value')
        )
        def update_output(cpu_dropdown_name):  # , table_graph_name):

            # Get the data with the CPU selected
            dff = df.query('CPU == @cpu_dropdown_name')

            # Group params to pass them to plotly
            columns = []
            columns.insert(
                0, {"name": "# Measure", "id": "# Measure", "type": "numeric"})
            for i in dff.columns:
                if i == "IPC":
                    columns.append({"name": "IPC", "id": "IPC", "type": "numeric",
                                    "format": Format(precision=4, scheme=Scheme.fixed)})
                else:
                    columns.append({"name": i, "id": i, "type": "numeric",
                                    "format": Format().group(True),"hideable": True})

            data = dff.to_dict('records')
            indexes = dff.index.values.tolist()
            for i in range(0, len(data)):
                data[i]["# Measure"] = indexes[i][0] + 1

            return data, columns

        # @app.callback(
        #     Output(component_id='datatable-upload-graph',
        #            component_property='figure'),
        #     Input(component_id='datatable-upload-container', component_property='data'))
        # def display_graph(rows):
        #     df = pd.DataFrame(rows)

        #     if (df.empty or len(df.columns) < 1):
        #         return {
        #             'data': [{
        #                 'x': [],
        #                 'y': [],
        #                 'type': 'bar'
        #             }]
        #         }
        #     return {
        #         'data': [{
        #             'x': df[df.columns[0]],
        #             'y': df[df.columns[1]],
        #             'type': 'bar'
        #         }]
        #     }

        app.run_server(debug=False)
    # ----------------------------------------------------------------------- #

    def get_rates_from_df(self, df):

        # Setting the dict of rate and the events needed to perform the operation
        events_dict = {
            "IPC": ["instructions", "cycles"],
            "Branch acc.": ["branch-misses", "branch-instructions"],
            "L1 rate": ["L1-dcache-load-misses", "L1-dcache-loads"]
        }

        indexes = df.index.values.tolist()
        for k,v in events_dict.items():
            if v[0] in df.columns and v[1] in df.columns:
                aux = self.calculate_rate(df[v[0]].tolist(), df[v[1]].tolist())
                for i in range(0, len(indexes)):
                    df[k] = aux[i]

        return df

    @staticmethod
    def sum_events(events_file, output_file):
        """Read the file 'output_file' and sum the same events.

        Parameters
        ----------
        events_file : str
        output_file : str
        """

        # Setting the dict of event name and how many computations represent
        # each count. Valid on node
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
            events = f.read().splitlines()

        # Set the header and read the csv
        header = ["CPU", "Value", "Unit", "Event Name"]
        data = pd.read_csv(output_file, header=None, sep=":", names=header)

        # Sum of the same events
        events_sum = {}
        for e in events:
            sum = data.loc[data["Event Name"] == e, "Value"].sum()
            events_sum[e] = sum

        # Print the sum of the events
        total_fp_events = 0
        for k, v in events_sum.items():
            print("Sum[{}] = {}".format(k, format_string('%.0f', v, True)))
            if k in computations_dict:
                total_fp_events += computations_dict[k] * v

        print("Total fp measured =", format_string('%.0f',
                                                   total_fp_events, True))
    # ----------------------------------------------------------------------- #

    @staticmethod
    def create_dash_table(csv_file):
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

        df = MyPapi.get_rates_from_df_static(df)

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

    @staticmethod
    def create_plotly_table(csv_file, html_file):
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

    @staticmethod
    def calculate_rate_static(dividend, divisor):
        aux = []
        if len(dividend) != len(divisor):
            return

        for i in range(0, len(dividend)):
            aux.append(dividend[i] / divisor[i])

        return aux
    # ----------------------------------------------------------------------- #

    @staticmethod
    def get_rates_from_df_static(df):

        # Setting the dict of rate and the events needed to perform the operation
        events_dict = {
            "IPC": ["instructions", "cycles"],
            "Branch acc.": ["branch-misses", "branch-instructions"],
            "L1 rate": ["L1-dcache-load-misses", "L1-dcache-loads"]
        }

        indexes = df.index.values.tolist()
        for k,v in events_dict.items():
            if v[0] in df.columns and v[1] in df.columns:
                aux = MyPapi.calculate_rate_static(df[v[0]].tolist(), df[v[1]].tolist())
                for i in range(0, len(indexes)):
                    df[k] = aux[i]

        return df

    @staticmethod
    def dash_table_by_cpus_static(csv_file):
        """Create a dash app and prints several tables grouped by the CPU.
        """

        # Read csv with the following header
        header = ["CPU", "Value", "Unit", "Event Name"]
        df = pd.read_csv(csv_file, header=None, sep=":", names=header)

        # Get the list of CPUs measured
        available_cpus = df["CPU"].unique()
        # And the events
        events_measured = df["Event Name"].unique()

        # Add to the first column the # of measure
        num_measure = 0
        df.insert(0, "# Measure", num_measure)
        # We have to modify them depending on the number of measures and cpus
        len_per_df = len(events_measured) * len(available_cpus)
        for i in range(int(len(df.index) / len_per_df), 0, -1):
            df.loc[df.index[-i * len_per_df:], "# Measure"] = num_measure
            num_measure += 1

        df = df.pivot_table(index=["# Measure", "CPU"], columns=[
            "Event Name"], values=["Value"]).fillna(0)
        # Drop the first multiindex
        df.columns = df.columns.droplevel()

        df = MyPapi.get_rates_from_df_static(df)

        # cpu_value = 2
        # dfff = dff.query('CPU == @cpu_value')

        # Create the app
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


        # Create the html page
        app.layout = html.Div([
            # Header
            html.Div([
                html.H1("MyPapi measure")
            ]),
            # Options
            html.Div([
                html.Table(
                    [
                        html.Thead([
                            html.Tr([
                                html.Th("CPU", style={'width': 200}),
                                html.Th("Type of representation")
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                html.Td([
                                    dcc.Dropdown(
                                        id='cpu-dropdown',
                                        options=[{'label': i, 'value': i}
                                                 for i in available_cpus],
                                        value='0',
                                        style={'width': 200, 'align-items': 'center', 'justify-content': 'center'}
                                    )
                                ], style={'width': 200, 'align-items': 'center', 'justify-content': 'center'}),
                                html.Td([
                                    dcc.RadioItems(
                                        id='table-graph-radio-items',
                                        options=[{'label': i, 'value': i}
                                                 for i in ['Table', 'Graph']],
                                        value='Table'
                                    )
                                ])
                            ], style={'align-items': 'center', 'justify-content': 'center'})
                        ], style={'align-items': 'center', 'justify-content': 'center'})
                    ]
                )
            ]),
            # Separator
            html.Hr(),
            # Figures: table or graph
            html.Div([
                # dash_table.DataTable(id='datatable-upload-container')
                dash_table.DataTable(
                    sort_action='native',
                    id='datatable-upload-container',
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
                    style_data=dict(backgroundColor="lavender"),
                    export_format='xlsx',
                    export_headers='display',
                    css=[
                    {"selector": ".column-header--delete svg", "rule": 'display: "none"'},
                    {"selector": ".column-header--delete::before", "rule": 'content: "X"'}]
                )
                # ,
                # dcc.Graph(id='datatable-upload-graph')
            ])
        ])

        @app.callback(
            # Output(component_id='table-graph', component_property='figure'),
            Output(component_id='datatable-upload-container',
                   component_property='data'),
            Output(component_id='datatable-upload-container',
                   component_property='columns'),
            Input(component_id='cpu-dropdown', component_property='value')
            # ,
            # Input(component_id='table-graph-radio-items', component_property='value')
        )
        def update_output(cpu_dropdown_name):  # , table_graph_name):

            # Get the data with the CPU selected
            dff = df.query('CPU == @cpu_dropdown_name')

            # Group params to pass them to plotly
            columns = []
            columns.insert(
                0, {"name": "# Measure", "id": "# Measure", "type": "numeric"})
            for i in dff.columns:
                if i == "IPC":
                    columns.append({"name": i, "id": i, "type": "numeric",
                                    "format": Format(precision=4, scheme=Scheme.fixed)})
                elif "acc" in i or "rate" in i:
                    columns.append({"name": i, "id": i, "type": "numeric",
                                    "format": Format(precision=2, scheme=Scheme.percentage)})
                else:
                    columns.append({"name": i, "id": i, "type": "numeric",
                                    "format": Format().group(True), "hideable": True})

            data = dff.to_dict('records')
            indexes = dff.index.values.tolist()
            for i in range(0, len(data)):
                data[i]["# Measure"] = indexes[i][0] + 1

            return data, columns

        # @app.callback(
        #     Output(component_id='datatable-upload-graph',
        #            component_property='figure'),
        #     Input(component_id='datatable-upload-container', component_property='data'))
        # def display_graph(rows):
        #     df = pd.DataFrame(rows)

        #     if (df.empty or len(df.columns) < 1):
        #         return {
        #             'data': [{
        #                 'x': [],
        #                 'y': [],
        #                 'type': 'bar'
        #             }]
        #         }
        #     return {
        #         'data': [{
        #             'x': df[df.columns[0]],
        #             'y': df[df.columns[1]],
        #             'type': 'bar'
        #         }]
        #     }

        app.run_server(debug=False)
    # ----------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #


class MyCallbacks(keras.callbacks.Callback):
    """
    Abstact class which have custom callbacks to use with my_papi library.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        My_callbacks class constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MyCallbacks, self).__init__()

        # Creates an object of the class my_papi
        self.mp = MyPapi(lib_path=lib_path)

        # Prepares the measure on ALL cpus
        # ! modify this to get the num of cpus automatic
        cpus = list(range(2, 32))
        self.mp.prepare_measure(events_file=events_file, cpus=cpus)

        # Save the output file variable for later
        self.output_file = output_file

    # --------------------------- Global methods ---------------------------- #
    def on_train_begin(self, logs=None):
        """Called at the beginning of fit."""

        pass

    def on_train_end(self, logs=None):
        """Called at the end of fit."""

        pass

    def on_test_begin(self, logs=None):
        """Called at the beginning of evaluate."""

        pass

    def on_test_end(self, logs=None):
        """Called at the end of evaluate."""

        pass

    def on_predict_begin(self, logs=None):
        """Called at the beginning of predict."""

        pass

    def on_predict_end(self, logs=None):
        """Called at the end of predict."""

        pass
    # ------------------------- END Global methods -------------------------- #

    # ------------------------- Batch-level methods ------------------------- #
    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        pass

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        pass

    def on_test_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during testing."""

        pass

    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of testing a batch. Within this method, logs is a
        dict containing the metrics results."""

        pass

    def on_predict_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during predicting."""

        pass

    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of predicting a batch. Within this method, logs is
        a dict containing the metrics results."""

        pass
    # ----------------------- END Batch-level methods ----------------------- #

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        pass

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        pass
    # ----------------------- END Epoch-level methods ----------------------- #

    def finalize_measure(self):
        """Ends the measure."""

        self.mp.finalize_measure()
# --------------------------------------------------------------------------- #


class MeasureOnEachEpoch(MyCallbacks):
    """
    Custom callback to run with my_papi library and measures the system in each
    epoch.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MeasureOnEachEpoch, self).__init__(events_file=events_file,
                                                 lib_path=lib_path,
                                                 output_file=output_file)

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        # Starts the measure with my_papi library
        self.mp.start_measure()

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)
    # ----------------------- END Epoch-level methods ----------------------- #
# --------------------------------------------------------------------------- #


class MeasureOnEachBatch(MyCallbacks):
    """
    Custom callback to run with my_papi library and measures the system in each
    batch.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MeasureOnEachBatch, self).__init__(events_file=events_file,
                                                 lib_path=lib_path,
                                                 output_file=output_file)

    # ------------------------- Batch-level methods ------------------------- #
    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        # Starts the measure with my_papi library
        self.mp.start_measure()

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)

    def on_test_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during testing."""
        pass

    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of testing a batch. Within this method, logs is a
        dict containing the metrics results."""
        pass

    def on_predict_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during predicting."""
        pass

    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of predicting a batch. Within this method, logs is
        a dict containing the metrics results."""
        pass
    # ----------------------- END Batch-level methods ----------------------- #
# --------------------------------------------------------------------------- #
