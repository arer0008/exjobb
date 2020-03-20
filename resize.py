from PIL import Image, ImageOps
import os

from_directory = "testcrops"

def resize():
    max_width = 0
    max_height = 0
    for filename in os.listdir(from_directory):
        if filename.endswith(".png"):

            original_image = Image.open("testcrops/" + filename)

            width, height = original_image.size
            """
            if width > 1000:
                print("File: " + filename)
            if width > max_width:
                max_width = width
            if height > max_height:
                max_height = height
            """
            size2 = (1000, 150)

            print(original_image.size)
            fit_and_resized_image = ImageOps.fit(original_image, size2, Image.ANTIALIAS)

            fit_and_resized_image.save("testcrops/test/" + filename, "png")

    print("Maxwidth: " + str(max_width))
    print("Maxheight: " + str(max_height))


if __name__ == "__main__":
    resize()
