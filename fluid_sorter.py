# Copyright and patents pending Jonathan Bannon Maher Corporation
# Inventor and author Jonathan Bannon Maher
# This software, when operating corresponding disclosed hardware,
# provides for the autonomous surgical removal of targeted cells including cancer,
# through artificial intelligence,
# while potentially leaving in tact all healthy cells.


from image_processing import image_processing

# import a library to connect to the relay

import telnetlib

# import library to pause program execution

import time

# import a library to receive the system time

from sys import time

# import a library to connect to access http(s) resources

import urllib

# create variables holding relay on off codes

off = 0
on = 1

# create variables each holding arrays of the relay states of each controlled embodiment

relay_1_motor_in_forward = [off]
relay_2_motor_in_backward = [off]
relay_3_motor_out_forward = [off]
relay_4_motor_out_backward = [off]

# create variables holding motor millimeters and seconds per step

motor_step_millimeters = 1
motor_step_seconds = 0.2

# initialize variables to hold the settings and log file

settings = None
log_file = None

# create variables holding the fluid chamber cubic millimeters, and running totals for
# cubic millimeters of fluid processed, and cubic millimeters of fluid sorted

fluid_chamber_cubic_millimeters = 0.2
fluid_processed_cubic_millimeters = 0
fluid_sorted_cubic_millimeters = 0

# establish an array holding embodiments camera IPs

camera_ips = ["127.0.0.1"]

# create variables holding the cameras' username and password

camera_username = "admin"
camera_password = "admin"

# create a variable to hold an array of embodiment relay IPs

relay_ips = ["127.0.0.2"]

# create variables to hold relays' username and password

relay_username = "admin"
relay_password = "admin"

# initialize a variable to hold an array of relay connections

relays = []
for relay_ip in relay_ips:
    relays.append(None)

# create a function that when called, iterates through each relay IP address,
# established a connection if one has not been initialized or has been dropped,
# then creates a string for of the relay board states, and sends the relay states
# to the relay board

def update_relays():
    index = 0
    for relay_ip in relay_ips:
        command = str(relay_1_motor_in_1_1[index])
        command+= str(relay_2_motor_in_1_2[index])
        command+= str(relay_3_motor_in_2_1[index])
        command+= str(relay_4_motor_in_2_2[index])
        command = str(relay_5_motor_out_1_1[index])
        command+= str(relay_6_motor_out_1_2[index])
        command+= str(relay_7_motor_out_2_1[index])
        command+= str(relay_8_motor_out_2_2[index])
        if not relay[index]:
            relays[index] = telnetlib.Telnet(relay_ips[index], 23)
            relays[index].read_until(b"User Name: ") 
            relays[index].write(relay_username.encode('ascii') + b"\n")
            relays[index].read_until(b"Password: ") 
            relays[index].write(
            relay_password.encode('ascii') + b"\n")
        relays[index].write(command.encode('ascii') + b"\n")
        index += 1


# create a function that will save a snapshot of the image of the fluid under the microscope,
# by opening a connection to the camera, accessing the current camera image,
# and writing the image to a file

def snapshot():

    camera_image_url = "http://%/?username=%&password=%" (camera_ip, camera_username, camera_password)
    camera_image = urllib2.urlopen(camera_image_url).read()

    image_file = open("snapshot.jpg","wb")
    image_file.write(image)
    image_file.close()


# create a function to process the fluid in the compartment using the previously created
# image recognition library

def process():

    # create an array of sort states of the embodiments

    sort_states = []

    # create a variable to hold the current embodiment index

    index = 0

    # inititalize to a variable to hold the saved image intiger index for
    # naming saved images of fluid sorted

    saved_image_index = 0

    # create an array to hold the retrieved image from each embodiment camera

    camera_images = []

    # iterate through each embodiment camera IP address

    for camera_ip in camera_ips:

        # retrieve the image from the current embodiment camera, and append it to the images array

        camera_image_url = "http://%/?username=%&password=%" (camera_ip, camera_username, camera_password)
        camera_image = urllib2.urlopen(camera_image_url).read()
        camera_images[index].append(camera_image)

        # increment the embodiment index

        index = index +1

        # reset the embodiment index to 0

        index = 0

        # iterate through each embodiment camera image

        for camera_image in camera_images:

        # default the sort state for each embodiment to False

            sort_states[index] = False

            # iterate through each setting, creating variables to hold the image file, color, or shape,
            # and the match threshold and or and if the fluid should be sorted and if a match was found

            for setting in settings:
                found = False
                setting = setting.split(" ")
                setting_one = ""
                setting_two = ""
                setting_three = ""
                try:
                    setting_mode = setting[0]
                except:
                    pass
                try:
                    setting_image_color_shape = setting[1]
                except:
                    pass
                try:
                    setting_match_threshold = setting[2]
                except:
                    pass

                # initialize a variable to hold the recognition mode and default it to image,
                # then determine based on the setting, if it should be color or shape

                recognition_mode = "image"

                if setting_image_color_shape.length()==6 and setting_image_color_shape.find(".")==-1:
                    recognition_mode = "color"

                if setting_file_or_color.find(",")>-1:
                    recognition_mode = "shape"

                # if the recognition mode is color, call the function to determine the match between
                # the current image and the color specified in the setting, and set the sort state
                # for the fluid chamber at the current index based on the result

                if recognition_mode == "color":
                    if image_processing.image_contain_color(image, color, threshold):
                        sort_states[index] = True

                # if the recognition mode is image, call the function to determine the match between
                # the current image and the image specified in the setting, and set the sort state
                # for the fluid chamber at the current index  based on the result

                if recognition_mode == "image":
                    if image_processing.image_contains_image(current_image, image_file) >= image_match_minimum:
                        sort_states[index] = True

                # if the recognition mode is shape, call the function to determine the match between
                # the current image and the shape specified in the setting, and set the sort state
                # for the fluid chamber at the current index based on the result

                if recognition_mode == "shape":
                    if image_processing.image_contains_shape(current_image, image_file) > image_match_minimum:
                        sort_states[index] = True

        # iterate through each embodiment sort state, open the outflow door to correspond to the sort state of
        # either keeping or discarding the fluid

        index = 0
        for sort in sort_states:
            if sort:
                relay_5_motor_out_1_1[index] = on
            if not sort:
                relay_8_motor_out_2_1[index] = on
            index = index + 1
        update_relays()
        time.sleep(motor_step_seconds)

        index = 0
        for sort in sort_states:
            if sort:
                relay_5_motor_out_1_1[index] = on
            if not sort:
                relay_8_motor_out_2_1[index] = on
            index = index + 1
        update_relays()
        time.sleep(motor_step_seconds)

        # for each sorter, open the inflow door

        index = 0
        for sort in sort_states:
            relay_5_motor_out_1_1[index] = on
            index = index + 1
        update_relays()
        time.sleep(motor_step_seconds)

        # for each sorter, set the inflow and outflow doors relays to close

        index = 0
        for sort in sort_states:
            relay_5_motor_out_1_1[index] = on

            # if sorted, add the fluid chamber volume to the total volume of fluid sorted out, save the image,
            # naming it after the saved image index and the embodiment index increment the saved image index,
            # and record to the log file the current system time and the name of the image file

            if sort:
                fluid_sorted_cubic_centimeters += fluid_chamber_cubic_centimeters
                image_file_name = "image" + str(saved_image_index) + "-" + str(index) + ".jpg"
                sorted_image_index += 1
                image_file = open("snapshot.jpg","wb")
                image_file.write(camera_image)
                image_file.close()
                log_file_line =  str(sys.time()) + " " + image_file
                log_file.write(log_file_line)

            # add the fluid chamber volume to the total volume of fluid processed

            fluid_processed_cubic_centimeters += fluid_chamber_cubic_centimeters
            index = index + 1

        # update the relays

        update_relays()
        time.sleep(motor_step_seconds)

        # display to the operator the total cubic centimeters processed and sorted

        print "cubic centimeters sorted: " + \
            str(fluid_sorted_cubic_centimeters) + " of " + \
            str(fluid_processed_cubic_centimeters)


# create a function to be called when the program is executed

def main():

    # retrieve any command line arguments, including  the settings file name, the log file name,
    # and any requested embodiment action

    parameters = sys.argv
    settings_file_name = ""
    log_file_name = ""
    try:
        settings_file_name = parameter[1]
        log_file_name = parameter[2]
        action = parameter[3]
    except:
        pass

    # if the requested function is to save a snapshot from an embodiment video camera,
    # call the corresponding function

    if settings_file_name  == "snapshot":
        snapshot()

    # if a snapshot was not requested, read in the settings from the previously specified file,
    # create a log file with the previously specified name, then continuously call the function
    # to process fluid flow

    else:
        settings = open(images_file_name,"r").readlines()
        log_file = open(log_file_name,"w+")
        while True:
            process()

