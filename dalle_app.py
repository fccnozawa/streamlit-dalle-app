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
    st.title("FCC内部用 DALL-e3 画像生成")

    prompt = st.text_input("生成したい画像の内容を入力してください。")

    if st.button("画像を生成する"):
        if prompt:
            with st.spinner("画像生成中..."):
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = response.data[0].url
                st.image(image_url, caption=prompt)
        else:
            st.warning("入力して！")
