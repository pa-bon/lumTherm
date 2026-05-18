# lumTherm
A software for analysis of optical thermometry

## Backend

### 1. Packages

The program will be written using:
* Pandas
* Numpy
* SciPy
* MatplotLib
* PyQt6
* pathlib

Details in `requirenments.txt`

### 2. Data storage

The imported data will be stored as Panda's dataframe

The analysed data will be stored as a series of 3D Numpy arrays (or xarray, to be determined) with `x` and `y` representing wavelenghts and `z` temperatures. The axes will not be a part of the array. 

Float32 will be used to reduce memory consumpition (6-8 signififcant digits, shold be enaught)

One aray with presessd data will be of size about: 2000 x 2000 x 40. This gives 80 000 000 numbers, 640 MB with float64, but only half of that with float32

The metadata will be stored in a dictionary

Current state of the program should be writable to .h5

### 3. Classes

#### LumFile

Current stste of the program. Handels writing and reading form .h5

#### LumSpectrum

Handels the data. Collests the functions for data analysis.

## Frontend

### 1. Windows
The program requires the following windows

#### The main window

Displays the data

#### Data import window

Allows to reda data from a text file. An interface to use `from_csv()` function from Pandas

It contains:

* **the browse section** with file path and 'browse' button
* **the tabel preview** updated continousely
* **the import settings** allowing to set:
    - delimeter (text)
    - rows to skip (list)
    - columns to skip (list)
    - columns headings (list or range)
* **the saving section** allowing to add or replace existing data

#### Smooth/bacground window

Handels the smoothing, bacground subtraction and uncetainty determination

#### Data export window

Allows to save results to .json, .csv or .opju

#### File browsing windows (open and save)

Provided within the PyQt6 library

