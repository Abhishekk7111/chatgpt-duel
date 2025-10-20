import streamlit as st
from openai import OpenAI
import time

# Initialize client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# App title
st.set_page_config(page_title="ChatGPT Duel", page_icon="⚔️")
st.title("🤖 ChatGPT Duel")
st.write("Two AI models discuss your topic, one logical and one creative. Sit back and enjoy!")

# User input
topic = st.text_input("💬 Enter a topic for the AI duel:", "Is AI good or bad for humanity?")
rounds = st.slider("Number of discussion rounds", 1, 5, 2)

if st.button("Start Duel"):
    if not topic.strip():
        st.warning("Please enter a valid topic!")
    else:
        st.subheader("⚔️ Duel Begins!")
        st.write(f"**Topic:** {topic}")
        st.markdown("---")

        ai1_last = topic
        for r in range(rounds):
            st.markdown(f"### 🧩 Round {r+1}")

            try:
                # --- AI 1: Logical responder ---
                resp1 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are ChatGPT 1, a logical and concise responder."},
                        {"role": "user", "content": ai1_last}
                    ],
                    temperature=0.7
                )
                ai1_msg = resp1.choices[0].message.content.strip()
                st.markdown(f"**🤖 ChatGPT 1:** {ai1_msg}")

                # Small pause to prevent rate limits
                time.sleep(2)

                # --- AI 2: Creative responder ---
                resp2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are ChatGPT 2, a creative and conversational responder."},
                        {"role": "user", "content": ai1_msg}
                    ],
                    temperature=0.8
                )
                ai2_msg = resp2.choices[0].message.content.strip()
                st.markdown(f"**🧠 ChatGPT 2:** {ai2_msg}")

                # Feed next round
                ai1_last = ai2_msg
                time.sleep(2)

            except Exception as e:
                # Friendly error message
                if "RateLimitError" in str(e):
                    st.error("⚠️ Rate limit reached! Please wait a minute or reduce the number of rounds.")
                elif "AuthenticationError" in str(e):
                    st.error("❌ Invalid API key! Please check your `.streamlit/secrets.toml` file.")
                else:
                    st.error(f"Unexpected error: {e}")
                break

        st.markdown("---")
        st.success("🏁 Duel complete!")

