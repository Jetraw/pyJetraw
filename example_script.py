import os
import tifffile
import jetraw
from jetraw.tiff_writer import TiffWriter
from jetraw.tiff_reader import TiffReader
import numpy as np
import pathlib


def process_image_tif(input_filename):
    # READ compressed images from disk
    # Option A: READ using imread function (whole stack)
    read_all_pages = jetraw.imread(input_filename)
    # Option B: READ using imread function (range)
    read_range_pages = jetraw.imread(input_filename, [3, 4, 7, 1, 6])
    # Option C: READ using imread function (single page)
    read_single_page = jetraw.imread(input_filename, 5)

    # write uncompressed image into disk as TIFF
    path = pathlib.Path(__file__).parent.absolute()
    tifffile.imwrite(os.path.join(path, "read_all_pages.tif"), read_all_pages)
    tifffile.imwrite(os.path.join(path, "read_range_pages.tif"), read_range_pages)
    tifffile.imwrite(os.path.join(path, "read_single_page.tif"), read_single_page)

    with TiffReader(input_filename) as reader:
        for page in range(reader.pages):
            image = reader.read(page)
            tifffile.imwrite(os.path.join(path, "image_") + str(page) + ".tif", image)

    # WRITE compressed image to disk (remember that uncompressed images are already dpcore prepared)
    # Option A: using jetraw Module
    compressed_filename = pathlib.Path(__file__).parent.absolute()
    jetraw.imwrite(str(compressed_filename.joinpath("test_jetraw_A.p.tif")), read_all_pages, "JetRaw compressed image")

    # Option B: using a writer object
    with TiffWriter(str(compressed_filename.joinpath("test_jetraw_B.p.tif")), "JetRaw compressed image") \
            as jetraw_writer:
        for page in range(read_all_pages.shape[0]):
            jetraw_writer.write(read_all_pages[page, :, :])


def process_dir(sourcedir):
    assert os.path.isdir(sourcedir), "Source directory does not exist."
    for root, dirs, files in os.walk(sourcedir):
        if root == sourcedir:
            tiffs = [f for f in files if not f.startswith(".")
                     and f.rpartition(".")[2].lower() == "tif"]
            if len(tiffs) == 0:
                print("  -- Nothing to do. --")
                continue
            for tif in tiffs:
                process_image_tif(os.path.join(sourcedir, tif))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("sourcedir", help="Directory containing TIF files.")
    args = parser.parse_args()
    # run processing pipeline
    process_dir(args.sourcedir)