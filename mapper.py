import os
import shutil

directory = '/home/arvid/PycharmProjects/exjobb/data/'
dir_list = []


def find(path):

    for root, dirs, files in os.walk(path):
        path = root.split(os.sep)
        for file in files:
            tmp = file.split("_")
            if len(tmp) == 3 and tmp[0] != ".":
                try:
                    if not tmp[1] in dir_list:
                        dir_list.append(tmp[1])
                        # Create target Directory
                        os.mkdir("/home/arvid/PycharmProjects/exjobb/data/" + tmp[1])
                        print("Directory ", tmp[1], " Created ")
                except FileExistsError:
                    print("Directory already exists")
                    pass
            for s in dir_list:
                if s in file:
                    try:
                        if not os.path.exists(directory + s + "/" + file):
                            shutil.copy(root + "/" + file, directory + s)
                    except Exception:
                        print("hej")
                        pass


if __name__ == "__main__":
    find("/home/arvid/Downloads/dataskriven underskrift/api")