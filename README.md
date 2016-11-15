
myiapws
=======

Myiapws is a python library for the calculation of thermophysical properties of water.  It is an implementation of certain formulations from the [International Association for the Properties of Water and Steam](http://www.iapws.org/) (IAPWS).

The primary use of the library is as an educational tool.  The publications describing the formulations map directly to the code.  The interfaces are simple, fully pythonic and [numpy](http://www.numpy.org/)-capable.

Developers interested in an advanced thermodynamics package covering over 100 species should check out [COOLPROP](http://www.coolprop.org/).


Installation
------------

Install into python3 (as root) by executing

~~~
# pip3 install git+https://github.com/tomduck/myiapws.git
~~~

The library should be tested (as a normal user) by executing

~~~
$ cd test
$ ./test.py
~~~

The unit tests are based on "computer program verification" values provided by IAPWS.


Modules
-------

The available modules are as follows:

  * `myiapws.iapws1992`: Thermodynamic properties on the coexistence curve of liquid water and vapor.  ([REF](http://www.iapws.org/relguide/supsat.pdf))

  * `myiapws.iapws1995`: Thermodynamic properties of ordinary water substance (liquid and gas).  The fundamental equation is in Helmholtz representation, and so all properties are functions of temperature and density. ([REF](http://iapws.org/relguide/IAPWS95-2014.pdf))

  * `myiapws.iapws2006`: Thermodynamic properties of ice Ih.  The fundamental equation is in Gibbs representation, and so all properties are functions of temperature and pressure. ([REF](http://iapws.org/relguide/Ice-Rev2009.pdf))

  * `myiapws.iapws2011`: Melting and sublimation pressures of liquid water and ice as a function of temperature. ([REF](http://www.iapws.org/relguide/MeltSub2011.pdf))

The modules are internally documented.  Execute `help(<module-name>)` at the python prompt to get full descriptions of each API.


Examples
--------

It is frequently not trivial to draw thermodynamic diagrams given the fundamental equations and their derivatives alone.  The liquid phase formulation, for example, provides thermodynamic functions dependent upon density and temperature.  If one wants to, say, plot heat capacity against pressure and temperature instead then some numerical work needs to be done.

The following examples are given in the `examples/` directory:

  * `cp.py`: Isobaric heat capacity of liquid water at normal pressure versus temperature.

  * `alpha.py`: Volumetric thermal expansion coefficient of liquid water at normal pressure versus temperature.

  * `v.py`: Specific volume of liquid water and ice at normal pressure versus temperature.

  * `pv.py`: Isotherms on pressure-volume axes for ice, liquid water and water vapour.

  * `Ts.py`: Isobars on temperature-entropy axes for liquid water and water vapour.

  * `pT.py`: Coexistence curves for the different mixed-phases of water.
