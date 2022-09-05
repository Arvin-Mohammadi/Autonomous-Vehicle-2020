
# =================================================================================================
# -- IMPORT ---------------------------------------------------------------------------------------
# =================================================================================================

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import requests
import colorama 
from colorama import Fore, Back, Style

colorama.init()

# =================================================================================================
# -- LIST OF URLS ---------------------------------------------------------------------------------
# =================================================================================================

def fetch_image_urls(query: str, max_link_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):

    # scroll to the end of the page 
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    # make the url with the search term
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page 
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    # looping over in page to find images 
    while image_count < max_link_to_fetch:

        scroll_to_end(wd)

        # get all image thumbnail results 
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        # clicking on the images and waiting till it loads 
        for img in thumbnail_results[results_start:number_results]:
            try: 
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue 

        # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))


            image_count = len(image_urls)

            if len(image_urls) >= max_link_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else: 
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            load_more_button = wd.find_elements_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

# =================================================================================================
# --  ---------------------------------------------------------------------------------------------
# =================================================================================================

def persist_image(folder_path: str, url: str, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")


    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()

        print(f"SUCCESS - saved {url} - as {folder_path}")

    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

# =================================================================================================
# -- DOWNLOADING THE IMAGES -----------------------------------------------------------------------
# =================================================================================================

def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=5): 

    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=15)

    print("this is res")
    print(type(res))
    print(res)

    counter = 0 
    
    file = open(target_folder + '\\urls.txt', 'a')
        
    for elem in res:
        file.write(str(elem) + '\n')

    for elem in res: 
        print("this is elem")
        print(type(elem))
        print(elem)
        persist_image(target_folder, elem, counter)
        counter += 1 


# =================================================================================================
# -- LOOP -----------------------------------------------------------------------
# =================================================================================================

def loop():
    
    DRIVER_PATH = 'D:\\chromedriver.exe'
    
    # looping over until input "exit" recieved by user
    while True: 
        print(Fore.GREEN + "\nexit - quit the script", "s search--term - starts searching the web" + Fore.WHITE, sep='\n')

        input_string = input("Input command: ") # input command

        if input_string == "exit":          # in case of entering "exit", exits the scripts
            break

        elif input_string[0] == "s":        # in case of entering "s search-term", initialize the search and download script
            search_term = input_string[2:]
            try:
                N_IMAGES = int(input('Number of Images: '))
            except:
                print(Fore.RED + "Input must be an integer" + Fore.WHITE)
                continue
            search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=N_IMAGES)
        
        else:                               # in any other case of input, goes back to the start of the loop
            pass

        

# =================================================================================================
# -- DOWNLOADING THE IMAGES -----------------------------------------------------------------------
# =================================================================================================

loop()