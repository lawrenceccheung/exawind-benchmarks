#!/usr/bin/env python3

from subprocess import call
import os,sys
import numpy as np 
import json
import ruamel.yaml as yaml
import argparse
import pathlib
from scipy.interpolate import interp1d
import pandas as pd
import re
import matplotlib
import matplotlib.pyplot as plt
import importlib
import time
import glob

#ofparamhome = os.environ.get('OPENFAST_PARAM')
#sys.path.append(ofparamhome + '/import')
#import plot_func as pf
#importlib.reload(sys.modules['plot_func'])

def find_line(lookup,filename):
    linelist = []
    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                linelist.append(num)
    return linelist

def get_bounds(data,time,azmin,azmax):
    tmax = np.max(time)
    dt = tmax/len(time)
    xmin = azmin - 20.0
    xmax = np.max(time)+5.0
    dplot = int(np.floor((tmax - xmin)/dt))
    ybmax = np.max(np.array(data[-dplot:-2]))
    ybmin = np.min(np.array(data[-dplot:-2]))
    ymin = ybmin-ybmin*0.08
    ymax = ybmax+ybmax*0.08
    if (ybmax < 0.2 and ybmin > -0.2):
        ymax = 0.2
        ymin = -0.2
    
    return xmin,xmax,ymin, ymax

def main():
    parser = argparse.ArgumentParser(description="Quickly plot and display openfast output")
    parser.add_argument(
        "-d",
        "--directory",
        help="Parent directory with case folders",
        required=False,
        type=str,
        default="",
    )

    args = parser.parse_args()

    case_list = ['nrel5mw_rigid_abl_noopenfast2']
    force_file_names = ['forces01.dat']
    case_lab = ['NREL 5MW Rigid']

    omega = 1.25663706
    diffn = 60000
    rotaxis = [0.862729916,0.498097349,-0.087155742]

    matplotlib.rcParams['font.size'] = 16

    fig = plt.figure(constrained_layout=True,figsize=(13,4))
    subfigs = fig.subfigures(nrows=1, ncols=1)
    ax = subfigs.subplots(nrows=1, ncols=2)

    for i,c in enumerate(case_list):

        print('Processing: ',c)

        fullpath = os.path.join(args.directory,c,force_file_names[i])
        print(fullpath)

        this_data = pd.read_csv(fullpath,sep='\s+',skipinitialspace=True)

        this_data['Thrust'] = (this_data['Fpx']*rotaxis[0] + this_data['Fpx']*rotaxis[1])/1000.0

        ax[0].plot(this_data['Time'], this_data['Thrust'], label=case_lab[i])
        #plt.axhline(y = ofpower, color = 'k', linestyle = ':')
        ax[0].set_xlabel("Time [s]")
        ax[0].set_ylabel("Thrust [kN]")
        ax[0].set_ylim([150,900])
        #ax.set_xlim([0,30])
        #ax[0].legend()

        ax[1].plot(this_data['Time'], this_data['Mtx']/1000.0, label="x-dir Moment")
        ax[1].plot(this_data['Time'], this_data['Mty']/1000.0, label="y-dir Moment")
        ax[1].plot(this_data['Time'], this_data['Mtz']/1000.0, label="z-dir Moment")
        ax[1].set_xlabel("Time [s]")
        ax[1].set_ylabel("Moment [kN-m]")
        ax[1].legend()

    plt.savefig('rigid_output.png')
    plt.close()

if __name__ == "__main__":
    main()

