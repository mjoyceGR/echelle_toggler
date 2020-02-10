#!/usr/bin/env python
#import numpy as np
import glob as glob
#import subprocess
#import sys
import matplotlib.pyplot as plt
import slider_MESA_module as sm


obs_file = 'deMeulenaer_observed_acenA.dat'

MESA_file = 'MESA_output.gyre'


## set these parameters according to YOUR star/problem

nmin =9
nmax =30
tsp = sm.reformat()		
sm.load(tsp, nmin=nmin, nmax=nmax, use_obs=True, observed=obs_file, Dnu_theory=107, Delta_Nu_obs=105.9, ospan_max=5000)

