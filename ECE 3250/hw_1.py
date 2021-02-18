# Kieran Humphreys kdh8az

# ECE 3250 HW 1 Problem 2

import cmath
import math

cap = 0
omega = 60

Zline = 0.75 + 20j

# takes the absolute value of a complex number
def Abs_Value_Comp(comp):
    return math.sqrt(math.pow(comp.real, 2) + math.pow(comp.imag, 2))

# iterate through capacitor values
for cap in range(1, 100, 1):

    cap = (cap / 1000000.0) 

    ZloadA = ((70 + 71.4j) * ((0 - 1j) * (1 / (math.pi * 2 * omega * cap)))) / ((70 + 71.4j) + ((0 - 1j) * (1 / (math.pi * 2 * omega * cap))))
    ZloadB = ((64.26 + 31.1j) * ((0 - 1j) * (1 / (math.pi * 2 * omega * cap)))) / ((64.26 + 31.1j) + ((0 - 1j) * (1 / (math.pi * 2 * omega * cap))))
    ZloadC = ((189.9 + 61.8j) * ((0 - 1j) * (1 / (math.pi * 2 * omega * cap)))) / ((189.9 + 61.8j) + ((0 - 1j) * (1 / (math.pi * 2 * omega * cap))))

    VloadA = (ZloadA / (ZloadA + Zline)) * (10000 + 0j)
    VloadB = (ZloadB / (ZloadB + Zline)) * (10000 + 0j)
    VloadC = (ZloadC / (ZloadC + Zline)) * (10000 + 0j)
    
    if ((Abs_Value_Comp(VloadA)) > 9000 and (Abs_Value_Comp(VloadA) < 11000)):
        if ((Abs_Value_Comp(VloadB)) > 9000 and (Abs_Value_Comp(VloadB) < 11000)):
            if ((Abs_Value_Comp(VloadC)) > 9000 and (Abs_Value_Comp(VloadC) < 11000)):
                print(cap)


# for problem 3

Iin = (10000 + 0j) / Zline

IloadA = (Iin * ZloadA) / ((1 / (2 * math.pi * 60 * 0.000015)) + ZloadA)
IloadB = (Iin * ZloadB) / ((1 / (2 * math.pi * 60 * 0.000015)) + ZloadB)
IloadC = (Iin * ZloadC) / ((1 / (2 * math.pi * 60 * 0.000015)) + ZloadC)

LineLossesA = math.pow(Abs_Value_Comp(IloadA), 2) * 0.75
LineLossesB = math.pow(Abs_Value_Comp(IloadB), 2) * 0.75
LineLossesC = math.pow(Abs_Value_Comp(IloadC), 2) * 0.75
        
print((LineLossesA + LineLossesB + LineLossesC) / 3)

Iline = (10000) / ( (0.75 + ((2 * math.pi * 60 * 0.000015))) + ((70 + 71.4j) * ((0 - 1j) * (1 / (math.pi * 2 * omega * cap)))) / ((70 + 71.4j) + ((0 - 1j) * (1 / (math.pi * 2 * omega * cap)))))

IlineAbs = math.pow(Iline, 2)

print (IlineAbs * 0.75)
