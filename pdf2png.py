# PDF TO IMAGE CONVERSION
# IMPORT LIBRARIES
import pdf2image
from PIL import Image
import time
import PyPDF2
import os
import shutil

# DECLARE CONSTANTS
DPI = 200
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'png'
USERPWD = None
USE_CROPBOX = False
STRICT = False
save_directory = "/home/arvid/PycharmProjects/exjobb/pngdata/fel signatur"


def convert(path_to_pdfs):
    dir_list = []
    print(path_to_pdfs)
    saved_name = ""

    for root, dirs, files in os.walk(path_to_pdfs):
        path = root.split(os.sep)
        for file in files:
            tmp = file.split("_")
            if len(tmp) == 3 and tmp[0] != ".":
                try:
                    if not tmp[1] in dir_list:

                        dir_list.append(tmp[1])
                        # Create target Directory
                        os.mkdir("/home/arvid/PycharmProjects/exjobb/pngdata/" + str(tmp[1]))
                        print("Directory ", tmp[1], " Created ")
                except FileExistsError:
                    print("Directory already exists")
                    pass
            for directory in dir_list:
                if directory in file:
                    try:
                        test = file.split(".")
                        filename = test[0]
                        saved_name = "/home/arvid/PycharmProjects/exjobb/pngdata/" + str(directory) + "/" + str(filename) + ".png"
                        #print("Filename: " + filename)
                        if not os.path.exists(saved_name):
                            pil_images = pdf2image.convert_from_path(path_to_pdfs + "/" + directory + "/" + file, dpi=DPI,
                                                                     output_folder=None, first_page=FIRST_PAGE,
                                                                     last_page=LAST_PAGE, fmt=FORMAT, userpw=USERPWD,
                                                                     use_cropbox=USE_CROPBOX, strict=STRICT)

                            pil_images[0].save(saved_name)

                    except Exception as e:
                        print(e)
                        pass


def convert2(path_to_pdfs):
    for root, dirs, files in os.walk(path_to_pdfs):
        path = root.split(os.sep)
        for file in files:

            try:
                filename = os.path.splitext(file)[0]
                saved_name = "/home/arvid/PycharmProjects/exjobb/pngdata/fel signatur/" + str(filename) + ".png"
                # print("Filename: " + filename)
                if not os.path.exists(saved_name):
                    pil_images = pdf2image.convert_from_path(path_to_pdfs + "/" + file,
                                                             dpi=DPI,
                                                             output_folder=None, first_page=FIRST_PAGE,
                                                             last_page=LAST_PAGE, fmt=FORMAT, userpw=USERPWD,
                                                             use_cropbox=USE_CROPBOX, strict=STRICT)

                    pil_images[0].save(saved_name)

            except Exception as e:
                print(e)
                pass


if __name__ == "__main__":
    #convert("/home/arvid/PycharmProjects/exjobb/data/Fel signatur")
    convert2("/home/arvid/PycharmProjects/exjobb/data/Fel signatur")

