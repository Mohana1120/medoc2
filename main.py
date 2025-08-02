import streamlit as st
import requests

st.set_page_config(page_title="AI Medical Prescription Verifier", layout="centered")
st.title("🩺 AI Medical Prescription Verifier")

text = st.text_area("📄 Paste Prescription Text", height=200)
age = st.number_input("🎂 Patient Age", min_value=1, max_value=120)

if st.button("Analyze"):
    if not text:
        st.warning("Please enter a prescription.")
    else:
        with st.spinner("Analyzing Prescription..."):
            try:
                res = requests.post("http://localhost:8000/analyze/", json={"text": text, "age": age})
                if res.status_code != 200:
                    st.error("❌ Failed to analyze prescription.")
                else:
                    data = res.json()

                    st.subheader("💊 Extracted Drugs")
                    if data["drugs"]:
                        for drug in data["drugs"]:
                            st.markdown(f"**🧪 Drug:** `{drug['drug']}`")
                            st.markdown(f"**📝 Context:** {drug['context']}")
                    else:
                        st.info("No drugs found.")

                    st.subheader("⚠️ Drug Interaction Issues")
                    if data["issues"]:
                        for issue in data["issues"]:
                            st.error(f"🚫 {issue}")
                    else:
                        st.success("✅ No interaction issues.")

                    st.subheader("📌 Dosage Recommendations")
                    if data["recommendations"]:
                        for rec in data["recommendations"]:
                            st.success(f"💡 {rec}")
                    else:
                        st.info("No dosage recommendations.")

                    st.subheader("🔁 Suggested Alternatives")
                    if data["alternatives"]:
                        for alt in data["alternatives"]:
                            st.info(f"🔄 {alt}")
                    else:
                        st.info("No alternatives suggested.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
