#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 08:28:19 2019

@author: sanijo
"""

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os

def getPatchInfo(path):
    """Function which determines name and type of boundary surface inside 
       polyMesh/boundary.
       Input: -path to case directory"""
    
    os.chdir(path+'/constant/polyMesh/')
    boundary_file = os.getcwd()+'/boundary'
    f = ParsedParameterFile(boundary_file, boundaryDict=True)
    patches = list()
    types = list()
    patch_info = dict()
    i = -1
    for n in f:
        i += 1
        if type(n) is str:
            patches.append(n)
        if isinstance(n, dict):
            types.append(f[i]['type'])
    for key, val in (zip(patches, types)):
        patch_info[key]=val
    print('Boundary surfaces in this polyMesh are: ' + str(patches))
    print('Boundary surfaces types are: ' + str(types))
    
    return patch_info

def U_dict(f, U, patch_info):
    
    f['internalField'] = 'uniform ' + U
    f['boundaryField']={}
    for key, value in patch_info.items():
        if key == 'inlet':
            f['boundaryField']['inlet']= {'type': 'fixedValue', 'value' : 'uniform ' + U}
        if key == 'outlet':
            f['boundaryField']['outlet']={'type': 'zeroGradient'}
        if value == 'wall':
            f['boundaryField']['walls'] = {'type': 'fixedValue', 'value' : 'uniform (0 0 0)'}
        
        f.writeFile()
        
def p_dict(f, p, patch_info):
    
    f['internalField'] = 'uniform ' + p
    f['boundaryField']={}
    for key, value in patch_info.items():
        if key == 'inlet':
            f['boundaryField'][key] = {'type': 'zeroGradient'}
        if key == 'outlet':
            f['boundaryField'][key] = {'type': 'fixedValue', 'value' : 'uniform ' + p}           
        if value == 'wall':
            f['boundaryField'][key] = {'type': 'zeroGradient'}
        
        f.writeFile()
        
def k_dict(f, k, patch_info):
    
    f['internalField'] = 'uniform ' + k
    f['boundaryField']={}
    for key, value in patch_info.items():
        if key == 'inlet':
            f['boundaryField'][key] = {'type': 'fixedValue', 'value' : 'uniform ' + k}
        if key == 'outlet':
            f['boundaryField'][key] = {'type': 'zeroGradient'}
        if value == 'wall':
            f['boundaryField'][key] = {'type': 'kqRWallFunction', 'value' : 'uniform ' + k}
        
        f.writeFile()
        
def omega_dict(f, w, patch_info):
    
    f['internalField'] = 'uniform ' + w
    f['boundaryField']={}
    for key, value in patch_info.items():
        if key == 'inlet':
            f['boundaryField'][key] = {'type': 'fixedValue', 'value' : 'uniform ' + w}
        if key == 'outlet':
            f['boundaryField'][key] = {'type': 'inletOutlet', 'inletValue': 'uniform ' + w,
                                       'value': 'uniform ' + w}
        if value == 'wall':
            f['boundaryField'][key] = {'Cmu': '0.09', 'kappa': '0.41', 'E': '9.8', 'beta1': '0.075',
                                       'type': 'omegaWallFunction', 'value' : 'uniform ' + w}
    
        f.writeFile()
        
def epsilon_dict(f, epsilon, patch_info):
    
    f['internalField'] = 'uniform ' + epsilon
    f['boundaryField']={}
    for key, value in patch_info.items():
        if key == 'inlet':
            f['boundaryField'][key] = {'type': 'fixedValue', 'value' : 'uniform ' + epsilon}
        if key == 'outlet':
            f['boundaryField'][key] = {'type': 'inletOutlet', 'inletValue': 'uniform ' + epsilon,                                       'value': 'uniform ' + epsilon}
        if value == 'wall':
            f['boundaryField'][key] = {'Cmu': '0.09', 'kappa': '0.41', 'E': '9.8',
                                       'type': 'epsilonWallFunction', 'value' : 'uniform ' + epsilon}
        
        f.writeFile()
        
def nut_dict(f, nut, patch_info):
    
    f['internalField'] = 'uniform ' + nut
    f['boundaryField']={}
    for key, value in patch_info.items():
        if key == 'inlet':
            f['boundaryField'][key] = {'type': 'calculated', 'value' : 'uniform ' + nut}
        if key == 'outlet':
            f['boundaryField'][key] = {'type': 'zeroGradient'}
        if value == 'wall':
            f['boundaryField'][key] = {'Cmu': '0.09', 'kappa': '0.41', 'E': '9.8',
                                       'type': 'nutUSpaldingWallFunction', 'value' : 'uniform ' + nut}
        
        f.writeFile()         
    
    
def pyPlate0(case_path, list_of_files, dict_of_values): 
    """Function for manipulating data in 0 folder (p, U, k, omega, epsilon, nut)
       Inputs: -path to case directory
               -list od directories inside case directory (use os.listid(path))
               -dictionary of all necessary values:
                e.g. values = {"U": velocity, 'p': pressure, 'k': k, 'w': w, 'epsilon': epsilon,
                               'nut': nut, 'rho': rho, 'nu': nu, 'simulationType': simulationType, 
                               'turbulence': RAS}"""
    
    patchInfo = getPatchInfo(case_path)
    
    for dir in list_of_files:
        if dir == '0':
            os.chdir(case_path+'/'+dir)
            local_files = os.listdir()
            for file in local_files:
                if file == 'U':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    U = dict_of_values['U']                   
                    U_dict(f, U, patchInfo)
                    
                if file == 'p':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    p = dict_of_values['p']
                    p_dict(f, p, patchInfo)
                    
                if file == 'k':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    k = dict_of_values['k']
                    k_dict(f, k, patchInfo)
                    
                if file == 'omega':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    w = dict_of_values['w']
                    omega_dict(f, w, patchInfo)
                    
                if file == 'epsilon':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    epsilon = dict_of_values['epsilon']
                    epsilon_dict(f, epsilon, patchInfo)
                    
                if file == 'nut':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    nut = dict_of_values['nut']
                    nut_dict(f, nut, patchInfo)
                    
###############################################################################
"""transportProperties and turbulenceProperties"""

def transportProperties(f, rho, nu):
    """Function for manipulating data in transportProperties.
       It's important to change few lines of code in __cmp__
       to work properly.
       INFO -> https://sourceforge.net/p/openfoam-extend/ticketspyfoam/223/"""
    
    f['transportModel'] = 'Newtonian'
    f['rho'][0] = '[1 -3 0 0 0 0 0]'  
    f['rho'][1] = rho
    f['nu'][0] =  '[0 2 -1 0 0 0 0]'
    f['nu'][1] =  nu
    
    f.writeFile()
    
def turbulenceProperties(f, stype, para):
    """Function for manipulating data in turbulenceProperties."""
    
    if stype == 'laminar':
        f['simulationType'] = stype 
        f['RAS'] = {'turbulence': 'off', 'printCoeffs': 'on'}
    else:    
        f['simulationType'] = stype
        f['RAS'] = para  
        
    f.writeFile()
    
def pyPlateConstant(case_path, list_of_files, dict_of_values):
    """Function for manipulating data in transportProperties
       and turbulenceProperties dictionary.
       Inputs: -path to case directory
               -list od directories inside case directory (use os.listid(path))
               -dictionary of all necessary values:
                e.g. values = {"U": velocity, 'p': pressure, 'k': k, 'w': w, 'epsilon': epsilon,
                               'nut': nut, 'rho': rho, 'nu': nu, 'simulationType': simulationType, 
                               'turbulence': RAS}"""
    
    for dir in list_of_files:
        if dir == 'constant':
            os.chdir(case_path + '/' + dir)
            local_files = os.listdir()
            for file in local_files:
                if file == 'transportProperties':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    rho, nu = dict_of_values['rho'], dict_of_values['nu']
                    transportProperties(f, rho, nu)
                if file == 'turbulenceProperties':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file) 
                    stype, para = dict_of_values['simulationType'], dict_of_values['turbulence']
                    turbulenceProperties(f, stype, para)
###############################################################################
"""system folder"""

def dictParameters():
    """Function for determination of controlDict parameters"""

def controlDict(f):
    
    print(f['functions'])
    
def pyPlateSystem(case_path, list_of_files, dict_of_values):
    """Function for manipulating data in controlDict.
       Inputs: -path to case directory
               -list od directories inside case directory (use os.listid(path))
               -dictionary of all necessary values:
                e.g. values = {"U": velocity, 'p': pressure, 'k': k, 'w': w, 'epsilon': epsilon,
                               'nut': nut, 'rho': rho, 'nu': nu, 'simulationType': simulationType, 
                               'turbulence': RAS}"""
    
    for dir in list_of_files:
        if dir == 'system':
            os.chdir(case_path + '/' + dir)
            local_files = os.listdir()
            for file in local_files:
                if file == 'controlDict':
                    f = ParsedParameterFile(case_path+'/'+dir+'/'+file)
                    controlDict(f)









    
def main():
    
    path ='/home/sanijo/OpenFOAM/sanijo-4.1/run/Cooling_plate_SCRIPT_TEST'
    curr_files = os.listdir(path)

#change values in this parameters 
    velocity = '(5 0 0)'
    pressure = '0'
    k, w, epsilon, nut = '0.002', '0.2', '0.5', '0'
    rho, nu = '1000', '0.0000027'
    simulationType = 'laminar'
    RAS = {'RASModel': 'kOmegaSST', 'turbulence': 'on', 'printCoeffs': 'on'}
    
#DONT change this if not necessary
    values = {"U": velocity, 'p': pressure, 'k': k, 'w': w, 'epsilon': epsilon,
          'nut': nut, 'rho': rho, 'nu': nu, 'simulationType': simulationType, 
          'turbulence': RAS}

    
#    pyPlate0(path, curr_files, values)
#    pyPlateConstant(path, curr_files, values)
    pyPlateSystem(path, curr_files, values)


if __name__ == "__main__":
    main()
 


