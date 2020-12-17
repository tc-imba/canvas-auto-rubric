import os
import pbr.version

import numpy as npy
import pandas


def get_version():
    return pbr.version.VersionInfo('canvasautorubric')


def read_data(input_file, header=False, sheet=0):
    if header:
        header = 0
    else:
        header = None
    filename, file_extension = os.path.splitext(input_file)
    df = None
    if file_extension == '.csv':
        df = pandas.read_csv(input_file, header=header, index_col=0)
    elif file_extension == '.xls' or file_extension == '.xlsx':
        df = pandas.read_excel(input_file, header=header, index_col=0, engine='openpyxl', sheet_name=sheet)
    if df is not None:
        df.fillna(0)
    return df
