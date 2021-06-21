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
import os
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash_table.DataTable import DataTable
from dash.dependencies import Input, Output
from dash_table.Format import Format, Scheme

# Forces the program to execute on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Last import or warnning will appear on screen (libcudart not found)
from tensorflow import keras
# --------------------------------------------------------------------------- #

# Dictionary with the key as the new event to generate. The values are 2
# sets with the same event but different name
events_dict = {
    "IPC": [{"instructions",
             "PAPI_TOT_INS",
             "PERF_COUNT_HW_INSTRUCTIONS",
             "INSTRUCTION_RETIRED"},
            {"cycles",
            "PAPI_TOT_CYC",
             "PERF_COUNT_HW_CPU_CYCLES"}],
    "Branch miss rate": [{"branch-misses",
                          "PAPI_BR_MSP",
                          "MISPREDICTED_BRANCH_RETIRED"},
                         {"branch-instructions",
                         "PAPI_BR_CN",
                          "BRANCHES",
                          "BRANCH_INSTRUCTIONS_RETIRED",
                          "PERF_COUNT_HW_BRANCH_INSTRUCTIONS"}],
    "L1 Data cache miss rate": [{"PAPI_L1_DCM",
                                 "PERF_COUNT_HW_CACHE_L1D.MISS"},
                                {"PERF_COUNT_HW_CACHE_L1D.ACCESS"}],
    "L1 Inst cache miss rate": [{"PAPI_L1_ICM",
                                 "PERF_COUNT_HW_CACHE_L1I.MISS"},
                                {"PERF_COUNT_HW_CACHE_L1I.ACCESS"}],
}


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

        # _library_file = lib_path
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

    @staticmethod
    def get_rates_from_df(df):
        """Read the dataframe and check if, with the events in it, is possible
        to calculate rates and new data from them.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe with the columns as events
        """

        cols = set(df.columns.tolist())
        for k, v in events_dict.items():
            if k in cols:
                continue
            # Check if we have the right events
            dividend = set.intersection(cols, v[0])
            divisor = set.intersection(cols, v[1])
            if len(dividend) != 0 and len(divisor) != 0:
                # Divide the two lists and add it to the dataframe
                df[k] = [i[0] / j[0] for i, j in
                         zip(df[dividend].values, df[divisor].values)]
        return df
    # ----------------------------------------------------------------------- #

    @staticmethod
    def read_csv_and_get_rates(csv_file):
        """Read the file with the results and create a pandas Dataframe from it.
        It also pivote the table to make the events as columns; and adds new
        columns calculating the rates (if its possible).

        Parameters
        ----------
        csv_file : str
            Path to the results file of the execution with MyPapi.
        """

        # Read csv with the following name of columns
        df = pd.read_csv(csv_file, header=None, sep=":",
                         names=["CPU", "Value", "Unit", "Event Name"])

        # Get the events and cpus measured
        events = df["Event Name"].unique()
        cpus = df["CPU"].unique()

        # Also the number of iterations (batch_size, epoch, etc)
        num_measures = int(len(df.index) / (len(events) * len(cpus)))

        # Creates a column with the number of iteration
        df.insert(0, "# Measure", 0)

        # We have to modify them depending on the number of measures and cpus
        aux = 0
        for i in range(num_measures, 0, -1):
            aux += 1
            df.loc[df.index[-i * len(events) * len(cpus):], "# Measure"] = aux

        # "Rotate" the table
        df = df.pivot_table(index=["# Measure", "CPU"], columns=[
            "Event Name"], values=["Value"]).fillna(0)

        # Drop the first multiindex
        df.columns = df.columns.droplevel()

        # Add columns with rates (IPC, acc., etc.)
        df = MyPapi.get_rates_from_df(df)

        # Remove name of columns
        df.columns.name = None
        # Reset the index to an auto-increment
        df = df.reset_index()

        # !convertir al principio
        # df = df.melt(id_vars=["CPU", "# Measure"])

        return df
    # ----------------------------------------------------------------------- #

    @staticmethod
    def read_csv_and_print_by_measures(csv_file):

        df = MyPapi.read_csv_and_get_rates(csv_file)

        # No need of CPU column
        df = df.drop(["CPU"], axis=1)

        # Get the list of measures
        measures = df["# Measure"].unique()
        events = df.columns

        # Array with 'num_measures' dicts as entries
        arr_measures = [{} for _ in measures]

        # Store the data
        for i in range(0, len(measures)):
            for e in events:
                dict_aux = arr_measures[i]
                dict_aux[e] = df.loc[df["# Measure"]
                                     == measures[i], e].mean()

        # Convert to pandas Dataframe
        df = pd.DataFrame(arr_measures)
        # Set the # Measure column as index
        df = df.set_index("# Measure")

        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        # Array with the figures/html files to create
        figs = [go.Figure(),
                make_subplots(
                    rows=1, cols=2,
                    specs=[[{"secondary_y": False}, {"secondary_y": False}]],
                    subplot_titles=("Rates", "Derived metrics"))
                ]

        # Add the value to the graphs
        for col in df.columns:
            if col not in events_dict.keys():
                figs[0].add_trace(
                    go.Scatter(x=df.index.values.tolist(), y=df[col], name=col)
                )
            else:
                if "rate" in col:
                    figs[1].add_trace(
                        go.Scatter(x=df.index.values.tolist(),
                                   y=df[col] * 100, name=col),
                        row=1, col=1, secondary_y=False
                    )
                else:
                    figs[1].add_trace(
                        go.Scatter(x=df.index.values.tolist(),
                                   y=df[col], name=col),
                        row=1, col=2, secondary_y=False
                    )
        # Change the name of the y axis
        figs[0].update_yaxes(title_text="Value")
        figs[1].update_yaxes(title_text="Miss rate (%)", row=1, col=1)
        figs[1].update_yaxes(title_text="Value", row=1, col=2)
                
        # Set options common to all traces with fig.update_traces
        for fig in figs:
            fig.update_traces(mode='lines+markers',
                              marker_line_width=2, marker_size=8)
            fig.update_layout(
                title='MyPaPi measure by iterations: ' + csv_file,
                # yaxis_zeroline=False, xaxis_zeroline=False,
                hovermode="x unified",
                legend=dict(
                    # x=-1,
                    # y=-1,
                    traceorder="normal",
                    font=dict(family="sans-serif",
                              size=12,
                              color="black"),
                    bgcolor="white",
                    bordercolor="Black",
                    borderwidth=2
                )
            )
            fig.update_xaxes(range=[0, len(measures) + 1],
                             title_text="Number of measure")
            # ! Open the files when end the execution
            # fig.show()

        # Save the html files
        name_html = csv_file + "_1_.html"
        figs[0].write_html(name_html)
        name_html = csv_file + "_2_.html"
        figs[1].write_html(name_html)
    # ----------------------------------------------------------------------- #

    @staticmethod
    def sum_events(csv_file):
        """Read the file with the results and sum the same events.

        Parameters
        ----------
        csv_file : str
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

        # Set the header and read the csv
        df = pd.read_csv(csv_file, header=None, sep=":",
                         names=["CPU", "Value", "Unit", "Event Name"])

        # Get the events measured
        events = df["Event Name"].unique()

        # Sum of the same events
        events_sum = {}
        for e in events:
            sum = df.loc[df["Event Name"] == e, "Value"].sum()
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
    def dash_create_table(csv_file):

        df = MyPapi.read_csv_and_get_rates(csv_file)

        # Get the cpus measured
        cpus = df["CPU"].unique()

        # Also the number of iterations (batch_size, epoch, etc)
        num_measures = len(df["# Measure"].unique())

        # Create the app
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        columns = []
        for i in df.columns:
            if i == "IPC":
                columns.append({"name": i, "id": i, "type": "numeric",
                                "format": Format(precision=4, scheme=Scheme.fixed)})
            elif "acc" in i or "rate" in i:
                columns.append({"name": i, "id": i, "type": "numeric",
                                "format": Format(precision=2, scheme=Scheme.percentage)})
            else:
                columns.append({"name": i, "id": i, "type": "numeric",
                                "format": Format().group(True), "hideable": True})

        # Create the html page
        app.layout = html.Div([
            # Header
            html.Div([
                html.H1("MyPapi measure: " + csv_file)
            ]),
            # Separator
            html.Hr(),
            # Figures: table or graph
            html.Div([
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=columns,
                    sort_action='native',
                    page_size=num_measures,
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
                        {"selector": ".column-header--delete svg",
                            "rule": 'display: "none"'},
                        {"selector": ".column-header--delete::before", "rule": 'content: "X"'}]
                )
            ])
        ])
        app.run_server(debug=False)
    # ----------------------------------------------------------------------- #

    @staticmethod
    def create_dash_table(csv_file):
        """Test the values in the file and check the total amount of each event
        """

        # Read csv
        df = MyPapi.read_csv_and_get_rates(csv_file)

        # Group params to pass them to plotly
        columns = []
        for i in df.columns:
            columns.append({"name": i, "id": i, "type": "numeric",
                           "format": Format().group(True)})

        data = df.to_dict('records')

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

        df = MyPapi.get_rates_from_df(df)

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
        fig.show()
        # Save it in a file and don't open it now
        # fig.write_html(html_file)
    # ----------------------------------------------------------------------- #

    @staticmethod
    def dash_table_by_cpus(csv_file):
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

        df = MyPapi.get_rates_from_df(df)

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

    @staticmethod
    def plotly_print_evolution(csv_file):

        import plotly.graph_objects as go

        df = MyPapi.read_csv_and_get_rates(csv_file)

        # Get the events and cpus measured
        cpus = df["CPU"].unique()
        num_measure = df["# Measure"].unique()


        url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
        dataset = pd.read_csv(url)

        # print(dataset)
        # exit(0)

        years = ["1952", "1962", "1967", "1972", "1977", "1982", "1987", "1992", "1997", "2002",
                "2007"]

        # make list of continents
        continents = []
        for continent in dataset["continent"]:
            if continent not in continents:
                continents.append(continent)
        # make figure
        fig_dict = {
            "data": [],
            "layout": {},
            "frames": []
        }

        # fill in most of layout
        fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
        fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
        fig_dict["layout"]["hovermode"] = "closest"
        fig_dict["layout"]["updatemenus"] = [
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": False},
                                        "fromcurrent": True, "transition": {"duration": 300,
                                                                            "easing": "quadratic-in-out"}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ]

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Year:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        # make data
        year = 1952
        for continent in continents:
            dataset_by_year = dataset[dataset["year"] == year]
            dataset_by_year_and_cont = dataset_by_year[
                dataset_by_year["continent"] == continent]

            data_dict = {
                "x": list(dataset_by_year_and_cont["lifeExp"]),
                "y": list(dataset_by_year_and_cont["gdpPercap"]),
                "mode": "markers",
                "text": list(dataset_by_year_and_cont["country"]),
                "marker": {
                    "sizemode": "area",
                    "sizeref": 200000,
                    "size": list(dataset_by_year_and_cont["pop"])
                },
                "name": continent
            }
            fig_dict["data"].append(data_dict)

        # make frames
        for year in years:
            frame = {"data": [], "name": str(year)}
            for continent in continents:
                dataset_by_year = dataset[dataset["year"] == int(year)]
                dataset_by_year_and_cont = dataset_by_year[
                    dataset_by_year["continent"] == continent]

                data_dict = {
                    "x": list(dataset_by_year_and_cont["lifeExp"]),
                    "y": list(dataset_by_year_and_cont["gdpPercap"]),
                    "mode": "markers",
                    "text": list(dataset_by_year_and_cont["country"]),
                    "marker": {
                        "sizemode": "area",
                        "sizeref": 200000,
                        "size": list(dataset_by_year_and_cont["pop"])
                    },
                    "name": continent
                }
                frame["data"].append(data_dict)

            fig_dict["frames"].append(frame)
            slider_step = {"args": [
                [year],
                {"frame": {"duration": 300, "redraw": False},
                "mode": "immediate",
                "transition": {"duration": 300}}
            ],
                "label": year,
                "method": "animate"}
            sliders_dict["steps"].append(slider_step)


        fig_dict["layout"]["sliders"] = [sliders_dict]

        fig = go.Figure(fig_dict)

        fig.show()

        name_html = "strides.html"
        fig.write_html(name_html)

        # fig write

    @staticmethod
    def plotly_print_n_graphs(csv_file):

        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        df = MyPapi.read_csv_and_get_rates(csv_file)

        # Get the events and cpus measured
        cpus = df["CPU"].unique()
        num_measure = df["# Measure"].unique()

        # print(df.columns)

        fig = go.Figure()
        # rows = 2
        # cols = 3
        # fig = make_subplots(
        #     rows=rows, cols=cols,
        #     specs=[[{"secondary_y": False}, {"secondary_y": False},
        #             {"secondary_y": False}],
        #            [{"secondary_y": False}, {"secondary_y": False},
        #             {"secondary_y": False}]],
        #     subplot_titles=(df.columns))

        # for k in events_dict.keys():
        #     if

        IPC_list = []
        for n in num_measure:
            dff = df[df["# Measure"] == n]
            IPC_list.append(dff["IPC"])
            fig.add_trace(go.Scatter(x=num_measure, y=IPC_list[-1]
                                    #  name="Measure "+str(n),
                                    #   range_x=[-1,32])
                                      ))

        fig.update_traces(mode='lines+markers')
        # fig.update_xaxes(range=[0, 31])
        # fig.update_yaxes(range=[0, 2])

        fig.show()

    @staticmethod
    def print_m1(csv_file):

        # Read csv with the following name of columns
        df = pd.read_csv(csv_file, header=None, sep=":",
                         names=["CPU", "Value", "Unit", "Event Name"])

        # Get the events and cpus measured
        events = df["Event Name"].unique()
        cpus = df["CPU"].unique()

        # Also the number of iterations (batch_size, epoch, etc)
        num_measures = int(len(df.index) / (len(events) * len(cpus)))

        # Calculate the mean of the 'num_measures' measures
        


        # Creates a column with the number of iteration
        df.insert(0, "# Measure", 0)

        # We have to modify them depending on the number of measures and cpus
        aux = 0
        for i in range(num_measures, 0, -1):
            aux += 1
            df.loc[df.index[-i * len(events) * len(cpus):], "# Measure"] = aux

        # "Rotate" the table
        df = df.pivot_table(index=["# Measure", "CPU"], columns=[
            "Event Name"], values=["Value"]).fillna(0)

        # Drop the first multiindex
        df.columns = df.columns.droplevel()

        # Add columns with rates (IPC, acc., etc.)
        df = MyPapi.get_rates_from_df(df)

        # Remove name of columns
        df.columns.name = None
        # Reset the index to an auto-increment
        df = df.reset_index()

        # !convertir al principio
        # df = df.melt(id_vars=["CPU", "# Measure"])


        # No need of CPU column
        df = df.drop(["CPU"], axis=1)

        # Get the list of measures
        measures = df["# Measure"].unique()
        events = df.columns

        # Array with 'num_measures' dicts as entries
        arr_measures = [{} for _ in measures]

        # Store the data
        for i in range(0, len(measures)):
            for e in events:
                dict_aux = arr_measures[i]
                dict_aux[e] = df.loc[df["# Measure"]
                                     == measures[i], e].mean()

        return df
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
        # cpus = None
        self.cpus = list(range(2, 32))
        # self.cpus = [2]
        self.mp.prepare_measure(events_file=events_file, cpus=self.cpus)

        # Save the output file variable for later
        self.output_file = output_file

        # We have to decompose the path, name and extension of the output file
        if self.output_file is not None:
            # Gets an array with head + tail: path + file_name
            self.head_tail = os.path.split(output_file)
            self.name_extension = os.path.splitext(self.head_tail[1])

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

class MeasureOnTrainPhase(MyCallbacks):
    """
    Custom callback to run with my_papi library and measures the system in the
    training phase.

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

        super(MeasureOnTrainPhase, self).__init__(events_file=events_file,
                                                  lib_path=lib_path,
                                                  output_file=output_file)

    # --------------------------- Global methods ---------------------------- #
    def on_train_begin(self, logs=None):
        """Called at the beginning of fit."""

        # Starts the measure with my_papi library
        self.mp.start_measure()

    def on_train_end(self, logs=None):
        """Called at the end of fit."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)
    # ------------------------- END Global methods -------------------------- #
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

class MeasureEpochAndBatch(keras.callbacks.Callback):
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

        super(MeasureEpochAndBatch, self).__init__()

        # Creates two objects of the class my_papi
        self.mp_epoch = MyPapi(lib_path=lib_path)
        self.mp_batch = MyPapi(lib_path=lib_path)

        # Prepares the measure on ALL cpus
        # ! modify this to get the num of cpus automatic
        # cpus = None
        self.cpus = list(range(2, 32))
        self.mp_epoch.prepare_measure(events_file=events_file, cpus=self.cpus)
        self.mp_batch.prepare_measure(events_file=events_file, cpus=self.cpus)

        # Save the output file variable for later
        self.output_file = output_file

        # We have to decompose the path, name and extension of the output file
        if self.output_file is not None:
            # Gets an array with head + tail: path + file_name
            self.head_tail = os.path.split(output_file)
            self.name_extension = os.path.splitext(self.head_tail[1])

            # From the file indicated, generate a new file
            self.batch_output_file = self.head_tail[0] + "/" + str(self.name_extension[0]
            + "_batch" + self.name_extension[1])
        else:
            self.batch_output_file = None
        # Just measure the batches indicated
        self.measure_batch = True

    # ------------------------- Batch-level methods ------------------------- #
    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        if self.measure_batch:
            self.mp_batch.start_measure()

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        if self.measure_batch:
            self.mp_batch.stop_measure()
            self.mp_batch.print_measure(self.batch_output_file)
    # ----------------------- END Batch-level methods ----------------------- #

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        print("Begin del epoch", epoch)

        if epoch == 1:
            self.measure_batch = False

        # Starts the measure with my_papi library
        self.mp_epoch.start_measure()

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        print("\nEnd del epoch", epoch)

        # Stops the measure with my_papi library
        self.mp_epoch.stop_measure()

        # Saves the results on a file
        self.mp_epoch.print_measure(self.output_file)

        # if epoch == 1:
        #     self.measure_batch = False
    # ----------------------- END Epoch-level methods ----------------------- #
# --------------------------------------------------------------------------- #
