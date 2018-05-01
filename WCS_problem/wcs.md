# WCS representation 

## Source of documentation

The most important document is of course the 
[fits standard paper](fits_standard40aa.pdf) which is actually in evolution.
The list of versions can be found on 
[this link](https://fits.gsfc.nasa.gov/fits_standard.html).

Another interesting source is [Greisen et.al 2006](greisen-2006.pdf)

In general de fits standard paper is not a good experience for a user but it
must be the starting point since it defines de standard.

## Summary or notes

- Finally, there is no new implementation of wcs tools but the list of actions
  was the following.
  - move `wsbuilder.py` from `goodman/goodman/spectroscopy` to `goodman/goodman/wsc`
  were `wcs` is a new directory.
  - rename `wsbuilder.py` to `wcs.py`
  - `wcs.py` contained three classes that all were used to handle all aspects of
  a wavelength solution creation or reading.
      - `WavelengthFitter`
      - `ReadWavelengthSolution`
      - `ReadMathFunctions`
  They were all removed and now they are integrated as a single class called
  `WCS`. Most of the methods were made private but only `WCS.fit`, `read` and 
  `get_model` were left public. 
  
  - Application example:
  
    - **Read a Wavelength Solution**
    
    ```python
    import matplotlib.pyplot as plt
    import astropy.units as  u
    from ccdproc import CCDData
    from goodman.wcs import WCS
    
    calibrated_image = '/path/to/image.fits'
    
    # instantiate the WCS class
    wcs = WCS()
    
    # read image
    ccd = CCDData.read(calibrated_image, unit=u.adu)

    # Read wavelength solution from fits header
    # for now it only works with Linear Solutions
    # Non-linear solutions will raise a NotImplementedError
    wavelength_axis, intensity = wcs.read(ccd=ccd)

    plt.plot(wavelength_axis, intensity, label='Calibrated Spectrum')
    plt.xlabel("Wavelength (Angstrom)")
    plt.ylabel("Intensity (ADU)")
    plt.legend(loc="best")
    plt.show()
    
    ```
    
    - **Fit a wavelength solution**
    ```python
    import matplotlib.pyplot as plt
    import astropy.units as  u
    from ccdproc import CCDData
    from goodman.wcs import WCS
    
    raw_image = '/path/to/image.fits'
    
    # instantiate the WCS class
    wcs = WCS()
    
    # read image
    ccd = CCDData.read(raw_image, unit=u.adu)

    # In between you need a method to find a match of pixel values and angstrom
    # values (The values below are fake values)
    
    line_center_pixel = [3,
                         45,
                         80,
                         320,
                         800,
                         850,
                         1000,
                         1200]
                     
    line_center_angstrom = [4545.0519,
                            4579.3495,
                            4589.8978,
                            4609.5673,
                            4726.8683,
                            4735.9058,
                            4764.8646,
                            4806.0205]
    # Get the mathematical model that represents the wavelength solution
    # in this case chebyshev and order 3 are the default for all goodman
    # pipeline processing other methods apart of linear are not implemented.
    wavelength_solution_math_model = wcs.fit(physical=line_center_pixel,
                                             wavelength=line_center_angstrom,
                                             model_name="chebyshev",
                                             order=3)
    # Asumming the length in pixels of your spectrum is 4096 then
    pixel_axis = range(4096)
    wavelength_axis = wavelength_solution_math_model(pixel_axis)

    
    # Asumming `ccd.data` is the extracted 1D data.
    plt.plot(wavelength_axis, ccd.data, label='Calibrated Spectrum')
    plt.xlabel("Wavelength (Angstrom)")
    plt.ylabel("Intensity (ADU)")
    plt.legend(loc="best")
    plt.show()
    
    ```
    
  