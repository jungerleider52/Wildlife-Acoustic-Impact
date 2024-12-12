# Assessing Acoustic Impact of Rocket Launches on Surrounding Wildlife

Joey Ungerleider, Valentina Paz Soldan, Jonathan Kogon

Rockets are powerful vehicles that play a critical role in space exploration, satellite deployment, and scientific research. Their value lies in their ability to overcome the challenges of Earth's gravity and enable human exploration of space. However, a major challenge in rocket launches is the threat of the massive acoustic loads that occur during liftoff. These acoustic loads can be caused by engine exhaust, aerodynamic turbulence, shock waves, and other factors. The excessive noise and vibration from launches can cause damage to the vehicle's structure, equipment, and payload, but it can also have effects on the surrounding environment. For public safety, rocket launches are held far away from populated areas, but local wildlife can still be affected. This paper will investigate how rocket sound levels affect wildlife in the surrounding geographical area.

# Dependencies

This repository depends on modules from Math, Numpy, SciPy, Datetime, Matplotlib, and OS libraries. 

USE PYTHON 3.10 when running this program to avoid compatibility issues.

# Program Functions

This repository consists of one main program, "Location-SPL_Grapher" which includes the following functions:

    meta_parse(filename):
        """Retrieve various metadata from a launch file.
    
        :param filename: .csv file of the microphone data
        :return: list of tuples of microphone coords
        :return: line/index at which the data begins
        :return: launch time in seconds
        :return: name of the vehicle
        """

    data_parse(filename):
        """Parse one microphone csv file to get a data frame of time[sec], and SPL [dB] (first column SPL).
    
        :param filename: .csv file of the microphone data
        :return: dataframe of time and SPL
        """

    distance(microphone, launch_pad):
        """Find distance between microphone and launchpad using haversine formula.
    
        :param microphone: tuple of microphone coords in degrees
        :param launch_pad: tuple of launchpad coords in degrees
        :return: distance in km
        """

    filter_data(data, window):
        """Filter data.
    
        :param data: array-like data to be filtered
        :param window: moving average window size
        :return: filtered data
        """

    process_data(folder, launch_pad_coords, graph=True):
        """Process stats and generate a 3D graph of distance from launchpad, SPL, and time into launch.
    
        :param folder: folder of .csv files to work from
        :param launch_pad_coords: coordinates of the launchpad
        :param graph: boolean to turn on/off creating a graph
        :return: max SPL in each microphone
        """

    max_curve(maxes, dist, name, graph=True):
        """Generate a curve of a launch's max SPL values.
    
        :param maxes: list of SPL max values
        :param dist: list of distances
        :param graph: boolean to turn on/off creating a graph
        :return: equation of the max SPL curve as a function of distance from the launchpad
        """

# Walkthrough

The general process of the primary program is as follows:

1) From a folder of microphone data, loop through each file/microphone:
2) Collect metadata from each set, like coordinates of that microphone
3) Calculate the distance from that microphone to the launch pad
4) Collect raw data from each set
5) Filter data with a moving average
6) Find the max sound level in each microphone
7) Fit an exponential decay function based on each microphone’s max sound level and distance from the launchpad. Now we have a formula for max sound level as a function of distance from the launch pad, and can extrapolate max sound levels farther away from the launchpad than we actually have data for.
8) Determine the maximum range around the launch pad, that would be loud enough to disrupt wildlife during a launch.

Note: The boolean variable "graph_switch" can be set to True or False to turn graph generation on or off, in the process_data() and max_curve() functions.

# Sample Results

Using the Antares 230 launch folder, with a maximum tolerable sound level of 100 [dBa]:

1) The following max SPLs in each microphone are generated: [129.43, 129.8, 130.01, 115.99, 112.58, 105.64, 107.45, 103.88, 102.38, 102.12, 102.42, 102.84, 102.66, 102.81, 102.58, 102.5, 102.52, 102.62, 102.51, 102.76, 100.38, 99.19, 98.91, 99.61, 101.09, 99.26, 99.54, 96.76, 96.52, 97.42, 94.65, 92.55, 92.42, 93.01, 90.21, 88.1, 87.96, 87.87, 87.95, 90.19, 90.55, 92.17, 85.15, 79.04, 81.96, 77.53]
2) This data is fitted to a negative logarithmic function of the format: -a * ln(b*x + c) + d

    Where coefficients: a = 15.3842, b = 0.0261, c = 0.0087, d = 63.8232
3) With this function, a maximum range is calculated of 3.31 [km] around the launchpad.

# Limitations

Although this function can automatically find certain information within the raw datasets, like coordinates, names, and indices of important events, a limitation is that the dataset must be of a very specific format to begin with.

# Future Work

In the future, the team plans to conduct further research into how different levels of sound affect different individual species. We also plan to investigate how different frequencies of sound affect wildlife.
