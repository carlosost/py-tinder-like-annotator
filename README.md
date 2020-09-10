# py-tinder-like-annotator
A Tinder like Python script to annotate images for AI trainning

## The context

Every time I need to train my networks, I need to annotate the image training set.
There are 5 different groups, like:
 1. Real - real images, taken following my business constraints.
 2. Fake - fake images, taken trying to simulate my business constraints in order to fraud.
 3. Review - images I am not sure and need to review later.
 4. Discard - images that are fake/real, but are not good to consider in the training set.
 5. Threshold - images that will be automatically discarded to avoid overfitting.
 
## The approach

I decided to build a Tinder like app to automate the annotation process and increase productivity.
I am using the arrow keys of the keyboard to perform the "swipe" movements, like:
 - Real -> "swipe" right, using the right arrow key
 - Fake -> "swipe" left, using the left arrow key
 - Review -> "swipe" up, using the up arrow key
 - Discard -> "swipe" down, using the down arrow key

To avoid memory problems, since the training set use to be very large, the annotation is done by moving the file from it's current location, to a subfolder with the name of the chosen annotation. I mean, I don't copy the image to a new structure, but move it in place.

## Business particularities

There are some business rules, that may not make any sense in your context, but to make the code understanding easier, I will point them bellow.
 - The file structure has only two levels (root and subfolders) like:
     ```
     |---- root
     |----|---- subfolder
     |----|----|---- <score>_<file_name1>.png
     |----|----|---- <score>_<file_name2>.jpg
     |----|----|---- <score>_<file_name3>.png
     |----|----|---- <score>_<file_name4>.png
     |----|----|---- <score>_<file_name4>.jpg
     ```
     And after the annotation process, it can becomes like:
     ```
     |---- root
     |----|---- subfolder
     |----|----|---- discard
     |----|----|----|---- <score>_<file_name1>.png
     |----|----|---- fake
     |----|----|----|---- <score>_<file_name2>.jpg
     |----|----|---- real
     |----|----|----|---- <score>_<file_name3>.png
     |----|----|---- review
     |----|----|----|---- <score>_<file_name4>.png
     |----|----|---- threshold     
     |----|----|----|---- <score>_<file_name5>.jpg
     ```
  
  ## How to use it
  
  ``python3 annotate.py <image_root_directory_path> <threshold>``
  
  ## Work in progress
  
  I am working on a functionality to review the annotation process. Acctually it is done, but I have a lot of images to annotate righ now, and update this file took me a lot of time. I will post the code updates later, sorry!
