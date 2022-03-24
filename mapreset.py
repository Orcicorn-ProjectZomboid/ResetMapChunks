#!/usr/bin/python3
"""
Provides a simplified interface to reset sections of a Zomboid Map

WRITTEN AND TESTED ON A LINUX DEDICATED SERVER.
ADJUST FOR WINDOWS INCLUDING LINE 1, 114 AND 122
"""

# ----------------------------------------------------------------------
# COMMON LIBRARIES -----------------------------------------------------
# ----------------------------------------------------------------------
from json import load as jsonload
from math import floor
from os import listdir, remove
from os.path import split as path_split, abspath, join, isfile
from time import time


# ----------------------------------------------------------------------
# CUSTOM LIBRARIES -----------------------------------------------------
# ----------------------------------------------------------------------
from common import logs


# ----------------------------------------------------------------------
# CONFIGURATION --------------------------------------------------------
# ----------------------------------------------------------------------
GLOBAL_CONFIG = join(path_split(abspath(__file__))[0], "config.json")


# ----------------------------------------------------------------------
# FUNCTIONS ------------------------------------------------------------
# ----------------------------------------------------------------------
def in_boundary(X, Y, startX, startY, endX, endY):
    """Determines if a co-ordinate is within a boundary

    Args:
        X (int): The X co-ordinate to test
        Y (int): The Y co-ordinate to test
        startX (int): The starting boundary (top-left) X co-ordinate
        startY (int): The starting boundary Y co-ordinate
        endX (int): The stopping boundary (bottom-right) X co-ordinate
        endY (int): The stopping boundary Y co-ordinate

    Returns:
        boolean: Is the defined X,Y within the boundaries of Start/Stop
    """
    return (int(X) >= int(startX)) and (int(X) <= int(endX)) and \
           (int(Y) >= int(startY)) and (int(Y) <= int(endY))


def load_configuration(file):
    """Loads the JSON Configuration document as defined

    Args:
        file (str): The full path and filename to the JSON Configuration

    Raises:
        ValueError: Improperly formatted configuration
        FileNotFoundError: File or Folder not found

    Returns:
        array: A JSON decoded array of values
    """
    if isfile(file):
        try:
            with open(file) as file_object:
                return jsonload(file_object)
        except Exception as error:
            raise ValueError("Improperly formatted configuration") from error
    else:
        raise FileNotFoundError(f"File not found: {file}")


def resetmap(log, path,
             startX, startY, startChunkX, startChunkY,
             endX, endY, endChunkX, endChunkY):
    """Deletes a series of files that are within the boundaries.

    Args:
        log (obj): The logfile object to record actions to
        path (str): Path to the Zomboid Save File Folder
        startX (int): The starting X co-ordinate (top left)
        startY (int): The starting Y co-ordinate
        startChunkX (int): The starting Chunk/Cell X co-ordinate
        startChunkY (int): The starting Chunk/Cell Y co-ordinate
        endX (int): The stopping X co-ordinate (bottom right)
        endY (int): The stopping Y co-ordinate
        endChunkX (int): The stopping Chunk/Cell X co-ordinate
        endChunkY (int): The stopping Chunk/Cell Y co-ordinate
    """
    files = listdir(path)
    counter_map = 0
    counter_meta = 0
    timer_start = time()

    # Co-ordinates are sent in in absolute tiles however the map stores them
    # in 10 tiles to a line, so we take the co-ordinates, divide by 10,
    #  floor it and then we can get a filename boundary check
    startX = floor(startX/10)
    startY = floor(startY/10)
    endX = floor(endX/10)
    endY = floor(endY/10)

    # Loop through the map files and delete any that are within our boundareies
    for file in files:
        current_item = file[:-4].split('_')
        # Clear out Map files that are within our co-ordinates
        if len(current_item) == 3 and current_item[0] == 'map':
            if in_boundary(current_item[1], current_item[2],
                           startX, startY, endX, endY):
                counter_map += 1
                log.add(f"> Deleting {file}")
                remove(f'{path}//{file}')
        # If not a map file, but actually meta data then if it's in chunk data
        elif len(current_item) == 3 and \
                (current_item[0] == 'chunkdata' or current_item[0] == 'zpop'):
            if in_boundary(current_item[1], current_item[2],
                           startChunkX, startChunkY, endChunkX, endChunkY):
                counter_meta += 1
                log.add(f"> Deleting {file}")
                remove(f'{path}//{file}')

    log.add_header("Summary")
    log.add(f"> Completed in {(time() - timer_start):.2f} seconds")
    log.add(f"> Removed {counter_map:,d} map files")
    log.add(f"> Removed {counter_meta:,d} meta files")


# ----------------------------------------------------------------------
# MAIN -----------------------------------------------------------------
# ----------------------------------------------------------------------
def main(user_config):
    """Main application routine

    Args:
        user_config (str): The Path & Filename of the configuration document
    """
    # Load Configuration settings
    config = load_configuration(user_config)

    # Setup Logfile settings
    log = logs.NewLog(65, config['logs']['save'], config['logs']['path'])
    log.enable_treeview()

    # Prompt the user for which region they want to be reset
    counter = 0
    print("Which region would you like to reset?")
    print("")
    for region in config['regions']:
        print(f"  {counter}\t{region['name']}")
        counter += 1
    print("")
    selection = input("Reset region #")
    try:
        selection = int(selection)
    except ValueError:
        print("ERROR: Incorrect region selection")
        exit(1)

    if int(selection) < 0 or (int(selection) >= int(counter)):
        print("ERROR: Region out of bounds")
        exit(2)

    # Setup the Log file and start resetting
    log.timestamp()
    log.add_header(f"{config['regions'][selection]['name']}")
    log.add(f"> Region: {selection}")
    log.add(f"> Start:  {config['regions'][selection]['start'][0]} x "
            f"{config['regions'][selection]['start'][1]} "
            f" Chunk ({config['regions'][selection]['start'][2]} x "
            f"{config['regions'][selection]['start'][3]})")
    log.add(f"> Stop:   {config['regions'][selection]['stop'][0]} x "
            f"{config['regions'][selection]['stop'][1]} "
            f" Chunk ({config['regions'][selection]['stop'][2]} x "
            f"{config['regions'][selection]['stop'][3]})")
    log.add_header("Reset Log")
    resetmap(log, config['path'],
             config['regions'][selection]['start'][0],
             config['regions'][selection]['start'][1],
             config['regions'][selection]['start'][2],
             config['regions'][selection]['start'][3],
             config['regions'][selection]['stop'][0],
             config['regions'][selection]['stop'][1],
             config['regions'][selection]['stop'][2],
             config['regions'][selection]['stop'][3])

    # Done
    log.timestamp()


# ----------------------------------------------------------------------
# ROUTINE --------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    main(GLOBAL_CONFIG)
