# MS_AI_School AI Search Project_2
본 프로젝트는 `MS Azure`를 활용하여 시행함,MS_AI_School AI Search Project_1에 이어서 추가적으로 만든 Project이다. <br>

## Data and Function
- **Data:**
  - `공공데이터포털`에 있는 '한국 농어촌 공사_계절테마여행정보.csv'를 활용한다.
  -  주제, 태그, 요약, 코스정보 등의 컬럼들이 존재한다.
  -  Data들을 Azure에서 저장 후 AI Search sercive에서 인덱스와 인덱서를 처리한다.
  -  음성 플레이그라운드를 통해 STT와 TTS를 할 수 있는 기능의 엔드포인트를 사용한다.
    
- **Function:**
  - GPT-4o를 사용하는 챗봇 기능을 한다.
  - 위 데이터를 `Fine-Tuning`하여 테마나 각 도를(ex. 경상북도, 전라남도, 강원도 등)입력하면 테마가 있는 여행을 추천한다.
  - STT에선 `record`를 누르고 원하는 메세지를 말하면 `prompt`로 그 문장이 넘어간다.
  - send 버튼을 누르면 메세지는 전송되고 답변 음성으로 읽어준다.
  - TTS는 메세지를 입력하면 음성으로 읽어준다.<br>
![1129_proj](https://github.com/user-attachments/assets/a4f4d56a-2a02-40c5-b70f-f8b197cf8146)


