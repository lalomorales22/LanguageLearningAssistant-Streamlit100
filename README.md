# Language Learning Assistant: AI-powered Conversational Practice

Language Learning Assistant is a Streamlit-based web application that provides AI-powered conversational practice for new languages. This interactive tool uses various language models to engage learners in conversations, offer corrections, and provide explanations to improve language skills.

## Features

- Interactive chat interface for practicing conversations in the target language
- Support for multiple AI models, including OpenAI's GPT models and Ollama's local models
- Customizable target language selection
- Adjustable proficiency levels (Beginner to Advanced)
- Dark/Light theme toggle
- Conversation saving and loading functionality
- Token usage tracking

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/language-learning-assistant.git
   cd language-learning-assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. (Optional) If you want to use Ollama models, make sure you have Ollama installed and running on your system.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run language_learning_assistant.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter your name, select your target language and proficiency level, and start practicing!

## Customization

- You can modify the `LANGUAGES` and `PROFICIENCY_LEVELS` lists in the code to add or remove languages and levels.
- The custom instructions for the AI can be adjusted in the sidebar of the application.

## Contributing

Contributions to improve the Language Learning Assistant are welcome! Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
