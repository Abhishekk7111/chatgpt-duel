import streamlit as st
import os
from openai import OpenAI

# Streamlit app title
st.set_page_config(page_title="ChatGPT Duel 💬", page_icon="🤖")
st.title("🤖 ChatGPT Duel — Two AIs Discuss Your Question")

# Load API key from Streamlit Secrets
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API key not found. Please set it in Streamlit → Settings → Secrets.")
    st.stop()

# Initialize client
client = OpenAI(api_key=api_key)

# Ask user for input
prompt = st.text_input("💭 Enter your question for both AIs:")
rounds = st.slider("Number of discussion rounds", 1, 5, 2)

# When button clicked
if st.button("Start Duel"):
    if not prompt.strip():
        st.warning("Please enter a question first.")
        st.stop()

    st.info("⚙️ Starting discussion between ChatGPT 1 and ChatGPT 2...")

    # Initialize conversation
    conv = []
    ai1_last = prompt
    ai2_last = prompt

    # Run discussion loop
    for i in range(rounds):
        # ChatGPT 1 responds
        resp1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are ChatGPT 1, a logical and concise responder."},
                      {"role": "user", "content": ai2_last}],
            temperature=0.7
        )
        ai1_msg = resp1.choices[0].message.content.strip()
        conv.append(("ChatGPT 1", ai1_msg))

        # ChatGPT 2 responds
        resp2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are ChatGPT 2, a creative and conversational responder."},
                      {"role": "user", "content": ai1_msg}],
            temperature=0.8
        )
        ai2_msg = resp2.choices[0].message.content.strip()
        conv.append(("ChatGPT 2", ai2_msg))

        ai1_last, ai2_last = ai1_msg, ai2_msg

    # Display results
    st.success("✅ Discussion complete!")
    for who, text in conv:
        st.markdown(f"**{who}:** {text}")
