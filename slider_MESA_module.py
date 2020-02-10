#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import glob
import sys
import subprocess

def load(f, nmin, nmax, *args, **kwargs):
	## .tspec formatted file
	use_obs = bool(kwargs.get('use_obs', False))
	observed=kwargs.get('observed',"")
	Delta_Nu_th = kwargs.get("Dnu_theory", 55)
	ospan_max = kwargs.get("ospan_max", 5000)

	if use_obs:
		with open(observed, "r") as inf:
			outf=open(observed+'.load',"w")
			for line in inf.readlines()[1:]:
				if 'nodata' in str(line):
					pass
				else:
					p=line.split()
					outf.write(str(p[0]) + "  " + str(p[1]) + "  " + str(p[2]) + " " + str(p[3]) +'\n')

			inf.seek(0)
		outf.seek(0)
		outf.close()
		n, l, ofrequency, freq_err=np.loadtxt(observed + '.load', usecols=(0,1,2,3), unpack=True)
		ospan=ofrequency
		Delta_Nu_obs=kwargs.get("Delta_Nu_obs",105.9)#103.3 ## for 16Cyg A
		#Delta_Nu_obs = Delta_Nu_obs

		oL0 =ofrequency[np.where(l ==0)[0]] 
		ot_L0 = oL0 % Delta_Nu_obs
		os_L0 = oL0
		oL1 =ofrequency[np.where(l ==1)[0]] 
		ot_L1 = oL1 % Delta_Nu_obs
		os_L1 = oL1
		oL2 =ofrequency[np.where(l ==2)[0]] 
		ot_L2 = oL2 % Delta_Nu_obs
		os_L2 = oL2
		oL3 =ofrequency[np.where(l ==3)[0]] 
		ot_L3 = oL3 % Delta_Nu_obs
		os_L3 = oL3
	else:
		#ospan = np.arange(1500,3000,5)
		ospan = np.arange(0,ospan_max,5)

	############################
	n, l, frequency =np.loadtxt(f,usecols=(0,1,2), unpack=True)
	## reduced to observed range only
	nrange=np.where( (n>=nmin) & (n<=nmax) )[0]
	n=n[nrange]
	l=l[nrange]
	frequency=frequency[nrange]
	L0 =frequency[np.where(l ==0)[0]] 
	t_L0 = L0 % Delta_Nu_th
	s_L0 = L0
	L1 =frequency[np.where(l ==1)[0]] 
	t_L1 = L1 % Delta_Nu_th
	s_L1 = L1
	L2 =frequency[np.where(l ==2)[0]] 
	t_L2 = L2 % Delta_Nu_th
	s_L2 = L2
	L3 =frequency[np.where(l ==3)[0]] 
	t_L3 = L3 % Delta_Nu_th
	s_L3 = L3
	############################

	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.25, bottom=0.25)

	if use_obs:
		toggler,  = plt.plot(ot_L0, os_L0, "mo", color='black', markersize=10, label="observed l=0")
		toggler1, = plt.plot(ot_L1, os_L1, "go", color='gray', markersize=10, label='observed l=1')
		toggler2, = plt.plot(ot_L2, os_L2, "mD", color='black', markersize=10, label="observed l=2")
		toggler3, = plt.plot(ot_L3, os_L3, "gD", color='gray', markersize=10, label='observed l=3')

	toggler_L0, = plt.plot(t_L0, s_L0, "mo", color='pink', markersize=8, label='theory l=0')
	toggler_L1, = plt.plot(t_L1, s_L1, "go", color='green', markersize=8, label='theory l=1')
	toggler_L2, = plt.plot(t_L2, s_L2, "mD", color='hotpink', markersize=8, label='theory l=2')
	toggler_L3, = plt.plot(t_L3, s_L3, "gD", color='darkgreen', markersize=8, label='theory l=3')

	## sets bounds [xmin, xmax, ymin, ymax]
	plt.axis([0, Delta_Nu_th+1, ospan.min()-50, ospan.max()+50])
	plt.legend(loc=2, fontsize = 10)
	plt.xlabel("Frequency ($\mu$Hz) mod Delta Nu", fontsize=18)
	plt.ylabel("Frequency ($\mu$Hz)", fontsize=14)
	plt.title(str(f))

	if use_obs:
		axdnu = plt.axes(       [0.25, 0.10, 0.65, 0.03], facecolor='gray') ##coordinates of button?
		o_dnu = Slider(axdnu, 'Delta_Nu_obs',    Delta_Nu_obs - 3, Delta_Nu_obs + 3, valinit=Delta_Nu_obs)
	
	axdnu_theory = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='pink') ##coordinates of button?
	t_dnu = Slider(axdnu_theory, 'Delta_Nu_theory', Delta_Nu_th - 3, Delta_Nu_th + 3, valinit=Delta_Nu_th)

	def update(val):
		#print "val: ", val
		if use_obs:
			odnu = o_dnu.val
			#toggler.set_ydata(amp*np.sin(2*np.pi*t))
			toggler.set_xdata(oL0 % odnu)
			toggler1.set_xdata(oL1 % odnu)
			toggler2.set_xdata(oL2 % odnu)
			toggler3.set_xdata(oL3 % odnu)
		tdnu = t_dnu.val
		toggler_L0.set_xdata(L0 % tdnu)
		toggler_L1.set_xdata(L1 % tdnu)
		toggler_L2.set_xdata(L2 % tdnu)
		toggler_L3.set_xdata(L3 % tdnu)
		fig.canvas.draw_idle()
	## check this
	if use_obs:
		o_dnu.on_changed(update)
	t_dnu.on_changed(update)


	resetax = plt.axes([0.8, 0.0, 0.1, 0.04]) ##coordinates of button?
	button = Button(resetax, 'Reset', color='lightgreen', hovercolor='0.975')

	## as defined, this will reset both toggle bars simultaneously;
	## need separate functions to reset independently
	def reset(event):
		if use_obs:
			o_dnu.reset()
		t_dnu.reset()
	button.on_clicked(reset)
	plt.show()
	plt.close()
	return 



	
def reformat(filename, *args, **kwargs):
	#subprocess.call("cp "+filename+" "+temp, shell = True)
	inf = open(filename, "r")
	lines=inf.readlines()
	newlines=[]
	newlines.append("#n_p   l   Re(freq)    E_norm\n")
	try:
		for line in lines[6:]:
			#print filename
			#print line
			#sys.exit()
			## these may not be correct indices
			l =  line.split()[0]
			n =  line.split()[2]
			nu = line.split()[5]
			#E_norm = line.split()[6]

			alt_string = str(n) + "   " + str(l) + "   " + str(nu)+"\n"#+ "   " + str(E_norm)
			newlines.append(alt_string)
		inf.seek(0)
		inf.close()	
		temp = filename +".temp"
		outf = open(temp,"w")
		for line in newlines:
			outf.write(line)
		outf.close()
		subprocess.call("cp "+temp+" "+filename +'.tspec', shell = True)
		subprocess.call("rm "+ temp, shell = True)
	except IndexError:
		print(filename+"already processed")
		pass
	return


