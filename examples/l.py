#! /usr/bin/env python3

# Copyright (C) 2016-2017 Thomas J. Duck
#
# Thomas J. Duck <tomduck@tomduck.ca>
# Department of Physics and Atmospheric Science, Dalhousie University
# PO Box 15000 | Halifax NS B3H 4R2 Canada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Enthalpies of transformation."""

# pylint: disable=invalid-name

import argparse

import numpy
from matplotlib import pyplot
from scipy.optimize import newton

from myiapws import iapws1992, iapws1995, iapws2006, iapws2011


# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', dest='path')
path = parser.parse_args().path


## Calculations ##

# Define a series of temperatures
Tt = iapws1995.Tt
Tc = iapws1995.Tc

# Vaporization ----------

T1 = numpy.linspace(Tt, Tc, 300)
hsat_liquid1 = iapws1992.hsat_liquid(T1)
hsat_vapor1 = iapws1992.hsat_vapor(T1)
Lvap = hsat_vapor1 - hsat_liquid1

# Sublimation ----------

T2 = numpy.linspace(150, Tt, 300)
psubl = iapws2011.psubl_ice_Ih(T2)
hsat_ice2 = iapws2006.h(T2, psubl)

rhoest = psubl/(iapws1995.R*T2)
# pylint: disable=cell-var-from-loop
rho = numpy.array([newton(lambda rho_: iapws1995.p(rho_, T_) - p_, rhoest_) \
                   for p_, T_, rhoest_ in zip(psubl, T2, rhoest)])
hsat_vapor2 = iapws1995.h(rho, T2)

Lsub = hsat_vapor2 - hsat_ice2

# Fusion ----------

T3 = numpy.linspace(251.165, Tt, 300)
pmelt = iapws2011.pmelt_ice_Ih(T3)
hsat_ice3 = iapws2006.h(T3, pmelt)

# pylint: disable=cell-var-from-loop
rho = numpy.array([newton(lambda rho_: iapws1995.p(rho_, T_) - p_, 1000) \
                   for p_, T_ in zip(pmelt, T3)])
hsat_liquid3 = iapws1995.h(rho, T3)

Lfus = hsat_liquid3 - hsat_ice3


## Plotting ##

fig = pyplot.figure(figsize=[4, 2.8])
fig.set_tight_layout(True)

pyplot.plot(T1, Lvap/1e6, 'k-', linewidth=1)
pyplot.plot(T2, Lsub/1e6, 'k-', linewidth=1)
pyplot.plot(T3, Lfus/1e6, 'k-', linewidth=1)

pyplot.xlabel(r'Temperature ($\mathregular{^{\circ}C}$)')
pyplot.ylabel('Enthalpy of\nTransformation (MJ/kg)')

pyplot.xlim(150, 700)
pyplot.ylim(0, 3)

pyplot.text(470, 1.5, r'$\ell_\mathrm{vap}$')
pyplot.text(185, 2.5, r'$\ell_\mathrm{sub}$')
pyplot.text(225, 0.45, r'$\ell_\mathrm{fus}$')

pyplot.plot([Tt, Tt], [0, 3], 'k:')
pyplot.text(Tt, 1.5, r'$T_\mathrm{tp}$', color='k',
            ha='center', va='center', bbox={'ec':'1', 'fc':'1'})

ax = pyplot.gca()
pyplot.plot([Tc, Tc], [0, 3], 'k:')
pyplot.text(Tc, 1.5, r'$T_\mathrm{c}$', color='k',
            ha='center', va='center', bbox={'ec':'1', 'fc':'1'})

if path:
    pyplot.savefig(path)
else:
    pyplot.show()
