from openai import OpenAI
import streamlit as st

client = OpenAI()
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    st.title("FCC内部用 DALL-E3 画像生成")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'input_key' not in st.session_state:
        st.session_state['input_key'] = 0

    if st.session_state['chat_history']:
        st.write("チャット履歴:")
        for chat in st.session_state['chat_history']:
            st.write(f"**入力内容:** {chat['prompt']}")
            st.image(chat['image_url'], caption=chat['prompt'], use_column_width=True)
    
    user_input = st.text_input(
        "画像生成したい内容を入力してください。\n\n"
        "画像生成後に追加で入力すると、入力内容を保持したまま次の画像が生成されます。\n\n"
        "※1回の生成はたったの10円。\n\n"
        "※具体的な内容で入力した方が精度が高くなります。（例：公園を散歩する黒髪ボブの25歳の女性 など）\n\n"
        "※イラストの生成も可能です。\n\n"
        "※入力した内容は公開されません。誤って送信してしまった場合も、情報漏洩の心配がありません。\n\n"
        "※生成した画像は商用利用が可能です。\n\n",
        key=f"user_input_{st.session_state['input_key']}"
    )

    if st.button("送信"):
        if user_input:
            with st.spinner("画像生成中..."):
                try:
                    # 以前の全てのプロンプトを結合して新しいユーザー入力を追加
                    combined_prompt = ' '.join(chat['prompt'] for chat in st.session_state['chat_history']) + ' ' + user_input
                    
                    # プロンプトに以下のワードが含まれている場合、「日本人の」を先頭に追加、その他の場合「日本の」を追加
                    if any(word in user_input for word in [ "女", "姉","おばさん", "乙女", "lady", "男", "おじさん", "兄", "man", "human", "人", "キャラクター"]):
                        final_prompt = "日本人の " + combined_prompt
                    else:
                        final_prompt = "日本の " + combined_prompt

                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=final_prompt,
                        n=1,
                        size="1024x1024",
                        style="vivid",
                        quality="standard"
                    )
                    image_url = response.data[0].url
                    st.session_state['chat_history'].append({
                        'prompt': user_input,
                        'image_url': image_url
                    })
                    st.image(image_url, caption=user_input, use_column_width=True)
                    
                    st.session_state['input_key'] += 1
                    st.experimental_rerun()
                except Exception as e:
                    if 'content_policy_violation' in str(e):
                        st.error("申し訳ありませんが、入力された内容が安全システムによって許可されませんでした。入力内容を調整して再試行してください。")
                    else:
                        st.error(f"エラーが発生しました: {str(e)}")
                    st.info("入力内容を調整するか、しばらく待ってから再試行してください。")
        else:
            st.warning("入力してください。")
