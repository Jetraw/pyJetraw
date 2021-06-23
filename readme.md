# pyJetRaw, the python module for JetRaw  

This is a Python module to read and write TIFF files with JetRaw compression. For more info visit
https://www.dotphoton.com/


## Requirements
- Jetraw installed on a Windows computer.
- For writing compressed files, a valid License. 

## Installation
First download the WHL file from [latest release](https://github.com/Jetraw/pyJetraw/releases/latest), or browse [previous releases](https://github.com/Jetraw/Jetraw/releases). 
Once the WHL file is downloaded in order to install pyJetraw run the following command:

```python
pip install JetRaw-x.y.z-py3-none-any.whl
```

## Usage
Here are some code snippets of how the module would typically be used.

```python
import jetraw

# Writing a numpy array representing dpcore-prepared stack.
jetraw.imwrite('temp.tif', data, description="Python Jetraw Tests")

# Reading whole stack from TIFF file as numpy array.
image_stack = jetraw.imread('temp.tif')
# image_stack.shape has number of pages as fist dimensions
# image_stack.dtype returns np.uint16

# Read selected pages
image = jetraw.imread('temp.tif', key=range(4, 40, 2))

# Iterate over all pages in TIFF file
with jetraw.TiffReader('temp.tif') as tif:
    for page in tif.pages:
        image = page.read_page(page)

# Successively write the frames of one contiguous series to a TIFF file
with jetraw.TiffWriter('temp.tif', description='JetRaw rocks!') as tif:
    for frame in data:
        tif.write(frame)

# Get information from JetRaw-compressed TIFF without reading data.
tif = jetraw.TiffReader('temp.tif')
tif.pages   # number of pages in the file
tif.width   # width of a page
tif.height  # Height of a page
tif.close()

```

## Contact

If you have any request or doubt please do not hesitate to contact us to:
https://dotphoton.com/contact

