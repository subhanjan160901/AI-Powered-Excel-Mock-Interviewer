<!-- ---
title: Personal Excel Interviewer
emoji: 🐨
colorFrom: green
colorTo: red
sdk: gradio
sdk_version: 5.39.0
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference -->

🤖 AI-Powered Excel Interviewer

This repository contains the source code for an advanced, AI-powered conversational agent designed to conduct technical interviews for Excel skills. The system uses a state machine built with LangGraph to manage the interview flow, evaluates answers with a local Phi-3 model, and includes a perplexity-based check to detect AI-generated responses.

![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Live%20Demo-yellow)
![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)


⭐ Features :
1. Conversational Interview Flow: Engages users in a natural, turn-by-turn conversation.

2. Dynamic Questioning: Asks a predefined set of questions in sequence.

3. AI-Powered Evaluation: Uses a local microsoft/phi-3-mini-4k-instruct model to provide real-time, nuanced feedback on the user's answers.

4. AI Plagiarism Detection: Integrates a perplexity check using a gpt-2 model to flag answers that are likely machine-generated, ensuring authentic responses.

5. Stateful Logic with LangGraph: The entire interview process is orchestrated by a robust state machine, making the logic easy to understand and extend.

6. Final Performance Report: At the end of the interview, the AI generates a comprehensive summary of the user's strengths and areas for improvement.

7. Modern & Responsive UI: Built with Gradio Blocks for a clean, intuitive, and mobile-friendly user experience.

🛠️ Tech Stack & Architecture:

The application uses a modern stack to separate the UI, logic, and AI model layers effectively.


    graph TD
        subgraph Frontend
            A[User Interface (Gradio Blocks)]
        end
        
        subgraph Backend Logic
            B(app.py) -- Manages UI events & state --> C{Stateful Graph (LangGraph)}
        end
    
        subgraph LangGraph Nodes
            C -- Routes to --> D[1. start_interview]
            C -- Routes to --> E[2. process_user_response]
            C -- Routes to --> F[3. ask_question]
            C -- Routes to --> G[4. generate_final_report]
        end
        
        subgraph AI Models
            H[Evaluation & Reporting (Phi-3 Mini)]
            I[Perplexity Detection (GPT-2)]
        end
        
        E -- Uses --> H
        E -- Uses --> I
        G -- Uses --> H
    
        A -- Interacts with --> B


    
🚀 Setup and Running Locally:

Follow these steps to get the application running on your own machine -

1. Prerequisites
Python 3.10 or higher
Git
2. Clone the Repository
git clone https://huggingface.co/spaces/Basu03/personal_excel_interviewer
cd personal_excel_interviewer
3. Create a Virtual Environment (Recommended)
# For Windows
python -m venv venv

venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv

source venv/bin/activate

4. Install Dependencies
   
The requirements.txt file is optimized to ensure torch is installed first and uses library versions known to be compatible with the AI models.

pip install -r requirements.txt

5. Run the Application
python app.py

Note: The very first time you run the app, it will download the AI models (~8 GB in total). This may take several minutes depending on your internet connection. The --- All models pre-loaded successfully --- message will appear in your terminal when it's ready. Subsequent startups will be much faster as the models will be cached.

⚙️ Configuration

You can easily customize the interview by modifying:

The Questions: Edit the EXCEL_QUESTIONS list in src/interview_logic.py.

The AI Detection Threshold: Change the threshold value in the is_ai_generated function call inside src/interview_logic.py. A lower value makes the detection more strict.

The AI Models: Update the model names in src/local_llm_handler.py and src/perplexity_detector.py to experiment with different language models.

📄 License:

This project is licensed under the MIT License. See the LICENSE file for details.
