import streamlit as st
from auth import login, signup
from api_store import get_user_keys, save_user_keys, get_free_usage, increment_free_usage

# Dummy fallback keys for freemium users
FREE_OPENAI_KEY = "sk-your-test-openai-key"
FREE_DEEPSEEK_KEY = "your-test-deepseek-key"
FREE_LIMIT = 5

st.set_page_config(page_title="YouTube to Medium Article", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎥 YouTube to Medium Article")

# Auth
if not st.session_state.user:
    choice = st.radio("Welcome!", ["Login", "Sign Up"])
    if choice == "Login":
        login()
    else:
        signup()
    st.stop()

user_id = st.session_state.user["id"]
user_keys = get_user_keys(user_id)

# API Key Logic
if not user_keys:
    st.subheader("🔑 Choose API Key Option")
    use_personal = st.radio("How would you like to use the app?", ["Use my own API keys", "Use free plan (5 videos)"])

    if use_personal == "Use my own API keys":
        openai_key = st.text_input("OpenAI API Key", type="password")
        deepseek_key = st.text_input("DeepSeek API Key", type="password")
        if st.button("Save Keys"):
            save_user_keys(user_id, openai_key, deepseek_key)
            st.success("✅ Your keys have been saved!")
            st.experimental_rerun()
        st.stop()

    else:
        used = get_free_usage(user_id)
        if used >= FREE_LIMIT:
            st.warning("🚫 Free plan limit reached. Please enter your API keys to continue.")
            st.stop()
        else:
            st.info(f"✅ You have {FREE_LIMIT - used} free uses remaining.")
            openai_key = FREE_OPENAI_KEY
            deepseek_key = FREE_DEEPSEEK_KEY
            using_free_keys = True
else:
    openai_key = user_keys["openai_api_key"]
    deepseek_key = user_keys["deepseek_api_key"]
    using_free_keys = False

# App Ready to Use
st.success("🎉 You're ready to go!")

youtube_url = st.text_input("Paste YouTube Video URL")

if st.button("Convert to Medium Article"):
    if not youtube_url:
        st.warning("Please enter a YouTube URL.")
        st.stop()

    st.info("🔄 Transcribing and summarizing... (dummy for now)")

    # [Replace this with real transcription + summarization]
    article = f"""
    ✍️ **Sample Output**
    
    Medium-style summary of: {youtube_url}

    This is a placeholder. Real transcription and AI-based summarization will go here.
    """

    st.markdown(article)

    if using_free_keys:
        increment_free_usage(user_id)