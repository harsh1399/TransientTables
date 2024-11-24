import json
from openai import OpenAI
import pandas as pd
import time

data_folders = ["cricket_team","gov_agencies","economy","cricketer","country"]
prediction_folders = ["gpt-4o"]
models = ["gpt-4o"]

client = OpenAI(api_key="")

def create_prompt(example_timeline,question1,task1_answer1,task2_answer1,task3_answer1,question2,task1_answer2,task2_answer2,task3_answer2,question3,task1_answer3,task2_answer3,task3_answer3,timeline,question):
    return f"""Perform the following tasks –
Task 1: For the question provided with the timeline, retrieve the relevant tables from the timeline that shall be used to answer the question. The task is to extract the appropriate tables rather than generate the answer to the question.
Task 2: From the tables retrieved in task 1, retrieve the relevant keys and values that would be used to answer the question.
Task 3: Answer the question using the retrieved keys from Task 2. The answer should be concise, within 5 to 10 words. Further, answer the question based solely on the information presented in the retrieved key(s) without referencing any external data or information.
Here’s an example for your reference –
Timeline: {example_timeline}
question 1: {question1}
Task 1 Answer: {task1_answer1}
Task 2 Answer: {task2_answer1}
Task 3 Answer: {task3_answer1}
question 2: {question2}
Task 1 Answer: {task1_answer2}
Task 2 Answer: {task2_answer2}
Task 3 Answer: {task3_answer2}
question 3: {question3}
Task 1 Answer: {task1_answer3}
Task 2 Answer: {task2_answer3}
Task 3 Answer: {task3_answer3}
Now, perform the tasks for the following timeline(premise) and question -  
Premise: {timeline}
Question: {question}
Provide answers for task 1,task 2, and task 3 separately. Also, give a final answer based on the reasoning in task 3. 
Task 1 Answer:
Task 2 Answer:
Task 3 Answer:
Final Answer:
"""

for data_folder in data_folders:
    for prediction_folder,model in zip(prediction_folders,models):
        with open(f'data/{data_folder}/{data_folder}_questions_selected.json','r') as f:
            entities = json.load(f)
        with open(f'data/{data_folder}/multi-stage-cot-examples/three-stage/few_shot_example.json','r') as f:
            few_shot_timeline = json.load(f)
        with open(f'data/{data_folder}/multi-stage-cot-examples/three-stage/COT_questions.json','r') as f:
            cot_questions = json.load(f)
        few_shot_timeline = json.dumps(few_shot_timeline)
        total_questions = 0
        tasks = []
        entity_count = 0
        for entity in entities:
            folder_question = 0
            entity_name = entity.split(" ")
            entity_name = "_".join(entity_name)
            with open(f'data/{data_folder}/{entity_name}.json','r') as f:
                timeline = json.load(f)
            if len(timeline)>20:
                continue
            timeline = json.dumps(timeline)

            df = {"entity": [],
                  "question": [],
                  "actual_answer": [],
                  "predicted_answer": []}
            for questions_category in entities[entity]:
                for question in entities[entity][questions_category]:
                    actual_question = entities[entity][questions_category][question]["Q"]
                    prompt = create_prompt(few_shot_timeline,cot_questions['Q1'],
                                           cot_questions['A1-Task1'],cot_questions['A1-Task2'],
                                           cot_questions['A1-Task3'],cot_questions['Q2'],
                                           cot_questions['A2-Task1'],cot_questions['A2-Task2'],
                                           cot_questions['A2-Task3'],cot_questions['Q3'],
                                           cot_questions['A3-Task1'],cot_questions['A3-Task2'],
                                           cot_questions['A3-Task3'],timeline,actual_question)
                    task = {
                        "custom_id":f"{entity}-{questions_category}-{question}",
                        "method":"POST",
                        "url":"/v1/chat/completions",
                        "body":{
                            "model": f"{model}",
                            "messages": [
                                {"role": "system",
                                    "content": "You are an intelligent and helpful assistant who does the tasks per the user's request. The user provides a question and a set of tables (premise) for an entity that captures the information evolving for that entity across the timeline. The tables are in JSON format. You perform the tasks by understanding the timeline (premise) and the question's requirements."},
                                {"role": "user", "content": prompt}
                            ],
                        }
                    }
                    tasks.append(task)
        file_name = f"data/{data_folder}/new_predictions/multi-stage/cot/three-stage/{prediction_folder}/batch-questions-new-gpt-4o.jsonl"
        with open(file_name, 'w') as file:
            for obj in tasks:
                file.write(json.dumps(obj) + '\n')
        batch_file = client.files.create(
          file=open(file_name, "rb"),
          purpose="batch"
        )
        tasks = []
        print(batch_file)
        batch_job = client.batches.create(
          input_file_id=batch_file.id,
          endpoint="/v1/chat/completions",
          completion_window="24h"
        )
        batch_job_status = client.batches.retrieve(batch_job.id)
        while batch_job_status.status != "completed":
            batch_job_status = client.batches.retrieve(batch_job.id)
            time.sleep(240)
            print(batch_job_status.status)
        print(batch_job_status)
        if batch_job_status.status == "completed":
            result_file_id = batch_job_status.output_file_id
            result = client.files.content(result_file_id).content
            result_file_name = f"data/{data_folder}/new_predictions/multi-stage/cot/three-stage/{prediction_folder}/batch-results.jsonl"
            with open(result_file_name, 'wb') as file:
                file.write(result)