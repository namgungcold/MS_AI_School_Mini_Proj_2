import gradio as gr
import requests
import re


### GPT
def request_gpt(prompt,histories=[]):    
    endpoint = "your endpoint"
    headers = {
        "Content-Type" : "application/json",
        "api-key": "your key"
    }
    message_list = list()
    message_list.append({
        "role": "system",
        "content": [{
            "type" : "text",
            "text":"사용자가 정보를 찾는 데 도움이 되는 AI 도우미입니다."
        }
            
        ]
    })
    
    for history in histories:
        for text in history:
            message_list.append( {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": text
                }
            ]
            })
    message_list.append({
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                }
            ]
            },

    )
    payload = {
        "messages" : message_list,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
        
    } 
    response = requests.post(endpoint,headers=headers,json=payload)
    
    if response.status_code == 200:
        response_json = response.json()
        response_text = response_json['choices'][0]['message']['content']
        return response_text
    else:
        print(response.status_code, response.text)
        return response.text
    
def click_send(prompt, histories):
    response_text = request_gpt(prompt=prompt,histories=histories)
    histories.append([prompt,response_text]) ##튜플 대신 리스트형식으로 전달
    return histories,""

###SPEACH    
SPEECH_REGION = "eastus"
SPEECH_KEY = "your key"

def request_stt(file_path):
    endpoint=f"https://{SPEECH_REGION}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ko-KR&format=detailed"
    headers={
        "Ocp-Apim-Subscription-Key" : SPEECH_KEY,
        "Content-Type" : "audio/wav"
    }
    
    with open(file_path,"rb") as audio:
        audio_data = audio.read()

    response = requests.post(endpoint, headers=headers, data=audio_data)
    print(response.status_code, response.text)
    if response.status_code == 200:
        response_json = response.json()
        is_succeed = response_json["RecognitionStatus"] =="Success"
        if is_succeed:
            response_text = response_json["DisplayText"]
        else:
            response_text = ""
        return response_text
    else:
        return ""

def request_stt_fast(file_path):
    

    endpoint = "your endpoint"
    headers={
        "Ocp-Apim-Subscription-Key" : "your search key"
        
    }
    with open(file_path,"rb") as audio:
        audio_data = audio.read()
    json={
        
        "definition":'{ "locale":["ko-KR"], "profanityFilterMode" : "Masked", "channels": [0,1]}'
    }
    files ={
        "audio":audio_data
    }

    
    # print("Fast",response.status_code)
    response = requests.post(endpoint, headers=headers, json=json,files=files)
    if response.status_code == 200:
        response_json = response.json()
        response_text = response_json['combinedPhrases'][0]['text']
        print(response_text)
        return response_text
    else:
        "text"

def request_tts(text):
    endpoint=f"https://{SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers={
        "Ocp-Apim-Subscription-Key" : SPEECH_KEY,
        "Content-Type" : "application/ssml+xml",
        "X-Microsoft-OutputFormat" : "audio-16khz-128kbitrate-mono-mp3"
    }
    payloads=f"""
        <speak version='1.0' xml:lang='ko-KR'>
            <voice xml:lang='en-US' xml:gender='Female' name='ko-KR-SunHiNeural'>{text}</voice>
        </speak>
    """
    response = requests.post(endpoint, headers=headers, data=payloads)
    if response.status_code == 200:
        response.content

        with open("response_audio.wav","wb") as audio_file:
            audio_file.write(response.content)
            return "response_audio.wav"
        return
    
    else:    
        return response

def change_audio(file_path,radio):
    if file_path:
        print("file_path",file_path)
        if radio == "빠른 번역":
            response_text = request_stt_fast(file_path=file_path)
        else:
            response_text = request_stt(file_path=file_path)
        return response_text
    else:
        return ""
    
def click_tts_send(text):
    audio_file_name = request_tts(text)
    return audio_file_name

def change_chabot(histories):

    assistant_text = histories[-1][1]
    print(assistant_text)
    pattern = r'[^가-힣a-zA-Z0-9\s]'
    formatted_response_text = re.sub(pattern, '', assistant_text)
    audio_file_name = request_tts(formatted_response_text)
    return audio_file_name


with gr.Blocks() as demo:

    with gr.Row():
        #ChatGPT    
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="대화 기록")

            with gr.Row():
                input_openai_textbox = gr.Textbox(label="Prompt",scale=5)
                send_button = gr.Button("send",scale=1)

            chatbot_audio = gr.Audio(label="GPT", interactive=False, autoplay=True)  
            

        input_openai_textbox.submit(fn=click_send, inputs=[input_openai_textbox,chatbot],outputs=[chatbot,input_openai_textbox])
        send_button.click(fn=click_send, inputs=[input_openai_textbox,chatbot],outputs=[chatbot, input_openai_textbox]) ## output수정
        chatbot.change(fn=change_chabot, inputs=[chatbot], outputs=[chatbot_audio])
        
        #Speech
        with gr.Column(scale=1):
            with gr.Tab("STT") as stt:
                gr.Markdown("<h3>STT</h3>")
                input_mic = gr.Audio(label="마이크 입력",sources="microphone",type="filepath",waveform_options=gr.WaveformOptions(
                    waveform_color="#00FFFF",
                    waveform_progress_color="#FF00FF",
                    skip_length=2,
                    show_controls=False

                ))

                stt_type_radio = gr.Radio(["빠른 번역","일반 번역"],label="번역 타입",info="속도를 정해주세요",value="일반 번역")


                output_textbox = gr.Textbox(label="출력 테스트")
                input_mic.change(fn=change_audio,inputs=[input_mic,stt_type_radio],outputs=[input_openai_textbox])
        #TTS
            with gr.Tab("TTS") as tts:
                gr.Markdown("<h3>TTS</h3>")
                tts_input_textbox = gr.Textbox(label="입력 테스트",placeholder="음성으로 변환할 텍스트를 입력하세요.")
                send_tts_button = gr.Button("전송")
                output_tts_audio = gr.Audio(interactive=False)

                tts_input_textbox.submit(fn=click_tts_send,inputs=[tts_input_textbox],outputs=[output_tts_audio])
                send_tts_button.click(fn=click_tts_send,inputs=[tts_input_textbox],outputs=[output_tts_audio])
            




demo.launch()