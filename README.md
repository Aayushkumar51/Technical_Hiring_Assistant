TalentScout
Streamlit App

Access the live deployed app here: https://talentscout-dhruv0126.streamlit.app/

TalentScout AI Interview Assistant 🤖
An AI-powered interview platform that generates personalized technical questions using Groq's Llama 3.1 model, designed to streamline technical candidate assessments.

🚀 Key Features
AI-Powered Question Generation Dynamic interview questions based on candidate skills and experience
Tech Stack Declaration Multi-category skill selection across 5 technical domains
Interactive Chat Interface
Real-time interview simulation with conversation logging
Session Recording
Automatic JSON export of complete interview sessions
Smart Exit System Natural language commands to end sessions (exit/quit/bye)
⚙️ Installation
Clone repository:
git clone https://github.com/yourusername/talentscout-ai.git
cd talentscout-ai
Install dependencies:
pip install -r requirements.txt
Configure environment:
echo "GROQ_API_KEY=your_api_key_here" > .env
🎯 Usage
Start the application:
streamlit run Sample.py
In the browser:
Fill candidate information
Select technical skills
Click Start Interview Chat
Interview flow:
AI generates 5 personalized questions
Answer questions in chat interface
Session auto-saves when complete
🔧 Configuration
Environment Variables
GROQ_API_KEY=sk-your-api-key-here  # Get from Groq Cloud
Customize Skill Categories
Modify skill_categories in TalentScoutGroq class:

self.skill_categories = {
    'New Category': ['Skill1', 'Skill2'],
    # ... existing categories
}
🛠️ Technologies Used
Core AI: Groq LPU + Llama-3.1-8b-instant
Framework: Streamlit 🎈
LangChain: Prompt templating & chain construction
Data Handling: JSON interview logging
Security: Dotenv configuration
🙏 Acknowledgments
Groq for their revolutionary inference engine
Streamlit for interactive web framework
LangChain team for LLM integration patterns
