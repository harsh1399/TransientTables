import re

def remove_html_spaces(text):
    if "&nbsp;" in text:
        return re.sub("&nbsp;", ' ', text)
    else:
        return re.sub("&nbsp", ' ', text)

def replace_br(text):
    if '<br/>' in text:
        return re.sub('\<br\/\>', ', ', text)
    elif '<br>' in text:
        return re.sub('\<br\>', ', ', text)
    return text

def replace_newlines(text):
    return re.sub("\n", '<>', text)

def clean_key(text):
    key = re.sub("<>\|\s*",'',text)
    return key.strip()

def remove_newlines(text):
    return re.sub("\n", '', text)

def replace_special(text):
    return re.sub("<>", ' ', text)

def replace_spaces(text):
    return re.sub(" ", '_', text)

def replace_colon(text):
    return re.sub(":", '_', text)

def remove_comments(text):
    return re.sub('<!--.*?-->','',text)

def replace_newlines_tabs(text):
    return re.sub("\n\|", '\n||', text)

def replace_tabs(text):
    return re.sub(" \| ", 'ZXC^', text)

def replace_insidebars(text):
    return re.sub("\[\[\|\]\]")

def replace_t(text):
    return re.sub("\| ","|",text)

def replace_line(text):
    return re.sub("\|",'',text)

def replace_tabs_alt(text):
    return re.sub("\|", 'ZXC^', text)

def replace_stars(text):
    return re.sub("\*", 'ZXC^', text)

def remove_braces(text):
    text = re.sub('{{','',text)
    return re.sub('}}','',text)

def remove_html(text):
    return re.sub('(?<=\<)(.*?)(?=\>)','',text)

def remove_refs(text):
    return re.sub('(?<=\<ref\>)(.*?)(?=\<\/ref\>)','',text)

def remove_pixel_info(text):
    return re.sub(r'\d+px', '', text)

def extract_text_between_braces(string):
    return re.findall(r'\[\[([^\[\]]+)\]\]', string)

def extract_text_between_curly_braces(string):
    return re.findall(r'{{(.*?)}}', string)


def clean(text):
    # remove html tags
    result = remove_refs(text)
    result = replace_br(result)
    result = remove_pixel_info(result)
    result = remove_html_spaces(result)
    result = remove_html(result) 
    result = replace_special(result)
    lst = extract_text_between_braces(result)
    lst_alt = []
    for ele in lst:
        if '|' in ele:
            result = result.replace(ele, ele.split('|')[1])
    lst = extract_text_between_curly_braces(result)
    lst_alt = []
    for ele in lst:
        if ('|' in ele) and ('hlist' not in ele):
            result = result.replace(ele, ele.split('|')[1])
    result = re.sub('[\[\]]+','',result) # remove [[around words]]
    return result

def post_clean(text):
    return remove_braces(tab_sep_alt(text.strip())) #tab_sep_alt

def clean_micro(text):
    text = text.strip()
    if(re.search("(?<={{)(.*?)(?=\|)",text)):
        text = text[re.search("(?<={{)(.*?)(?=\|)",text).end()+1:-2]
    return text

def tab_sep_alt(text):
    if(re.search('\S\|\S',text)):
        text = text[re.search('\S\|\S',text).start()+2:]
    return text

def extract_curly(text,phrase):
    text2 = text[re.search(phrase,text).start()+2:]
    i=2
    temp = ''
    for char in text2:
        if (i==0):
            break
        temp += char
        if char=='{':
            i = i+1
        elif char=='}':
            i = i-1
    return re.sub("{{"+temp,'',text)

def modify(json_dict,key):
    # removing curly brace part for specific cases
    try:
        temps = ["{{ctitle","{{cite","{{Cite"]
        for temp in temps:
            while(re.search(temp,json_dict[key])):
                json_dict[key] = extract_curly(json_dict[key],temp)
    except:
        pass
    try:
        if(re.search("{{flatlist",json_dict[key]) or re.search("{{flat list",json_dict[key]) or re.search("{{plainlist",json_dict[key]) or ('*' in json_dict[key])):
            if 'top score' not in key:
                json_dict[key] = replace_stars(json_dict[key]+'*')
                json_dict[key] = [remove_braces(s.strip()) for s in re.findall('\^(.*?)ZXC',json_dict[key])]
    except:
        pass
    try:
        if(re.search("{{unbulleted",json_dict[key])): #not clear yet
            try:
                json_dict[key] = [re.sub('}}','',ele) for ele in json_dict[key].split("|{{")[1:]]
            except:
                json_dict[key] = json_dict[key].split("|")[1:]
    except:
        pass
    try:
        if(re.search("{{hlist",json_dict[key])):
            json_dict[key] = replace_tabs_alt(json_dict[key]+'|')
            json_dict[key] =  [remove_braces(s.strip()) for s in re.findall('\^(.*?)ZXC',json_dict[key])]
    except:
        pass
    try:
        if(re.search("(?<={{)(.*?)(?=\|)",json_dict[key])):
            json_dict[key] = json_dict[key][:re.search("(?<={{)(.*?)(?=\|)",json_dict[key]).start()-2]+json_dict[key][re.search("(?<={{)(.*?)(?=\|)",json_dict[key]).end()+1:-2]
    except:
        pass