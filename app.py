import openai
import gradio

# OpenAI API 키를 입력하는 부분
openai.api_key = "xxxxxx"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

# Textbox에 사용되는 prompt의 내용을 작성하는 부분
# prompt를 통해 ChatGPT의 대화 특성을 설정할 수 있음
prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt):
    # ChatGPT로부터 원하는 응답을 받을 수 있도록 속성을 설정하는 부분
    response = openai.Completion.create(
    # 제공되는 여러 모델 중 ChatGPT 3.5를 선택하는 부분
    model="text-davinci-003",
    # ChatGPT에 입력(Prompt)을 전달하는 부분
    prompt=prompt,
    # 0 ~ 1 값을 가질 수 있으며, 값이 높을수록 창의적인 응답을 하게 됨
    temperature=0.9,
    # ChatGPT의 정보 단위
    # ChatGPT가 기억하는 token의 개수를 설정하는 부분
    max_tokens=150,
    # 문맥을 기반으로 다음에 등장할 단어를 예측하는 부분
    # 0 ~ 1 값을 가질 수 있으며, 값이 높을수록 다양한 응답을 하게 됨
    top_p=1,
    # 이전 대화에서 더 자주 나타나는 단어를 피하는 정도를 지정하는 부분
    frequency_penalty=0,
    # 이전 대화에 등장하지 않은 단어나 구문을 피하는 정도를 지정하는 부분
    presence_penalty=0.6,
    # ChatGPT가 응답 생성을 중단해야 하는 지시어를 지정하는 부분
    stop=[" Human:", " AI:"]
    )

    # ChatGPT의 응답을 반환하는 부분
    return response.choices[0].text

# ChatGPT 모델의 응답을 생성하고 기록하는 기능을 제공합니다.
def chatgpt_clone(input, history):
    # 이전 대화 기록을 나타내는 매개변수입니다. 이전 대화 기록이 제공되지 않은 경우, history를 빈 리스트로 초기화합니다.
    history = history or []
    # 이전 대화 기록(history)을 모두 하나의 리스트로 합칩니다.
    s = list(sum(history, ()))
    # 입력 문장(input)을 s 리스트에 추가합니다.
    s.append(input)
    # 리스트의 모든 요소를 공백으로 구분하여 하나의 문자열로 결합합니다.
    inp = ' '.join(s)
    # ChatGPT의 응답을 받습니다.
    output = openai_create(inp)
    # history에 input과 ChatGPT의 응답을 모두 넣어 모든 응답을 기억하도록 함
    history.append((input, output))
    print(input, output, history)
    return history, history


# Gradio의 Blocks 객체를 생성합니다. 이 객체는 코드 블록을 정의하고 관리하는 데 사용됩니다.
block = gradio.Blocks()


with block:
    # 마크다운 문법을 통해 웹 앱 화면의 텍스트를 설정하는 부분
    gradio.Markdown("""<h1><center>니만의 GPT 챗봇</center></h1>""")
    # Gradio에서 제공하는 ChatBot GUI
    chatbot = gradio.Chatbot()
    # ChatGPT에 입력을 넣는 텍스트 박스를 정의하는 코드
    # placeholder를 통해 텍스트 박스에 사전에 작성한 prompt를 띄움
    message = gradio.Textbox(placeholder=prompt)
    # 데이터가 유지될 수 있도록 하는 State
    state = gradio.State()
    # SEND라고 쓰여 있는 submit 버튼을 만드는 부분
    submit = gradio.Button("SEND")
    # send 버튼이 클릭되었을 때 chatgpt_clone 함수가 호출되며,
    # chatgpt_clone의 매개변수인 input, history에 inputs와 outputs가 들어감
    # state를 input, output에 넣으면 데이터를 유지할 수 있음
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

# debug 모드로 로컬에서 웹을 실행
# 에러 메세지를 확인할 수 있음
block.launch(debug=True)

# 72시간동안 웹을 배포하는 share 옵션
# block.launch(share=True)