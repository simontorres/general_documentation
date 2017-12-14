# Notes from the Sofware Meeting of 2017/12/14

Attended: Cesar, Bruno, Simon.

## List of taks for Simon:

- Create a library of comparison lamps obtained with the slit of 0.45"
  with the _Spectroscopic 1x1_ ROI.
  - Let the lamp warm up for two minutes.
  - Take five exposures and combine using `median combine`
- Develop a set of unittest code for wavelength solution validation. This should
  work automatically for all the lamps in the library.
  - Compare `$\lambda_{pipeline}$` versus `$\lambda_{iraf}$`
  - Cross correlate two calibrated lamps.
  - Compare RMS of Pipeline and RMS IRAF
- Create informative plots that will be used in the documentation
  - RMS per slit size
  - RMS per grating - for 0.45" slit
  
The creation of the library will requiere taking lamps with goodman. The plan is 
to start after the astronomer observing ends the night. Before starting, an e-mail
should be sent to soarteam (Cesar will confirm the list) In any case, Bart and 
Stephen should be included.