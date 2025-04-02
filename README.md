# **[TransientTables](https://transienttables.github.io)**

This repository contains the code, and data for the paper - **TRANSIENTTABLES: Evaluating LLMs’ Reasoning on Temporally Evolving Semi-structured Table**.

## **For more details checkout our TransientTables - [website](https://transienttables.github.io/)**

## **Table of Contents**

- [📌 Introduction](#introduction)
- [📊 Dataset](#dataset)
- [⚙️ Installation](#installation)
- [🛠️ Data Collection](#data-collection)
- [❓ Question Answer Generation](#qa-generation)
- [🧪 Experiments](#experiments)

## 📌 **Introduction**

We introduce **TransientTables**, a novel dataset designed to advance temporal reasoning in large language models (LLMs). Featuring 3,971 questions from over 14,000 tables, covering 1,238 entities across various time, TRANSIENTTABLES challenges LLMs to reason dynamically over time. Built using a template-based question-generation pipeline and refined by LLMs, this dataset sets a new benchmark for temporal reasoning tasks. We establish baseline results using state-of-the-art LLMs to create a benchmark. Additionally, we present new modeling strategies based on task decomposition to improve LLM performance. 

## 📊 **Dataset**

**TransientTables** consists of infobox tables from various categories, Each category features multiple entities, such as the USA, India, and Kenya, in the 'country' category, with 7 to 12 infoboxes per entity that capture temporal changes to form a timeline. All the infoboxes representing a timeline for an entity is present in a single JSON file.

Categories present in the dataset - 
- Cricket Team
- Government Agencies
- Economy
- Cricketer
- Country
- Cyclist
- Equesterian
- Field Hockey
- Golfer
- Table Tennis Player

The `Dataset` directory structure - 
```
Dataset/
  timelines/
    cricket_team/
      Australia_national_cricket_team.json, India_national_cricket_team.json ....
    country/
      Bulgaria.json, Egypt.json ...
    ...
  question-answer.csv
```
The `question-answer.csv` file contains a set of questions and their corresponding answers for each entity within every category.

The structure of `question-answer.csv` is as follows:
```category, entity, question, answer```

## ⚙️ **Installation**

Clone the repository and install the required dependencies:

```bash
git clone ..
cd TransientTables
pip install -r requirements.txt
```

## 🛠️ **Data Collection**
We extract the infoboxes from the latest Wikipedia page and older versions of the same page. We start by extracting the current table from the latest Wikipedia page. Then, we go through the update history to extract the important or pivotal moments for the entity of the current page.

The `code/infobox_extraction` directory contains the script (`timeline_extraction.py` and all the required dependencies) used to extract infoboxes for the `cricket_team` category. Each category has a unique infobox structure, requiring slight modifications to the extraction script for each category.

**How to run**

Since `timeline_extraction.py` uses selenium webdriver to automate extraction, the script requires a webdriver (`chromedriver.exe` file) for execution. Once that file is downloaded, you can simply execute the script using - 
```bash
python timeline_extraction.py
```

## ❓ **Question Answer Generation**
Question-answer pairs are generated through a semi-automated approach utilizing predefined templates. We manually crafted templates for each category and employed automated scripts to populate the details and generate qa pairs. For example, cricket team category have following templates - 
```
- Name the person(s) who served as the <coach/test-coach/odi-coach/batting-coach/bowling-coach/fielding-coach> when <captain/test-captain/odi-captain/t20i-captain:value1> was the <captain/test-captain/odi-captain/t20-captain:key1>?
- Does the Indian Cricket Team have the best win percentage in the <test/odi/t20i> format in <year:value1> or <year:value2>}?
```
The `code/qa-generation` directory contains the script (`question_initialization.py`) for generating question-answer pairs for the `cricket_team` category. Since each category has unique question templates, separate question-answer generation scripts are required for other categories. These scripts will be uploaded soon.

**How to Run**

To execute `question_initialization.py`, use the following command:
```bash
python question_initialization.py
```
This will create a JSON file that will contain the question-answer pair for every entity in the category.

## 🧪 **Experiments**
The `cot_task_decomposition` directory contains the scripts for new modeling strategies based on task decomposition. The directory contains - 
 - `cot-information retrieval-extraction.py` - In this method the language model identifies and retrieves the relevant tables needed to answer the question, and then extracts pertinent attributes, such as infobox table keys, from the extracted tables. Finally, the model utilize the extracted keys to reason and derive the correct answer to the question.
 - `cot-information-retrieval.py` - In this method the language model extracts relevant tables from the timeline necessary to answer the question and then utilizes these extracted tables for reasoning.
 - `cot-information-extraction.py` - In this method model focuses on directly extracting specific attributes, such as infobox keys, from tables relevant to the query, and then utilized these specific attributes for reasoning.

**How to run**
To execute any of these files, you need to set GPT keys - 
```code
client = OpenAI(api_key="")
```
To execute any file - 
```bash
python filename.py
```
