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

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Display chat history
    if st.session_state['chat_history']:
        st.write("チャット履歴:")
        for chat in st.session_state['chat_history']:
            st.write(f"**入力内容:** {chat['prompt']}")
            st.image(chat['image_url'], caption=chat['prompt'], use_column_width=True)
    
    # Input field for user prompt
    user_input = st.text_input(
        "画像生成または修正のプロンプトを入力してください。\n\n"
        "※1回の生成はたったの10円。\n\n"
        "※具体的な内容で入力した方が精度が高くなります。イラストの生成も可（例：日本人の黒髪ボブの25歳の女性 など）\n\n"
        "※入力した内容は学習されません。誤って送信してしまった場合も、情報漏洩の心配がありません。\n\n"
        "※生成した画像は商用利用が可能です。\n\n"
    )

    if st.button("送信"):
        if user_input:
            with st.spinner("画像生成中..."):
                combined_prompt = user_input if not st.session_state['chat_history'] else f"{st.session_state['chat_history'][-1]['prompt']} {user_input}"
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=combined_prompt,
                    n=1,
                    size="1024x1024",
                    style="vivid"
                )
                image_url = response.data[0].url
                st.session_state['chat_history'].append({
                    'prompt': user_input,  # Save the user input only
                    'image_url': image_url
                })
                st.image(image_url, caption=user_input, use_column_width=True)
        else:
            st.warning("入力してください。")
