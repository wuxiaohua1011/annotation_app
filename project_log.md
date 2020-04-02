# Project Log

#### March 13, 2020
- Established the goal that we will have a fully functioning system by April 6, 2020
- ** Please note that below content have been moved to internal Google doc
- [ ] Have a full system with the following flow of the program: `Welcome screen/ Scene selecting` `->` `Layout Segmentation` `->` `Plane fitting/annotation` `->` `save` `->` `exit`
    - [ ] `Welcome Screen that directs to remote download screen and annotation tool`
        - @Chetana, please write down the subtasks
    - [ ] `Layout Secmentation(The current Annotation Tool)`
    - [ ] `Plane fitting screen`
        - Please see Task 3
    - [ ] `Local saving functionality and implement testing for the entire app`
        - @Michael
- [ ] Be able to read pointcloud from remote server and write annotation as json file to remote server when done
    - [ ] `Download Functionality and screen`
    - [ ] `Upload data screen and functionality`
        - @Star&Bernard please write down the subtasks
- [ ] Finish the Layout annotation and its UX interaction
    - [ ] Plane fitting for all the segments
    - [ ] getting all the segments that should intersect
    - [ ] generating the lines and corners that comprise the wireframe for the scene
    - [ ] saving it to file
    - @Joy&Chris, please write more about this task


#### Feb 13, 2020
1. Moved the project to MVC model
2. Started Github Action of Pre-commit to lint code
3. start to implement plane-fitting algorithm
4. server started. Based in Berkeley OCF




#### Dec 12, 2019
1. Floodfilling and boundingbox implemented
2. Saving and loading function implemented


Problems:
1. Single point floodfilling is not working
2. Loading erroreous files should not crash the program
      a. ex: load a json segment, click the LOAD button, click on a wrong file
3. bounding box should ALWAYS show when in bounding box mode
4. Clicking on save button changes the camera angle


Todo:
1. Writing unittest for the interface
2. Connecting to server to download data files
3. implement the DELETE button to delete a single json entry on press
4. on double click json segment, render result on lower panel
5. Unhighlight stuff using a button


#### Nov 24, 2019
    1. Create Server such that data can be transferred from another computer
        - request to purchase a domain name, for hosting data
        - http://www.science.smith.edu/dftwiki/index.php/PyQt5_Tutorial:_A_Window_Application_with_File_IO#Create_A_Window_UI

    2. re-implement rendering function so that it is rendering mesh instead of point cloud


## Ryan's Notes
### HOWTO Remove Elements from the VisPy Canvas
Some of the operations in the application are now able to remove (or "undraw") specific objects in the 3D canvas, without needing to clear and reset everything. To accomplish this, the instance of the desired object must be accessed from within the canvas's children. Then, the parent of that object must be set to 'None', breaking its connection to the VisPy framework.

An example of this can be seen in the *start_bbox* function within the **main.py** file. The desired objects are collected from the VisPy's view instance:
```
self.bbox_vispy = [self.ui_elements.upperScene.view.children[0].children[i] for i in range(self.children_before_bbox, len(self.ui_elements.upperScene.view.children[0].children))]
```
<br/>The construction of this list is arguably a good and convenient method to keep track of objects, as the list contains references to the actual instances within this VisPy view instance.

To remove the desired objects from the scene, a good example is in the *destroy_bbox** function. In this function, the *self.bbox_vispy* list is iterated upon, and the parents of each of the referenced objects are set to *None*:
```
for vispy_line in self.bbox_vispy:
        vispy_line.parent = None
```

### BBOX
#### Order of Operations
It is important to know that the BBOX class works by accumulating all operations for *translation*, *scale*, *rotation*, **each** in separate lists. They are only combined during any call for viewing the outline or for cropping (it is never permanently saved anywhere), in which the original positions of the bounding box's endpoints are matrix multiplied by the strict ordering of TRANSLATE * ROTATION * SCALE * point, for each point.
#### Misc
The Bounding Box interface currently uses the QDoubleSpinBox class to allow for manipulation of the boundaries before cropping. In the future, it would be ideal to implement a CAD-like system of 3 arrows/arcs within the 3D environment to allow for intuitive manipulation of the bounding box.
