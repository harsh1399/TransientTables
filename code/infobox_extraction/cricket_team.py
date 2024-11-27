import re
from functions import *
redundant = ['image', 'alt', 'caption', 'image_size','url','title','date','first_test','wtc_first','first_odi'
             'association','nickname','test_status_year','icc_status','icc_member_year','icc_region',
             'first_t20i','wt20_first','website']

interesting_keys = ['name','captain','coach','test_rank','odi_rank','t20i_rank','test_rank_best',
                    'odi_rank_best','t20i_rank_best','most_recent_test','num_tests','num_tests_this_year',
                    'test_record','test_record_this_year','wtc_apps','wtc_best','most_recent_odi',
                    'num_odis','num_odis_this_year','odi_record','odi_record_this_year','wc_apps',
                    'wc_best','most_recent_t20i','num_t20is','num_t20is_this_year','wt20_apps','wt20_best',
                    'title1wins','title1','title2','title2wins','owner','manager','ipl_wins']

timeline_keys = ['birth_date', 'medaltemplates', 'years', 'clubs', 'nationalteams']

final_timeline_keys = ['medaltemplates', 'clubs', 'years', 'nationalteams']

def squashMod(json_dict, key):
    # Nickname and height
    if key in ['nickname', 'height', 'birth_place', 'weight']:
        json_dict[key] = re.sub('url(.*)', '', json_dict[key])
        json_dict[key] = re.sub('https(.*)', '', json_dict[key])
        json_dict[key] = re.sub('title(.*)', '', json_dict[key])

    # Name and fullname
        if key in ['name', 'full_name']:
            json_dict[key] = re.sub("post-nominals","",json_dict[key])

def clubAddendum(json_dict):
    club_lst = []    
    for i in range(1,18):
        if f'years{i}' in json_dict.keys():
            club_lst.append(i)

    lst = {}
    for num in club_lst:
        try:
            lst[json_dict[f'team{num}']] = json_dict[f'years{num}']
        except:
            pass
                
        try:
            del json_dict[f'team{num}']
        except:
            pass
        
        try:
            del json_dict[f'years{num}']
        except:
            pass
        
    if lst:
        json_dict['clubs'] = lst

def ntAddendum(json_dict):
    nt_lst = []    
    for i in range(1,18):
        if f'nationalyears{i}' in json_dict.keys():
            nt_lst.append(i)

    lst = {}
    for num in nt_lst:
        try:
            lst[json_dict[f'nationalteam{num}']] = json_dict[f'nationalyears{num}']
        except:
            pass
                
        try:
            del json_dict[f'nationalteam{num}']
        except:
            pass
        
        try:
            del json_dict[f'nationalyears{num}']
        except:
            pass
        
    if lst:
        json_dict['nationalteams'] = lst