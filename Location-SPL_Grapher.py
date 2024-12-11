"""Microphone-location-based Sound Data Analysis.

This program contains a multitude of functions designed
to take specially formatted .csv files and generate
graphs from them.

Author: Joey Ungerleider
Version: 9/30/2024
"""
import numpy as np
import math
import matplotlib.pyplot as plt
from os import listdir
from scipy.optimize import curve_fit
from datetime import datetime


def meta_parse(filename):
    """Retrieve various metadata from a launch file.

    :param filename: .csv file of the microphone data
    :return: list of tuples of microphone coords
    :return: line/index at which the data begins
    :return: launch time in seconds
    :return: name of the vehicle
    """
    with open(filename) as file:
        data = np.loadtxt(file, delimiter=',', dtype=str, usecols=[0,1])
        for i, tag in enumerate(data[:,0]):
            if tag == ";LATITUDE......................":
                lat = float(data[i, 1])
            elif tag == ";LONGITUDE.....................":
                long = float(data[i, 1])
            elif tag == "AMBIENT":
                start = int(i)
            elif tag == ";LAUNCH TIME  (UTC ZULU).......":
                launch = data[i, 1]
            elif tag == ";VEHICLE NAME..................":
                name = data[i, 1]

    launch = str(launch).strip()
    pt = datetime.strptime(str(launch), '%H:%M:%S.%f')
    launch_time = pt.second + pt.minute * 60 + pt.hour * 3600

    return (lat, long), start, launch_time, name


def data_parse(filename):
    """Parse one microphone csv file to get a data frame of time[sec], and SPL [dB] (first column SPL).

    :param filename: .csv file of the microphone data
    :return: dataframe of time and SPL
    """
    # get the coords, start index, and launch time from other funcs
    coords, start_index, launch, name = meta_parse(filename)

    # get the time col and first SPL col
    with open(filename) as file:
        # column 0 is time, column 1 is dB SPL, column 2 is dBa, column 3 is dBb
        data = np.loadtxt(file, delimiter=',', dtype=str, usecols=[0,2], skiprows=start_index+1)
        SPL = data[:, 1]

        # if the file has 'NaN' data, indicate that it's a "bad" file, and dont save it
        if SPL[0] == 'NaN':
            print(f"File: \"{filename}\" is bad!")
            return None

        # normalize each time measure relative to the launch time of the rocket
        for i, time in enumerate(data[:, 0]):
            pt = datetime.strptime(str(time), '%H:%M:%S.%f')
            secs_time = pt.second + pt.minute*60 + pt.hour*3600
            data[i, 0] = secs_time - launch

    return data


def distance(microphone, launch_pad):
    """Find distance between microphone and launchpad using haversine formula.

    :param microphone: tuple of microphone coords in degrees
    :param launch_pad: tuple of launchpad coords in degrees
    :return: distance in km
    """
    # isolate the lats and longs of each coords, and convert coords from degrees to rads
    mc_lat= math.radians(microphone[0])
    mc_long = math.radians(microphone[1])
    lp_lat = math.radians(launch_pad[0])
    lp_long = math.radians(launch_pad[1])

    # calculate the spherical angle change between the microphone using the haversine formula
    d_angle = 2 * math.asin(math.sqrt(((math.sin((mc_lat - lp_lat) / 2)) ** 2)
            + ((math.cos(mc_lat) * math.cos(lp_lat)) * ((math.sin((mc_long - lp_long) / 2)) ** 2))))

    # calculate the position change
    earth_radius = 6369.920155 # km
    dist = earth_radius * d_angle

    return dist


def filter_data(data, window):
    """Filter data.

    :param data: array-like data to be filtered
    :param window: moving average window size
    :return: filtered data
    """
    # filter with a moving average
    N = window # moving average window
    data = np.pad(data, pad_width=(N//2, N-1-N//2), mode='edge')
    data = np.convolve(data, np.ones((N,))/N, mode='valid')
    return data


def process_data(folder, launch_pad_coords, graph=True):
    """Process stats and generate a 3D graph of distance from launchpad, SPL, and time into launch.

    :param folder: folder of .csv files to work from
    :param launch_pad_coords: coordinates of the launchpad
    :param graph: boolean to turn on/off creating a graph
    :return: max SPL in each microphone
    """
    max_list = []
    dist_list = []

    # open the folder and put all the file names in a list
    file_list = listdir(folder)

    if graph:
        # create a 3D figure
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlabel('Distance from Launchpad [km]')
        ax.set_ylabel('Time [s]')
        ax.set_zlabel('SPL [dBa]')

    # loop through the folder of files, processing and plotting each one
    for i in range(len(file_list)):
        file_path = f"{folder}\\{file_list[i]}"
        coords, start_index, launch, name = meta_parse(file_path)
        data = data_parse(file_path)

        # since our bad files return NoneType, skip if a None is returned
        if data is None:
            continue

        # define what our 'x' 'y' and 'z' will be in the graph
        dist = distance(coords, launch_pad_coords) # in km
        time = [float(t) for t in data[:, 0]]
        SPL = [float(s) for s in data[:, 1]]

        # filter the dependent variable data
        # SPL = filter_data(SPL, window=12)

        if graph:
            # plot this file on the figure
            ax.plot(dist, time, SPL)
            ax.set_title(f"(Unfiltered) Location Sorted SPL vs. Time for: {name}")

        max_list.append(round(float(max(SPL)), 2))
        dist_list.append(dist)

    if graph:
        plt.show()

    return max_list, dist_list


def max_curve(maxes, dist, name, graph=True):
    """Generate a curve of a launch's max SPL values.

    :param maxes: list of SPL max values
    :param dist: list of distances
    :param graph: boolean to turn on/off creating a graph
    :return: equation of the max SPL curve as a function of distance from the launchpad
    """
    # general negative logarithm solution
    def fit_log(x, a, b, c, d):
        return -a * np.log(b*x + c) + d

    popt = curve_fit(fit_log, dist, maxes, bounds=(0, [np.inf, np.inf, np.inf, np.inf]))
    a, b, c, d = popt[0]
    fitted_values = [fit_log(km, a, b, c, d) for km in dist]

    if graph:
        plt.figure()
        plt.scatter(dist, maxes)
        plt.plot(dist, fitted_values)
        plt.title(f"Actual SPL maxes vs. fitted max curve for {name}")
        plt.xlabel(f"Distance from Launchpad [km]")
        plt.ylabel(f"Maximum Sound Pressure Level [dBa]")
        plt.show()

    return a, b, c, d


if __name__ == "__main__":
    # launch pad coordinates
    marspad0A_coords = (37.833879, -75.487709) # antares launch pad
    slc37B_coords = (28.531986, -80.566821) # delta IV heavy launch pad
    slc40_coords = (28.562106, -80.57718) # falcon 9 launch pad
    lc39A_coords = (28.608333, -80.604444) # falcon heavy launch pad

    # launch folders
    antares_folder = 'RocketNoiseCSV\ANTARES230_CRS-8E(OA-8E)-LAUNCHNOISE'
    d4h_folder = 'RocketNoiseCSV\DELTAIVHEAVY_PARKERSOLARPROBE-LAUNCHNOISE'
    f9_folder = 'RocketNoiseCSV\FALCON9_CRS-15-LAUNCHNOISE'
    fh_folder = 'RocketNoiseCSV\FALCONHEAVY_ARABSAT6A-LAUNCHNOISE'

    # switch to turn graphing on/off
    graph_switch = True

    # generate graphs
    antares_max, antares_dist = process_data(antares_folder, marspad0A_coords, graph_switch)
    # d4h_max, d4h_dist = process_data(d4h_folder, slc37B_coords, graph_switch)
    # f9_max, f9_dist = process_data(f9_folder, slc40_coords, graph_switch)
    # fh_max, fh_dist = process_data(fh_folder, lc39A_coords, graph_switch)

    # processing for the antares rocket:
    a, b, c, d = max_curve(antares_max, antares_dist, "Antares-230", graph_switch)
    print(f"\nMax SPL in each microphone around the launch pad: {antares_max}")

    print(f"\nFunction format: -a * ln(b*x + c) + d")
    print(f"where: a = {a:.4f}, b = {b:.4f}, c = {c:.4f}, d = {d:.4f}")

    max_db = 100
    radius = ((math.exp(-((max_db-d)/a))) - c) / b
    print(f"For max sound level of {max_db}[dBa], use range of {radius:.2f}[km].")
