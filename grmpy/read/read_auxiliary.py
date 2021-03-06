"""This module provides auxiliary functions for the import process of the init file."""
import numpy as np


def process(list_, dict_, keyword):
    """The function processes keyword parameters and creates dictionary elements."""
    if len(list_) == 4:
        name, val, type_, frac_ = list_[0], list_[1], list_[2], list_[3]
    elif list_[0] == 'direc':
        name, val = list_[0], [list_[i] for i in range(len(list_)) if i > 0]
    else:
        name, val = list_[0], list_[1]

    if name not in dict_[keyword].keys() and name in ['coeff']:
        dict_[keyword][name] = []
    if keyword in ['TREATED', 'UNTREATED', 'COST'] and 'types' not in dict_[keyword].keys():
        dict_[keyword]['types'] = []
    if keyword in ['TREATED', 'UNTREATED', 'COST']:
        if len(list_) == 4:
            dict_[keyword]['types'] += [[type_, float(frac_)]]
        else:
            dict_[keyword]['types'] += ['nonbinary']

    # Type conversion
    if name in ['agents', 'seed', 'maxiter', 'disp']:
        val = int(val)
    elif name in ['source', 'file', 'optimizer', 'start']:
        val = str(val)
    elif name in ['direc']:
        val = list(val)
    else:
        val = float(val)
    if name in ['coeff']:
        dict_[keyword][name] += [val]
    else:
        dict_[keyword][name] = val
    # Finishing.
    return dict_


def auxiliary(dict_):
    """The function creates an new dictionary entry 'AUX' that includes starting values of each
    parameter and the number of covariates.
    """
    dict_['AUX'] = {}
    if dict_['DIST']['coeff'] == [0.0] * len(dict_['DIST']['coeff']):
        is_deterministic = True
    else:
        is_deterministic = False

    for key_ in ['UNTREATED', 'TREATED', 'COST', 'DIST']:
        if key_ in ['UNTREATED', 'TREATED', 'COST']:
            dict_[key_]['all'] = dict_[key_]['coeff']
            dict_[key_]['all'] = np.array(dict_[key_]['all'])
        else:
            dict_[key_]['all'] = dict_[key_]['coeff']
            dict_[key_]['all'] = np.array(dict_[key_]['all'])

    # Number of covariates
    num_covars_out = len(dict_['TREATED']['all'])
    num_covars_cost = len(dict_['COST']['all'])

    dict_['AUX']['num_covars_out'] = num_covars_out
    dict_['AUX']['num_covars_cost'] = num_covars_cost

    # Number of parameters
    dict_['AUX']['num_paras'] = 2 * num_covars_out + num_covars_cost + 2 + 2

    # Starting values
    dict_['AUX']['init_values'] = []

    for key_ in ['TREATED', 'UNTREATED', 'COST', 'DIST']:
        dict_['AUX']['init_values'] += dict_[key_]['all'].tolist()

        for j in sorted(dict_[key_].keys()):
            if j in ['all', 'types']:
                pass
            else:
                del dict_[key_][j]
    dict_['DETERMINISTIC'] = is_deterministic
    dict_ = check_types(dict_)

    return dict_


def check_types(dict_):
    """This function ensures that the variable types agree across the two treatment states."""
    if dict_['UNTREATED']['types'] != dict_['TREATED']['types']:
        for i in range(len(dict_['UNTREATED']['types'])):
            if isinstance(dict_['TREATED']['types'][i], list):
                dict_['UNTREATED']['types'][i] = dict_['TREATED']['types'][i]
            if isinstance(dict_['UNTREATED']['types'][i], list):
                dict_['TREATED']['types'][i] = dict_['UNTREATED']['types'][i]

    return dict_
