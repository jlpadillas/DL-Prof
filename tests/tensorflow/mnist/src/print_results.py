#! /usr/bin/env python3
# -- coding: utf-8 --

# ------------------------------------------------------------------------ #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["University of Cantabria"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    """TODO:
    """

    # standard library
    import locale

    # Define the locale format
    locale.setlocale(locale.LC_ALL, '')

    # -------------------------------------------------------------------- #
    # Loads the my_papi library
    # -------------------------------------------------------------------- #
    import os
    import pathlib
    import sys

    # Absolute path to this script
    PATH_FILE = pathlib.Path(__file__).absolute()
    # Now, we have to move to the root of this workspace ([prev. path]/TFG)
    MY_PAPI_DIR = PATH_FILE.parent.parent.parent.parent.parent.absolute()
    # From the root (TFG/) access to my_papi dir. and its content
    MY_PAPI_DIR = MY_PAPI_DIR / "my_papi"
    # Folder where the library is located
    LIB_DIR = MY_PAPI_DIR / "lib"
    # Folder where the source codes are located
    SRC_DIR = MY_PAPI_DIR / "src"

    # Add the source path and import the library
    sys.path.insert(0, str(SRC_DIR))
    from MyPapi import *

    # -------------------------------------------------------------------- #
    # Params for the measure
    # -------------------------------------------------------------------- #
    # Path to the library, needed to create an object of class my_papi
    libname = LIB_DIR / "libmy_papi.so"



    folder = "out/"
    # folder = "out/opti_tensorflow/"
    # csv_file = folder + "mnist_papi.csv"
    # csv_file = folder + "mnist_each_epoch.csv"
    # MyPapi.plotly_print_evolution(csv_file)
    # MyPapi.dash_create_table(csv_file)
    # MyPapi.create_plotly_table(csv_file, None)
    # MyPapi.plotly_print_evolution(csv_file)
    # MyPapi.read_csv_and_print_by_measures(csv_file)

    csv_file = folder + "mnist_train_papi.csv"
    # MyPapi.create_plotly_table(csv_file, None)

    # csv_file = folder + "mnist_test_papi.csv"
    # MyPapi.create_plotly_table(csv_file, None)

    # csv_file = folder + "mnist_predict_papi.csv"
    MyPapi.create_dash_table(csv_file)
    exit(0)




    # Plot the next csv files
    csv_files = ["out/mnist_each_epoch.csv",
                 "out/mnist_papi.csv"]

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    # Since we're adding callbacks to elements that don't exist in the app.layout,
    # Dash will raise an exception to warn us that we might be
    # doing something wrong.
    # In this case, we're adding the elements through a callback, so we can ignore
    # the exception.
    app = dash.Dash(__name__, suppress_callback_exceptions=True)

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    index_page = html.Div([
        dcc.Link('Go to the measure of mnist with MyPapi', href='/page-1'),
        html.Br(),
        dcc.Link('Go to the measure of mnist in each epoch', href='/page-2'),
    ])



    page_1_layout = html.Div([
        html.H1('Page 1'),
        dcc.Dropdown(
            id='page-1-dropdown',
            options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
            value='LA'
        ),
        html.Div(id='page-1-content'),
        html.Br(),
        dcc.Link('Go to Page 2', href='/page-2'),
        html.Br(),
        dcc.Link('Go back to home', href='/'),
    ])

    @app.callback(dash.dependencies.Output('page-1-content', 'children'),
                [dash.dependencies.Input('page-1-dropdown', 'value')])
    def page_1_dropdown(value):
        return 'You have selected "{}"'.format(value)


    page_2_layout = html.Div([
        html.H1('Page 2'),
        dcc.RadioItems(
            id='page-2-radios',
            options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
            value='Orange'
        ),
        html.Div(id='page-2-content'),
        html.Br(),
        dcc.Link('Go to Page 1', href='/page-1'),
        html.Br(),
        dcc.Link('Go back to home', href='/')
    ])

    @app.callback(dash.dependencies.Output('page-2-content', 'children'),
                [dash.dependencies.Input('page-2-radios', 'value')])
    def page_2_radios(value):
        return 'You have selected "{}"'.format(value)


    # Update the index
    @app.callback(dash.dependencies.Output('page-content', 'children'),
                [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/page-1':
            return page_1_layout
        elif pathname == '/page-2':
            return page_2_layout
        else:
            return index_page
        # You could also return a 404 "URL not found" page here


    app.run_server(debug=True)











    exit(0)
    # -------------------------------------------------------------------- #
    
    csv_file = "out/mnist_each_epoch.csv"
    df = MyPapi.read_csv_and_get_rates(csv_file)
    MyPapi.dash_create_table(df)

    exit(0)

    # ! main_papi.py
    csv_file = "out/mnist_papi.csv"
    # html_file = "out/mnist_papi.html"
    # # fm.create_plotly_table(csv_file, html_file)
    # MyPapi.create_dash_table(csv_file)

    # ! mnist_each_epoch.py
    csv_file = "out/mnist_each_epoch.csv"
    html_file = "out/main_callback_batch.html"
    # fm.create_plotly_table(csv_file, html_file)
    # fm.create_dash_table(csv_file)
    # MyPapi.dash_table_by_cpus(csv_file)
    MyPapi.create_plotly_table(csv_file, html_file)

    # ! mnist_each_batch.py
    csv_file = "out/mnist_each_batch.csv"
    # html_file = "out/main_callback_epoch.html"
    # # fm.create_plotly_table(csv_file, html_file)
    # # fm.create_dash_table(csv_file)
    # MyPapi.dash_table_by_cpus(csv_file)
