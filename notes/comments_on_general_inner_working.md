# How does the pipeline operates.

All images should be first processed by `redccd` and then by `redspec`.

## redccd

The first action is to classify the data, this does not mean ordering but just
evaluate three aspects of the data.

- full path: Full path to data to be processed.
- instrument: `Blue` or `Red` Camera.
- technique: `Imaging` or `Spectroscopy`.

Then comes a night organizer module which is the one that orders the data.
For instatiating the class it requieres the the three values obtained by the
previous method.

A new feature added is the possibility to ignore all the data that does not matches 
the observing "technique" this is particularly useful for Spectroscopy where some
users might want to use the Imaging mode for slit/target acquisition, then those
images will be ignored. For Imaging it will also ignore all non-Imaging data
which is kind of redundant.