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

Detail in `requirenments.txt`

### 2. Data storage

The imported data will be stored as Panda's dataframe

The analysed data will be stored as a 3D Numpy array with `x` and `y` representing wavelenghts and `z` temperatures. The axes will not be a part of the array. 

> WARNING: there might be a problem with a derivatine in `z` if the sapceing is uneven - investigate

The metadata will be stored in a dictionary

Current state of the program should be writable to .json

### 3. Classes

#### LumFile

Current stste of the program. Handels writing and reading form .json

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

#### Data export window

Alowws to save results to .json, .csv or .opju

#### File browsing windows (open and save)

Provided within the PyQt6 library

