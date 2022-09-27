# SELF-DRIVING CAR
 this repository is dedicated to making a step by step guide to simulate a self-driving car in **CARLA** using deep learning models 
 if you want to see more of my stuff you can check out my [telegram channel](https://t.me/engineering_stuff_69)

# CARLA

![CARLA 9.5](https://i.ibb.co/ysPTLMq/Untitled.png)

- you can download the version of CARLA you need from this link: [CARLA WEBSITE](https://carla.org/)
- and this is a [good playlist](https://www.youtube.com/playlist?list=PLQVvvaa0QuDeI12McNQdnTlWz9XlCa0uo) on how to get started with CARLA plus he codes a bunch of stuff using RL. 

-- setup carla using the following steps --------------------------------------------------------------------------------------

1. **where to download**: go to [this link](https://github.com/carla-simulator/carla/blob/master/Docs/download.md) and get the *version 9.5 CARLA*

2. **what version of python is needed?**: according to the following path: <br /> `\CARLA\CARLA 9.5\PythonAPI\carla\dist\carla-0.9.5-py3.7-win-amd64.egg` <br /> you'll need the *python version 3.7 windows amd64* so download that from the official python website (depending on the version of carla you'll be using, this might be different)

3. **can you give me an example of running a code ?**: you should note the following 
    - don't forget to add the python 3.7 to your system path [check here if you don't know how to do that](https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))
    - you'll need to install pygame and numpy (and any other module you'll use) for your python       version 3.7
      ```
      py -3.7 -m pip install --upgrade pip
      py -3.7 -m pip install numpy pygame 
      ```
    - CARLA uses TCP ports 2000 and 2001 by defaul, you'll need to open them (or if it's occupied, empty them), [here's how to open tcp ports](https://www.firehousesoftware.com/webhelp/FH/Content/FHEnterprise/FHEnterpriseInstallationGuide/24_StaticPort.htm)
    - open CARLA and then go the path <br /> `C:\CARLA\CARLA 9.5\PythonAPI\examples` <br /> then open cmd in that path and run this command: 
      ```
      py -3.7 spawn_npc.py -n 80
      ```
      this will spawn 80 vehicles to your carla server
    

# DATASET
here's how you can gather some decent datasets:
 
### WEB-SCRAPING:

1. GOOGLE IMAGE: here's a little [script](https://github.com/ArthasMenethil-A/CARLA/blob/main/other%20code/web_scraper.py) i've coded for web-scraping, all you need to do is to download the script and run the following command in your cmd:
```
    python web_scraper.py
```

2. PARSEHUB: there is also the "parsehub" software you can download and use. (just google parsehub)

### CARLA:

![CARLA 9.5](https://i.ibb.co/bdkMCbK/1245568.png)

this is the script i've coded for gathering dataset from carla. all you have to do is run this file [spawn_vehicle](https://github.com/ArthasMenethil-A/Self-driving-car/blob/main/CARLA%20CODES/spawn_npc.py) to make a bunch of cars in CARLA and then run: [my code](https://github.com/ArthasMenethil-A/CARLA/blob/main/CARLA%20CODES/object_detection_dataset.py)
run these commands on cmd 

    py -3.7 spawn_vehicle.py -n 160 
    py -3.7 object_detection_dataset.py 

then in the window that appears push down "a" key to toggle autopilot and push "s" key to toggle save_data (which saves an image every 3 seconds to your hard drive)
i've commented quite a bit in my code so you can probably analyse quite easily to make changes as you would want 

# FINE-TUNING YOLO

![object detection](https://i.ibb.co/ZL8dW5S/detected-picture.jpg)

so here we can use **Transfer Learning and Fine Tuning** to build an accurate model that doesn't use a lot of computational power. 

if you want to see what does yolo looks while running on CARLA, you can run [my script](https://github.com/ArthasMenethil-A/CARLA/blob/main/CARLA%20CODES/object_detection_dataset.py) by entering the following commands on cmd:
    ```
    py -3.7 spawn_vehicle.py -n 160 
    py -3.7 object_detection_dataset.py 
    ```
and then press 'd' key and that will save a picture to your default path with applied object detection (real time object detection was really demanding with CARLA running)

## Steps for using yolo from scratch

1. make a virtual environment.

use the following command in cmd or terminal: 
```
    python -m venv virtual_environment_name
```
and then for activating this virtual environment you can use the following command in windows: 
```
    .\virtual_environment_name\scripts\activate
```
and the similar command for linux is:
```
    source virtual_environment_name/bin/activate
```

2. find the compatible versions of "torch" and "CUDA", you can check [this link](https://pytorch.org/get-started/locally/) for choosing the version of torch you want to use. then you can find the compatible version of cuda in [this link](https://developer.nvidia.com/cuda-toolkit-archive)

3. pip install numpy, jupyter notebook, pandas, cv2 in your virtual environment
- NOTE: when you run the command `pip install numpy` when your virtual environment it might say requirements already met or that it is now installed but when you want to import the numpy or use it anywhere, you get an error `no module named numpy` in that case you should use `pip install -U --force-reinstall numpy`
- NOTE: you might get permission error in your virtual environment. the way to resolve this is to go to the path `virtual_environment_name\pyvenv.cfg` and in that file, change the line `include-system-site-packages = false` to `include-system-site-packages = true`

4. add your virtual envirnment to ipykernel 
```
    python -m ipykernel install --user --name=virtual_environment_name
```

5. run the jupyter notebook script in [this file](https://github.com/ArthasMenethil-A/Self-driving-car/blob/main/object%20detection/Yolo_Fine_Tuning.ipynb)  

- follow the steps from [this video](https://www.youtube.com/watch?v=tFNJGim3FXw&list=WL&index=1&t=1282s&ab_channel=NicholasRenotte) if you didn't understand the steps

# DISTANCE APPROXIMATION
In order to determine the distance from our camera to a known object or marker we're going to utilize Traingle Similarity. 
$$F = \frac{P\times D}{W}$$
where:
- $W$ is width of a known object 
- $D$ = distance of the known object 
- $P$ = apparent width in pixels 
- $F$ = focal legnth

## Theory 
These are the steps to be taken for finding the distance approximation

### Step 1 (Reference Image)
Capture reference image: Measure the disntance from the object to the camera, capture a reference image and note down the measured distance.

### Step 2 (Measurement)
Measure the object width make sure that measurement units are kept for reference image and object width 

### Step 3 (Object Detection)
**INPUT: image
OUTPUT: face width**
this function will detect the object and return the object width in **pixel** values.

### Step 4 (Focal Length Finder)
**INPUT:** 
**- measured distance (unit meters)**
**- real width (unit meters)**
**- width in image (unit pixels)**
**OUTPUT: $Focal length = measured_distance\times image_width/real_width$**

### Step 5 (Distance Finder)
**INPUT:**
**- focal length (unit pixels)**
**- real width (unit meters)**
**- width in image (unit meters)**
**OUTPUT: $approximated distance = focal length \times real width/image width$**

## Python Implementation


## source
[Find distance from camera to object/marker using python and OpenCV](https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/)
[Real-time Distance Approximation using openCV-Python](https://www.geeksforgeeks.org/realtime-distance-estimation-using-opencv-python/)

# OTHER RESOURCES

1. in this step i'll introduce a good source for learning how object detection works: [object detection course](https://www.youtube.com/watch?v=yqkISICHH-U&ab_channel=NicholasRenotte)
i've cleaned up and commented a bit on the source code of this course in this file so it might be a little easier to understand: [object detection file](https://github.com/ArthasMenethil-A/CARLA/blob/main/object%20detection/Training_model.ipynb)

