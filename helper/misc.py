import os 
from config import FOLDER_PATH
import logging 
from helper.InternalApis import get_pdf_url ,download_pdf,get_video_details,get_m3u8_info
import time
log = logging.getLogger(__name__)
import subprocess
def handle_pdf_download(data,folder_path):
    # response = get_pdf_url(data['title'])
    complete_data = download_pdf(data['data']['pdf_full'],folder_path+"/"+data['title'].replace("\\"," ").replace("/"," ").replace("?"," ")+".pdf")

def parse_m3u8_data(dt):
    dt = dt.split("\n")
    next= False
    for each in dt:
        if(next):
            return each
        if(each.find("720") != -1):
            next= True


def extract_course(data):
    log.info("Trying to Create Folders")
    i = 0;
    for each in data['course']['sections']:
        section_ = data['course']['sections'][each]
        # log.info("In the section "+section_)
        name_ = section_['title'];#time.sleep(3);
        complete_path = FOLDER_PATH+"/"+name_
        complete_path= complete_path.strip();
        #if(i<=38):
        #    print("skipping ",name_);i+=1;continue
        if(not os.path.exists(complete_path)):
            os.makedirs(complete_path)
            log.info("Folder Created for section: "+name_)
        else:
            log.info("Folder already exists "+complete_path)
            time.sleep(4);continue
        description_file = complete_path +"/README.txt"
        with open(description_file, "w+") as file:
            file.write(section_['description'])
        for each in section_['learningPath']:
            if(each['type'] == "pdf"):
                pdf_data = data['course']['objects'][each['id']]
                print(pdf_data)
                handle_pdf_download(pdf_data,complete_path)
            
            if(each['type'] == "ivideo"):
                video_data = get_video_details(each['id']);print(each['id'])
                print(video_data)
                log.info("Trying To Download Video : "+video_data['video']['title'])
                complete_video_path = complete_path+"/"+video_data['video']['title'].replace("\\"," ").replace("/"," ").replace("?"," ").replace("'","^")+".mp4"
                complete_video_path = complete_video_path
                source_data = get_m3u8_info(video_data['video']['sourceid'])
                parsed_url = parse_m3u8_data(source_data)
                # subprocess.call(["ffmpeg", "-i", "{}".format(parsed_url),"-c" , "copy" ,"-bsf:a", "aac_adtstoasc", "".format(complete_video_path)])
                subprocess.call("ffmpeg -i {} -c copy -bsf:a aac_adtstoasc \"{}\"".format(parsed_url,complete_video_path),shell=True)
            time.sleep(2)
