from driver import driver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re

import os
import json
from functions import *
from cricket_team import *
from constants import XPATH
from deepdiff import DeepDiff

import time
start = time.time()

with open(f"link_timeline.json") as f:
    links = json.load(f)

titles = links.keys()

templates = ['cricket_team']
global_keys = list()
for template in templates:
    try:
        os.mkdir(f"infoboxes/cricket_team")
    except Exception as ex:
        print(ex)

    for page_title in titles:
        if(os.path.exists(f"infoboxes/{remove_newlines(template)}/{page_title.replace(':', '')}/logs.txt")):
            continue
        try:
            os.mkdir(f"infoboxes/{remove_newlines(template)}/{page_title.replace(':', '')}/")
        except:
            pass

        # Getting the infoboxes
        prev_json = dict()
        links[page_title] = links[page_title][:5000]
        for rev_num, link in enumerate(links[page_title]):
            try:
                json_dict = dict()
                global_lst = []
                championship_years = {}
                birth_date = ''
                revid = link['revid']  
                url = f'https://en.wikipedia.org/w/index.php?title={page_title}&oldid={revid}&action=raw'
                driver.get(url)
                page =  replace_newlines(remove_comments(driver.find_element(By.XPATH,XPATH).text))
                find_info = re.findall('(?<=\{\{Infobox)(.*)', replace_newlines(page))
                temp = replace_special(re.findall('(?<=\{\{Infobox)(.*)',replace_newlines(page))[0])
                # Figuring out where }} ends to mark end of infobox
                i=2
                infobox = ''
                for char in find_info[0]:
                    if (i==0):
                        break
                    infobox = infobox + char
                    if char=='{':
                        i = i+1
                    elif char=='}':
                        i = i-1

                infobox_keys = re.findall("<>\|\s*[a-zA-Z0-9_]*", infobox)
                infobox_keys = [clean_key(k) for k in infobox_keys]
                infobox = replace_special(infobox)
                for key_num,key_value in enumerate(infobox_keys):
                    try:
                        new_key = replace_line(key_value)
                        new_key = new_key.split('=')[0]
                        if (key_num + 1) < len(infobox_keys):
                            new_val = infobox.split(('|'+infobox_keys[key_num+1]).strip())[0]
                            new_val = new_val.split(new_key)[1]
                            new_val = new_val.split('=')[1]
                            new_val = new_val.split('|')[0]
                        else:
                            new_val = infobox.split(new_key)[1].split('=')[1]
                        #new_val = new_val.split('|')[0]
                        key = key_value.split('=')[0]
                        val = key_value.split()
                        value = '='.join(key_value.split('=')[1:])
                        if value.strip() == '':
                            key = key_value.split(': ')[0]
                            value = ': '.join(key_value.split(':')[1:])
                        # Do i need these strips??
                        key = key.strip()
                        new_key = new_key.strip()
                        new_val = new_val.strip()
                        json_dict[new_key] = clean(new_val)
                        squashMod(json_dict, new_key)
                        modify(json_dict,new_key)
                        
                    except:
                        continue

                # Post Modification Cleaning
                for key in json_dict:
                    if type(json_dict[key]) is str:
                        json_dict[key] = post_clean(json_dict[key])
                    elif type(json_dict[key]) is list:
                        json_dict[key] = [post_clean(a) for a in json_dict[key]]
                        
                # Removing empty slots
                remove = []
                for key in json_dict.keys():
                    try:
                        if(json_dict[key].strip() == ''):
                            remove.append(key)
                    except:
                        pass
                for key in remove:
                    json_dict.pop(key)
            
                # Removing redundant slots
                for key in redundant:
                    try:
                        json_dict.pop(key)
                    except:
                        pass

                interesting_keys = json_dict.keys()
            except:
                continue

            json_dict_temp = json_dict.copy()
            prev_json_temp = prev_json.copy()
            keys = []
            for key in json_dict.keys():
                for ele in interesting_keys:
                    if ele in key:
                        keys.append(key)
                        break

            json_dict_temp_keys = [] 
            prev_json_temp_keys = []       
            for key in keys:
                if key in json_dict.keys():
                    json_dict_temp_keys.append(key)
            for key in keys:
                if key in prev_json.keys():
                    prev_json_temp_keys.append(key)

            json_dict_temp = {key: json_dict_temp[key] for key in json_dict_temp_keys}
            prev_json_temp = {key: prev_json_temp[key] for key in prev_json_temp_keys}
            ddiff = DeepDiff(json_dict_temp, prev_json_temp, verbose_level=2)
            if(ddiff != {}):
                with open(f"infoboxes/{template}/{page_title.replace(':', '')}/logs.txt", "a", encoding="utf-8") as logs:
                    logs.write(str(rev_num) + ': '+ str(DeepDiff(json_dict, prev_json, verbose_level=2))+'\n')
                    logs.close()

                with open(f"infoboxes/{template}/{page_title.replace(':', '')}/{rev_num}.json", "w", encoding="utf-8") as f:
                    new_dict = dict()
                    new_dict = json_dict.copy()
                    new_dict["DATE_TIME"] = link['timestamp']
                    json.dump(new_dict, f, indent=4)
                    f.close()
                prev_json = json_dict.copy()

end = time.time()
print(end - start)
with open(f"infoboxes/{remove_newlines(template)}/{page_title.replace(':', '')}/logs.txt", "a", encoding="utf-8") as logs:
    logs.write('\n'+str(end-start))
    logs.close()


    