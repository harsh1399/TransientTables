
import re
import json
import os
from datetime import datetime
import random
important_keys = ['name','captain','test_captain','od_captain','t20i_captain','1captain','2captain','coach','test_coach',
                  'od_coach','chairman','batting_coach','bowling_coach','fielding_coach','overseas','overseas1','overseas2',
                  'owner','ceo','manager','adviser','num_titles','title1','title1wins','title2','title2wins','title3','title3wins',
                  'title4','title4wins','title5','title5wins','title6','title6wins','title7','title7wins','title8','title8wins',
                  'sheffield','frc_wins','t20_wins','ipl_wins','clt20_wins','bpl_wins','psl_wins','WCL_division','test_rank',
                  'test_rank_best','odi_rank','odi_rank_best','t20i_rank','t20i_rank_best','wodi_rank','wodi_rank_best','wt20i_rank',
                  'wt20i_rank_best','num_tests','test_record','num_tests_this_year','test_record_this_year','wtc_apps','num_odis',
                  'odi_record','num_odis_this_year','odi_record_this_year','wc_apps','num_t20is','t20i_record','num_t20is_this_year',
                  't20i_record_this_year','wt20_apps','wcq_apps','wcq_best','wt20q_apps','wt20q_best','num_wtests','wtest_record',
                  'num_wtests_this_year','wtest_record_this_year','num_wodis','wodi_record','num_wodis_this_year','wodi_record_this_year',
                  'wwc_apps','wwc_best','num_wt20is','num_wt20is_this_year','wt20i_record_this_year','wwt20_apps','wwt20_best']


questions = {
    "q1":["Name the person(s) who served as the {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain} when {captain/test_captain/od_captain/t20i_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:value1} was the {captain/test_captain/od_captain/t20i_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:key1} of the {folder_name}.",
          "Who were the individual(s) serving as the {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain} during the tenure of {captain/test_captain/od_captain/t20i_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:value1} as the {captain/test_captain/od_captain/t20i_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:key1} of the {folder_name}?"],
    "q2":["Does the {folder_name} have the best win percentage in the {test/odi/t20i} format in {year:value1} or {year:value2}?(Answer in year)(Include no results/ties/draws in total number of matches.)",
          "Was the {folder_name}'s win percentage the highest in the {test/odi/t20i} format in either {year:value1} or {year:value2}?(Answer in year)(Include no results/ties/draws in total number of matches.)"],
    "q3":["Who was the {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain} when {captain/t20i_captain/od_captain/test_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:key1} was {captain/t20i_captain/od_captain/test_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:value1} and {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/t20i_captain/od_captain/test_captain:key2} was {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/t20i_captain/od_captain/test_captain:value2} of the {folder_name}?",
          "Name the person(s) who served as the {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain} during the tenure of {captain/t20i_captain/od_captain/test_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:value1} and {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/t20i_captain/od_captain/test_captain:value2} as the {captain/t20i_captain/od_captain/test_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach:key1} and {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/t20i_captain/od_captain/test_captain:key2}, respectively, of the {folder_name}."],
    "q4":["In which year did {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain:value1} become the {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain} of the {folder_name} for the first time?",
          "In which year did {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain:value1} first assume the role of {coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/captain/test_captain/od_captain/t20i_captain} for the {folder_name}?"],
    "q5":["How long did {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:value} serve as the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} of {folder_name}? (answer in number of days)(Assume that tenure for a position starts when the person appears in the timeline in that role and ends when either the timeline ends, or someone else replaces him.)",
          "What was the duration of {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:value}'s tenure as the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} of {folder_name}? (answer in number of days)(Assume that tenure for a position starts when the person first in the timeline in that role and ends when either the timeline ends, or someone else replaces him.)"],
    "q6":["Which person had the {longest/shortest} tenure as the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:key} of the {folder_name}?(Assume that tenure for a position starts when the person appears in the timeline in that role and ends when either the timeline ends, or someone else replaces him.)",
          "Who had the {longest/briefest} stint as the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:key} of the {folder_name}?(Assume that tenure for a position starts when the person appears in the timeline in that role and ends when either the timeline ends, or someone else replaces him.)"],
    "q7":["How many people served as the {test_captain/od_captain/t20i_captain/captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach} of the {folder_name}?",
          "How many individuals took on the role of {test_captain/od_captain/t20i_captain/captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach} of the {folder_name}?"],
    "q8":["Who was the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} of the {folder_name} before {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:value}?",
          "Who served as the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} of the {folder_name} prior to {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:value}?"],
    "q9":["Who was the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} of {folder_name} after {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:value}?",
          "Who assumed the role of {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} for the {folder_name} following {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach:value}?"],
    "q10":["How many {total(including ODIs,Tests,T20Is)/test/odi/t20} matches did the {folder_name} play in {year:value}?"],
    "q11":["How many {total(including ODIs,Tests,T20Is)/test/odi/t20} matches did the {folder_name} play between {year:value1} and {year:value2}? (including both the years)"],
    "q12":["Name the people who serve as {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} of {folder_name} between {year:value1} and {year:value2}. (including both the years)",
           "Who were the individual(s) who held the position of the {test_captain/od_captain/t20i_captain/captain/coach/bowling_coach/fielding_coach/batting_coach} for the {folder_name} from {year:value1} and {year:value2}? (including both the years)"],
    "q13":["Name the person(s) who served as the {test_captain/captain/od_captain/t20i_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/manager/ceo/owner} of the {folder_name} in {year:value}.",
           "Who were the individual(s) who acted as the {test_captain/captain/od_captain/t20i_captain/coach/test_coach/od_coach/batting_coach/bowling_coach/fielding_coach/manager/ceo/owner} of the {folder_name} in {year:value}?"],
    "q14":["what was the best {test/odi/t20i} rank of the {folder_name} in {year:value}?",
           "What was the highest ranking achieved by the {folder_name} in the {test/odi/t20i} format in {year:value}?"],
    "q15":["What is the win to loss ratio of {folder_name} in {test/odi/t20i} format in {year:value1}?(Answer in decimal form.)",
           "What is the ratio of wins to losses for the {folder_name} in the {test/odi/t20i} format for {year:value1}?(Answer in decimal form.)"]
    }

def remove_comma(string):
    return re.sub(',','',string)

def win_to_lose_ratio_year(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        year_set = set()
        question_key = " ".join(question_key.split("_"))
        for time1 in json_data:
            rand_num = random.randint(0,len(question)-1)
            quest =  question[rand_num]
            final_question = quest
            year1 = re.findall(r'\d{4}',time1)
            if year1[0] in year_set:
                continue
            year_set.add(year1[0])
            pattern_value1 = re.compile(r'{([^{}]*value1[^{}]*)}')
            final_question = pattern_value1.sub(year1[0],final_question)
            pattern_question_key = re.compile(r"{(.*?)}")
            final_question = pattern_question_key.sub(question_key,final_question)
            required_key1,required_key2 = None, None
            for key1 in json_data:
                if key1[:10] == f"{year1[0]}-12-31":
                    required_key1 = key1
            if required_key1 is not None:
                if f"{question_key}_record_this_year" not in json_data[required_key1].keys():
                    continue
                required_val1 = json_data[required_key1][f"{question_key}_record_this_year"]
                bracket_pattern = re.compile(r'\(.*?\)')
                win_percentages = []
                best_year = None
                flag = 0
                for required_val in [required_val1]:
                    val = bracket_pattern.findall(required_val)
                    if len(val)!=0:
                        val_ties = re.findall(r'\d+\s*tie[s]*',val[0])
                        val_noresults = re.findall(r'\d+\s*no\s*result[s]*',val[0])
                        val_draws = re.findall(r'\d+\s*draw[s]*',val[0])
                    val_results = re.findall(r'\d+/\d+',required_val)
                    if len(val_results) == 0:
                        continue
                    val_totalmatches = 0
                    # val_wins = int(val_results[0][0])
                    if len(val_ties) !=0:
                        val_totalmatches += int(val_ties[0][0])
                    if len(val_noresults) !=0:
                        val_totalmatches += int(val_noresults[0][0])
                    if len(val_draws) !=0:
                        val_totalmatches += int(val_draws[0][0])
                    win_lose = val_results[0].split("/")
                    val_totalmatches += (int(win_lose[0]) + int(win_lose[1])) 
                    val_wins = int(win_lose[0])
                    val_loss = int(win_lose[1])
                    
                    if val_totalmatches == 0 or val_loss==0:
                        flag = 1
                        break
                    win_percentages.append((val_wins/val_loss))
                if flag == 1:
                    continue
                questions[f'question{question_count}'] = {"Q":final_question,"A":round(win_percentages[0],2)}
                question_count += 1
    return questions



def best_rank(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        year_set = set()
        question_key = " ".join(question_key.split("_"))
        for time1 in json_data:
            year1 = re.findall(r'\d{4}',time1)
            if year1[0] in year_set:
                continue
            year_set.add(year1[0])
            rand_num = random.randint(0,len(question)-1)
            quest =  question[rand_num]
            final_question = quest
            # required_val = json_data[time1][question_key]
            regex_value = re.compile(r'{([^{}]*value[^{}]*)}')
            final_question = regex_value.sub(year1[0],final_question)
            pattern_question_key = re.compile(r"{(.*?)}")
            final_question = pattern_question_key.sub(question_key,final_question)
            min_rank = None
            required_key1 = None
            required_key2 = None
            for key1 in json_data:
                if key1[:10] == f"{str(int(year1[0]) - 1)}-12-31" or key1[:10] == f"{str(int(year1[0]))}-01-01" :
                    required_key1 = key1
                if key1[:10] == f"{str(int(year1[0]))}-12-31":
                    required_key2 = key1
            if required_key1 is not None and required_key2 is not None:
                if f"{question_key}_rank" not in json_data[required_key1].keys():
                    continue
                rank = re.findall(r'\d+',json_data[required_key1][f"{question_key}_rank"])
                # min_rank = int(json_data[required_key1][f"{question_key}_rank"][:-2])
                if len(rank) == 0:
                    continue
                min_rank = int(rank[0])
                for key2 in json_data:
                    if int(key2[:4]) == int(year1[0]):
                        if f"{question_key}_rank" not in json_data[key2].keys():
                            continue
                        rank = re.findall(r'\d+',json_data[key2][f"{question_key}_rank"])
                        if len(rank) == 0:
                            continue
                        if int(rank[0]) < min_rank:
                            min_rank = int(rank[0])
                if min_rank is not None:
                    questions[f'question{question_count}'] = {"Q":final_question,"A":f"{min_rank}"}
                    question_count += 1
            else:
                continue
    return questions

def person_in_year(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        year_set = set()
        question_key = " ".join(question_key.split("_"))
        for time1 in json_data:
            year1 = re.findall(r'\d{4}',time1)
            if year1[0] in year_set:
                continue
            year_set.add(year1[0])
            rand_num = random.randint(0,len(question)-1)
            quest =  question[rand_num]
            final_question = quest
            # required_val = json_data[time1][question_key]
            regex_value = re.compile(r'{([^{}]*value[^{}]*)}')
            final_question = regex_value.sub(year1[0],final_question)
            pattern_question_key = re.compile(r"{(.*?)}")
            final_question = pattern_question_key.sub(" ".join(question_key.split("_")),final_question)
            answer = set()
            required_key1 = None
            for key1 in json_data:
                if key1[:10] == f"{str(int(year1[0]) - 1)}-12-31" or key1[:10] == f"{str(int(year1[0]))}-01-01":
                    required_key1 = key1
            if required_key1 is not None:
                if question_key not in json_data[required_key1].keys():
                    continue
                year1_val = json_data[required_key1][question_key]
                answer.add(year1_val)
                for key2 in json_data:
                    if int(key2[:4]) == int(year1[0]):
                        if question_key not in json_data[key2].keys():
                            continue
                        required_val = json_data[key2][question_key]
                        if required_val not in answer:
                            answer.add(required_val)
                answer.discard('TBD')
                answer.discard('TBA')
                answer.discard('Vacant')
                answer.discard('vacant')
                if answer is not None:
                    questions[f'question{question_count}'] = {"Q":final_question,"A":f"{", ".join(ans for ans in answer)}"}
                    question_count += 1
            else:
                continue
    return questions

def year_first_time(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        key_val = set()
        for time1 in json_data:
            if question_key not in json_data[time1].keys():
                continue
            rand_num = random.randint(0,len(question)-1)
            quest =  question[rand_num]
            final_question = quest
            required_val = json_data[time1][question_key]
            if required_val in key_val:
                continue
            if required_val == 'TBD' or required_val == 'TBA' or required_val == 'Vacant':
                continue
            key_val.add(required_val)
            regex_value = re.compile(r'{([^{}]*value1[^{}]*)}')
            final_question = regex_value.sub(required_val,final_question)
            pattern_question_key = re.compile(r"{(.*?)}")
            final_question = pattern_question_key.sub(question_key,final_question)
            year1 = re.findall(r'\d{4}',time1)[0]
            required_key1 = None
            for key1 in json_data:
                if key1[:10] == f"{int(year1)-1}-12-31":
                    required_key1 = key1
            if required_key1 is None:
                continue
            questions[f'question{question_count}'] = {"Q":final_question,"A":year1}
            question_count += 1
    return questions


## win-to-loss ratio
def win_to_lose_ratio(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        year_set = set()
        for time1 in json_data:
            for time2 in json_data:
                if time2!=time1:
                    rand_num = random.randint(0,len(question)-1)
                    quest =  question[rand_num]
                    final_question = quest
                    year1 = re.findall(r'\d{4}',time1)
                    year2 = re.findall(r'\d{4}',time2)
                    if year1[0] == year2[0]:
                        continue
                    if (year1[0],year2[0]) in year_set or (year2[0],year1[0]) in year_set:
                        continue
                    year_set.add((year1[0],year2[0]))
                    year_set.add((year2[0],year1[0]))
                    pattern_value1 = re.compile(r'{([^{}]*value1[^{}]*)}')
                    pattern_value2 = re.compile(r'{([^{}]*value2[^{}]*)}')
                    final_question = pattern_value1.sub(year1[0],final_question)
                    final_question = pattern_value2.sub(year2[0],final_question)
                    pattern_question_key = re.compile(r"{(.*?)}")
                    final_question = pattern_question_key.sub(question_key,final_question)
                    required_key1,required_key2 = None, None
                    for key1 in json_data:
                        if key1[:10] == f"{year1[0]}-12-31":
                            required_key1 = key1
                        if key1[:10] == f"{year2[0]}-12-31":
                            required_key2 = key1
                    
                    if required_key1 is not None and required_key2 is not None:
                        if f"{question_key}_record_this_year" not in json_data[required_key1].keys() or f"{question_key}_record_this_year" not in json_data[required_key2].keys():
                            continue
                        required_val1 = json_data[required_key1][f"{question_key}_record_this_year"]
                        required_val2 = json_data[required_key2][f"{question_key}_record_this_year"]
                        bracket_pattern = re.compile(r'\(.*?\)')
                        win_percentages = []
                        best_year = None
                        flag = 0
                        for required_val in [required_val1,required_val2]:
                            val = bracket_pattern.findall(required_val)
                            if len(val)!=0:
                                val_ties = re.findall(r'\d+\s*tie[s]*',val[0])
                                val_noresults = re.findall(r'\d+\s*no\s*result[s]*',val[0])
                                val_draws = re.findall(r'\d+\s*draw[s]*',val[0])
                            val_results = re.findall(r'\d+/\d+',required_val)
                            if len(val_results) == 0:
                                continue
                            val_totalmatches = 0
                            
                            if len(val_ties) !=0:
                                val_totalmatches += int(val_ties[0][0])
                            if len(val_noresults) !=0:
                                val_totalmatches += int(val_noresults[0][0])
                            if len(val_draws) !=0:
                                val_totalmatches += int(val_draws[0][0])
                            win_lose = val_results[0].split("/")
                            val_totalmatches += (int(win_lose[0]) + int(win_lose[1])) 
                            val_wins = int(win_lose[0])
                            if val_totalmatches == 0:
                                flag = 1
                                break
                            win_percentages.append((val_wins/val_totalmatches))
                        if flag == 1:
                            continue
                        if win_percentages[0] > win_percentages[1]:
                            best_year = year1[0]
                        else:
                            best_year = year2[0]
                        questions[f'question{question_count}'] = {"Q":final_question,"A":best_year}
                        question_count += 1
    return questions

def how_many_ppl_between_years(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        keys_to_be_used = []
        for key in json_data.keys():
            if question_key in json_data[key].keys():
                keys_to_be_used.append(key)
        if len(json_data) == len(keys_to_be_used):
            year_set = set()
            for time1 in json_data:
                for time2 in json_data:
                    if time2!=time1:
                        tempdate1 = datetime.strptime(time1[:10],'%Y-%m-%d')
                        tempdate2 = datetime.strptime(time2[:10],'%Y-%m-%d')
                        if tempdate2 > tempdate1:
                            rand_num = random.randint(0,len(question)-1)
                            quest =  question[rand_num]
                            final_question = quest
                            year1 = re.findall(r'\d{4}',time1)
                            year2 = re.findall(r'\d{4}',time2)
                            if year1[0] == year2[0]:
                                continue
                            if (year1[0],year2[0]) in year_set:
                                continue
                            year_set.add((year1[0],year2[0]))
                            pattern_value1 = re.compile(r'{([^{}]*value1[^{}]*)}')
                            pattern_value2 = re.compile(r'{([^{}]*value2[^{}]*)}')
                            final_question = pattern_value1.sub(year1[0],final_question)
                            final_question = pattern_value2.sub(year2[0],final_question)
                            pattern_question_key = re.compile(r"{(.*?)}")
                            final_question = pattern_question_key.sub(question_key,final_question)
                            answer = set()
                            # year1 = str(int(year1[0]) - 1)
                            required_key1 = None
                            required_key2 = None
                            for key1 in json_data:
                                if key1[:10] == f"{str(int(year1[0]) - 1)}-12-31" or key1[:10] == f"{str(int(year1[0]))}-01-01":
                                    required_key1 = key1
                                if key1[:10] == f"{year2[0]}-12-31":
                                    required_key2 = key1
                            if required_key1 is not None and required_key2 is not None:
                                year1_val = json_data[required_key1][question_key]
                                answer.add(year1_val)
                                for key2 in json_data:
                                    if int(key2[:4]) >= int(year1[0]) and int(key2[:4]) <= int(year2[0]):
                                        required_val = json_data[key2][question_key]
                                        if required_val not in answer:
                                            answer.add(required_val)
                                answer.discard('TBD')
                                answer.discard('TBA')
                                answer.discard('Vacant')
                                answer.discard('vacant')
                                if answer is not None:
                                    questions[f'question{question_count}'] = {"Q":final_question,"A":f"{", ".join(ans for ans in answer)}"}
                                    question_count += 1
                            else:
                                continue
    return questions

def number_of_between_time(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        year_set = set()
        for time1 in json_data:
            for time2 in json_data:
                if time2!=time1:
                    tempdate1 = datetime.strptime(time1[:10],'%Y-%m-%d')
                    tempdate2 = datetime.strptime(time2[:10],'%Y-%m-%d')
                    if tempdate2 > tempdate1:
                        rand_num = random.randint(0,len(question)-1)
                        quest =  question[rand_num]
                        final_question = quest
                        # year1 = re.findall(r'\d{4}',time1)
                        # year2 = re.findall(r'\d{4}',time2)
                        # if year1[0] == year2[0]:
                        #     continue
                        if (time1,time2) in year_set:
                            continue
                        year_set.add((time1,time2))
                        pattern_value1 = re.compile(r'{([^{}]*value1[^{}]*)}')
                        pattern_value2 = re.compile(r'{([^{}]*value2[^{}]*)}')

                        final_question = pattern_value1.sub(time1.split('T')[0],final_question)
                        final_question = pattern_value2.sub(time2.split('T')[0],final_question)
                        pattern_question_key = re.compile(r"{(.*?)}")
                        final_question = pattern_question_key.sub(question_key,final_question)
                        required_key1,required_key2 = None, None
                        answer = None
                        # year1 = str(int(year1[0]) - 1)
                        for key1 in json_data:
                            if key1[:10] == time1.split('T')[0]:
                                required_key1 = key1
                            if key1[:10] == time2.split('T')[0]:
                                required_key2 = key1
                        if required_key1 is not None and required_key2 is not None:
                            if question_key == "test":
                                if "num_tests" in json_data[required_key1].keys() and "num_tests" in json_data[required_key2].keys():
                                    answer = int(remove_comma(json_data[required_key2]["num_tests"])) - int(remove_comma(json_data[required_key1]["num_tests"]))
                            elif question_key == "odi":
                                if "num_odis" in json_data[required_key1].keys() and "num_odis" in json_data[required_key2].keys():
                                    answer = int(remove_comma(json_data[required_key2]["num_odis"])) - int(remove_comma(json_data[required_key1]["num_odis"]))
                            elif question_key == "t20":
                                if "num_t20is" in json_data[required_key1].keys() and "num_t20is" in json_data[required_key2].keys():
                                    answer = int(remove_comma(json_data[required_key2]["num_t20is"])) - int(remove_comma(json_data[required_key1]["num_t20is"]))
                            else:
                                if "num_t20is" in json_data[required_key1].keys() and "num_t20is" in json_data[required_key2].keys() and \
                                "num_tests" in json_data[required_key1].keys() and "num_tests" in json_data[required_key2].keys() and \
                                "num_odis" in json_data[required_key1].keys() and "num_odis" in json_data[required_key2].keys():
                                    answer = (int(remove_comma(json_data[required_key2]["num_t20is"])) + int(remove_comma(json_data[required_key2]["num_tests"])) + int(remove_comma(json_data[required_key2]["num_odis"]))) \
                                        - (int(remove_comma(json_data[required_key1]["num_t20is"] ))+ int(remove_comma(json_data[required_key1]["num_tests"])) + int(remove_comma(json_data[required_key1]["num_odis"])))
                            if answer is not None:
                                questions[f'question{question_count}'] = {"Q":final_question,"A":answer}
                                question_count += 1
                        else:
                            continue
    return questions


def number_of_between_years(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        year_set = set()
        for time1 in json_data:
            for time2 in json_data:
                if time2!=time1:
                    tempdate1 = datetime.strptime(time1[:10],'%Y-%m-%d')
                    tempdate2 = datetime.strptime(time2[:10],'%Y-%m-%d')
                    if tempdate2 > tempdate1:
                        rand_num = random.randint(0,len(question)-1)
                        quest =  question[rand_num]
                        final_question = quest
                        year1 = re.findall(r'\d{4}',time1)
                        year2 = re.findall(r'\d{4}',time2)
                        if year1[0] == year2[0]:
                            continue
                        if (year1[0],year2[0]) in year_set:
                            continue
                        year_set.add((year1[0],year2[0]))
                        pattern_value1 = re.compile(r'{([^{}]*value1[^{}]*)}')
                        pattern_value2 = re.compile(r'{([^{}]*value2[^{}]*)}')
                        final_question = pattern_value1.sub(year1[0],final_question)
                        final_question = pattern_value2.sub(year2[0],final_question)
                        pattern_question_key = re.compile(r"{(.*?)}")
                        final_question = pattern_question_key.sub(question_key,final_question)
                        required_key1,required_key2 = None, None
                        answer = None
                        year1 = str(int(year1[0]) - 1)
                        for key1 in json_data:
                            if key1[:10] == f"{year1}-12-31":
                                required_key1 = key1
                            if key1[:10] == f"{year2[0]}-12-31":
                                required_key2 = key1
                        if required_key1 is not None and required_key2 is not None:
                            if question_key == "test":
                                if "num_tests" in json_data[required_key1].keys() and "num_tests" in json_data[required_key2].keys():
                                    answer = int(remove_comma(json_data[required_key2]["num_tests"])) - int(remove_comma(json_data[required_key1]["num_tests"]))
                            elif question_key == "odi":
                                if "num_odis" in json_data[required_key1].keys() and "num_odis" in json_data[required_key2].keys():
                                    answer = int(remove_comma(json_data[required_key2]["num_odis"])) - int(remove_comma(json_data[required_key1]["num_odis"]))
                            elif question_key == "t20":
                                if "num_t20is" in json_data[required_key1].keys() and "num_t20is" in json_data[required_key2].keys():
                                    answer = int(remove_comma(json_data[required_key2]["num_t20is"])) - int(remove_comma(json_data[required_key1]["num_t20is"]))
                            else:
                                if "num_t20is" in json_data[required_key1].keys() and "num_t20is" in json_data[required_key2].keys() and \
                                "num_tests" in json_data[required_key1].keys() and "num_tests" in json_data[required_key2].keys() and \
                                "num_odis" in json_data[required_key1].keys() and "num_odis" in json_data[required_key2].keys():
                                    answer = (int(remove_comma(json_data[required_key2]["num_t20is"])) + int(remove_comma(json_data[required_key2]["num_tests"])) + int(remove_comma(json_data[required_key2]["num_odis"]))) \
                                        - (int(remove_comma(json_data[required_key1]["num_t20is"] ))+ int(remove_comma(json_data[required_key1]["num_tests"])) + int(remove_comma(json_data[required_key1]["num_odis"])))
                            if answer is not None:
                                questions[f'question{question_count}'] = {"Q":final_question,"A":answer}
                                question_count += 1
                        else:
                            continue
    return questions


def number_of_matches(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    
    for question_key in key_dict["question_key"]:
        year_set = set()
        for key in json_data:
            rand_num = random.randint(0,len(question)-1)
            quest =  question[rand_num]
            final_question = quest
            year_values = re.findall(r'\d{4}',key)
            if year_values[0] in year_set:
                continue
            year_set.add(year_values[0])
            pattern_value = re.compile(r'{([^{}]*value[^{}]*)}')
            final_question = pattern_value.sub(year_values[0],final_question)
            pattern_question_key = re.compile(r"{(.*?)}")
            final_question = pattern_question_key.sub(question_key,final_question)
            answer = None
            key_regex = r''+ str(year_values[0]) + r"-12-31"
            required_key = None
            for key1 in json_data:
                if key1[:10] == f"{year_values[0]}-12-31":
                    required_key = key1
            # required_key = re.findall(key_regex,str(json_data.keys()))
            if required_key is not None:
                if question_key == "test":
                    if "num_tests_this_year" in json_data[required_key].keys():
                        answer = int(json_data[required_key]["num_tests_this_year"])
                elif question_key == "odi":
                    if "num_odis_this_year" in json_data[required_key].keys():
                        answer = int(json_data[required_key]["num_odis_this_year"])
                elif question_key == 't20':
                    if "num_t20is_this_year" in json_data[required_key].keys():
                        answer = int(json_data[required_key]["num_t20is_this_year"])
                else:
                    if "num_t20is_this_year" in json_data[required_key].keys() and "num_odis_this_year" in json_data[required_key].keys() \
                          and "num_tests_this_year" in json_data[required_key].keys():
                        answer = int(json_data[required_key]["num_tests_this_year"]) + int(json_data[required_key]["num_odis_this_year"]) + int(json_data[required_key]["num_t20is_this_year"])
                if answer is not None:
                    questions[f'question{question_count}'] = {"Q":final_question,"A":answer}
                    question_count += 1
            else:
                continue
    return questions


def before_question(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        keys_to_be_used = []
        for key in json_data.keys():
            if question_key in json_data[key].keys():
                keys_to_be_used.append(key)
        if len(json_data) == len(keys_to_be_used):
            key_values = set()
            for time in keys_to_be_used:
                key_value = json_data[time][question_key]
                if key_value in key_values:
                    continue
                if key_value == 'TBD' or key_value == 'TBA' or key_value == 'Vacant':
                    continue
                key_values.add(key_value)
                rand_num = random.randint(0,len(question)-1)
                quest =  question[rand_num]
                final_question = quest
                pattern_value = re.compile(r'{([^{}]*value[^{}]*)}')
                final_question = pattern_value.sub(key_value,final_question)
                pattern_question_key = re.compile(r"{(.*?)}")
                final_question = pattern_question_key.sub(" ".join(question_key.split("_")),final_question)
                prev_key = None
                current_key = None
                answers = set()
                for time1 in keys_to_be_used:
                    if current_key is None:
                        current_key = time1
                    else:
                        prev_key = current_key
                        current_key = time1
                    if json_data[current_key][question_key] == key_value and prev_key is None:
                        continue
                    elif json_data[current_key][question_key] == key_value and prev_key is not None and json_data[prev_key][question_key] != key_value:
                        if json_data[prev_key][question_key] not in answers:
                            answers.add(json_data[prev_key][question_key])
                if 'TBD' in answers or 'TBA' in answers or 'Vacant' in answers or 'vacant' in answers:
                    continue
                if len(answers)!=0:
                    questions[f'question{question_count}'] = {"Q":final_question,"A":f"{", ".join(ans for ans in answers)}"}
                    question_count += 1
    return questions


def after_question(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        keys_to_be_used = []
        for key in json_data.keys():
            if question_key in json_data[key].keys():
                keys_to_be_used.append(key)
        if len(json_data) == len(keys_to_be_used):
            key_values = set()
            for time in keys_to_be_used:
                key_value = json_data[time][question_key]
                if key_value in key_values:
                    continue
                if key_value == 'TBD' or key_value == 'TBA' or key_value == 'Vacant':
                    continue
                key_values.add(key_value)
                rand_num = random.randint(0,len(question)-1)
                quest =  question[rand_num]
                final_question = quest
                pattern_value = re.compile(r'{([^{}]*value[^{}]*)}')
                final_question = pattern_value.sub(key_value,final_question)
                pattern_question_key = re.compile(r"{(.*?)}")
                final_question = pattern_question_key.sub(" ".join(question_key.split("_")),final_question)
                prev_key = None
                current_key = None
                answers = set()
                for time1 in keys_to_be_used:
                    if current_key is None:
                        current_key = time1
                    else:
                        prev_key = current_key
                        current_key = time1
                    if json_data[current_key][question_key] == key_value and prev_key is None:
                        continue
                    elif json_data[current_key][question_key] != key_value and prev_key is not None and json_data[prev_key][question_key] == key_value:
                        if json_data[prev_key][question_key] not in answers:
                            answers.add(json_data[current_key][question_key])
                if 'TBD' in answers or 'TBA' in answers or 'Vacant' in answers or 'vacant' in answers:
                    continue
                if len(answers)!=0:
                    questions[f'question{question_count}'] = {"Q":final_question,"A":f"{", ".join(ans for ans in answers)}"}
                    question_count += 1
    return questions

def how_many_ppl(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        keys_to_be_used = []
        for key in json_data.keys():
            if question_key in json_data[key].keys():
                keys_to_be_used.append(key)
        if len(json_data) == len(keys_to_be_used):
            rand_num = random.randint(0,len(question)-1)
            quest =  question[rand_num]
            final_question = quest
            pattern_question_key = re.compile(r"{(.*?)}")
            final_question = pattern_question_key.sub(" ".join(question_key.split("_")),final_question)
            answer = set()
            for time1 in json_data:
                if json_data[time1][question_key] in answer:
                    continue
                answer.add(json_data[time1][question_key])
            answer.discard('TBD')
            answer.discard('TBA')
            answer.discard('Vacant')
            answer.discard('vacant')
            questions[f'question{question_count}'] = {"Q":final_question,"A":f"{len(answer)}"}
            question_count += 1
    return questions

## how long did they serve
def time_measurement(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        keys_to_be_used = []
        for key in json_data.keys():
            if question_key in json_data[key].keys():
                keys_to_be_used.append(key)
        if len(json_data) == len(keys_to_be_used):
            key_values = set()
            for time in keys_to_be_used:
                key_value = json_data[time][question_key]
                if key_value == 'TBD' or key_value == 'TBA' or key_value == 'Vacant':
                    continue
                if key_value in key_values:
                    continue
                key_values.add(key_value)
                rand_num = random.randint(0,len(question)-1)
                quest =  question[rand_num]
                final_question = quest
                pattern_value = re.compile(r'{([^{}]*value[^{}]*)}')
                final_question = pattern_value.sub(key_value,final_question)
                pattern_question_key = re.compile(r"{(.*?)}")
                final_question = pattern_question_key.sub(" ".join(question_key.split("_")),final_question)
                mindate = None
                maxdate = None
                total_days = 0
                for time1 in keys_to_be_used:
                    tempdate = datetime.strptime(time1[:10],'%Y-%m-%d')
                    if json_data[time1][question_key] != key_value and mindate is None:
                        continue
                    elif json_data[time1][question_key] == key_value and mindate is None:
                        mindate = datetime.strptime(time1[:10],'%Y-%m-%d')
                    elif json_data[time1][question_key] != key_value and mindate is not None:
                        maxdate = datetime.strptime(time1[:10],'%Y-%m-%d')
                        total_days += (maxdate-mindate).days
                        mindate = None
                        maxdate = None
                    elif json_data[time1][question_key] == key_value and tempdate < mindate:
                        mindate = datetime.strptime(time1[:10],'%Y-%m-%d')
                    elif json_data[time1][question_key] == key_value and tempdate > mindate:
                        maxdate = datetime.strptime(time1[:10],'%Y-%m-%d')
                if mindate is not None and maxdate is not None:
                    total_days += (maxdate-mindate).days
                if total_days == 0:
                    continue
                questions[f'question{question_count}'] = {"Q":final_question,"A":f"{total_days} days"}
                question_count += 1
    return questions

##which person had the longest/shortest tenure
def longest_shortest_tenure(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {}
    question_count = 1
    for question_key in key_dict["question_key"]:
        for dependent_key in key_dict["key"]:
            keys_to_be_used = []
            for key in json_data.keys():
                if dependent_key in json_data[key].keys():
                    keys_to_be_used.append(key)
            if len(json_data) == len(keys_to_be_used):
                rand_num = random.randint(0,len(question)-1)
                quest =  question[rand_num]
                final_question = quest
                pattern_value = re.compile(r'{([^{}]*key[^{}]*)}')
                final_question = pattern_value.sub(" ".join(dependent_key.split("_")),final_question)
                pattern_question_key = re.compile(r"{(.*?)}")
                final_question = pattern_question_key.sub(" ".join(question_key.split("_")),final_question)
                dependent_key_set = set()
                for time1 in keys_to_be_used:
                    if json_data[time1][dependent_key] in dependent_key_set:
                        continue
                    dependent_key_set.add(json_data[time1][dependent_key])
                dependent_key_timeline = {}
                for key_value in dependent_key_set:
                    mindate = None
                    maxdate = None
                    total_days = 0
                    for time1 in keys_to_be_used:
                        tempdate = datetime.strptime(time1[:10],'%Y-%m-%d')
                        if json_data[time1][dependent_key] != key_value and mindate is None:
                            continue
                        elif json_data[time1][dependent_key] == key_value and mindate is None:
                            mindate = datetime.strptime(time1[:10],'%Y-%m-%d')
                        elif json_data[time1][dependent_key] != key_value and mindate is not None:
                            maxdate = datetime.strptime(time1[:10],'%Y-%m-%d')
                            total_days += (maxdate-mindate).days
                            mindate = None
                            maxdate = None
                        elif json_data[time1][dependent_key] == key_value and tempdate < mindate:
                            mindate = datetime.strptime(time1[:10],'%Y-%m-%d')
                        elif json_data[time1][dependent_key] == key_value and tempdate > mindate:
                            maxdate = datetime.strptime(time1[:10],'%Y-%m-%d')    
                    if mindate is not None and maxdate is not None:
                        total_days += (maxdate-mindate).days
                    dependent_key_timeline[key_value] = total_days
                answer = None
                if question_key == "longest":
                    answer = max(dependent_key_timeline,key = dependent_key_timeline.get)
                elif question_key == "shortest":
                    answer = min(dependent_key_timeline,key = dependent_key_timeline.get)
                if answer == 'TBD' or answer == 'TBA' or answer == 'Vacant' or answer == 'vacant':
                    continue
                questions[f'question{question_count}'] = {"Q":final_question,"A":f"{answer}"}
                question_count += 1
    return questions


## Multiple timeline multiple keys
def initialize_question(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {"multiple_ans":{},"single_ans":{}}
    count1 = 0
    count2 = 0
    for question_key in key_dict['question_key']:
        for kv in key_dict:
            if kv == "question_key":
                continue
            if "key" in kv:
                for dependent_key in key_dict[kv]:
                    if dependent_key == question_key:
                        continue
                    dep_val_set = set()
                    for time in json_data:
                        if dependent_key in json_data[time].keys():
                            dependent_val = json_data[time][dependent_key]
                            if dependent_val == 'TBD' or dependent_val == 'TBA' or dependent_val == 'Vacant':
                                continue
                            if dependent_val in dep_val_set:
                                continue
                            dep_val_set.add(dependent_val)     
                            rand_num = random.randint(0,len(question)-1)
                            quest =  question[rand_num]
                            final_question = quest
                            regex = r"{([^{}]*"+kv+r"[^{}]*)}"
                            regex_val = r"{([^{}]*"+"value"+kv[-1]+r"[^{}]*)}"
                            regex_pattern = re.compile(regex)
                            regex_valpattern = re.compile(regex_val)
                            final_question = regex_pattern.sub(" ".join(dependent_key.split("_")),final_question)
                            final_question = regex_valpattern.sub(dependent_val,final_question)
                            regex_question_key = re.compile(r"{(.*?)}")
                            final_question = regex_question_key.sub(" ".join(question_key.split("_")),final_question)
                            answer = set()
                            for time1 in json_data:
                                if dependent_key in json_data[time1].keys():
                                    if json_data[time1][dependent_key] == dependent_val:
                                        if question_key in json_data[time1].keys():
                                            if json_data[time1][question_key] in answer:
                                                continue
                                            answer.add(json_data[time1][question_key])
                            flag = 0
                            for ans in answer:
                                if ans in final_question:
                                    flag = 1
                                
                            answer.discard('TBA')
                            answer.discard('TBD')
                            answer.discard('Vacant')
                            answer.discard('vacant')
                            if flag == 1:
                                continue
                            if len(answer)!=0:
                                ans = f"{", ".join(ans for ans in answer)}"
                                if ',' in ans:
                                    count1 += 1
                                    questions["multiple_ans"][f"question{count1}"] = {"Q":f"{final_question}","A":ans}   
                                else:
                                    count2 += 1
                                    questions["single_ans"][f"question{count2}"] = {"Q":f"{final_question}","A":ans}    
                                # count += 1
                                # questions[f"question{count}"] = {"Q":f"{final_question}","A":f"{", ".join(ans for ans in answer)}"}                            
    return questions

## multiple timeline multiple keys - many keys in the questions
def initialize_question_multiplekeys(question,json_data):
    brackets = re.findall(r"{(.*?)}",question[0])
    key_dict = {}
    for selection in brackets:
        select = selection.split(":")
        if len(select)==1:
            key_dict["question_key"] = select[0].split("/")
        else:
            key_dict[select[1]] = select[0].split("/")
    questions = {"multiple_ans":{},"single_ans":{}}
    count1 = 0
    count2 = 0
    for question_key in key_dict['question_key']:
        for kv in key_dict:
            if kv == "question_key":
                continue
            if "key1" in kv:
                dep_val_set = set()
                for dependent_key in key_dict[kv]:
                    if dependent_key == question_key:
                        continue
                    for dependent_key2 in key_dict['key2']:
                        if dependent_key2 == dependent_key or dependent_key2 == question_key:
                            continue
                        for time in json_data:
                            if (question_key in json_data[time].keys()) and (dependent_key in json_data[time].keys()) and (dependent_key2 in json_data[time].keys()):
                                dependent_val = json_data[time][dependent_key]
                                dependent_val2 = json_data[time][dependent_key2]
                                if dependent_val == 'TBD' or dependent_val == 'TBA' or dependent_val == 'Vacant' or dependent_val2 == 'TBD' or dependent_val2 == 'TBA' or dependent_val2 == 'Vacant':
                                    continue
                                if dependent_val == dependent_val2:    #### when od_captain and t2oi_captain are same
                                    continue
                                if (dependent_val,dependent_val2) in dep_val_set or (dependent_val2,dependent_val) in dep_val_set:
                                    continue
                                dep_val_set.add((dependent_val,dependent_val2))
                                dep_val_set.add((dependent_val2,dependent_val))
                                rand_num = random.randint(0,len(question)-1)
                                quest =  question[rand_num]
                                final_question = quest
                                regex_key1 = r"{([^{}]*key1[^{}]*)}"
                                regex_val1 = r"{([^{}]*value1[^{}]*)}"
                                regex_key2 = r"{([^{}]*key2[^{}]*)}"
                                regex_val2 = r"{([^{}]*value2[^{}]*)}"
                                regex_pattern_key1 = re.compile(regex_key1)
                                regex_pattern_value1 = re.compile(regex_val1)
                                regex_pattern_key2 = re.compile(regex_key2)
                                regex_pattern_value2 = re.compile(regex_val2)
                                final_question = regex_pattern_key1.sub(" ".join(dependent_key.split("_")),final_question)
                                final_question = regex_pattern_value1.sub(dependent_val,final_question)
                                final_question = regex_pattern_key2.sub(" ".join(dependent_key2.split("_")),final_question)
                                final_question = regex_pattern_value2.sub(dependent_val2,final_question)
                                regex_question_key = re.compile(r"{(.*?)}")
                                final_question = regex_question_key.sub(" ".join(question_key.split("_")),final_question)
                                answer = set()
                                for time1 in json_data:
                                    if (question_key in json_data[time1].keys()) and (dependent_key in json_data[time1].keys()) and (dependent_key2 in json_data[time1].keys()):
                                        if json_data[time1][dependent_key] == dependent_val and json_data[time1][dependent_key2] == dependent_val2:
                                            if json_data[time1][question_key] in answer:
                                                continue
                                            answer.add(json_data[time1][question_key])
                                flag = 0
                                for ans in answer:
                                    if ans in final_question:
                                        flag = 1
                                answer.discard('TBA')
                                answer.discard('TBD')
                                answer.discard('Vacant')
                                answer.discard('vacant')
                                if flag == 1:
                                    continue
                                if len(answer)!=0:
                                    ans = f"{", ".join(ans for ans in answer)}"
                                    if ',' in ans:
                                        count1 += 1
                                        questions["multiple_ans"][f"question{count1}"] = {"Q":f"{final_question}","A":ans}   
                                    else:
                                        count2 += 1
                                        questions["single_ans"][f"question{count2}"] = {"Q":f"{final_question}","A":ans}    
                                                                
    return questions



questions_dict = {}
total_questions = 0
folders = os.listdir("../Dataset/timelines/cricket_team")
for folder in folders:
    folder_path = f"scripts/info_cricket_team/infoboxes/cricket_team/{folder[:-1]}"
    questions_dict[f"{folder[:-1]}"] = {} 
    with open(f'{folder_path}/{folder[:-1]}.json','r') as f:
        output = json.load(f)
    folder_name_pattern = re.compile(r'{folder_name}')
    for q in questions:
        question = questions[q]
        new_question_lst = question.copy()
        for ind in range(0,len(question)):
            if re.search(folder_name_pattern,question[ind]):
                f_name = folder[:-1].split("_")
                new_question_lst[ind] = folder_name_pattern.sub(" ".join(f_name),question[ind])
        question_number = int(q[1:])
        if question_number == 3:
            ans = initialize_question_multiplekeys(new_question_lst,output)
            questions_dict[f"{folder[:-1]}"][f"{q}-multi"] = ans["multiple_ans"]
            questions_dict[f"{folder[:-1]}"][f"{q}-single"] = ans["single_ans"]
            total_questions += len(questions_dict[f"{folder[:-1]}"][f"{q}-multi"]) + len(questions_dict[f"{folder[:-1]}"][f"{q}-single"])
            continue
        elif question_number == 2:
            questions_dict[f"{folder[:-1]}"][q] = win_to_lose_ratio(new_question_lst,output)
        elif question_number == 4:
            questions_dict[f"{folder[:-1]}"][q] = year_first_time(new_question_lst,output)
        elif question_number == 5:
            questions_dict[f"{folder[:-1]}"][q] = time_measurement(new_question_lst,output)
        elif question_number == 6:
            questions_dict[f"{folder[:-1]}"][q] = longest_shortest_tenure(new_question_lst,output)
        elif question_number == 7:
            questions_dict[f"{folder[:-1]}"][q] = how_many_ppl(new_question_lst,output)
        elif question_number == 8:
            questions_dict[f"{folder[:-1]}"][q] = before_question(new_question_lst,output)
        elif question_number == 9:
            questions_dict[f"{folder[:-1]}"][q] = after_question(new_question_lst,output)
        # elif question_number == 10:
        #     questions_dict[f"{folder[:-1]}"][q] = number_of_matches(new_question_lst,output)
        elif question_number == 11:
            questions_dict[f"{folder[:-1]}"][q] = number_of_between_years(new_question_lst,output)
        elif question_number == 12:
            questions_dict[f"{folder[:-1]}"][q] = how_many_ppl_between_years(new_question_lst,output)
        elif question_number == 13:
            questions_dict[f"{folder[:-1]}"][q] = person_in_year(new_question_lst,output)
        elif question_number == 14:
            questions_dict[f"{folder[:-1]}"][q] = best_rank(new_question_lst,output)
        elif question_number == 15:
            questions_dict[f"{folder[:-1]}"][q] = win_to_lose_ratio_year(new_question_lst,output)
        # elif question_number == 16:
        #     questions_dict[f"{folder[:-1]}"][q] = number_of_between_time(question,output)
        else:
            ans = initialize_question(new_question_lst,output)
            questions_dict[f"{folder[:-1]}"][f"{q}-multi"] = ans["multiple_ans"]
            questions_dict[f"{folder[:-1]}"][f"{q}-single"] = ans["single_ans"]
            total_questions += len(questions_dict[f"{folder[:-1]}"][f"{q}-multi"]) + len(questions_dict[f"{folder[:-1]}"][f"{q}-single"])
            continue
        total_questions += len(questions_dict[f"{folder[:-1]}"][q])
print(f"total questions:{total_questions}")
json_obj = json.dumps(questions_dict,indent = 4)
with open('scripts/info_cricket_team/cricket_questions_latest.json','w') as f:
    f.write(json_obj)