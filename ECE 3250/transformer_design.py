# Kieran Humphreys ECE 3250 Transformer Design Project
import math

class xfmr:

    # core parameters
    coreWidth = 3.175
    windowHeight = 4.76
    windowWidth = 1.5875
    wtper1K = 14.95
    laminationThickness = 0.035
    laminationWeightPerK = 14.95
    stackingFactor = 0.9
    windowArea = windowHeight * windowWidth

    # winding bobbin parameters
    windingLength = 4.47
    windingHeightTotal = 1.422
    aDimension = 3.607
    bDimension = 3.48

    # system level constants
    kf = 4.44
    ku = 0.3
    freq = 60

    # specs
    VARated = 75
    VPrimary = 120
    VSecondary = 45
    efficiency = 0.85         # set for 3250 project
    bestEfficiency = 0.85
    regulation = 0.04         
    plausible = True
    notplausible = False

    # transformer values
    B = 0
    J = 0
    Pt = 0
    areaProduct = 0
    systemConstants = 0
    nLaminations = 0
    physCoreDepth = 0
    coreWeight = 0
    coreArea = 0

# setting up final values
numLaminations, PWG, numPrimary, SWG, numSecondary = 0, 0, 0, 0, 0
RCuF, jXlF, RCoreF, jXmF, vRegFinal, coreLossFinal, copperLossFinal, bFinal, jFinal, PWD, SWD, TWD = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 

# hard code the CSV file necessary values and skip the headers
#   AWG     Bare Area   Resistance  Diameter    Turns Per cm    
Wire = [

    [10, 52.61, 32.7, 0.267, 3.9],

    [11, 41.68, 41.4, 0.238, 4.4],

    [12, 33.08, 52.1, 0.213, 4.9], 

    [13, 26.26, 65.6, 0.19, 5.5],

    [14, 20.82, 82.8, 0.171, 6],

    [15, 16.51, 104.3, 0.153, 6.8],

    [16, 13.07,	131.8, 0.137, 7.3],

    [17, 10.39, 165.8, 0.122, 8.2],

    [18, 8.228, 209.5, 0.109, 9.1],

    [19, 6.531, 263.9, 0.098, 10,2],

    [20, 5.188, 332.3, 0.0879, 11.4],

    [21, 4.116, 418.9, 0.0785, 12.8],

    [22, 3.243, 531.4, 0.0701, 14.3],

    [23, 2.588, 666, 0.0632, 15.8],

    [24, 2.047, 842.1, 0.0566, 17.6]

]

# outer loop (setting B value)
for i in range(160, 130, -1):

    i = i / 100         # adjusting i value to account for python not allowing floats in for loop

    xfmr.B = i

    # inner loop (setting J value)
    for j in range(3000, 250, -1):

        j = j / 10      # adjusting j value

        xfmr.J = j

        # transformer calculation
        xfmr.Pt = xfmr.VARated * (1 + (1 / xfmr.efficiency))
        xfmr.areaProduct = ((xfmr.Pt * 10000) / (i * j * xfmr.freq * xfmr.kf * xfmr.ku))
        xfmr.systemConstants = xfmr.kf * xfmr.ku * xfmr.freq * xfmr.windowArea * xfmr.laminationThickness * xfmr.coreWidth
        xfmr.nLaminations = math.ceil((xfmr.Pt * 10000) / (xfmr.systemConstants * i * j))
        xfmr.physCoreDepth = ((xfmr.nLaminations * xfmr.laminationThickness) / xfmr.stackingFactor)
        xfmr.coreWeight = ((xfmr.nLaminations * xfmr.laminationWeightPerK) / 1000)
        xfmr.coreArea = xfmr.physCoreDepth * xfmr.stackingFactor * xfmr.coreWidth

        # core loss calculations and winding data
        pLossPerKg = 0.0618 * math.exp(3.155 * i)
        sPerKg = 0.0288 * math.exp(5.148 * i)
        qPerKg = math.sqrt(sPerKg**2 - pLossPerKg**2)
        pCoreLoss = pLossPerKg * xfmr.coreWeight
        qCore = qPerKg * xfmr.coreWeight
        RFe = ((xfmr.VPrimary**2) / pCoreLoss)
        Xm = ((xfmr.VPrimary**2) / qCore)
        nPrimary = math.ceil((xfmr.VPrimary * 10000) / (xfmr.kf * xfmr.freq * i * xfmr.coreArea))
        nSecondary = math.ceil(((nPrimary * xfmr.VSecondary) / xfmr.VPrimary) * (1 + xfmr.regulation))

        # finding copper related values
        iSec = (xfmr.VARated / xfmr.VSecondary)
        wireAreaSecondary = iSec / j
        iPrimary = (xfmr.VARated / xfmr.efficiency) / xfmr.VPrimary
        wireAreaPrimary = iPrimary / j
        primindex = 0
        secindex = 0

        # for loop to iterate through AWG values (for secondary)
        for w in range(0, 15, 1):
            if (((Wire[w][1]) * 0.001) < wireAreaPrimary):
                primindex = w - 1
                break
        # for loop to iterate through AWG values (for primary)
        for x in range(0, 15, 1):
            if (((Wire[x][1]) * 0.001) < wireAreaSecondary):
                secindex = x - 1
                break

        # checking table
        secondaryWireGauge = Wire[secindex][0]
        secondaryResitancePerCm = Wire[secindex][2] * 0.000001
        secondaryTurnsPerCm = Wire[secindex][4]
        secondaryWireDia = Wire[secindex][3]
        primaryWireGauge = Wire[primindex][0]
        primaryResistancePerCm = Wire[primindex][2] * 0.000001
        primaryTurnsPerCm = Wire[primindex][4]
        primaryWireDia = Wire[primindex][3]

        # calculate winding info
        primaryTurnsPerLayer = math.floor(primaryTurnsPerCm * xfmr.windingLength)
        primaryLayers = math.ceil(nPrimary / primaryTurnsPerLayer)
        totalDepthOfPrimaryWinding = primaryLayers * primaryWireDia

        # repeat for secondary
        secondaryTurnsPerLayer = math.floor(secondaryTurnsPerCm * xfmr.windingLength)
        secondaryLayers = math.ceil(nSecondary / secondaryTurnsPerLayer)
        totalDepthOfSecondaryWinding = secondaryLayers * secondaryWireDia

        totalDepthOfAllWindings = totalDepthOfPrimaryWinding + totalDepthOfSecondaryWinding

        # necessary plausibility check
        if (totalDepthOfAllWindings < xfmr.windingHeightTotal):
            xfmr.plausible = True
        else:
            xfmr.plausible = False

        # calculate wire lengths and resistances
        MLTPrimary = ((2 * xfmr.aDimension) + (2 * xfmr.bDimension) + (math.pi * totalDepthOfPrimaryWinding))
        totalPrimaryLength = nPrimary * MLTPrimary
        resistancePrimary = totalPrimaryLength * primaryResistancePerCm
        MLTSecondary = (2 * xfmr.aDimension) + (2 * xfmr.bDimension) + (math.pi * ((2 * totalDepthOfPrimaryWinding) + totalDepthOfSecondaryWinding))
        totalSecondaryLength = MLTSecondary * nSecondary
        resistanceSecondary = totalSecondaryLength * secondaryResitancePerCm

        # reflect secondary resistance to primary for RCu evaluation in model
        RCu = resistancePrimary + (resistanceSecondary * ((nPrimary / nSecondary)**2))

        # now get effective leakage reactance
        Llp = ((4 * math.pi * MLTPrimary * (nPrimary**2)) / xfmr.windingLength) * (((totalDepthOfPrimaryWinding + totalDepthOfSecondaryWinding) / 3) * 0.000000001)
        Xllp = (Llp * 2 * math.pi * xfmr.freq)

        # check efficiency
        PCu = RCu * ((iSec * (nSecondary / nPrimary))**2)
        PFe = (xfmr.VPrimary**2 / RFe)
        eff = xfmr.VARated / (xfmr.VARated + PCu + PFe)

        # calculate voltage regulation
        magnitudeOfZPrimary = math.sqrt(RCu**2 + Xllp**2)
        voltageRegulation = (xfmr.VPrimary - (xfmr.VPrimary - (magnitudeOfZPrimary * (iSec * (nSecondary / nPrimary))))) / (xfmr.VPrimary - (RCu * (iSec * (nSecondary / nPrimary))))

        # do final check to ensure regulation and efficiency is better than required
        if (voltageRegulation < xfmr.regulation and eff > xfmr.efficiency and xfmr.plausible == True):
            if (eff > xfmr.bestEfficiency):

                # save best efficiency
                xfmr.bestEfficiency = eff

                numLaminations = xfmr.nLaminations
                PWG = primaryWireGauge
                numPrimary = nPrimary
                SWG = secondaryWireGauge
                numSecondary = nSecondary
                RCuF = RCu
                jXlF = Xllp         # converted to Henry's in model
                RCoreF = RFe
                jXmF = Xm           # converted to Henry's in model
                vRegFinal = voltageRegulation
                coreLossFinal = pCoreLoss
                copperLossFinal = PCu
                bFinal = i
                jFinal = j
                PWD = totalDepthOfPrimaryWinding
                SWD = totalDepthOfSecondaryWinding
                TWD = totalDepthOfAllWindings

# print statements
print("Number of laminations: " + str(numLaminations) + "\n")
print("Primary Wire Gauge: " + str(PWG))
print("Number of Turns Primary: " + str(numPrimary) + "\n")
print("Secondary Wire Gauge: " + str(SWG))
print("Number of Turns Secondary: " + str(numSecondary) + "\n")
print("RCu: " + str(RCuF) + " Ohms")
print("jXl: " + str(jXlF) + " jOhms")
print("Rcore: " + str(RCoreF) + " Ohms")
print("jXm: " + str(jXmF) + " jOhms" + "\n")
print("Voltage Regulation: " + str(vRegFinal))
print("Efficiency: " + str(xfmr.bestEfficiency) + "%")
print("Core Loss: " + str(coreLossFinal) + " W")
print("Copper Loss: " + str(copperLossFinal) + " W" + "\n")
print("B: " + str(bFinal) + " Teslas")
print("J: " + str(jFinal) + " Amps / cm^2")
print("Depth of Primary Winding: " + str(PWD) + " cm")
print("Depth of Secondary Winding: " + str(SWD) + " cm")
print("Total Depth of all Windings: " + str(TWD) + " cm")
print("Winding Height Total: " + str(xfmr.windingHeightTotal) + " cm")
print("Extra Window Space: " + str(xfmr.windingHeightTotal - TWD) + " cm")
print("Percent Window Used: " + str(1 - ((xfmr.windingHeightTotal - TWD) / 1.422)))  




