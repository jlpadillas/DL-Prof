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

# Imports
from ctypes import *
import locale
import os

# Forces the program to execute on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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

    def check_results(self, file_name):
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
        with open(self.events_file) as f:
            events = f.read().splitlines()

        # Read csv
        data = pd.read_csv(file_name, header=None, sep=":", names=range(4))

        # Assign new header
        header = ["CPU", "Value", "Unit", "Event Name"]
        data.columns = header

        # Sum of the same events
        events_sum = {}
        for e in events:
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

    def create_table(self, file_name):
        """Test the values in the file and check the total amount of each event
        """

        import plotly.graph_objects as go
        import pandas as pd

        # Read events from file
        with open(self.events_file) as f:
            events = f.read().splitlines()

        # Read csv
        df = pd.read_csv(file_name, header=None, sep=":", names=range(4))

        # Assign new header
        header = ["CPU", "Value", "Unit", "Event Name"]
        df.columns = header

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=df["CPU"],
                       fill_color='lavender',
                       align='left'))
        ])

        fig.write_html("out/file.html")
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


class MyResults(object):
    """
    Permite realizar medidas de los eventos mediante el uso de la
    libreria libmy_papi.so, que a su vez se basa en el codigo de PAPI.

    Attributes
    ----------
    self.cores          # Array de cores logicos pertenecientes al mismo fisico
    self.p_lib          # Con el se puede acceder a la liberia y sus func.
    self.num_event_sets # numero de event_sets
    self.event_sets     # lista con los event_setss
    """

    def __init__(self):
        """Constructor de la clase my_papi que recibe por parametro la
        localizacion de la liberia libmy_papi.so."""

        super(MyResults, self).__init__()
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
        self.mp.prepare_measure(events_file=events_file, cpus=None)

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
