import streamlit as st
import asyncio
import nest_asyncio
from agents import create_startup_crew

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
                # إنشاء الـ Crew بالمخرجات المحددة
                crew = create_startup_crew(api_key, repo_url, repo_description)
                
                # تشغيل الـ Async بأمان تام لحل مشكلة الـ RuntimeError
                result = asyncio.run(crew.kickoff_async())
                
                st.success("🏆 Analysis Complete!")
                st.markdown("### 📊 Generated Strategy & Marketing Campaign")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")