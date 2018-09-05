#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:30:20 2018

@author: pedro
"""
import os, pandas, numpy, logging
from nist_partition import partition_matrix, iterable_remove_non_ascii

logging.Logger.root.setLevel('DEBUG')

data = pandas.read_excel('data.xlsx')

temperatures = numpy.array(data.iloc[1])[2:].astype(str)
elements = numpy.array(data['Unnamed: 1'])

elements_1 = numpy.unique(iterable_remove_non_ascii(elements[2:26]))
elements_2 = numpy.unique(iterable_remove_non_ascii(elements[30:]))

string_elements = ', '.join([', '.join(elements_1), ', '.join(elements_2)])
string_temperatures = ', '.join(temperatures)

partition_matrix(string_elements, string_temperatures,
                 filename = 'all_data',
                 rename = True, output = 'excel')
    
#ele sobrescreveu a temperatura 0 do array.