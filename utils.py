import os
import random

from os.path import basename
from shutil import copyfile
from zipfile import ZipFile

def genlabels(labels):
    f = open("labels.txt","w+")

    f.write("__ignore__\r\n")
    f.write("_background_\r\n")
    for label in labels:
        f.write(label + "\r\n")

    f.close()

def splitdata(input_folder, output_folder, train_size = 0.8):
    if not os.path.exists(output_folder + '/train'):
        train_dir = output_folder + '/train'
        os.makedirs(train_dir)
    if not os.path.exists(output_folder + '/validation'):
        val_dir = output_folder + '/validation'
        os.makedirs(val_dir)

    train_counter = 0
    validation_counter = 0

    # Randomly assign an image to train or validation folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"): 
            filetypes = ["json", "png"]
            fileparts = filename.split('.')

            if random.uniform(0, 1) <= train_size:
                copyfile(os.path.join(input_folder, fileparts[0] + "." + filetypes[0]), os.path.join(train_dir, str(train_counter) + '.' + filetypes[0]))
                copyfile(os.path.join(input_folder, filename), os.path.join(train_dir, str(train_counter) + '.' + filetypes[1]))
                train_counter += 1
            else:
                copyfile(os.path.join(input_folder, fileparts[0] + "." + filetypes[0]), os.path.join(val_dir, str(validation_counter) + '.' + filetypes[0]))
                copyfile(os.path.join(input_folder, filename), os.path.join(val_dir, str(validation_counter) + '.' + filetypes[1]))
                validation_counter += 1

    print('Copied ' + str(train_counter) + ' images to ' + train_dir)
    print('Copied ' + str(validation_counter) + ' images to ' + val_dir)

def compress(folder_name, zip_name):
    with ZipFile(zip_name + ".zip", "w") as zipObj:
        for folderName, subfolders, filenames in os.walk(folder_name):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))