import os
import tifffile
from src.jetraw import jetraw_tiff
from src.jetraw.tiff_writer import TiffWriter
from src.jetraw.tiff_reader import TiffReader
import numpy as np
import subprocess
import pathlib

dpcore_prepared_image_path = ""

def create_dpcore_prepared_image(pages, width, height):
    if pages == 1:
        # 2D container
        image = np.zeros((height, width))
        for row in range(image.shape[0]):
            for column in range(image.shape[1]):
                image[row][column] = column * 40
    else:
        # 3D container
        image = np.zeros((pages, height, width))
        for page in range(image.shape[0]):
            for row in range(image.shape[1]):
                for column in range(image.shape[2]):
                    image[page][row][column] = column * 40

    path = pathlib.Path(__file__).parent.absolute()
    input_image_path = os.path.join(path, "test_write_image_python.tif")
    tifffile.imsave(input_image_path, data=image.astype(np.uint16))
    # arguments for dpcore
    destination = "-d " + os.path.join(path, "dpcore_prepared\\")
    identifier = "-i PCO_3A2DD3A"
    params = "-p " + os.path.join(path, "pco_3a2dd3a.dat")
    # call system dpcore (WINDOWS)
    subprocess.check_call(["dpcore.exe", input_image_path, destination, identifier, params, "--overwrite"])
    # set prepared image path
    return os.path.join(os.path.join(path, "dpcore_prepared\\"), "test_write_image_python.tif")


def process_image_tif(input_filename, output_filename):
    # READ compressed images from disk
    # Option A: READ using imread function (whole stack)
    read_all_pages = jetraw_tiff.imread(input_filename)
    # Option B: READ using imread function (range)
    read_range_pages = jetraw_tiff.imread(input_filename, [3, 4, 7, 1, 6])
    # Option C: READ using imread function (single page)
    read_single_page = jetraw_tiff.imread(input_filename, 5)

    # write uncompressed image into disk as TIFF
    path = pathlib.Path(__file__).parent.absolute()
    tifffile.imwrite(os.path.join(path, "read_all_pages.tif"), read_all_pages)
    tifffile.imwrite(os.path.join(path, "read_range_pages.tif"), read_range_pages)
    tifffile.imwrite(os.path.join(path, "read_single_page.tif"), read_single_page)

    with TiffReader(input_filename) as reader:
        for page in range(reader.pages):
            image = reader.read(page)
            tifffile.imwrite(os.path.join(path, "image_") + str(page) + ".tif", image)

    # WRITE compressed images to disk
    dpcore_prepared_filename = create_dpcore_prepared_image(10, 320, 240)
    image = tifffile.imread(dpcore_prepared_filename)
    # WRITE compressed image into disk
    # Option A: using jetraw Module
    jetraw_tiff.imwrite(output_filename, image, "JetRaw compressed image")

    # Option B: using a writer object
    with TiffWriter(output_filename, "JetRaw compressed image") as jetraw_writer:
        for page in range(image.shape[0]):
            jetraw_writer.write(image[page, :])


def process_dir(sourcedir, destdir):
    assert os.path.isdir(sourcedir), "Source directory does not exist."
    compressed_dir = os.path.join(destdir, "compressed_tif")
    os.makedirs(compressed_dir, exist_ok=True)
    for root, dirs, files in os.walk(sourcedir):
        if (root == sourcedir):
            tiffs = [f for f in files if not f.startswith(".")
                     and f.rpartition(".")[2].lower() == "tif"]
            if len(tiffs) == 0:
                print("  -- Nothing to do. --")
                continue
            for tif in tiffs:
                process_image_tif(os.path.join(sourcedir, tif), os.path.join(compressed_dir, tif))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("sourcedir", help="Directory containing TIF files.")
    parser.add_argument("-d", "--destdir",
                        help="Directory for output file. Defaults to sourcedir.")

    args = parser.parse_args()
    if args.destdir is None:
        args.destdir = args.sourcedir

    process_dir(args.sourcedir, args.destdir)
