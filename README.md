# **TransientTables**

This repository contains the code, and data for the paper - **TRANSIENTTABLES: Evaluating LLMs’ Reasoning on Temporally Evolving Semi-structured Table**.

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

## ❓ **Question Answer Generation**
Question-answer pairs are generated through a semi-automated approach utilizing predefined templates. We manually crafted templates for each category and employed automated scripts to populate the details and generate qa pairs. For example, cricket team category have following templates - 
```
- Name the person(s) who served as the <coach/test-coach/odi-coach/batting-coach/bowling-coach/fielding-coach> when <captain/test-captain/odi-captain/t20i-captain:value1> was the <captain/test-captain/odi-captain/t20-captain:key1>?
- Does the Indian Cricket Team have the best win percentage in the <test/odi/t20i> format in <year:value1> or <year:value2>}?
```

