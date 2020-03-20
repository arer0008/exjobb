import pytesseract
from pytesseract import pytesseract
import cv2
import os


from_directory = "/home/arvid/PycharmProjects/exjobb/pngdata/fel signatur"
save_failed = "Manual review/"


def crop_signature2():
    h = 0
    for root, dirs, files in os.walk(from_directory):
        path = root.split(os.sep)
        for file in files:
            save_directory = "/home/arvid/PycharmProjects/exjobb/cropped/felaktiga/"

            image = cv2.imread(root + "/" + file)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            extension = os.path.splitext(file)[1]
            if extension == '.png':
                test = pytesseract.image_to_osd(image)
                rotation = int(test.split('\n')[1].split(':')[1])
                if rotation == 180:
                    image = cv2.rotate(image, cv2.ROTATE_180)
                elif rotation == 90:
                    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif rotation == 270:
                    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

                test, image = cv2.threshold(image, 150, 255, cv2.THRESH_TOZERO)
                data = pytesseract.image_to_string(image)
                height = image.shape[0]
                width = image.shape[1]
                found = find_all(data, image, height, width, file, save_directory)

                if found == 0:
                    h = h + 1
                    cv2.imwrite(save_failed + "/" + "felaktiga/" + file, image)
                    f = open(save_failed + "felaktiga/" + str(file.split('.')[0]) + ".txt", "w+")
                    f.write(data)
                    f.close()

    print("Antal där inget ord hittades: " + str(h))


def crop_signature():

    h = 0
    for root, dirs, files in os.walk(from_directory):
        path = root.split(os.sep)
        for file in files:
            tmp = file.split("_")
            if len(tmp) != 3:
                tmp = file.split("-")
            save_directory = "/home/arvid/PycharmProjects/exjobb/cropped/" + str(tmp[1]) + "/"
            if len(tmp) == 3 and tmp[0] != ".":
                try:
                    #if not tmp[1] in dir_list:
                    if not os.path.exists("/home/arvid/PycharmProjects/exjobb/cropped/" + str(tmp[1])):
                        # Create target Directory
                        os.mkdir("/home/arvid/PycharmProjects/exjobb/cropped/" + str(tmp[1]))
                        print("Directory " + tmp[1] + " Created")
                except FileExistsError:
                    print("Directory already exists")
                    pass

            image = cv2.imread(root + "/" + file)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            extension = os.path.splitext(file)[1]
            if extension == '.png':
                test = pytesseract.image_to_osd(image)
                rotation = int(test.split('\n')[1].split(':')[1])
                if rotation == 180:
                    image = cv2.rotate(image, cv2.ROTATE_180)
                elif rotation == 90:
                    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif rotation == 270:
                    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

                test, image = cv2.threshold(image, 150, 255, cv2.THRESH_TOZERO)
                data = pytesseract.image_to_string(image)
                height = image.shape[0]
                width = image.shape[1]
                found = find_all(data, image, height, width, file, save_directory)

                if found == 0:
                    h = h+1
                    if not os.path.exists("/home/arvid/PycharmProjects/exjobb/Manual review/" + str(tmp[1])):
                        # Create target Directory
                        os.mkdir("/home/arvid/PycharmProjects/exjobb/Manual review/" + str(tmp[1]))
                    cv2.imwrite(save_failed + "/" + str(tmp[1]) + "/" + file, image)
                    f = open(save_failed + str(tmp[1]) + "/" + str(file.split('.')[0]) + ".txt", "w+")
                    f.write(data)
                    f.close()

    print("Antal där inget ord hittades: " + str(h))


def find_all(data, image, height, width, file, save_directory):

    if data.find("Namnt") != -1:
        find_namnteckning(image, height, width, file, save_directory)
    elif data.find("Ort") != -1:
        find_ort(image, height, width, file, save_directory)
    elif data.find("Namn:") != -1:
        find_namn(image, height, width, file, save_directory)
    elif data.find("Namnf") != -1:
        find_namnfortydligande(image, height, width, file, save_directory)
    elif data.find("Ansvari") != -1:
        find_ansvarig(image, height, width, file, save_directory)
    elif data.find("Datu") != -1:
        find_datum(image, height, width, file, save_directory)
    elif data.find("Signatur") != -1:
        find_signature(image, height, width, file, save_directory)
    elif data.find("Place") != -1:
        find_place(image, height, width, file, save_directory)
    elif data.find("Name") != -1:
        find_name(image, height, width, file, save_directory)
    else:
        return 0
    return 1


def find_signature(image, height, width, file, save_directory):

    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'S' and new_data[i + 1][0] == 'i' and new_data[i + 2][0] == 'g' \
                and new_data[i + 3][0] == 'n' and new_data[i + 4][0] == 'a':
            print(new_data[i])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            starty = int(height - y - 15)
            sluty = int(height - y + (0.04 * height))
            startx = int(x)
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "CroppedS-" + file, im1)
            break


def find_place(image, height, width, file, save_directory):

    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'P' and new_data[i + 1][0] == 'l' and new_data[i + 2][0] == 'a' \
                and new_data[i + 3][0] == 'c' and new_data[i + 4][0] == 'e':
            print(new_data[i])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            starty = int(height - y + (0.025 * height))
            sluty = int(height - y + (0.09 * height))
            startx = int(x)
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "CroppedP-" + file, im1)
            break


def find_name(image, height, width, file, save_directory):
    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'N' and new_data[i + 1][0] == 'a' and new_data[i + 2][0] == 'm' \
                and new_data[i + 3][0] == 'e':
            print(new_data[i + 4])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            starty = int(height - y - (0.08 * height))
            sluty = int(height - y - (0.01 * height))
            startx = int(x)
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "CroppedNa-" + file, im1)
            break


def find_namnteckning(image, height, width, file, save_directory):

    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'N' and new_data[i + 1][0] == 'a' and new_data[i + 2][0] == 'm' \
                and new_data[i + 3][0] == 'n' and new_data[i + 4][0] == 't' and new_data[i + 5][0] == 'e':
            print(new_data[i])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            starty = int(height - y - 15)
            sluty = int(height - y + (0.04 * height))
            startx = int(x)
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "CroppedN-" + file, im1)
            break


def find_ort(image, height, width, file, save_directory):

    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'O' and new_data[i + 1][0] == 'r' and new_data[i + 2][0] == 't':
            print(new_data[i])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            starty = int(height - y + (0.025 * height))
            sluty = int(height - y + (0.09 * height))
            startx = int(x)
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "CroppedO-" + file, im1)
            break


def find_namnfortydligande(image, height, width, file, save_directory):

    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'N' and new_data[i + 1][0] == 'a' and new_data[i + 2][0] == 'm' \
                and new_data[i + 3][0] == 'n' and new_data[i + 4][0] == 'f':
            print(new_data[i + 4])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            starty = int(height - y - (0.07 * height))
            sluty = int(height - y - (0.01 * height))
            startx = int(x)
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "CroppedF-" + file, im1)
            break


def find_namn(image, height, width, file, save_directory):
    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'N' and new_data[i + 1][0] == 'a' and new_data[i + 2][0] == 'm' \
                and new_data[i + 3][0] == 'n' and new_data[i + 4][0] == ':':
            print(new_data[i + 4])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            starty = int(height - y - (0.07 * height))
            sluty = int(height - y - (0.01 * height))
            startx = int(x)
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "Cropped:-" + file, im1)
            break


def find_ansvarig(image, height, width, file, save_directory):
    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'A' and new_data[i + 1][0] == 'n' and new_data[i + 2][0] == 's' \
                and new_data[i + 3][0] == 'v':
            print(new_data[i])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])
            if x > 400:
                break
            starty = int(height - y - (0.135 * height))
            sluty = int(height - y - (0.07 * height))
            startx = x
            slutx = int(x + (0.55 * width))
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x
            cv2.imwrite(save_directory + "CroppedA-" + file, im1)
            break


def find_datum(image, height, width, file, save_directory):
    boxes = pytesseract.image_to_boxes(image)
    new_data = boxes.split('\n')
    for i in range(len(new_data)):
        if new_data[i][0] == 'D' and new_data[i + 1][0] == 'a' and new_data[i + 2][0] == 't' \
                and new_data[i + 3][0] == 'u':
            print(new_data[i])
            coords = new_data[i].split(' ')
            x = int(coords[1])
            y = int(coords[2])

            starty = int(height - y + (0.03 * height))
            sluty = int(height - y + (0.1 * height))
            startx = int(x - (0.5 * width))
            if startx < 0:
                startx = 0
            slutx = int(0.55 * width)
            im1 = image[starty:sluty, startx:slutx]  # Start y, slut y, start x, slut x

            cv2.imwrite(save_directory + "CroppedD-" + file, im1)
            break


if __name__ == "__main__":
    #crop_signature()
    crop_signature2()
