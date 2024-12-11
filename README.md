# Assessing Acoustic Impact of Rocket Launches on Surrounding Wildlife

Joey Ungerleider, Valentina Paz Soldan, Jonathan Kogon

Rockets are powerful vehicles that play a critical role in space exploration, satellite deployment, and scientific research. Their value lies in their ability to overcome the challenges of Earth's gravity and enable human exploration of space. However, a major challenge in rocket launches is the threat of the massive acoustic loads that occur during liftoff. These acoustic loads can be caused by engine exhaust, aerodynamic turbulence, shock waves, and other factors. The excessive noise and vibration from launches can cause damage to the vehicle's structure, equipment, and payload, but it can also have effects on the surrounding environment. For public safety, rocket launches are held far away from populated areas, but local wildlife can still be affected. This paper will investigate how rocket sound levels affect wildlife in the surrounding geographical area.

# Dependencies

This repository depends on modules from Math, Numpy, SciPy, Datetime, Matplotlib, and OS libraries. 

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

From a folder of microphone data, loop through each file/microphone:
Collect metadata from each set, like coordinates of that microphone
Calculate the distance from that microphone to the launch pad
Collect raw data from each set
Filter data
Find the max sound level in each microphone
Fit an exponential decay function based on each microphone’s max sound level and distance from the launchpad. Now we have a formula for max sound level as a function of distance from the launch pad, and can extrapolate max sound levels farther away from the launchpad than we actually have data for.
Determine the maximum range around the launch pad, that would be loud enough to disrupt wildlife during a launch.


# Sample Results



# Limitations

# Future Work
