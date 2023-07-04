import streamlit as st
import openai

st.title("엠파스봇의 이미지 생성기")
openai.api_key = st.secrets["apikey"]
with st.form("form"):
    user_input = st.text_input("간단한 이미지에 대한 설명을 적어주세요")
    image_size = st.selectbox("그림 크기를 선택하세요", ("1024x1024", "512x512", "256x256"))
    submit = st.form_submit_button("만들기")

    if submit and user_input:
        gpt_prompt = [
            {
                "role": "system",
                "content": "You are an art gallery docent with the unique ability to imagine and eloquently describe images based on simple words or phrases. Your goal is to portray these images in an artistic, picture-like style, creating a vivid mental image. Your descriptions should be concise, utilising rich vocabulary, and limited to approximately two sentences. Please respond in English.",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ]

        with st.spinner("이미지 생각 중..."):
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=gpt_prompt
            )

        image_prompt = gpt_response["choices"][0]["message"]["content"]

        # Translate English image prompt to Korean
        translation_prompt = [
            {
                "role": "system",
                "content": "You are a highly skilled translator capable of translating English to Korean. Please translate the following text.",
            },
            {
                "role": "user",
                "content": image_prompt,
            },
        ]

        with st.spinner("번역 중..."):
            translation_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=translation_prompt
            )

        image_prompt_korean = translation_response["choices"][0]["message"]["content"]

        st.write(image_prompt_korean)
        with st.spinner("그림 그리는중..."):
            dalle_response = openai.Image.create(prompt=image_prompt, size=image_size)

        st.image(dalle_response["data"][0]["url"])
