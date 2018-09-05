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
import periodictable as pt
import logging

periodic_table = [str(pt.elements[i]) for i in range(1, 119)]

#Implementar:
#1. Verificação de entrada. ok!
#2. Multiprocessing - nos downloads de dados.
#3. Repetição automatizada - evitar realizar o mesmo post mais de uma vez.

def partition_function(element = '', T_e = 0, opt = 0):
    [input_verification(i) for i in [element, T_e]]

    URL = r'https://physics.nist.gov/cgi-bin/ASD/energy1.pl'
    payload = dict(
                spectrum = element, temp = T_e,
                conf_out = opt, term_out = opt, level_out = opt, 
                unc_out = opt, j_out = opt, lande_out = opt, 
                perc_out = opt, biblio = opt, splitting = opt
            )
    
    post = requests.post(URL, data = payload)
    soup = BeautifulSoup(post.text, "lxml")
    data_line = soup.find_all('span')[-1]
    logging.debug(' : '.join([element, str(T_e)]))
    

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
            if elmt == '' or temp == '':    continue
            Z = partition_function(elmt.strip(), float(temp), **kwargs)
            matrix[elmt.strip()].append(Z)
    
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
    return '.'.join([filename, names[kind]])

def input_verification(value):
    ##bug if input == 'C', 'Ca', 'Hg' (without ' I' in the end)
    global periodic_table
    if type(value) == str:
        if value[:2].rstrip() not in periodic_table:
            error = ''.join([value, ' is not a valid ion or element.'])
            raise ValueError(error)
        else:   pass
    elif type(value) == float or type(value) == int:
        if value <= 0:
            error = ''.join([value, 'eV is not a valid temperature.'])
            raise ValueError(error)
        else:   pass
    else:
        error = ''.join([value, 'is not a valid input.'])
        raise ValueError(error)
        

def remove_non_ascii(string):
    new_string = []
    for i in string:
        if ord(i) < 128:
            new_string.append(i)
        else:
            pass

    return ''.join(new_string)

def iterable_remove_non_ascii(iterable, ret='list'):
    if ret == 'str':
        return ', '.join(remove_non_ascii(i) for i in iterable)
    elif ret == 'list':
        return [remove_non_ascii(i) for i in iterable]


if __name__ == '__main__':
    x = partition_matrix(
		'Ca II, Fe II',
		'0.7, 0.8, 0.8',
 	rename = True)
"""
    x = partition_matrix(
 'Mg I, Mg II, Fe I, Fe II, Al I, Al II, Ti I, Ti II, Na I, Na II, K I, K II, Ca I, Ca II, Mn I, Mn II',
 '0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0',
 rename = True)
"""
