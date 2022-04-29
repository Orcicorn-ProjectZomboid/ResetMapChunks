# resetMapChunks

This very simple script allows you to delete portions of a Project Zomboid
 map by simply providing X,Y co-ordinates as well as chunk references.

## Understanding the co-ordinates

When adding a "region" to the configuration document you are required to
 provide 8 co-ordinates which are broken down into 2 groups; Start and Stop. The "Start" is considered to be the top-left of a box while the "Stop" is
 to be considered the bottom-right of a box. This defines a region.

You can acquire co-ordinates by utilizing the
 [Project Zomboid Map Project](https://map.projectzomboid.com/) and accessing
 the *"Map coordinates (on Level 0)*" menu item.  This will expand the menu
 and allow you to not only view the actual co-ordinates but lock in specific
 locations.

In the Project Zomboid Map, the co-ordinates are in a "***X** x **Y***" format and
 the Chunk co-ordinates are referred to as "*Cells*". We do not need the "*Rel*"
 values.

## Adding Regions to Configurations

The configuration file can contain an unlimited number of regions. Simply append
 a new region to the bottom of the document within the square brackets of the
 regions key.

You must provide 9 pieces of information:

1. A human friendly name for this region.
1. A Starting co-ordinate plot array consisting of
   - A starting X co-ordinate
   - A starting Y co-ordinate
   - A starting X chunk co-ordinate
   - A starting Y chunk co-ordinate
1. A Stopping co-ordinate plot array consisting of
   - A stopping X co-ordinate
   - A stopping Y co-ordinate
   - A stopping X chunk co-ordinate
   - A stopping Y chunk co-ordinate

For example, Muldraugh would look like this:

```json/plain-text
{
    "name":     "Muldraugh",
    "start":    [10030, 8984, 32, 29],
    "stop":     [11428, 10807, 38, 36]
}
```

This would definte the start of Muldraugh as 10030x8984 in Chunk 32x29 and
 ending at 11428x10807 in Chunk 38x36.  This boundary would then allow the
 script to determine which files are located in this area and delete them from
 the map which would cause a complete respawn the next time a person visited
 this area.

## Caveats

This has been written and tested on Linxu only. It may require a little tweaking
 to fuction correclty on windows.  Primarily due to the pathing differences
 in file paths in config.json

In `mapreset.py` you will need to tweak line #1 to properly represent the
 python binary location or remove it entirely.

In `config.json` you will need to change your save file paths and if on
 windows, use double-slashes for paths.  For example `C:\Users\JSmith` should
 be written as `C:\\Users\\JSmith`

## !!! WARNING !!!

When you run this script and choose a region **IT WILL PERMANENTLY DELETE
 FILES FROM YOUR SAVED WORLD**.  If you do not know what you're doing turn
 back now. This is unrecoverable.

Do not contact me if you mess up. This is on you.
Turn back now, don't run this script if you are not 100% sure of what you
 are doing.

## Credits

Inspired and based loosely on [zomboidClearMap by Michaellaneous](https://github.com/Michaellaneous/zomboidClearMap/tree/master)