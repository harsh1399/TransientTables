# **TransientTables**

This repository contains the code, and data for the paper - **TRANSIENTTABLES: Evaluating LLMs’ Reasoning on Temporally Evolving Semi-structured Table**.

## **Table of Contents**

- [📌 Introduction](#introduction)
- [📊 Dataset](#dataset)
- [⚙️ Installation](#installation)
- [🛠️ Data Collection](#data-collection)
- [🧪 Experiments](#experiments)

## 📌 **Introduction**

We introduce **TransientTables**, a novel dataset designed to advance temporal reasoning in large language models (LLMs). Featuring 3,971 questions from over 14,000 tables, covering 1,238 entities across various time, TRANSIENTTABLES challenges LLMs to reason dynamically over time. Built using a template-based question-generation pipeline and refined by LLMs, this dataset sets a new benchmark for temporal reasoning tasks. We establish baseline results using state-of-the-art LLMs to create a benchmark. Additionally, we present new modeling strategies based on task decomposition to improve LLM performance. 

## 📊 **Dataset**

**TransientTables** consists of infobox tables from various categories, Each category features multiple entities, such as the USA, India, and Kenya, in the 'country' category, with 7 to 12 infoboxes per entity that capture temporal changes to form a timeline in JSON format.

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
```

## ⚙️ **Installation**

Clone the repository and install the required dependencies:

```bash
git clone ..
cd TransientTables
pip install -r requirements.txt
```

## 🛠️ **Data Collection**
