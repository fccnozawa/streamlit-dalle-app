from openai import OpenAI
client = OpenAI()
import streamlit as st

# Set your OpenAI API key from Streamlit secrets
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

# Simple password authentication
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Remove password from the session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    st.title("FCC内部用 DALL-E3 画像生成")

    if 'image_url' not in st.session_state:
        st.session_state['image_url'] = None
    if 'prompt' not in st.session_state:
        st.session_state['prompt'] = None

    prompt = st.text_input("生成したい画像の内容を入力してください。\n\n※1回の生成はたったの10円。\n\n※具体的な内容で入力した方が精度が高くなります。（例：黒髪ボブの24歳の女性 など）\n\n※入力した内容は学習されません。誤って送信してしまった場合も、情報漏洩の心配がありません。\n\n※生成した画像は商用利用が可能です。\n\n")

    if st.button("画像を生成する"):
        if prompt:
            with st.spinner("画像生成中..."):
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                    style="vivid"
                )
                image_url = response.data[0].url
                st.session_state['image_url'] = image_url
                st.session_state['prompt'] = prompt
                st.image(image_url, caption=prompt)
        else:
            st.warning("入力してください。")

    if st.session_state['image_url']:
        st.write("画像の修正を行うための新しいプロンプトを入力してください。")
        modify_prompt = st.text_input("修正したい内容を入力してください。")

        if st.button("画像を修正する"):
            if modify_prompt:
                combined_prompt = st.session_state['prompt'] + " " + modify_prompt
                with st.spinner("画像再生成中..."):
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=combined_prompt,
                        n=1,
                        size="1024x1024",
                        style="vivid"
                    )
                    modified_image_url = response.data[0].url
                    st.session_state['image_url'] = modified_image_url
                    st.session_state['prompt'] = combined_prompt
                    st.image(modified_image_url, caption=modify_prompt)
            else:
                st.warning("修正する内容を入力してください。")
