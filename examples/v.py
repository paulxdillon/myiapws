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

"""Specific volume versus temperature for liquid water and ice
at normal pressure."""

# pylint: disable=invalid-name

import argparse

import numpy
from scipy.optimize import newton
from matplotlib import pyplot

from myiapws import iapws1992, iapws1995, iapws2006

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', dest='path')
path = parser.parse_args().path


## Calculations ##

# Define a series of temperatures
Tl = numpy.linspace(273.16, 373.15, 200)

# Determine the density at normal pressure for this series of temperatures.
# Use the liquid saturation density for each temperature as an estimate.
# pylint: disable=cell-var-from-loop
rhoest = iapws1992.rhosat_liquid(Tl)
rhol = numpy.array([newton(lambda rho_: iapws1995.p(rho_, T_) - 101325, rhoest_)
                    for rhoest_, T_ in zip(rhoest, Tl)])

vl = 1/rhol

# Ice (solid) temperatures and volumes
Ts = numpy.linspace(-25, 0, 100) + 273.15
vs = 1/iapws2006.rho(Ts, 101325)


## Plotting ##

fig = pyplot.figure(figsize=[4, 2.8])
fig.set_tight_layout(True)

# Isobar
pyplot.plot(Tl-273.15, vl*1000, 'k-', linewidth=1)
pyplot.plot(Ts-273.15, vs*1000, 'k-', linewidth=1)
pyplot.plot([Tl[0]-273.15, Ts[-1]-273.15], [vl[0]*1000, vs[-1]*1000],
            'k:', linewidth=2)

pyplot.xlim(-25, 100)
pyplot.ylim(0.995, 1.100)
pyplot.xlabel(r'Temperature ($\mathregular{^{\circ}C}$)')
pyplot.ylabel(r'Volume $\mathregular{(L/kg)}$')

pyplot.text(60, 1.01, '101.325 kPa', size=9)

pyplot.annotate('', xy=(6, 1.002), xycoords='data',
                xytext=(24, 1.035), textcoords='data',
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

ax_inset = fig.add_axes([0.5, 0.55, 0.3, 0.3]) # Inset
ax_inset.plot(Tl[:100]-273.15, vl[:100]*1000., 'k-', linewidth=1)

ax_inset.set_xlim(0, 10)
ax_inset.set_ylim(1., 1.0003)
ax_inset.set_yticks([1, 1.0001, 1.0002, 1.0003])
ax_inset.set_yticklabels(['1.0000', '1.0001', '1.0002', '1.0003'])
ax_inset.tick_params(axis='both', which='major', labelsize=9)

if path:
    pyplot.savefig(path)
else:
    pyplot.show()
