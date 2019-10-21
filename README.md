This is a fork of owenb321's repo which is itself a port of Atarity's plugin.
This for is designed to have the python run in the background of windows controlling your LEDs
It no longer is designed as a plugin for prismatik but rather as a background task that interacts with Prismatik's API
This is a messy bit of code tid bits and files all with the end goal of being able to change the running animation on the fly with keyboard short cuts

The .vbs files are set up to launch and run without opening any windows, this is so that the running animation can change without interrupting any programs (IE it won't alt-tab you out of games)
Simply bind a key combo to launch the vbs and it will kill any running animation and start running the one you want
!!!This is done by terminating any running python2, if your python2.7 doesn't run as python2, it will need to be updated to match in the batch files

The txt files are simply used as an input to select the animation in the program so that you don't have to

The MiamiAnimation method is setup to simply span a color palette across all of your LEDs and slowly shift them
It works with an arbitrary sized list of rgb values as long as the size of the list is less than your number of leds
If you want colors to take up less LEDs on your LED strip, just append your color pallete to itself effectively cutting in half the space each color takes up.

This code was hacked together, poorly at times, to do what I couldn't find any other software to do (Aside from shelling out way to much money for litestrips that use another companies software which are generaly overpriced)


#Prismatik Animate plugin

##Description
This is a port of the Animate plugin for Prismatik, originally written by [Atarity](https://github.com/Atarity/Prismatik-plugins).

## Version 0.1

##Dependencies
* Python 2.7
* Prismatik (tested on 5.11.1)

##Installation
* Install Python 2.7
* Download the ZIP from the repository
* Unzip to a new local folder
* In Prismatik:
  * Enable the API
    * Enable `Expert mode` under `Profiles`
    * Check `Enable server` under `Experimental`
* Place the unzipped folder in the Prismatik plugins directory (e.g. `C:\Users\owenb321\Prismatik\Plugins\Animate`)
* Adjust settings in the Animate.ini file
* Refresh the plugin list in Prismatik

##Configuration
Settings are configured in the `Animate.ini` file.
* Main
  * These are used by Prismatik to identify the plugin
* Lightpack
  * `host` - Address of the API server. `127.0.0.1` is the local machine.
  * `port` - API server port number. `3636` is the Prismatik default.
  * `ledmap` - Specifies the clockwise order of your LEDs (comma-separated). This is needed for the Snake animation. LED numbers can be found on the screen grabber setup boxes. If commented out, the Snake animation defaults to an ordered list of all LEDs
  * `cylonmap` - Specifies groups of LEDs to use for the Cylon animation. Groups are semicolon-separated, LEDs within the groups are comma-separated. For example, the default setting is `10,9,8; 7,6; 5,4; 3,2,1` in these groups, `10,9,8'`are the left side LEDs, `7,6` are the top-left `5,4` are the top-right, and `3,2,1` are the right side. If commented out, these default groups are used.
* Animation
  * `type` - Selects animation type; 1 = 1-dimension plasm, 2 = Disco distro, 3 = Snake, 4 = Cylon
