# pyJetRaw, the Python Module for Jetraw  
This is the Jetraw Python Module which allows you to read and write TIFF files using Jetraw's compression. For more info visit
https://www.dotphoton.com/

## Requirements
- Windows 10 64 bits or Linux
- Jetraw installed.<br/>
*Note:* if you do not have Jetraw installed visit https://www.jetraw.com/downloads/software and for usage information https://github.com/Jetraw/Jetraw
- For writing compressed files, a valid License. 

## Installation Windows
First download the WHL file from [latest release](https://github.com/Jetraw/pyJetraw/releases/download/21.06.23.2/JetRaw-0.9.1-py3-none-any.whl), or browse [previous releases](https://github.com/Jetraw/pyJetraw/releases). 
Once the WHL file is downloaded in order to install pyJetraw run the following command:

```python
pip install JetRaw-x.y.z-py3-none-any.whl
```

## Installation Linux
The WHL file needs to be installed like in the previous section but an extra step is necessary. 

You need to add to the LD_LIBRARY_PATH variable the dpcore and jetraw libraries location so pyDpcore is able to find them:

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path_to_jetraw_folder/lib/
```

It is recommended to **add this instruction in your bashrc (/home/user/.bashrc)** file, then everytime a bash environment is created everything is set up to use pyJetraw. Remember that if you are using an IDE to run python, you will need to launch it from the Terminal. If not the enviroment will not be correctly configured.  

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
Feel free to use the [issues section](https://github.com/Jetraw/pyJetraw/issues) to report bugs or request new features. You can also ask questions and give comments by visiting the [discussions](https://github.com/Jetraw/pyJetraw/discussions), or following the contact information at https://jetraw.com.

