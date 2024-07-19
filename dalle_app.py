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
    st.title("DALL-E Image Generator")

    prompt = st.text_input("Enter a prompt for DALL-E:")

    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                response = client.images.generate(
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = response['data'][0]['url']
                st.image(image_url, caption=prompt)
        else:
            st.warning("Please enter a prompt!")
