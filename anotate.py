import os
import sys
import shutil
import tkinter as tk
from PIL import Image, ImageTk

import multiprocessing

class App:
    def __init__(self, root_path, threshold, tkWindow=tk.Tk()):

        # Create the main window
        self.tkWindow = tkWindow
        self.tkWindow.title("TinderLike Anotator")
        self.tkWindow.geometry("480x640")

        # Create a label to use as image holder
        self.image_label = tk.Label(self.tkWindow)
        self.image_label.pack()

        # Bind keyboard arrows to simulate swipes
        self.tkWindow.bind("<Left>", self.swipe_left)
        self.tkWindow.bind("<Right>", self.swipe_right)
        self.tkWindow.bind("<Up>", self.swipe_up)
        self.tkWindow.bind("<Down>", self.swipe_down)

        # Bind keyboard escape to stop annotation
        self.tkWindow.bind("q", self.close)
        self.tkWindow.bind("<Escape>", self.close)
        self.is_active = True
        
        # "Trigger" to hold directories walk through
        self.next_img = tk.IntVar()

        # Reserved folder names to move the images after swipe.
        # Useful to avoid re-annotate images in case of stop/restart
        # annotation proccess
        anotation_folders = ['fake', 'real', 'discard', 'review', 'threshold']

        # Traverse the root folder looking for images
        for folder, _, files in os.walk(root_path):

            # Test if the image was already annotated
            if any(fd in folder for fd in anotation_folders):
                print(folder + ' - already annotated')
                continue

            for filename in files:
                # "global" variables to be used by swipe functions
                self.img_dir = folder
                self.img_name = filename
                self.img_path = os.path.join(folder, filename)

                # Test if file is an image
                file_type = os.path.splitext(filename)[1]
                if file_type == '.jpg' or file_type == '.png':
                    file_score = int(filename.split("_")[0])

                    # Test if the image score is bellow a cut threshold
                    if file_score < threshold:
                        print(filename + ' - accepted')
                        self.load_image()
                        self.tkWindow.wait_variable(self.next_img)
                    else:
                        print(filename + ' - above threshold')
                        self.throw_away()
                else:
                    print(filename + ' - not an image')
                    self.throw_away()

            print('No more images at the directory ' + folder)
        
        print('No more images to annotate.') 
        self.close()

    def load_image(self):
        # Update the image
        self.fig_image = ImageTk.PhotoImage(Image.open(self.img_path))
        # Update image holder
        self.image_label.config(image=self.fig_image)
        # Set "trigger" to wait for user swipe 
        self.next_img.set(0)

    def swipe_left(self, event):
        try:
            # Move image to correct directory
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'fake', self.img_name))
        except FileNotFoundError:
            os.mkdir(os.path.join(self.img_dir, 'fake'))
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'fake', self.img_name))
        # Set "trigger" to load next image
        self.next_img.set(1)

    def swipe_right(self, event):
        try:
            # Move image to correct directory
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'real', self.img_name))
        except FileNotFoundError:
            os.mkdir(os.path.join(self.img_dir, 'real'))
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'real', self.img_name))
        # Set "trigger" to load next image
        self.next_img.set(1)

    def swipe_up(self, event):
        try:
            # Move image to correct directory
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'review', self.img_name))
        except FileNotFoundError:
            os.mkdir(os.path.join(self.img_dir, 'review'))
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'review', self.img_name))
        # Set "trigger" to load next image
        self.next_img.set(1)

    def swipe_down(self, event):
        try:
            # Move image to correct directory
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'discard', self.img_name))
        except FileNotFoundError:
            os.mkdir(os.path.join(self.img_dir, 'discard'))
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'discard', self.img_name))
        self.next_img.set(1)

    def throw_away(self):
        try:
            # Move image to correct directory
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'threshold', self.img_name))
        except FileNotFoundError:
            os.mkdir(os.path.join(self.img_dir, 'threshold'))
            shutil.move(
                self.img_path,
                os.path.join(self.img_dir, 'threshold', self.img_name))
        # Set "trigger" to load next image
        self.next_img.set(1)

    def close(self, *args):
        print('GUI closed...')
        self.tkWindow.quit()
        self.is_active = False

    def is_closed(self):
        return not self.is_active

    def mainloop(self):
        self.tkWindow.mainloop()
        print('mainloop closed...')

if __name__ == '__main__':

    # First argument is the root directory
    imgs_root = sys.argv[1]

    # Second argument is the threshold to cut
    threshold = int(sys.argv[2])

    app = App(imgs_root, threshold)
    app.mainloop()