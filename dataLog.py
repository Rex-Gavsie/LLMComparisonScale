from ProofOfConcept import calculateSuccessRate
import os, csv

"""
This is gonna start by collecting a graph of success rate with respect to dilution proportion
"""

def getSuccessRateForVariousDilutions(instruction, numTestsAtDilution, callsPerTest, maxTokensPerGeneration, fileNameSuffix, numDilutionLevels):

    data_points = [(x, calculateSuccessRate(instruction, numTestsAtDilution, False, x, callsPerTest, maxTokensPerGeneration)) for x in [i/float(numDilutionLevels-1) for i in range(0, numDilutionLevels)]]

    with open(f'data{fileNameSuffix}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Probability Of 3.5-Instruct', 'Success Rate'])
        for point in data_points:
            writer.writerow(point)

getSuccessRateForVariousDilutions("Write a python script to print 1 to 100", 30, 30, 1, "test2-30R-30T-50I", 50)