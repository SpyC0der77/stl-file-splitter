# STL Splitter: Divide STL Files into Equal Segments for Printing

This tool divides an STL file into smaller, manageable pieces along the X and Y axes, facilitating easier 3D printing. It's designed to be more efficient and user-friendly than splitting models within slicer software.

## Prerequisites
Ensure that you have Python 3 installed on your system.
  ```bash
  pip3 install trimesh numpy
  pip3 install manifold3d
```

## Usage
```bash
python split-file.py inputFileName.stl [options]
Options
--xsplit N: Specify the number of divisions along the X-axis.
--ysplit N: Specify the number of divisions along the Y-axis.
--max-x N or -mx N: Set the maximum printable dimension along the X-axis in millimeters.
--max-y N or -my N: Set the maximum printable dimension along the Y-axis in millimeters.
--flip: Flip the STL model over the X-axis before splitting.
```

## Examples
### Basic Usage:
  ```bash
  python split-file.py testfile.stl
  ```
  This command splits testfile.stl into equal-sized pieces using the default settings.

### Specify Number of Splits:
```bash
python split-file.py testfile.stl --xsplit 4 --ysplit 6
```
This command divides testfile.stl into 4 segments along the X-axis and 6 segments along the Y-axis.

### Set Maximum Printable Dimensions:
```bash
python split-file.py testfile.stl --max-x 200 --max-y 200
```

This command calculates the necessary divisions to ensure each piece fits within a 200mm x 200mm print area.

### Combine Options:
```
python split-file.py testfile.stl --xsplit 3 --max-y 150 --flip
```
This command splits testfile.stl into 3 parts along the X-axis, calculates the required divisions along the Y-axis to fit within 150mm, and flips the model over the X-axis before splitting.

### Notes
If both --xsplit and --max-x (or --ysplit and --max-y) are provided, the script will prioritize the explicit split count (--xsplit or --ysplit).
The --flip option is useful for adjusting the model's orientation before splitting, depending on your printing requirements.

Ensure your input STL file is properly formatted and free of errors to avoid issues during the splitting process.

### Troubleshooting
Python Version: If you encounter issues running the script, verify that Python 3 is installed on your system. You can check your Python version with:

```python3 --version```
If Python 3 is not installed, you can install it using your package manager. For example, on Debian-based systems:

```
sudo apt-get install python3
After ensuring Python 3 is installed, use python3 to run the script:
```

```bash
python3 split-file.py inputFileName.stl [options]
```
Dependencies: Ensure all required Python packages are installed. You can install them using pip:

```
pip3 install trimesh numpy
```

### Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request with your proposed changes.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

vbnet
Copy code

You can save this content into a file named `README.md` in your project's root directory. This will provide users with clear instructions on how to use your STL splitting tool, including the new features and options you've implemented.
::contentReference[oaicite:0]{index=0}
 





