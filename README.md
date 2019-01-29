# visualProtractor

This program is designed to simulate a simple protractor.

When running:
1. A window of the video stream will pop up, the user must select an item by clicking on it.
2. At this point 2 new windows will pop up, the first is the mask being applied to detect the object, the second is a bounding box being drawn around the object.
3. When the user is satisfied with the initial position of the object they can press "r" to set this as the position to base all future measurements from.
4. The user can now rotate the object along the z access and read the change in angle in the console.


Things to keep in mind:
1. The object detection can be finicky depending on the lighting and camera, I recommend you use a simple shape on a different background (blue tape on a white background for instance).
2. The program is not rotation invariant and currently only works in one direction (more directions coming in the future).
3. The program is not necessarily shift invariant depending on the camera lens being used.
4. The program will default to the first camera it detects, if you wish to switch cameras it can easily be done by modifying line 180 in the code.
5. It is recommended that the user keep both the camera and the object being detected as still as possible (I used a camera jig) for the most accurate results.
6. An angle of -1 means that the object has either moved too much or the bounding box has been set improperly, to fix the user can reselect their bounding box by clicking on the initial video stream and press "r" at any time.
