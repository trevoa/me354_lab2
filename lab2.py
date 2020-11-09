from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from numpy import mean, std, trapz

Files = [x for x in listdir() if '.csv' in x] #this is a list comprehension that finds all the current folder files that contain '.csv'
thickness = 6.2 # Input thickness in mm
width = 12.3 # Input Width in mm
Area = thickness*width #in mm^2


def readFiles(thickness, width):
    Area = thickness * width
    Files = [x for x in listdir() if '.csv' in x]
    Data = {x: {} for x in Files} #This is a list comprehension that creates an empty dictionary for all the file data.

    for File in Files:
        Data[File] = pd.read_csv(File)

    for File in Files:
        Data[File]['Stress (MPa)'] = Data[File]['Load (N)'] / Area  # this adds stress to the data
        Data[File]['Instantaneous Area (mm^2)'] = [(thickness - thickness*trans_strain) * (width -)]
        print(Data[File])


readFiles(thickness, width)
