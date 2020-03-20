import os
import cv2


def convert_to_grayscale():
    for root, dirs, files in os.walk(from_directory):
        path = root.split(os.sep)
        for file in files:
            image = cv2.imread(root + "/" + file)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            cv2.imwrite(save_directory + file, gray)

if __name__ == "__main__":
    #filename = str(raw_input("test.png"))
    #img = Image.open("test.png")
    save_directory = "/home/arvid/PycharmProjects/exjobb/TESTDATA/Invalid/"
    from_directory = "/home/arvid/PycharmProjects/exjobb/TESTDATA/Invalid"
    convert_to_grayscale()
