# Kieran Humphreys kdh8az

# This .py file is meant to store useful conversion methods for ECE 3250

import cmath

# This function takes a normal complex number, converts to admittance, 
# multiplies by complex conjugate, then returns the resulting complex number
def admittance_mult_conj(comp):
    comp_conj = comp.conjugate()
    admittance = 1 / comp

    return admittance * (comp_conj / comp_conj)

# This function takes the representation of the admittance, and converts
# it to the parallel form by taking the reciprocal of each term
def series_to_parallel(comp):
    adm = admittance_mult_conj(comp)

    return str(1 / adm.real) + " + j" + str(-1 / adm.imag)


