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
    

# HOW TO MAKE A DATASET
here's how you can gather some decent datasets:
 
### WEB-SCRAPING:

1. GOOGLE IMAGE: here's a little [script](https://github.com/ArthasMenethil-A/CARLA/blob/main/other%20code/web_scraper.py) i've coded for web-scraping, all you need to do is to run the following command:
```
    python web_scraper.py
```

2. PARSEHUB: there is also the "parsehub" software you can download and use. (just google parsehub)

### CARLA:

![CARLA 9.5](https://i.ibb.co/bdkMCbK/1245568.png)

here's a little code i've written. all you have to do is run [spawn_vehicle](https://github.com/ArthasMenethil-A/Self-driving-car/blob/main/CARLA%20CODES/spawn_npc.py) to make a bunch of cars in CARLA and then run: [my code](https://github.com/ArthasMenethil-A/CARLA/blob/main/CARLA%20CODES/object_detection_dataset.py)
run these commands on cmd 

    py -3.7 spawn_vehicle.py -n 160 
    py -3.7 object_detection_dataset.py 

then in the window that appears push down "a" key to toggle autopilot and push "s" key to toggle save_data (which saves an image every 3 seconds to your hard drive)
i've commented quite a bit in my code so you can probably analyse quite easily to make changes as you would want 

# step 3: OBJECT DETECTION


![object detection](https://i.ibb.co/ZL8dW5S/detected-picture.jpg)

so here we can use **transfer learning** and fine tuning to build an accurate model that doesn't use a lot of computational power. 

- one way is to use this repository for [Yolo version 4](https://github.com/AlexeyAB/darknet) and follow the steps to make a fine tuned model 

- another way is to follow the steps from [this video](https://www.youtube.com/watch?v=tFNJGim3FXw&list=WL&index=1&t=1282s&ab_channel=NicholasRenotte)

to run my code for this run this command:
    ```
    py -3.7 spawn_vehicle.py -n 160 
    py -3.7 object_detection_dataset.py 
    ```
and then press 'd' key and that will save a picture to your default path that 

# OTHER RESOURCES

 1. in this step i'll introduce a good source for learning how object detection works: [object detection course](https://www.youtube.com/watch?v=yqkISICHH-U&ab_channel=NicholasRenotte)
  i've cleaned up and commented a bit on the source code of this course in this file so it might be a little easier to understand: [object detection file](https://github.com/ArthasMenethil-A/CARLA/blob/main/object%20detection/Training_model.ipynb)

