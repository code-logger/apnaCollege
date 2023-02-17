import logging 
from helper.InternalApis import course_details
from helper.misc import extract_course

logging.basicConfig(level=logging.DEBUG,handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ],format='%(levelname)s - %(message)s')


def main(): 
    logging.debug("Started Running")
    base_data = course_details()
    extract_course(base_data)
if __name__ == "__main__":
    main() 
