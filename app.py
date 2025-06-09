import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="InstaPitch - AI Startup Pitch Coach", layout="wide")
st.title("🚀 InstaPitch – Your Instant Startup Pitch Coach")

# Session state setup
if "qa_round" not in st.session_state:
    st.session_state.qa_round = 0

st.markdown("""
### 🎯 Purpose:
Many aspiring entrepreneurs have ideas but struggle to present them well. InstaPitch helps you craft and refine your startup pitch using AI.
""")

st.subheader("🔤 Step 1: Enter Your Startup Idea")

with st.form("idea_input_form"):
    problem = st.text_area("🔻 Problem", max_chars=500)
    solution = st.text_area("🧩 Solution", max_chars=500)
    audience = st.text_input("🎯 Target Audience")
    business_model = st.text_input("💸 Business Model")
    market_size = st.text_input("📈 Market Size (Optional)")
    competitors = st.text_input("🤼 Competitors (Optional)")
    submitted = st.form_submit_button("Generate Elevator Pitch")

if submitted:
    idea_prompt = f"""
You are a startup mentor. Based on the following inputs, write a 1-minute elevator pitch with:
- A strong hook
- Mission statement
- Key differentiator
- Call to action

Inputs:
Problem: {problem}
Solution: {solution}
Target Audience: {audience}
Business Model: {business_model}
Market Size: {market_size}
Competitors: {competitors}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": idea_prompt}]
    )

    pitch = response['choices'][0]['message']['content']
    st.success("✅ Here's your AI-generated elevator pitch:")
    st.markdown(f"""```text\n{pitch}```""")

    st.session_state['user_pitch'] = pitch

    # Persona Selection
    persona = st.selectbox("🎭 Choose Investor Persona", [
        "Tech VC", "Social Impact Funder", "Angel Investor", "Shark Tank-style Tough Investor", "Government/Incubator Reviewer"])

    if st.button("🎯 Refine Pitch for Persona"):
        persona_prompt = f"Rewrite this pitch to appeal to a {persona} investor:\n\n{pitch}"
        persona_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": persona_prompt}]
        )
        refined_pitch = persona_response['choices'][0]['message']['content']
        st.markdown("### 🎯 Persona-Aligned Pitch")
        st.markdown(f"""```text\n{refined_pitch}```""")
        st.session_state['refined_pitch'] = refined_pitch

    if st.button("❓ Simulate Investor Q&A"):
        q_prompt = f"Act as a {persona}. Ask 3 challenging questions about the following startup pitch:\n\n{st.session_state.get('refined_pitch', pitch)}"
        q_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": q_prompt}]
        )
        questions = q_response['choices'][0]['message']['content']
        st.markdown("### ❓ Investor Questions")
        st.markdown(f"""```text\n{questions}```""")

    if st.button("✅ Score My Pitch"):
        score_prompt = f"Rate this pitch for Clarity, Innovation, Business Viability, and Scalability. Then give improvement tips:\n\n{pitch}"
        score_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": score_prompt}]
        )
        score = score_response['choices'][0]['message']['content']
        st.markdown("### 📊 Pitch Score & Improvement Tips")
        st.markdown(f"""```text\n{score}```""")

st.markdown("---")
st.markdown("💡 *Built with Streamlit and GPT-4. Extend this further by adding PowerPoint or PDF exports, LangChain prompt chaining, or pitch deck visuals.*")
