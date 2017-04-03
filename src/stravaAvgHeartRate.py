#
# This program parses Strava gpx activities from a local directory
# and calculates the average heart rate
# and plots the data using matplot and seaborn
# Written by Brandon Markwalder 2016
#

import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def stravaAvgHeartRate():
    data = dataPrep("LOCAL PATH TO GPX FILES/*.gpx")

    plotDate, values, numIncidents = np.array(data[0]), np.array(data[1]), np.array(data[2])

    sns.set(color_codes=True)
    plt.xticks(numIncidents, plotDate, rotation='vertical', fontsize=8)
    plt.margins(0.005)
    plt.plot(values, 'ro')
    plt.show()
    sns.set(style="whitegrid")
    sns.regplot(numIncidents, values, lowess=True)
    sns.plt.show()

def dataPrep(directory):
    # Invoke gpxParse for each file in a given directory
    data = [gpxParse(gpx) for gpx in glob.iglob(directory)]

    # Filter out tuples in data list that do not contain heart rate data
    plotData = [i for i in data if i[1] != 'no data']

    # Unpack into two lists for plotting
    dates, values = zip(*plotData)

    # Filter dates to select first day of each month
    dateLst = []
    pointer = 0

    for i in dates:
        while pointer < int(i[5:7]):
            pointer += 1
            if pointer == int(i[5:7]):
                dateLst.append(i)
            else:
                pointer += 1
        if pointer == 12:
            pointer = 0

    # Count number of date points so they can be plotted as custom ticks
    numIncidents = [i for i in range(len(dates))]

    # Build datePlot list with filtered dates and empty strings to match ticks
    # Convert date string YYYY-MM-DD to Mon YYYY
    dict = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
            '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    plotDate = [(dict[i[5:7]] + ' ' + i[0:4]) if i in dateLst else '' for i in dates]

    return plotDate, values, numIncidents

def gpxParse(activity):
    infile = open(activity, 'r')
    content = infile.read()
    infile.close()
    hrAvg = [(heartRate(content))]
    dates = [(date(content))]
    combine = (dates + hrAvg)
    return combine

def date(content):
    for date in content.split():
        if '<time>' in date:
            return date[6:16]

def heartRate(content):
    hrData = [(int(hrPoint.replace('<gpxtpx:hr>', '').replace('</gpxtpx:hr>', ''))) for hrPoint in content.split() if
              '<gpxtpx:hr>' in hrPoint]
    if hrData:
        return (sum(hrData) // len(hrData))
    return ('no data')

stravaAvgHeartRate()
