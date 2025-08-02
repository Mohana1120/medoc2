import streamlit as st
import requests

st.set_page_config(page_title="AI Medical Prescription Verifier", layout="centered")
st.title("🩺 AI Medical Prescription Verifier")

text = st.text_area("📄 Paste Prescription Text", height=200)
age = st.number_input("🎂 Patient Age", min_value=1, max_value=120)

if st.button("Analyze"):
    with st.spinner("Analyzing Prescription..."):
        response = requests.post("http://localhost:8000/analyze/", json={"text": text, "age": age})
        
        if response.status_code != 200:
            st.error("❌ Failed to analyze prescription. Server error.")
        else:
            result = response.json()


            st.subheader("💊 Extracted Drugs")
            if result["drugs"]:
                for drug in result["drugs"]:
                    with st.container():
                        st.markdown(f"🧪 Drug Name:** {drug['drug'].title()}")
                        st.markdown(f"📝 Context:** {drug['context']}")
            else:
                st.info("No drugs extracted.")

    
            st.subheader("⚠ Drug Interaction Issues")
            if result["issues"]:
                for issue in result["issues"]:
                    st.error(f"🚫 {issue}")
            else:
                st.success("✅ No interaction issues found.")

            
            st.subheader("📌 Dosage Recommendations")
            if result["recommendations"]:
                for rec in result["recommendations"]:
                    st.success(f"💡 {rec}")
            else:
                st.info("No dosage recommendations.")
            st.subheader("🔁 Suggested Alternatives")
            if result["alternatives"]:
                for alt in result["alternatives"]:
                    st.info(f"🔄 {alt}")
            else:
                st.info("No alternatives suggested.")
