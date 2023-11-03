from fastapi import APIRouter
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("API_KEY")


def generate_sleep_feedback(messages, max_tokens=1000, temperature=0):
    # API 요청 전송
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response


router = APIRouter(
    tags=["Web Pages"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")


@router.get("/gpt", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "gpt.html",
        {
            "request": request,
        },
    )


# 결과 표시 함수
@router.post("/gpt", response_class=HTMLResponse)
async def get_feedback(request: Request, user_input: str = Form(...)):
    # 사용자 입력을 포함하는 대화 메시지 작성
    messages = [
        {
            "role": "system",
            "content": """
            
            # Role
            you are a famous sleep doctor
            give them feedback

            # Output Format
              ' start : 1 lines of feedback on start sleep time '
              ' total : 1 line of feedback on total sleep time '
              ' posture : 3 sentences of feedback about each bad posture ' 
              ' improvement : 3 sentences of improvement. '
              Translate Output to Korean follow the rules below 'pose label translate rules '
              Do not add any content other than that.
            

            # Task
            The goal is to give you sleep scores and improve your sleeping posture
            
            # Contents
            - Bad label : shrimp, manse, is_raise_arm, side, knee_up, cross_legs
            - irrelevant label : front, right, left
            - good label : standard
            - The shrimp posture is not good because the back is bent in a C-shape, making the arrangement of the spine and muscles bend only to one side. In addition, the shrimp sleeping position shortens the iliopsoas muscles, the muscles that connect the lumbar spine and pelvis, causing back pain. In addition, the fatigue that the back muscles feel when sleeping shrimp is three times more pressure than when lying down in the right position.

            - If you sleep in a hurrah position, your arms are raised, so you can put pressure on your neck, shoulders, back, and back while you sleep, and you can continue to be in a tense state, leading to a systemic imbalance.In addition, tense muscles can pressure blood vessels and nerves, interfering with blood circulation, and symptoms such as nerve numbness may occur.In addition, care should be taken because the airways are temporarily narrowed and snoring may worsen, or gastrointestinal diseases such as reflux esophagitis may occur.

            - A prone position increases pressure on the head and neck and interferes with blood circulation in the eyes, increasing intraocular pressure, causing glaucoma, and also causes neck ligaments and spine to warp and pain as the hips and back bones bend toward the ceiling. Also, a prone position causes neck wrinkles, irritates the skin by pressing the entire face, and is prone to wrinkles around the eyes and mouth, and sleeps with the face on the pillow, making it easy for acne to occur. This is because many bacteria reproduce on the pillow by sweat or dandruff.

            - If you keep sleeping with your legs crossed, your spine and pelvis are twisted, causing your body's left and right symmetries to be twisted, and your hamstrings, femoral muscles, and groin muscles are shortened, causing pain when you take the right posture.


            ## Step 1
            ### Scoring criteria
            #### Sleep time
            The recommended sleep time is 7-9 hours
            #### the percentage of sleeping in a bad posture
            Less than 20% of people slept in bad positions
            #### number of posture changed
            The recommended posture change is no more than five
            #### the time you fell asleep
            The recommended sleep start time is 10pm to 11pm

            ## Step 2
            Please refer to the contents of the contents
            Make sure you follow the criteria
            If you don't have the recommended range, please think about it yourself


            # Policy
            Please answer according to the format
            Please kindly tell me your feedback
            Summarize the feedback in three lines
            Give me feedback on bad posture and any improvements
            Check the number of times for each pose
            
            ## pose label translate rules
            - sleep_labels : 잠든 자세 목록
            - shrimp : 새우잠
            - is_raise_arm : 만세자세
            - cross_legs : 다리를 꼰 자세
            - standard : 바른 자세
            
            Translate Output to Korean follow the rules below 'pose label translate rules'
            """,
        },
        {
            "role": "user",
            "content": """
            {
            "total_sleep": '8:30:20',
            "start_sleep": '01:20:45',
            "bad_position_time": '2:00:30',
            "sleep_labels" : ["front standard", "shrimp is_raise_arm", "front cross_legs is_raise_arm", "right shrimp", "shrimp"] 
        }
            """,
        },
    ]

    # 결과 생성 요청 보내기
    result = generate_sleep_feedback(messages)

    # 결과를 HTML 템플릿에 전달하기
    feedback = result["choices"][0]["message"]["content"].replace("\n", "<br>")
    print(feedback)

    return templates.TemplateResponse(
        "gpt.html",
        {
            "request": request,
            "feedback": feedback,
        },
    )
