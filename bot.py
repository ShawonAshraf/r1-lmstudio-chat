import openai
import streamlit as st
from loguru import logger

ENDPOINT = "http://localhost:1234/v1"
MODEL = "deepseek-r1-distill-qwen-7b"
DEBUG = True
if not DEBUG:
    logger.info("Disabled Logging")
    logger.remove()

def format_response(raw_response):
    # separate the answer and the thought process
    parts = raw_response.split("</think>")

    assert len(parts) == 2

    thought = parts[0]
    # remove the remaining think tag
    thought = thought.replace("<think>", "").strip()

    answer = parts[1]
    # remove if there's an "Answer:" part
    answer = answer.replace("Answer:", "").strip()

    logger.debug(f"Thought: {thought}")
    logger.debug(f"Answer: {answer}")

    return thought, answer


def generate_response(user_prompt, model=MODEL, endpoint=ENDPOINT, api_key="lm-studio"):
    # init oai client
    client = openai.Client(
        base_url=endpoint,
        api_key=api_key
    )

    logger.debug(f"User: {user_prompt}")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.1
    )

    # format response
    raw_response = response.choices[0].message.content
    logger.debug(f"Raw: {raw_response}")

    cleaned = format_response(raw_response)

    return cleaned

def chatbot():
    st.title("AGI But Dumb")

    # session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # get user prompt and generate response
    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # put the thought process inside a collapsed element
        with st.status("Reasoning"):
            thought, ans = generate_response(prompt)
            if thought:
                st.markdown(thought)
            else:
                st.markdown("**You think an AGI like me has to think twice to answer this? huh!**")

        # separate element for answer
        with st.chat_message("assistant"):
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans, "thought": thought})


def main():
    chatbot()



if __name__ == "__main__":
    main()
