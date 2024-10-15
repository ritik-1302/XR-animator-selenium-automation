import os
import time
import math


import cv2

from flask import Flask
from flask import request,send_from_directory

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)



@app.route('/vrm_animator', methods=['POST'])
def vrm_animator():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    


    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    video_path = os.path.join(os.getcwd(),os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    data=cv2.VideoCapture(video_path)
    video_duration=math.ceil(data.get(cv2.CAP_PROP_FRAME_COUNT)/data.get(cv2.CAP_PROP_FPS))
    options = ChromeOptions()
    options.add_experimental_option("prefs", {
    "download.default_directory": os.path.join(os.getcwd(),app.config['DOWNLOAD_FOLDER']),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options=options)
    action=webdriver.ActionChains(driver)
    
    try:
        driver.get('https://ritik-1302.github.io/XR_Animator.html')# Replace with your URL
        driver.maximize_window()

    #------------------- Opening Page---------------------------------#
        time.sleep(2)
        
        #file input trigger
        file_input_trigger_button=driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[4]')
        action.move_to_element(file_input_trigger_button).perform()
        file_input_trigger_button.click()
        
        #sending files
        driver.switch_to.frame(driver.find_element(By.ID, 'Idialog'))
        file_input_button=driver.find_element(By.ID,'LBFF_browse')
        file_input_button.send_keys(os.path.join(os.getcwd(),'model_new.vrm'))
        time.sleep(2)
        
        #sumbit button
        ok_button=driver.find_element(By.XPATH, '/html/body/div/div/span[2]/input[1]')
        action.move_to_element(ok_button).perform()
        ok_button.click()
        
        time.sleep(2)
        
        # start button
        driver.switch_to.default_content()
        start_button= driver.find_element(By.ID, 'LMMD_StartButton')
        start_button.click()
        time.sleep(10)
        #------------------- Opening Page---------------------------------#
        
        
        #----------------------- XR-Animator Loading Video------------------------------#
        file_input_trigger_button=driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[4]')
        action.move_to_element(file_input_trigger_button).perform()
        file_input_trigger_button.click()
        
        #sending files
        driver.switch_to.frame(driver.find_element(By.ID, 'Idialog'))
        file_input_button=driver.find_element(By.ID,'LBFF_browse')
        file_input_button.send_keys(video_path)
        time.sleep(2)
        
        #sumbit button
        ok_button=driver.find_element(By.XPATH, '/html/body/div/div/span[2]/input[1]')
        action.move_to_element(ok_button).perform()
        ok_button.click()
        driver.switch_to.default_content()
        
        time.sleep(2)
        #----------------------- XR-Animator Loading Video------------------------------#
        
        
        #----------------------- XR-Animator MoCap Record------------------------------#
        mocap_record_button=driver.find_element(By.ID, 'Ldungeon_inventory_item0')
        action.move_to_element(mocap_record_button).double_click().perform()
        time.sleep(1)
        action.send_keys(Keys.NUMPAD2).perform()
        action.send_keys("x").perform()
        action.send_keys(Keys.F9).perform()
        time.sleep(video_duration)
        action.send_keys(Keys.F10).perform()
        #----------------------- XR-Animator MoCap Record------------------------------#

        

        time.sleep(5)
        for filename in os.listdir(os.path.join(os.getcwd(), app.config['DOWNLOAD_FOLDER'])):
            return send_from_directory(os.path.join(os.getcwd(), app.config['DOWNLOAD_FOLDER']), filename)

    finally:
        
        driver.quit()
        os.remove(video_path)
        for filename in os.listdir(os.path.join(os.getcwd(), app.config['DOWNLOAD_FOLDER'])):
            os.remove(os.path.join(os.path.join(os.getcwd(), app.config['DOWNLOAD_FOLDER']), filename))
            
    
    




if __name__ == '__main__':
    app.run(debug=True)