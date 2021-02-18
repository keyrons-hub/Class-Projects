# Kieran Humphreys Module 3 Problem 2
import math
import numpy

beta = 1000.0
check = 0

for n in range(100):
    if check == 1:
        break

    for fc in range range(beta, 1.2*beta):
        passband = 20*math.log(1/(math.sqrt(1 + math.pow((beta/fc),(2*n)))))
        harmonic = 20*math.log(1/(math.sqrt(1 + math.pow((1.2*beta/fc),(2*n)))))

        if (passband >= -0.5 & harmonic < -80):
            print("n value is: " + n)
            print("fc value is: " + fc + " Hz")

            check += 1


