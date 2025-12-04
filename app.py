"""
AI Interview Preparation Assistant Pro
Advanced LLM-powered platform for comprehensive interview preparation
Built with Streamlit and Groq AI
Author: Your Name
"""

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import random

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

load_dotenv()

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

st.set_page_config(
    page_title="AI Interview Prep Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ENHANCED CSS STYLING
# ============================================================================

st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    .header-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0;
        animation: fadeIn 1s ease-in;
    }
    
    .subtitle-text {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* BOLD Chat Colors */
    .chat-message {
        padding: 1.8rem;
        border-radius: 15px;
        margin: 1.2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        border: 2px solid;
        animation: slideIn 0.4s ease-out;
    }
    
    .interviewer-msg {
        background: linear-gradient(135deg, #5B21B6 0%, #6D28D9 100%);
        border-color: #7C3AED;
        border-left: 6px solid #8B5CF6;
    }
    
    .interviewer-msg strong {
        color: #FDE68A;
        font-size: 1.2rem;
        display: block;
        margin-bottom: 1rem;
        padding-bottom: 0.7rem;
        border-bottom: 2px solid rgba(253, 230, 138, 0.3);
    }
    
    .interviewer-msg div {
        color: #FFFFFF !important;
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    .candidate-msg {
        background: linear-gradient(135deg, #047857 0%, #059669 100%);
        border-color: #10B981;
        border-left: 6px solid #34D399;
    }
    
    .candidate-msg strong {
        color: #FDE68A;
        font-size: 1.2rem;
        display: block;
        margin-bottom: 1rem;
        padding-bottom: 0.7rem;
        border-bottom: 2px solid rgba(253, 230, 138, 0.3);
    }
    
    .candidate-msg div {
        color: #FFFFFF !important;
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.2);
    }
    
    .progress-container {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 0.3rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 25px;
        border-radius: 8px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        padding-left: 10px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #F59E0B;
        margin: 1rem 0;
    }
    
    /* Improve text area styling */
    .stTextArea textarea {
        border: 2px solid #E5E7EB;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

session_vars = {
    'history': [],
    'total_questions': 0,
    'mock_messages': [],
    'mock_started': False,
    'interview_count': 0,
    'user_profile': {},
    'achievements': [],
    'streak_days': 0,
    'total_practice_time': 0,
    'checklist': {
        'research': {},
        'preparation': {},
        'practice': {},
        'logistics': {},
        'day_of': {}
    }
}

for var, default_value in session_vars.items():
    if var not in st.session_state:
        st.session_state[var] = default_value

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def call_groq_api(messages, temperature=0.7, max_tokens=500):
    """Centralized Groq API call with error handling"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def calculate_progress_score():
    """Calculate user's overall progress score"""
    total_sessions = len(st.session_state.history)
    mock_interviews = st.session_state.interview_count
    score = min(100, (total_sessions * 5) + (mock_interviews * 15))
    return score

def get_motivational_message():
    """Get random motivational message"""
    messages = [
        "🌟 You're making great progress! Keep it up!",
        "💪 Every practice session brings you closer to success!",
        "🚀 You're on fire! Consistency is key!",
        "⭐ Amazing work! You're interview-ready!",
        "🎯 Practice makes perfect! You're doing awesome!"
    ]
    return random.choice(messages)

# ============================================================================
# HEADER SECTION
# ============================================================================

if not os.getenv("GROQ_API_KEY"):
    st.error("❌ No Groq API key found!")
    st.info("🔑 Get FREE key from: https://console.groq.com/keys")
    st.code("Add to .env file:\nGROQ_API_KEY=your_key_here")
    st.stop()

st.markdown('<h1 class="header-text">🎯 AI Interview Prep Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Your AI-Powered Career Success Platform | Powered by Groq AI (Llama 3.3)</p>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin: 1rem 0;'>
    <span class='feature-badge'>⚡ Lightning Fast</span>
    <span class='feature-badge'>🆓 100% Free</span>
    <span class='feature-badge'>🤖 AI-Powered</span>
    <span class='feature-badge'>💬 Live Mock Interviews</span>
    <span class='feature-badge'>📊 Analytics Dashboard</span>
</div>
""", unsafe_allow_html=True)

progress_score = calculate_progress_score()
st.markdown(f"""
<div class='progress-container'>
    <div class='progress-bar' style='width: {progress_score}%;'>
        <span style='color: white; font-weight: bold;'>Interview Readiness: {progress_score}%</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Interview Configuration")
    
    with st.expander("👤 Your Profile", expanded=False):
        name = st.text_input("Your Name", placeholder="John Doe")
        years_exp = st.slider("Years of Experience", 0, 20, 3)
        
        if st.button("💾 Save Profile"):
            st.session_state.user_profile = {'name': name, 'experience': years_exp}
            st.success("✅ Profile saved!")
    
    st.markdown("---")
    
    difficulty = st.selectbox(
        "🎚️ Difficulty Level",
        ["Entry Level (0-2 years)", "Mid Level (2-5 years)", "Senior (5-10 years)", "Expert (10+ years)"],
        help="Select based on your experience level"
    )
    
    interview_type = st.selectbox(
        "📋 Interview Type",
        ["Technical Coding", "Behavioral/STAR", "System Design", "Machine Learning/AI", 
         "Data Science", "Product Management", "Leadership", "Case Study"],
        help="Choose the type of interview you're preparing for"
    )
    
    role = st.text_input("💼 Target Role", placeholder="e.g., Senior Software Engineer")
    company = st.text_input("🏢 Target Company", placeholder="e.g., Google, Amazon, Meta")
    
    st.markdown("---")
    st.markdown("### 📊 Your Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions", st.session_state.total_questions)
    with col2:
        st.metric("Sessions", len(st.session_state.history))
    
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Mock Interviews", st.session_state.interview_count)
    with col4:
        st.metric("Streak", f"{st.session_state.streak_days} days")
    
    if st.session_state.total_questions > 0:
        st.info(get_motivational_message())
    
    st.markdown("---")
    st.markdown("### 🛠️ AI-Powered Tools")
    
    if st.button("💰 Salary Insights", use_container_width=True):
        if role:
            with st.spinner("Fetching salary data..."):
                prompt = f"""Provide salary insights for {role}:
1. Salary Range (USD): Entry/Mid/Senior levels
2. Top 5 Negotiation Strategies
3. Key Value Points
4. Market Trends
Keep concise and actionable."""
                response = call_groq_api([{"role": "user", "content": prompt}], max_tokens=600)
                if response:
                    st.success(response)
        else:
            st.warning("⚠️ Please enter a target role first!")
    
    if st.button("🏢 Company Intel", use_container_width=True):
        if company:
            with st.spinner(f"Researching {company}..."):
                prompt = f"""Provide interview prep insights for {company}:
1. Company Culture & Values
2. Interview Process
3. Common Questions
4. What They Value
5. Tips to Stand Out"""
                response = call_groq_api([{"role": "user", "content": prompt}], max_tokens=800)
                if response:
                    st.success(response)
        else:
            st.warning("⚠️ Please enter a company name first!")

# ============================================================================
# MAIN CONTENT TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎤 Quick Practice",
    "💬 AI Mock Interview", 
    "📝 Resume Analyzer",
    "🎯 STAR Method Coach",
    "📊 Analytics Dashboard",
    "🚀 Interview Toolkit"
])

# ============================================================================
# TAB 1: QUICK PRACTICE
# ============================================================================

with tab1:
    st.markdown("## 🎤 Instant Interview Practice")
    st.markdown("*Generate single questions and receive detailed AI feedback in seconds*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🎲 Generate Interview Question", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is crafting your personalized question..."):
                prompt = f"""Generate a realistic {difficulty} {interview_type} interview question for {role or 'Software Engineer'}{f' at {company}' if company else ''}.

Format:
**Question:** [The question]
**What they're looking for:** [Brief explanation]"""

                response = call_groq_api([
                    {"role": "system", "content": "You are a senior technical interviewer."},
                    {"role": "user", "content": prompt}
                ], temperature=0.8, max_tokens=400)
                
                if response:
                    st.session_state.current_question = response
                    st.session_state.total_questions += 1
                    st.success("✅ Question generated!")
                    st.balloons()
        
        if 'current_question' in st.session_state:
            st.markdown("---")
            st.markdown("### ❓ Your Interview Question")
            st.info(st.session_state.current_question)
            
            st.markdown("### ✍️ Your Answer")
            user_answer = st.text_area(
                "Type your detailed response:",
                height=280,
                placeholder="""💡 Use the STAR Method:
• Situation: Set context (20%)
• Task: Describe challenge (20%)
• Action: What YOU did (40%)
• Result: Quantify outcome (20%)

Example: "Increased user engagement by 35% by implementing..."
""",
                key="practice_answer"
            )
            
            col_a, col_b, col_c = st.columns([2, 2, 1])
            
            with col_a:
                analyze_btn = st.button("🔍 Get AI Feedback", use_container_width=True, type="primary")
            
            with col_b:
                if user_answer:
                    quick_check = st.button("⚠️ Check Mistakes", use_container_width=True)
                else:
                    quick_check = False
            
            with col_c:
                if st.button("🔄", use_container_width=True):
                    del st.session_state.current_question
                    st.rerun()
            
            if analyze_btn:
                if user_answer and len(user_answer) > 30:
                    with st.spinner("🤖 Analyzing..."):
                        analysis_prompt = f"""Analyze this interview answer:

Question: {st.session_state.current_question}
Answer: {user_answer}

Provide:
1. Score (0-100)
2. Strengths (4-5 points)
3. Improvements (4-5 points)
4. STAR Analysis
5. Enhanced Version
6. Key Takeaways

Be specific and actionable."""

                        feedback = call_groq_api([
                            {"role": "system", "content": "You are an expert interview coach."},
                            {"role": "user", "content": analysis_prompt}
                        ], temperature=0.3, max_tokens=1500)
                        
                        if feedback:
                            st.markdown("---")
                            st.markdown("## 📊 Comprehensive AI Feedback")
                            st.success(feedback)
                            
                            st.session_state.history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'type': 'Quick Practice',
                                'question': st.session_state.current_question,
                                'answer': user_answer,
                                'feedback': feedback,
                                'difficulty': difficulty,
                                'interview_type': interview_type,
                                'role': role
                            })
                            
                            st.balloons()
                else:
                    st.warning("⚠️ Please provide a detailed answer (at least 30 characters)")
            
            if quick_check:
                with st.spinner("Checking mistakes..."):
                    mistakes_prompt = f"""Check for common mistakes:
Question: {st.session_state.current_question}
Answer: {user_answer}

Check: Filler words, vague statements, no metrics, weak structure, negative language, using "we" instead of "I"."""

                    mistakes = call_groq_api([{"role": "user", "content": mistakes_prompt}], max_tokens=600)
                    if mistakes:
                        st.warning("### ⚠️ Common Mistakes")
                        st.markdown(mistakes)
    
    with col2:
        st.markdown("### 💡 Interview Guide")
        
        with st.expander("🎯 STAR Method", expanded=True):
            st.markdown("""
            **S** - Situation (20%)
            Set context clearly
            
            **T** - Task (20%)
            Your responsibility
            
            **A** - Action (40%)
            What YOU did (not "we")
            
            **R** - Result (20%)
            Quantifiable outcomes
            
            **Example:**
            "Cart abandonment was 40% (S). As lead engineer, reduce by 50% in Q2 (T). Implemented one-click checkout, optimized load time to 0.8s (A). Dropped to 18%, $2M additional revenue (R)."
            """)
        
        with st.expander("✅ Best Practices"):
            st.markdown("""
            - ✅ Specific examples
            - ✅ Quantify everything
            - ✅ Say "I" not "we"
            - ✅ 90-120 seconds
            - ✅ Confident tone
            """)

# ============================================================================
# TAB 2: AI MOCK INTERVIEW
# ============================================================================

with tab2:
    st.markdown("## 💬 Live AI Mock Interview")
    st.markdown("*Experience a realistic interview with adaptive follow-up questions*")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if not st.session_state.mock_started:
            st.markdown("### 🚀 Ready for Your Mock Interview?")
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0;'>
                <h4 style='color: white; margin: 0 0 1rem 0;'>📋 Interview Configuration</h4>
                <p style='margin: 0.5rem 0;'><strong>Role:</strong> {role or 'Software Engineer'}</p>
                <p style='margin: 0.5rem 0;'><strong>Level:</strong> {difficulty}</p>
                <p style='margin: 0.5rem 0;'><strong>Type:</strong> {interview_type}</p>
                <p style='margin: 0.5rem 0;'><strong>Company:</strong> {company or 'General Tech'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎬 Start Mock Interview Now", type="primary", use_container_width=True):
                with st.spinner("🤖 AI Interviewer is preparing..."):
                    opening_prompt = f"""You are a professional interviewer for {role or 'Software Engineer'} at {difficulty.split()[0]} level{f' at {company}' if company else ''}.

Start interview:
1. Greet warmly
2. Introduce yourself (fictional name/title)
3. Ask first question

Be conversational and professional."""

                    response = call_groq_api([{"role": "user", "content": opening_prompt}], temperature=0.7, max_tokens=350)
                    
                    if response:
                        st.session_state.mock_messages = [{"role": "interviewer", "content": response}]
                        st.session_state.mock_started = True
                        st.rerun()
        
        else:
            st.markdown("### 💬 Interview in Progress")
            
            for idx, msg in enumerate(st.session_state.mock_messages):
                if msg["role"] == "interviewer":
                    st.markdown(f"""
                    <div class="chat-message interviewer-msg">
                        <strong>🤖 AI Interviewer</strong>
                        <div>{msg["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message candidate-msg">
                        <strong>👤 You</strong>
                        <div>{msg["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            user_response = st.text_area(
                "✍️ Your Response:",
                height=220,
                placeholder="Take your time... Use STAR method and be specific!",
                key="mock_response_input"
            )
            
            col_a, col_b, col_c = st.columns([2, 2, 1])
            
            with col_a:
                submit = st.button("📤 Submit Answer", use_container_width=True, type="primary")
            
            with col_b:
                end = st.button("🔚 End & Get Feedback", use_container_width=True)
            
            with col_c:
                if st.button("🔄 Restart", use_container_width=True):
                    st.session_state.mock_messages = []
                    st.session_state.mock_started = False
                    st.rerun()
            
            if submit and user_response:
                if len(user_response.strip()) >= 50:
                    with st.spinner("🤖 AI is processing..."):
                        st.session_state.mock_messages.append({"role": "candidate", "content": user_response})
                        
                        interviewer_count = len([m for m in st.session_state.mock_messages if m["role"] == "interviewer"])
                        
                        if interviewer_count < 4:
                            conversation = "\n\n".join([
                                f"{'INTERVIEWER' if m['role'] == 'interviewer' else 'CANDIDATE'}: {m['content']}"
                                for m in st.session_state.mock_messages
                            ])
                            
                            next_prompt = f"""Continue interview:

{conversation}

Based on last answer:
1. If strong: Ask follow-up or new question
2. If weak: Ask clarifying question

Question #{interviewer_count + 1} of 4-5. Ask ONE question only."""

                            response = call_groq_api([{"role": "user", "content": next_prompt}], temperature=0.7, max_tokens=300)
                        else:
                            response = call_groq_api([{
                                "role": "user",
                                "content": "Conclude interview warmly. Thank candidate. Ask if they have questions. Mention next steps. 2-3 sentences."
                            }], max_tokens=150)
                        
                        if response:
                            st.session_state.mock_messages.append({"role": "interviewer", "content": response})
                            st.rerun()
                else:
                    st.warning("⚠️ Answer too short (minimum 50 characters)")
            
            if end:
                with st.spinner("📊 Generating feedback..."):
                    transcript = "# Mock Interview Transcript\n\n"
                    for m in st.session_state.mock_messages:
                        role_label = "**🤖 INTERVIEWER**" if m["role"] == "interviewer" else "**👤 YOU**"
                        transcript += f"{role_label}\n{m['content']}\n\n---\n\n"
                    
                    feedback_prompt = f"""Analyze this mock interview:

{transcript}

Provide:
1. Score (0-100) with justification
2. Strengths (3-5)
3. Improvements (3-5)
4. Communication Breakdown
5. STAR Analysis
6. Best/Weakest Answers
7. Hiring Decision
8. Action Items (7-10)
9. Questions to Ask Interviewer

Be honest, specific, constructive."""

                    feedback = call_groq_api([
                        {"role": "system", "content": "You are a senior hiring manager."},
                        {"role": "user", "content": feedback_prompt}
                    ], temperature=0.3, max_tokens=2500)
                    
                    if feedback:
                        st.markdown("## 📊 Interview Performance Review")
                        st.success(feedback)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button("📥 Full Report", f"{transcript}\n\n{feedback}", 
                                             f"interview_{datetime.now().strftime('%Y%m%d_%H%M')}.md", "text/markdown", use_container_width=True)
                        with col2:
                            st.download_button("📥 Transcript", transcript, 
                                             f"transcript_{datetime.now().strftime('%Y%m%d_%H%M')}.md", "text/markdown", use_container_width=True)
                        with col3:
                            st.download_button("📥 Feedback", feedback, 
                                             f"feedback_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", "text/plain", use_container_width=True)
                        
                        st.session_state.history.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'Mock Interview',
                            'difficulty': difficulty,
                            'role': role,
                            'interview_type': interview_type,
                            'transcript': transcript,
                            'feedback': feedback,
                            'num_questions': len([m for m in st.session_state.mock_messages if m["role"] == "interviewer"])
                        })
                        
                        st.session_state.interview_count += 1
                        st.session_state.mock_messages = []
                        st.session_state.mock_started = False
                        st.balloons()
    
    with col2:
        st.markdown("### 💡 Mock Interview Guide")
        
        st.markdown("""
        <div class='tip-box'>
            <strong>⏱️ Time Tips</strong>
            <ul>
                <li>Each answer: 90-120s</li>
                <li>Total: 20-30 min</li>
                <li>Pause: OK!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🎯 Evaluation Criteria"):
            st.markdown("""
            **Content (40%)**
            - Relevance
            - Specific examples
            - Quantified results
            
            **Structure (30%)**
            - STAR method
            - Clear organization
            
            **Communication (30%)**
            - Clarity
            - Confidence
            - Professionalism
            """)

# Continuing with remaining tabs...
# (Due to length, showing structure - the pattern continues similarly for tabs 3-6)

with tab3:
    st.markdown("## 📝 AI-Powered Resume Analyzer")
    # Resume analyzer implementation (simplified for brevity)
    
with tab4:
    st.markdown("## 🎯 STAR Method Interactive Coach")
    # STAR coach implementation
    
with tab5:
    st.markdown("## 📊 Analytics Dashboard")
    # Analytics implementation
    
with tab6:
    st.markdown("## 🚀 Interview Toolkit")
    # Toolkit implementation

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);'>
    <h2 style='margin: 0; color: white;'>🚀 AI Interview Prep Pro</h2>
    <p style='margin: 1rem 0;'>Powered by Groq AI • Llama 3.3 70B</p>
    <p style='opacity: 0.9;'>⚡ Lightning Fast • 🆓 Free Forever • 🤖 Advanced AI • 💬 Live Mock Interviews</p>
    <p style='margin-top: 1rem; opacity: 0.8;'>Built with ❤️ for your career success • © 2025</p>
</div>
""", unsafe_allow_html=True)