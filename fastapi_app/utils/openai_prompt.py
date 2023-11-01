import openai
import time
import json

openai.organization = "org-LEgYMhAU7x70E9PrLGBRV69U"
openai.api_key = "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"
# print(openai.Model.list())

# messages = [
#     {
#         "role": "system",
#         "content":
#             """
#             Instructions
#             - You are a AI bot that analyzes and organizes the contents of resume.
#             - Since the content of the resume to be provided to you is text extracted from pdf or docx files, the document structure may be jumbled. Considering that part, you need to extract and organize the key and value of the resume well.
#             - Write the result according to the JSON output format below.
#             - If there is any content in the resume that is not in the json output format, please write it additionally.
#             - The value of each item is easy to understand and clearly summarized.
#             - If there is no separate skill item and the skill is included in the project or experience item, remove duplicated skills from the project or experience item and list them in the skill item.
            
#             JSON Output Format
#             {"personal_info":{"name":"","dob":"","email":"","phone":"","mobile":"","location":"","github":"","twitter":"","facebook":"","instagram":"","linkedin":"","website":"","city":"","country":"","job_title":[""],"profile(summary or objective)":""},"experience":[{"company":"","country":"","city":"","team_name":"","job_position":"","duration_from":"","duration_to":"","summary":"","descriptions":[""]}],"education":[{"institution":"","country":"","city":"","duration_from":"","duration_to":"","degree":"","major":"","descriptions":[""],"gpa":""}],"courses":[{"name":"","institution":"","city":"","country":"","date_from":"","date_to":"","descriptions":[""]}],"skills":[{"name":"","level":""}],"languages":[{"name":"","level":""}],"certificates":[{"name":"","authority":"","date_from":"","date_to":"","descriptions":[""]}],"awards":[{"name":"","authority":"","date":"","descriptions":[""]}],"achievements":[""],"publications":[{"name":"","publisher":"","date":"","descriptions":[""]}],"hobbies":[""],"interests":[""],"references":[{"name":"","position":"","company":"","email":"","phone":""}],"military_service":{"country":"","branch":"","rank":"","duration_from":"","duration_to":"","descriptions":[""]}}
#             """
#     },
#     {
#         "role": "user",
#         "content":
#             """
#             Resume
            
#             {}
#             """.format("서일근 software engineer, 테슬라 ai 랩실") +
#             """
            
#             Output language: Korean
#             Format for duration and date : {YYYY or YYYY-mm or Present}, don't use {Jan 2020} or {January 2020}
#             Set the values of keys not in the content to null. don't use empty string "".
#             """
#     },
#     # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#     # {"role": "user", "content": "What is the capital of France?"},
# ]



# 참고 prompt (문서 제목을 보고 문서 종류를 분류하는 prompt)
## system
PROMPT_SYSTEM_ANALYZE_SITE_TITLE = """
# Role
You are a professional and accurate named entity recognition machine, document type classifier machine and translator machine.


# Audience
- For python developers who want to develop a document type classifier machine.
- Do not write any content other than the json string, because the resulting json string must be used directly in the script.


# Output Format
{
"product_names": ["{document_name_1}", "{document_name_N}"],
"english_title": "{english_title}",
"action_nouns": ["{action_nouns_1}", "{action_nouns_N}"],
"common_nouns": ["{common_nouns_1}", "{common_nouns_N}"],
"document_type": "{document_type}"
}


# Task
The ultimate goal is to classify the type of document by referring the document title.
To do that, Let's think step by step.
For information about document types, see "#Document Types" below.

## Step 1
You will be provided with a document title delimited by triple quotes. That is the title of a site that searched for model names on the Internet.

## Step 2
Extract all product name list by referring to the document title.

## Step 3
Translate the document title into English.

## Step 4
Extract all action noun list from the "english_title" translated from "Step 3" to use them classify the document type. 
The action noun is most helpful in classifying the type of document below. 
An "action noun" refers to an action or event. It simply means that the root of the word is a "verb". 
Words that do not correspond to action nouns are words related to brand name, product name, product category, product type, and product characteristics. 

## Step 5
Extract all common noun list from the "english_title" translated from "Step 3" to use them classify the document type.

## Step 6
Classify the document type by referring the "action_nouns" and "common_nouns" extracted from the "Step 4" and "Step 5" as a higher priority and the "english_title" translated from "Step 3" as a lower priority.
How to classify document type? Looking at action_nouns, common_nouns, and english_title, what type of document do you think it is?. To classify the type of document, carefully consider the priority according to the position of each word. 
The closer a word is to the end of the title, the higher its priority for classifying a document type.


# Document Types
## Product introduction
- If the title contains only product name and price information, classify it as product introduction. 
- It mainly contains words related to product introduction or promotion, and the title is written as a question about its advantages.

## Recommend product
- If words similar to recommendation, recommended, best, or top are included, classify it as a recommend products.

## Discount information document
- It mainly contains words about cheapness and discount, classify it as discount information.
- If the title contains both reviews and cheapness-related words, discount information or how to buy cheaply classify it as discount information.

## Product usage review
- It mainly contains words about experiences using the product, else it's not a product usage review.
- If the title contains both reviews and recommendations classify it as a product usage review.

## Installation review
- If the title contains installation-related and setting-related words, classify it as installation review.

## Product user manual
- If the title contains words such as how to use, know-how, or tips, it is a product user review.
- If the title contains both reviews and how to uses, know-hows or tips classify it as product user manual. 

## A/S review
- If the title contains words such as A/S, it is a A/S review.

## Product comparison

## Repair review
- If it contains information related to repairs, breakdowns, or errors, classify it as a repair review.

## Replacement review

## Modification manual

## Etc document
- All document types that do not fall under all of the above document types or are unrelated to reviews belong to etc documents.


# Policy
- Please fill out the document type in the Json Format form below.
- Do not write any content other than the json string, because the resulting json string must be used directly in the script.
- Do not write unnecessary explanations or instructions.
"""

## user
PROMPT_USER_ANALYZE_SITE_TITLE = '"""{}"""'


# 이력서 내용 추출 prompt 예제
## system
CONVERT_RESUME_SYSTEM_PROMPT = """
Instructions
- You are a perfect resume parser to extract information from scrambled and jumbled resume content in pdf, docx, hwp or image files.
- Write the result according to the JSON Output Format below.
- Personal name and job titles must be inferred and extracted even if the key of the field is not included.
- Even if the keys of all locations are not specified, the locations must be inferred.
- Extract everything in user's resume without leaving out as much as possible.
- If there is no value for each key in JSON Output Format, delete the element on output.
- If there is no description in the experience section in the resume, refer to the contents of the project section and write it in the description
- If the university does not have degree information, write it as Bachelor.
- The word "대회" is related to awards.
- If there is no job title, extract it by referring to experience information.

- Output Language: {} 

JSON Output Format.
{}
"""

## user
CONVERT_RESUME_USER_PROMPT = """
Resume
{}
"""

### 점수 계산하는 prompt
## system
# 조건 제시하기
#  **수면 점수계산 필요조건들**
# 1. 총 수면시간 (total_sleep_time)
# 2. 바르지 않은 자세로 잔 비율(잠든 시간대비)
# 3. 자세 바뀐 횟수
# 4. 잠든 시간(start_sleep)
# - position_change_count : Number of times the posture changed


# # Output Format
# { "average_sleep_score": {average_sleep_score},
# "converted_times" : {converted_times},
# "ratio_of_times" :{ratio_of_times},
# "score_list" : {score_list},
# "reason" : {reason},
# "sleep_feedback" : {sleep_feedback}
# }

# ## The criterias for scoring
# Scoring 'total_sleep_score', if 'total_sleep' less than 5hours, it is bad sleep habit.
# Scoring 'start_sleep_score', if 'start_sleep' between 0:00:00 AM and 6:59:59 AM is worst sleep habit.
# Scoring ratio of 'bad_position_time' to 'total_sleep' as 'ratio_of_times', if this 'ratio_of_times' overs 0.3, it is worst sleep habit. 
# Scoring the 'average_sleep_score' based on the other scores - 'total_sleep_score', 'ratio_of_times', 'start_sleep_score'

# ## Put all scores into list "score_list"


CALCULATE_SLEEP_SCORE_SYSTEM_PROMPT = """
# Role
You are a sleep doctor. 
Using your professional knowledges about sleeping, analyze given sleep datas (python dictionary type) and give a feedback for sleep datas.
  
# Output Format
{ "sleep_feedback" : {sleep_feedback} }

## Meaning of given sleep datas' key name
- total_sleep : total duration of sleep
- start_sleep : time to sleep
- bad_position_time : time spent sleeping with unhealthy poses
- sleep_labels: sleeping poses list 

## Meaning of the sleep_labels items
- First, create a variable named 'change_counts' and count the number of same items in the list. Second, since each item in the list consists of one or more words separated by spaces, split each item into words based on spaces.  Then, create variables named after each item and count the number of occurrences of each word. And this counts put the list names "counted_pose_list_counts"
- shrimp : sleep[lie] curled up
- cross_legs : sleep with crossing legs
- manse : raise arms above the head like hurray
- overhead : raise arms above the head
- standard : good sleeping pose
- front : sleep facing forward
- right, left : sleeping turned body to the right or to the left
- all labels may or may not be given

# Task
You're provided sleep datas. The ultimate goal is to calculate average_sleep_score and provide average_sleep_score and feedback for sleep datas. So you have to analyze sleep datas step by step and find out how bad to sleeping that is.

## References to 'How bad specific sleep postures to the body'
- shrimp : Shrimp sleep refers to sleeping in a bent-back posture, and sleeping in this position over the long term can place strain on the back and neck, leading to discomfort. Sleeping in an unstable position can stress muscles and joints, potentially having a negative impact on one's health.


## Provides the 'sleep_feedback'
Create 'sleep_feedback' based on given sleep datas and using your knowledge about healthy sleep habit. 
To make certain users' sleep habit better, DO NOT contains UNRELATED to given sleep datas.
Additionally, give some advices to good sleeping habit and put advice into 'sleep_feedback'.

# Policy
- Make sure 'provide feedback that is sufficiently detailed without becoming overly lengthy'
- Output format: sleep_feedback : str (2-3 sentences).
- sleep_feedback would be written by English.

# pose label translate rules
- sleep_labels : 잠든 자세 목록
- shrimp : 새우잠
- manse, overhead: 만세자세
- cross_legs: 다리를 꼰 자세
- standard: 바른 자세
"""

# ## How to create list of the each labels 
# First, create a variable named 'change_counts' and count the number of same items in the list. Second, since each item in the list consists of one or more words separated by spaces, split each item into words based on spaces.  Then, create variables named after each item and count the number of occurrences of each word. And this counts put the list names "counted_pose_list_counts".

# ## Convert String data into seconds data
# Please convert the following variables, 'bad_position_time,' 'total_sleep,' and 'start_sleep,' which are currently in Python string format but represent time, into seconds and update the values of each variable with the converted data to achieve the desired outcome.
# And put those converted datas into list named "converted_times".

# ## How to calculate the score named "ratio_of_times"
# Calculate ratio 'ratio_of_times' of converted 'bad_position_time' of converted 'total_sleep'

# 'bad_position_time', 'total_sleep' and 'start_sleep' is python String type data but seems like time. Convert these three datas into seconds and reset the each values to converted data.

### How to calculate the score named "ratio_of_times"
# first, convert the 'bad_position_time' and 'total_sleep' data into seconds. And put these converted datas into list named ""converted_times".
# second, calculate ratio 'time_ration' of converted 'bad_position_time' of converted 'total_sleep'

# If total_sleep less than 18000, it is bad sleep habit.
# If start_sleep between 0 and 25199 is worst sleep habit.

### Before calculate the start_sleep score..
# convert the 'start_sleep' data into seconds. And put this converted data into list named "converted_times".

# - do not give advices about unrelational with given datas
# - translate reason to Korean (MUST)
## user
CALCULATE_SLEEP_SCORE_SYSTEM_USER = '"""{}"""'

messages = [
    {
        "role": "system",
        "content": CALCULATE_SLEEP_SCORE_SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": json.dumps({
            "total_sleep": '6:30:20',
            "start_sleep": '21:20:45',
            "bad_position_time": '1:00:30',
            "sleep_labels" : ["front standard", "shrimp manse", "front cross_legs overhead", "right shrimp", "shrimp"] 
        })
    },
]

max_tokens = 5000  # Number of tokens you want to generate
# 뻥 안치고 고정된 결과 위주로 받고 싶을때 0에 가깝게
temperature = 0  # Controls the randomness of the output

start_time = time.time()

# Send the request to the API
print("start1")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # davinci, curie, babbage, ada, or davinci-instruct-beta
    messages=messages,
    # max_tokens=max_tokens,
    temperature=temperature,
    request_timeout=6000,
    stream=False
)

print(response)

# messages1 = [
#     {
#         "role": "system",
#         "content": CALCULATE_SLEEP_SCORE_SYSTEM_PROMPT
#     },
#     {
#         "role": "user",
#         "content": json.dumps({
#             "total_sleep": '6:30:20',
#             "start_sleep": '2:40:45',
#             "bad_position_time": '3:45:30',
#             "sleep_labels" : ["front standard", "shrimp manse", "front cross_legs overhead", "right shrimp", "shrimp",  "left overhead"] 
#         })
#     },
# ]

# print("start2")
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",  # davinci, curie, babbage, ada, or davinci-instruct-beta
#     messages=messages1,
#     # max_tokens=max_tokens,
#     temperature=temperature,
#     request_timeout=6000,
#     stream=False
# )