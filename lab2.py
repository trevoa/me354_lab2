from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from numpy import mean, std, trapz, log

Files = [x for x in listdir() if '.csv' in x] #this is a list comprehension that finds all the current folder files that contain '.csv'
Samples = [('6061 Aluminum Sample 1.csv', 6.48, 12.32), ('6061 Aluminum Sample 2.csv', 6.4, 12.02),
         ('6061 Aluminum Sample 3.csv', 6.4, 12.1), ('A36 Steel Sample 1.csv', 6.2, 12.4),
         ('A36 Steel Sample 2.csv', 6.2, 12.11), ('A36 Steel Sample 3.csv', 6.22, 12.4),
         ('CFRP 0 Degree Sample 1.csv', 1.02, 18.6), ('CFRP 0 Degree Sample 2.csv', 1.1, 18.48),
         ('CFRP 0 Degree Sample 3.csv', 1, 18.4), ('CFRP 90 Degree Sample 1.csv', 2.12, 19.05),
         ('CFRP 90 Degree Sample 2.csv', 2.33, 18.27), ('CFRP 90 Degree Sample 3.csv', 2.28, 18.91)]


class Sample:

    def __init__(self, file, thickness, width):
        self.file = file
        self.thickness = thickness
        self.width = width
        self.area = self.thickness * self.width
        self.data = pd.read_csv(file)

        self.data['Stress (MPa)'] = self.data['Load (N)'] / self.area
        self.data['Delta Thickness (mm)'] = -self.data['Transverse Strain (mm/mm)'] * self.thickness
        self.data['Delta Width (mm)'] = -self.data['Transverse Strain (mm/mm)'] * self.width
        self.data['Instantaneous Thickness (mm)'] = self.thickness + self.data['Delta Thickness (mm)']
        self.data['Instantaneous Width (mm)'] = self.width + self.data['Delta Width (mm)']
        self.data['True Area (mm^2)'] = self.data['Instantaneous Thickness (mm)'] * self.data['Instantaneous Width (mm)']

        self.data['True Stress (MPa)'] = self.data['Load (N)'] / self.data['True Area (mm^2)']
        self.data['True Strain (mm/mm)'] = log(self.data['Axial Strain (mm/mm)'] + 1)

    def modulusFit(self, end_val):
        index = abs(self.data['Stress (MPa)'] - end_val).idxmin()
        Stress = self.data['Stress (MPa)']
        Strain = self.data['Axial Strain (mm/mm)']

        # Fit the modulus
        E, C, R, P, Err = linregress(Strain[:index], Stress[:index])

        # Make a line for the fit data
        Y = [0.0, max(Stress)]  # this is a list of length 2 for plotting the fit data later
        X = [(y - C) / E for y in
             Y]  # these are points that you can plot to visualize the data being fit, inverted from y=E*x+C, x=(y-C)/E
        return E, C, R, X, Y

    def ult_values(self):
        ult_stress = self.data['Stress (MPa)'].max()
        max_index = self.data['Stress (MPa)'].idxmax()
        ult_strain = self.data['Axial Strain (mm/mm)'][max_index]
        vals = {'Ultimate Stress (MPa)': ult_stress, 'Ultimate Strain (mm/mm)': ult_strain}
        return vals

    def tensile_tough(self):
        yData = self.data['Stress (MPa)']
        xData = self.data['Axial Strain (mm/mm)']

        # Calculate the area
        tensileToughness = trapz(yData, x=xData)  # if we don't include xData, it will take the spacing to be 1

        val = round(tensileToughness, 2)
        return val

    def stress_strain_plot(self):
        fig = plt.figure()
        ax = fig.gca()
        ax.plot(self.data['Axial Strain (mm/mm)'], self.data['Stress (MPa)'], label=self.file)  # the label corresponds to what the legend will output
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        plt.title("Engineering Stress vs Strain")
        plt.ylabel('Stress (MPa)')
        plt.xlabel('Strain (mm/mm)')
        plt.legend()  # this turns the legend on, you can manually change entries using legend(['Sample 1', 'Sample 2',...])
        plt.show()

    def stress_zoom_view(self):
        eZoom = 0.01;
        sZoom = 350
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.plot(self.data['Axial Strain (mm/mm)'], self.data['Stress (MPa)'], label=self.file)
        ax2.plot(self.data['Axial Strain (mm/mm)'], self.data['Stress (MPa)'], label=self.file)

        # Plot the zoomed box
        ax1.plot([0, 0, eZoom, eZoom, 0], [0, sZoom, sZoom, 0, 0], 'r--')

        # Add Labels
        ax1.set_xlim(left=0)
        ax1.set_ylim(bottom=0)
        ax2.set_xlim(left=0, right=eZoom)
        ax2.set_ylim(bottom=0, top=sZoom)
        ax1.set_title("Engineering Stress vs Strain")
        ax2.set_title("Engineering Stress vs Strain Magnified")
        ax1.set_ylabel('Stress (MPa)')
        ax2.set_ylabel('Stress (MPa)')
        ax1.set_xlabel('Strain (mm/mm)')
        ax2.set_xlabel('Strain (mm/mm)')
        ax1.legend()
        ax2.legend()
        plt.show()

    def strain_zoom_view(self):
        eZoom = 0.01;
        aZoom = 0.002
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
        ax1.plot(self.data['Axial Strain (mm/mm)'], self.data['Transverse Strain (mm/mm)'], label=self.file)
        ax2.plot(self.data['Axial Strain (mm/mm)'], self.data['Transverse Strain (mm/mm)'], label=self.file)

        # Plot the zoomed box
        ax1.plot([0, 0, eZoom, eZoom, 0], [0, aZoom, aZoom, 0, 0], 'r--')

        # Add Labels
        ax1.set_xlim(left=0)
        ax1.set_ylim(bottom=0)
        ax2.set_xlim(left=0, right=eZoom)
        ax2.set_ylim(bottom=0, top=aZoom)
        ax1.set_title("Axial Stress vs Transverse Strain")
        ax2.set_title("Axial Stress vs Transverse Strain Magnified")
        ax1.set_xlabel('Axial Strain (mm/mm)')
        ax2.set_xlabel('Axial Strain (mm/mm)')
        ax1.set_ylabel('Transverse Strain (mm/mm)')
        ax2.set_ylabel('Transverse Strain (mm/mm)')
        ax1.legend()
        ax2.legend()
        plt.show()


cases = [Sample(*sample) for sample in Samples]
for case in cases:
    print(case.file)
    print(case.ult_values())








