import configparser
from dotenv import load_dotenv
import os
load_dotenv()

config = configparser.ConfigParser()
config.read('config/config.ini')

APP_IP =  str(os.getenv("APP_IP")) if os.getenv("APP_IP") else config.getint('APP', 'APP_IP',fallback='127.0.0.1')
APP_PORT =  int(os.getenv("APP_PORT")) if os.getenv("APP_PORT") else config.getint('APP', 'APP_PORT',fallback=8100)

DEMO =  int(os.getenv("DEMO")) if os.getenv("DEMO") else config.getint('APP', 'DEMO')

DB_FILE_PATH_barrier = "./Database/DB/barriers.db"
DB_FILE_PATH_events = "./Database/DB/events.db"

    


def replace_line_with_substring(file_path, substring, new_line):

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if substring in line:

            lines[i] = new_line + '\n'
            break  

    with open(file_path, 'w') as file:
        file.writelines(lines)
    print(f"{substring}  found replace by {new_line}")


replace_line_with_substring('./static/config.js', "var ipAddress", 'var ipAddress="'+str(APP_IP)+'"')
replace_line_with_substring('./static/config.js', "var portep", 'var portep="'+str(APP_PORT)+'"')