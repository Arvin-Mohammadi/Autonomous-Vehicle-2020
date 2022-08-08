# SELF-DRIVING CAR
 this repository is dedicated to making a step by step guide to simulate a self-driving car in **CARLA** using deep learning models 
 if you want to see more of my stuff you can check out my [telegram channel](https://t.me/engineering_stuff_69)

# step 1: CARLA SETUP

1. you can download the version of CARLA you need from this link: [CARLA WEBSITE](https://carla.org/)

2. and this is a [good playlist](https://www.youtube.com/playlist?list=PLQVvvaa0QuDeI12McNQdnTlWz9XlCa0uo) on how to get started with CARLA plus he codes a bunch of stuff using RL but i don't think RL is the right answer to this, i'm going to use CNN and image-processing to solve this problem.

# step 2: MAKING A DATASET
there are two ways to go about this issue, first is to gather dataset from internet (like google image, or kaggle, etc) 
the second step is to get the data using CARLA itself
 
## 1. INTERNET:

1. DATASET FROM DIFFERENT WEBSITES: <br />

- https://www.kaggle.com/datasets/brsdincer/vehicle-detection-image-set?resource=download    # cars <br />

- https://www.kaggle.com/datasets/dataclusterlabs/indian-vehicle-dataset                     # cars <br />

- https://www.kaggle.com/datasets/sshikamaru/car-object-detection                            # cars <br />

- https://www.kaggle.com/datasets/saravananchandran/pedestrian-detection-data-set            # pedestrian <br />

- https://www.kaggle.com/datasets/alincijov/penn-fudan                                       # pedestrian <br />

- https://www.kaggle.com/datasets/andrewmvd/dog-and-cat-detection                            # dog and cat <br />

- https://universe.roboflow.com/alec-hantson-student-howest-be/carla-izloa/dataset/20        # CARLA object detection <br />

- https://www.kaggle.com/datasets/alechantson/carladataset                                   # CARLA object detection <br />

   
2. GOOGLE IMAGE: here's a little code i've written for webscraping file attached: [web_scraper.py](https://github.com/ArthasMenethil-A/CARLA/blob/main/other%20code/web_scraper.py)

3. PARSEHUB: there is also the "parsehub" software you can download and use. (just google parsehub)

## 2. CARLA:
here's a little code i've written. all you have to do is run [spawn_vehicle]() to make a bunch of cars in CARLA and then run: [my code](https://github.com/ArthasMenethil-A/CARLA/blob/main/CARLA%20CODES/object_detection_dataset.py)
run these commands on cmd 

    py -3.7 spawn_vehicle.py -n 160 
    py -3.7 object_detection_dataset.py 

then in the window that appears push down "a" key to toggle autopilot and push "s" key to toggle save_data (which saves an image every 3 seconds to your hard drive)
i've commented quite a bit in my code so you can probably analyse quite easily to make changes as you would want 

# step 3: MODEL TRAINING

so here we can use transfer learning and fine tuning to build an accurate model that doesn't use a lot of computational power. i'll be using YOLO plus the COCO dataset to detect the following 
1. pedestrian  
2. bike
3. truck
4. car 
5. dog
6. cat <br />
these 6 will be our labels for the object detection model (softmax layer)
[Yolo version 4](https://github.com/AlexeyAB/darknet)
[COCO dataset](https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/)


# OTHER RESOURCES

 1. in this step i'll introduce a good source for learning how object detection works: [object detection course](https://www.youtube.com/watch?v=yqkISICHH-U&ab_channel=NicholasRenotte)
  i've cleaned up and commented a bit on the source code of this course in this file so it might be a little easier to understand: [object detection file](https://github.com/ArthasMenethil-A/CARLA/blob/main/object%20detection/Training_model.ipynb)

