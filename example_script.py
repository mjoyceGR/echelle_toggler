#!/usr/bin/env python
#import numpy as np
import glob as glob
#import subprocess
#import sys
import matplotlib.pyplot as plt
import slider_MESA_module as sm


obs_file = 'deMeulenaer_observed_acenA.dat'

## slider module should convert MESA-default-formatted GYRE output to the 'tspec' format
tsp = 'MESA_output.tspec'

nmin =9
nmax =30

#for tsp in glob.glob('*.tspec'):		
sm.load(tsp, nmin=nmin, nmax=nmax, use_obs=True, observed=obs_file, Dnu_theory=107, Delta_Nu_obs=105.9, ospan_max=5000)

