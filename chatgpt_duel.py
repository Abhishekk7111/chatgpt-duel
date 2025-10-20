import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="ChatGPT Duel", layout="wide")
st.title("🤖 ChatGPT-1 vs ChatGPT-2 Debate")

# Use OpenAI key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

question = st.text_input("Ask any question:")
rounds = st.slider("Number of debate rounds:", 1, 5, 3)

if st.button("Start Debate") and question.strip() != "":
    chat1 = [{"role": "user", "content": question}]
    chat2 = [{"role": "user", "content": question}]

    col1, col2 = st.columns(2)
    with col1: st.subheader("ChatGPT-1")
    with col2: st.subheader("ChatGPT-2")

    for i in range(rounds):
        # ChatGPT-1 responds
        resp1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat1,
            temperature=0.7
        )
        reply1 = resp1.choices[0].message.content
        chat1.append({"role": "assistant", "content": reply1})
        chat2.append({"role": "user", "content": reply1})

        # ChatGPT-2 responds
        resp2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat2,
            temperature=0.7
        )
        reply2 = resp2.choices[0].message.content
        chat2.append({"role": "assistant", "content": reply2})
        chat1.append({"role": "user", "content": reply2})

        # Show debate side by side
        with col1: st.markdown(f"**Round {i+1}:** {reply1}")
        with col2: st.markdown(f"**Round {i+1}:** {reply2}")
