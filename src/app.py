import streamlit as st
import nest_asyncio
from agents import run_startup_strategy

# تفعيل الـ Async المتوافق مع الـ Web Apps والنوت بوك
nest_asyncio.apply()

# إعدادات الصفحة المظهرية
st.set_page_config(page_title="Universal Repo Strategy Engine", page_icon="🚀", layout="centered")

st.title("🚀 Universal Repository Strategy Engine")
st.caption("AMD Hackathon Act II — Powered by Fireworks AI & CrewAI")

st.markdown("---")

# صندوق إدخال مفتاح الـ API بشكل آمن
api_key = st.text_input("🔑 Enter Fireworks API Key", type="password", placeholder="fw_...")

# مدخلات المشروع
repo_url = st.text_input("📥 GitHub Repository URL", placeholder="https://github.com/...")
repo_description = st.text_area("📝 Project Description", placeholder="Describe what this project/startup does...")

if st.button("🔥 Run AI Strategy Crew", use_container_width=True):
    if not api_key:
        st.error("Please provide your Fireworks API Key.")
    elif not repo_url or not repo_description:
        st.error("Please fill in both the Repository URL and Description.")
    else:
        with st.spinner("🤖 Crew is collaborating... Analyzing repo and writing marketing copy..."):
            try:
                result = run_startup_strategy(api_key, repo_url, repo_description)

                st.success("🏆 Analysis Complete!")
                st.markdown("### 📊 Generated Strategy & Marketing Campaign")

                tab1, tab2, tab3 = st.tabs(["📌 Project Summary", "📣 Marketing Posts", "🚀 Growth Strategy"])

                with tab1:
                    st.markdown(result["summary"])

                with tab2:
                    st.markdown(result["marketing_posts"])

                with tab3:
                    st.markdown(result["growth_strategy"])

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")