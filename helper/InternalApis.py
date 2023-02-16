import requests 
import logging
# from ..config import COURSE_NAME, TOKEN
from config import COURSE_NAME, TOKEN,COURSE_ID,COOKIE_TOKEN
log = logging.getLogger(__name__)

cookies = {
    "slim_session":COOKIE_TOKEN
}
headers = {
    'authority': 'www.apnacollege.in',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'token': TOKEN,
    'sec-gpc': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


def course_details():
    headers_copy = headers
    headers_copy['referer'] = "https://www.apnacollege.in/path-player?courseid="+COURSE_NAME
    URL = "https://www.apnacollege.in/api/course/{}?contents&path-player".format(COURSE_NAME)
    try:
        log.info("Trying to get Data for course: "+COURSE_NAME)
        response = requests.get(
        'https://www.apnacollege.in/api/course/placement-course-java?contents&path-player',
        headers=headers_copy)
        log.info("Got Data for the course")
        return response.json()
    except Exception as e:
        log.error(str(e))

def download_pdf(url_file_name,file_name):
    headers = {
        'authority': 'lwpdf1.learnworlds.com',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        'accept': '*/*',
        'sec-gpc': '1',
        'origin': 'https://cdn.mycourse.app',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://cdn.mycourse.app/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    try:
        url = "https://api.us-e2.learnworlds.com/unlock/file?lw_client=62a6cd5e1e9e2fbf212d608d&access_token={}&file={}".format(TOKEN,url_file_name)
        log.info("Trying to download pdf")
        response = requests.get(url,headers=headers)
        with open(file_name,"wb") as f:
            f.write(response.content)
        log.info("Downloaded in "+file_name)
    except Exception as e:
        log.error(str(e))
    
def get_pdf_url(section):
    headers_copy = headers
    headers_copy['referer'] = "https://www.apnacollege.in/path-player?courseid="+COURSE_NAME
    try:
        log.info("Trying to get info for pdf of section: "+section)
        response = requests.get(
            'https://www.apnacollege.in/api/unlock/pdf/website.pdf?courseid={}&section={}&json'.format(COURSE_NAME,section),
            headers=headers_copy,
        )
        return response.json()
    except Exception as e:
        log.error(str(e))


def get_video_details(id_):
    headers_copy = headers
    headers_copy['referer'] = 'https://www.apnacollege.in/videoplayer?courseid=placement-course-java&videoid={}&courseslug={}'.format(id_,COURSE_ID)
    headers_copy['x-api-version'] = '0.0.1'
    try:
        response = requests.get(
        'https://www.apnacollege.in/api/video/{}/{}'.format(COURSE_ID,id_),
        headers=headers_copy,
        cookies=cookies
     )
        return response.json()
    except Exception as e:
        log.error(str(e))



def get_m3u8_info(src_id):
    try: 
        url = "https://fast.wistia.com/embed/medias/{}.m3u8".format(src_id)
        response = requests.get(url
     )
        return response.text
    except Exception as e:
        log.error(str(e))