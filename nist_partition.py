#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 16:32:01 2018

@author: pedro
"""

import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pandas as pd

def partition_function(element = '', T_e = 0, opt = 0):
    #Need to deal with invalid input errors.
    URL = r'https://physics.nist.gov/cgi-bin/ASD/energy1.pl'
    payload = dict(
                spectrum = element,
                conf_out = opt,
                term_out = opt,
                level_out = opt,
                unc_out = opt,
                j_out = opt,
                lande_out = opt,
                perc_out = opt,
                biblio = opt,
                splitting = opt,
                temp = float(T_e)
            )
    
    post = requests.post(URL, data = payload)
    soup = BeautifulSoup(post.text, "lxml")
    data_line = soup.find_all('span')[-1]

    #gets 'Z = 2.64'
    Z_line = list(data_line.descendants)[-1]
    Z_value = re.findall("\d+\.\d+", Z_line)
    Z = float(Z_value[0])
    
    return Z

def partition_matrix(elements = [], samples_temps = [], output = '', 
                     rename = False, filename = 'ani', **kwargs):
    matrix = defaultdict(list)
    
    if type(elements) == str:   elements = elements.split(',')
    if type(samples_temps) == str:  samples_temps = samples_temps.split(',')
    
    for elmt in elements:
        for temp in samples_temps:
            Z = partition_function(elmt, temp, **kwargs)
            matrix[elmt].append(Z)
    
    df = pd.DataFrame.from_dict(matrix, orient = 'index')
    if rename:  df.columns = samples_temps
    if output:  df_output(df, filename, kind = output)
    else:       return df

    
def df_output(df, filename, kind):
    filename = filename_gen(filename, kind)
    if kind == 'csv' or kind == 'dat':
        df.to_csv(filename, sep = '\t')
    elif kind == 'json':
        df.to_json(filename)
    elif kind == 'excel' or kind == 'xlsx':
        df.to_excel(filename)
    else: pass

        
def filename_gen(filename, kind):
    names = dict(
                csv = 'dat',
                json = 'JSON',
                excel = 'xlsx',
                xlsx = 'xlsx'
            )
    return ''.join(filename, names[kind])

if __name__ == '__main__':
    x = partition_matrix(
 'Mg I, Mg II, Fe I, Fe II, Al I, Al II, Ti I, Ti II, Na I, Na II, K I, K II, Ca I, Ca II, Mn I, Mn II',
 '0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0',
 rename = True)