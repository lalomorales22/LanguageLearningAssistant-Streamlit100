import streamlit as st
import ollama
import time
import json
import os
from datetime import datetime
from openai import OpenAI

# List of available models
MODELS = [
    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo",  # OpenAI models
    "llama3.1:8b", "gemma2:2b", "mistral-nemo:latest", "phi3:latest",  # Ollama models
]

# Languages and proficiency levels
LANGUAGES = [
    "Spanish", "French", "German", "Italian", "Chinese", "Japanese",
    "Korean", "Russian", "Arabic", "Portuguese"
]

PROFICIENCY_LEVELS = ["Beginner", "Elementary", "Intermediate", "Upper Intermediate", "Advanced"]

def get_ai_response(messages, model):
    if model.startswith("gpt-"):
        return get_openai_response(messages, model)
    else:
        return get_ollama_response(messages, model)

def get_openai_response(messages, model):
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def get_ollama_response(messages, model):
    try:
        response = ollama.chat(
            model=model,
            messages=messages
        )
        return response['message']['content'], response['prompt_eval_count'], response['eval_count']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def stream_response(messages, model):
    if model.startswith("gpt-"):
        return stream_openai_response(messages, model)
    else:
        return stream_ollama_response(messages, model)

def stream_openai_response(messages, model):
    client = OpenAI()
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def stream_ollama_response(messages, model):
    try:
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def save_conversation(messages, filename):
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    os.makedirs('conversations', exist_ok=True)
    file_path = os.path.join('conversations', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                conversations = json.load(f)
        else:
            conversations = []
    except json.JSONDecodeError:
        conversations = []
    
    conversations.append(conversation)
    
    with open(file_path, 'w') as f:
        json.dump(conversations, f, indent=2)

def load_conversations(uploaded_file):
    if uploaded_file is not None:
        try:
            conversations = json.loads(uploaded_file.getvalue().decode("utf-8"))
            return conversations
        except json.JSONDecodeError:
            st.error(f"Error decoding the uploaded file. The file may be corrupted or not in JSON format.")
            return []
    else:
        st.warning("No file was uploaded.")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("Language Learning Assistant: AI-powered Conversational Practice")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "token_count" not in st.session_state:
        st.session_state.token_count = {"prompt": 0, "completion": 0}

    if "user_name" not in st.session_state:
        st.session_state.user_name = "Learner"

    st.session_state.user_name = st.text_input("Enter your name:", value=st.session_state.user_name)

    st.sidebar.title("Language Learning Options")
    model = st.sidebar.selectbox("Choose a model", MODELS)

    custom_instructions = st.sidebar.text_area("Custom Instructions", 
        """You are a helpful Language Learning Assistant AI. Your role is to engage in conversational practice with language learners, helping them improve their skills in their target language. You should adapt your language use to the learner's proficiency level, provide corrections when appropriate, and offer explanations about language usage.

Your capabilities include:
1. Engaging in conversations in the target language
2. Providing translations and explanations of words and phrases
3. Correcting grammar and pronunciation errors
4. Offering cultural context and idiomatic expressions
5. Adapting conversation topics to the learner's interests
6. Suggesting exercises and activities for further practice

When interacting:
- Use the target language primarily, with explanations in the learner's native language when necessary
- Adjust your language complexity to match the learner's proficiency level
- Provide gentle corrections and explanations for errors
- Encourage the learner to express themselves and take conversational risks
- Offer positive reinforcement and motivation
- Introduce new vocabulary and grammatical structures gradually

Remember, your goal is to create a supportive and engaging environment for language practice, helping learners build confidence and fluency in their target language.""")

    target_language = st.sidebar.selectbox("Choose target language", LANGUAGES)
    proficiency_level = st.sidebar.selectbox("Select proficiency level", PROFICIENCY_LEVELS)

    theme = st.sidebar.selectbox("Choose a theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.token_count = {"prompt": 0, "completion": 0}

    st.sidebar.subheader("Conversation Management")
    save_name = st.sidebar.text_input("Save conversation as:", f"{target_language.lower()}_practice_session.json")
    if st.sidebar.button("Save Conversation"):
        save_conversation(st.session_state.messages, save_name)
        st.sidebar.success(f"Conversation saved to conversations/{save_name}")

    st.sidebar.subheader("Load Conversation")
    uploaded_file = st.sidebar.file_uploader("Choose a file to load conversations", type=["json"], key="conversation_uploader")
    
    if uploaded_file is not None:
        try:
            conversations = load_conversations(uploaded_file)
            if conversations:
                st.sidebar.success(f"Loaded {len(conversations)} conversations from the uploaded file")
                selected_conversation = st.sidebar.selectbox(
                    "Select a conversation to load",
                    range(len(conversations)),
                    format_func=lambda i: conversations[i]['timestamp']
                )
                if st.sidebar.button("Load Selected Conversation"):
                    st.session_state.messages = conversations[selected_conversation]['messages']
                    st.sidebar.success("Conversation loaded successfully!")
            else:
                st.sidebar.error("No valid conversations found in the uploaded file.")
        except Exception as e:
            st.sidebar.error(f"Error loading conversations: {str(e)}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Start chatting in {target_language}:"):
        st.session_state.messages.append({"role": "user", "content": f"{st.session_state.user_name}: {prompt}"})
        with st.chat_message("user"):
            st.markdown(f"{st.session_state.user_name}: {prompt}")

        language_instruction = f"Converse in {target_language}. "
        level_instruction = f"Adapt language to {proficiency_level} level. "
        ai_messages = [
            {"role": "system", "content": custom_instructions + language_instruction + level_instruction},
            {"role": "system", "content": "Remember to provide gentle corrections, introduce new vocabulary gradually, and offer cultural context when appropriate."},
        ] + st.session_state.messages

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in stream_response(ai_messages, model):
                if chunk:
                    if model.startswith("gpt-"):
                        full_response += chunk.choices[0].delta.content or ""
                    else:
                        full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

        _, prompt_tokens, completion_tokens = get_ai_response(ai_messages, model)
        st.session_state.token_count["prompt"] += prompt_tokens
        st.session_state.token_count["completion"] += completion_tokens

    st.sidebar.subheader("Token Usage")
    st.sidebar.write(f"Prompt tokens: {st.session_state.token_count['prompt']}")
    st.sidebar.write(f"Completion tokens: {st.session_state.token_count['completion']}")
    st.sidebar.write(f"Total tokens: {sum(st.session_state.token_count.values())}")

if __name__ == "__main__":
    main()