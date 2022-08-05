# CARLA
 this repository is dedicated to making a step by step guide to simulate a self-driving car in CARLA using deep learning models 
 if you want to see more of my stuff you can check out this link:
 https://t.me/engineering_stuff_69

# step 1: CARLA SETUP

 1. you can download the version of CARLA you need from this link: 
 https://carla.org/

 2. and this is a good playlist on how to get started with CARLA plus he codes a bunch of stuff using RL but i don't think RL is the right answer to this, i'm going to use CNN and image-processing to solve this problem
 https://www.youtube.com/playlist?list=PLQVvvaa0QuDeI12McNQdnTlWz9XlCa0uo

# step 2: MAKING A DATASET
 there are two ways to go about this issue, first is to gather dataset from internet (like google image, or kaggle, etc) 
 the second step is to get the data using CARLA itself
 
 ## 1. INTERNET:
  1. DATASET FROM DIFFERENT WEBSITES:

   https://www.kaggle.com/datasets/brsdincer/vehicle-detection-image-set?resource=download    # cars

   https://www.kaggle.com/datasets/dataclusterlabs/indian-vehicle-dataset                     # cars

   https://www.kaggle.com/datasets/sshikamaru/car-object-detection                            # cars

   https://www.kaggle.com/datasets/saravananchandran/pedestrian-detection-data-set            # pedestrian

   https://www.kaggle.com/datasets/alincijov/penn-fudan                                       # pedestrian

   https://www.kaggle.com/datasets/andrewmvd/dog-and-cat-detection                            # dog and cat

   https://universe.roboflow.com/alec-hantson-student-howest-be/carla-izloa/dataset/20        # CARLA object detection 

   https://www.kaggle.com/datasets/alechantson/carladataset                                   # CARLA object detection
   
  2. GOOGLE IMAGE: here's a little code i've written for webscraping file attached ---> [web_scraper.py](https://github.com/ArthasMenethil-A/CARLA/blob/main/web_scraper.py)
   
  3.PARSEHUB: there is also the "parsehub" software you can download and use. (just google parsehub)

# step 2: IMAGE-PROCESSING (OBJECT DETECTION)

 1. in this step i'll introduce a good source for learning how object detection works:
 https://www.youtube.com/watch?v=yqkISICHH-U&ab_channel=NicholasRenotte

 2. i cleaned up the object detection code a little bit you can check the jupyter notebook files --> [object detection](https://github.com/ArthasMenethil-A/CARLA/tree/main/object%20detection)

# step 4: MODEL TRAINING

 1. use the Image_preprocessing.ipynb file to label the data

 2. in this step we need to use the [Training_model.ipynb](https://github.com/ArthasMenethil-A/CARLA/blob/main/object%20detection/Training_model.ipynb) file to train and evaluate the model

