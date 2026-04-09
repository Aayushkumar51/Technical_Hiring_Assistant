import streamlit as st
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import json 
import re
from langchain_core.runnables import RunnableSequence
#load api key 
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


#custom CSS for tech-themed design
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)



#load custom css
local_css("style.css")



class TalentScoutGroq:
    def __init__(self):
        self.skill_categories= {
             'Software Development': ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'Go', 'Rust', 'TypeScript', 'Swift'],
            'Web Development': ['React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring Boot', 'ASP.NET Core'],
            'Cloud & DevOps': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 'Terraform'],
            'Data Science & AI': ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Scikit-learn', 'Keras', 'langchain', 'langgraph'],
            'Mobile Development': ['Android', 'iOS', 'React Native', 'Flutter', 'Kotlin', 'Swift']






        }
        #Updated prompt template using 'desired_position'
        self.question_prompt=PromptTemplate(
            input_variables=['desired_position', 'skills', 'experience'],
            template=(
                "Generate exactly five interview questions for a candidate applying for {desired_position} "
                "with {experience} years of experience.\n"
                "Skills: {skills}\n\n"
                "Output the result as a JSON array of objects. Each object must have two keys: "
                "'id' (an integer starting at 1) and 'question' (the text of the question).\n"
                "Ensure that the output is valid JSON and nothing else."



            )



        )
        self.llm=ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=0.7
        )

    def generate_ai_interview_questions(self, candidate):
        skill_str=', '.join(candidate.get('skills', [])) #convert ['a','b','c'] into ['a,b,c']
        chain=self.question_prompt | self.llm


        inputs = {
            "desired_position": candidate.get('desired_position', ''),
            'skills': skill_str,
            'experience': str(candidate.get('experience', 0))




        }

        try:
            response = chain.invoke(inputs)
            response_text = response.content if hasattr(response, 'content') else str(response)
            json_match = re.search(r'(\[.*\])', response_text, re.DOTALL)
            json_str = json_match.group(1) if json_match else response_text
            questions = json.loads(json_str)
            return questions[:5] if isinstance(questions, list) else [] #isinsatnce check wheater a question is list or not
        except json.JSONDecodeError:
            return []
        
    
    
    
    
    def save_interview_results(self, candidate, questions, conversation):
        results = {"candidate": candidate, "question": questions, "conversation": conversation}
        filename= f"interview_results_{candidate.get('name','candidate')}.json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        st.success(f"Interview results saved to {filename}")

    '''Take candidate data
       ↓
       Create dictionary
       ↓
       Generate filename
       ↓
       Open file
       ↓
       Save as JSON
       ↓
       Show success message'''
    


    def run_streamlit_app(self):
        st.markdown(
            '''

            <style>
             .gradient-title {
                font-size: 2.8rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 0.5em;
                background: linear-gradient(270deg, #7C4DFF, #8F00FF, #563C5C, #00FFEA, #FF61A6, #7C4DFF);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                color: transparent;
                text-shadow: 0 2px 8px rgba(44,0,60,0.18);
                animation: gradientMove 4s ease-in-out infinite;
            }
            @keyframes gradientMove {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
            </style>
            ''',
            unsafe_allow_html=True


        )
        # Sidebar with instructions
        st.sidebar.title("Instructions")
        st.sidebar.markdown(
            "Fill in your details, select your skills, and click **Start Interview Chat**. \n\n"
            "During the interview, if you wish to exit, simply type **exit**, **quit**, or **bye** in the chat input."
        )

        st.markdown(
            """
            <div style="background: linear-gradient(90deg, #563C5C 0%, #7C4DFF 100%); padding: 16px; border-radius: 12px; margin-bottom: 1.5em; text-align:center;">
                <h2 style="color: #FFFFFF; font-size: 2rem; font-weight: 600; margin-bottom: 0.2em;">Welcome to <span style='color:#7C4DFF;'>TalentScout AI</span></h2>
                <p style="color: #F3EFFF; font-size: 1.1rem;">Your AI-powered interview assistant.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Candidate Information Form
        with st.container():
            st.header("Candidate Information")
            candidate = {
                'name': st.text_input("Full Name", placeholder="Enter your full name"),
                'email': st.text_input("Email Address", placeholder="Enter your email"),
                'phone': st.text_input("Phone Number", placeholder="Enter your phone number"),
                'experience': st.number_input("Years of Experience", min_value=0, max_value=50, value=0),
                'desired_position': st.text_input("Desired Position(s)", placeholder="Enter your desired position(s)"),
                'current_location': st.text_input("Current Location", placeholder="Enter your current location"),
                'skills': []
            }
        
        # Tech Stack Selection
        with st.container():
            st.header("Tech Stack Declaration")
            for category, skills in self.skill_categories.items():
                st.subheader(category)
                selected = st.multiselect(f"Select {category} Skills", skills)
                candidate['skills'].extend(selected)
        
        # Start Interview Button with validation and initial greeting
        if st.button("Start Interview Chat", key="start_interview"):
            if not candidate['name'] or not candidate['desired_position'] or not candidate['skills'] or not candidate['current_location']:
                st.warning("Please fill in all required fields: Full Name, Desired Position(s), Current Location, and at least one Skill.")
                return
            st.session_state["questions"] = self.generate_ai_interview_questions(candidate)
            # Initialize conversation with a greeting from the assistant
            st.session_state["conversation"] = [{
                "role": "assistant", 
                "content": "Hello, I'm TalentScout AI Interview Assistant. Welcome to your interview session. "
                           "If you wish to exit at any time, please type 'exit', 'quit', or 'bye'."
            }]
            st.session_state["current_question"] = 0
            st.session_state["candidate"] = candidate
        
        # Interview Chat Area
        if "questions" in st.session_state:
            st.header("Interview Chat")
            conv = st.session_state["conversation"]
            questions = st.session_state["questions"]
            current_index = st.session_state["current_question"]

            # Display conversation history
            for msg in conv:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # If we need to ask the next question
            if current_index < len(questions):
                # If the last message is not the current question, append it
                if not (len(conv) > 0 and conv[-1]["role"] == "assistant" and conv[-1]["content"].startswith(f"Q{questions[current_index]['id']}:")):
                    conv.append({
                        "role": "assistant",
                        "content": f"Q{questions[current_index]['id']}: {questions[current_index]['question']}"
                    })
                    st.session_state["conversation"] = conv
                    st.rerun()

                answer = st.chat_input("Type your answer here...")
                if answer:
                    # Check for conversation-ending keywords
                    if answer.strip().lower() in ['exit', 'quit', 'bye']:
                        st.session_state["conversation"].append({"role": "user", "content": answer})
                        st.session_state["conversation"].append({"role": "assistant", "content": "Thank you for your time. The conversation has been ended. We appreciate your interest."})
                        self.save_interview_results(
                            candidate=st.session_state.get("candidate", {}),
                            questions=st.session_state.get("questions", []),
                            conversation=st.session_state.get("conversation", [])
                        )
                        st.stop()
                    else:
                        st.session_state["conversation"].append({"role": "user", "content": answer})
                        st.session_state["conversation"].append({"role": "assistant", "content": "Answer recorded."})
                        st.session_state["current_question"] += 1
                        # If all questions have been answered, conclude the interview
                        if st.session_state["current_question"] >= len(questions):
                            st.success("You have answered all the questions!")
                            st.session_state["conversation"].append({"role": "assistant", "content": "Thank you for completing the interview. We will be in touch with you regarding the next steps."})
                            self.save_interview_results(
                                candidate=st.session_state.get("candidate", {}),
                                questions=st.session_state.get("questions", []),
                                conversation=st.session_state.get("conversation", [])
                            )
                        st.rerun()



def main():
    talent_scout = TalentScoutGroq()
    talent_scout.run_streamlit_app()


if __name__=="__main__":
    main()






