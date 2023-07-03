import gradio as gr

def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    greet_btn = gr.Button("Greet")
    # greet_btn이 클릭되었을 때, name을 인자로 greet 함수를 실행하고,
    # greet 함수의 결과값을 Output Box를 통해 출력
    greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")

# 로컬에서 웹을 실행
demo.launch()