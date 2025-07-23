import streamlit as st
import json
import random
from typing import Dict, List, Any

# Configure Streamlit page
st.set_page_config(
    page_title="New Jersey DMV Practice Test",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DMV Test Data
DMV_SECTIONS = {
    1: {
        "title": "Vehicle Registration & Age Requirements",
        "description": "Learn about vehicle registration, license age requirements, and basic vehicle operations.",
        "icon": "📋",
        "questions": [
            {
                "question": "At what age can you get a learner's permit in New Jersey?",
                "options": ["14 years old", "15 years old", "16 years old", "17 years old", "18 years old"],
                "correct": 2,
                "explanation": "In New Jersey, you can get a learner's permit at 16 years old with parental consent and completion of driver education."
            },
            {
                "question": "How long is a New Jersey driver's license valid?",
                "options": ["2 years", "4 years", "6 years", "8 years", "10 years"],
                "correct": 1,
                "explanation": "New Jersey driver's licenses are valid for 4 years from the date of issue."
            },
            {
                "question": "What documents do you need to register a vehicle in NJ?",
                "options": ["Title only", "Insurance only", "Title and insurance", "Title, insurance, and ID", "Registration form only"],
                "correct": 3,
                "explanation": "You need the vehicle title, proof of insurance, and valid identification to register a vehicle in New Jersey."
            },
            {
                "question": "When must you renew your vehicle registration?",
                "options": ["Every year", "Every 2 years", "Every 3 years", "Every 4 years", "When it expires"],
                "correct": 0,
                "explanation": "Vehicle registration in New Jersey must be renewed annually."
            },
            {
                "question": "What happens if you drive with an expired registration?",
                "options": ["Warning only", "Small fine", "Large fine and points", "License suspension", "Vehicle impoundment"],
                "correct": 2,
                "explanation": "Driving with expired registration results in fines and points on your license."
            },
            {
                "question": "How many points result in license suspension?",
                "options": ["6 points", "8 points", "10 points", "12 points", "15 points"],
                "correct": 3,
                "explanation": "In New Jersey, accumulating 12 or more points results in license suspension."
            },
            {
                "question": "What is required for a teenage driver's first license?",
                "options": ["Permit only", "Road test only", "Permit and road test", "Permit, road test, and 6 months practice", "Parent signature only"],
                "correct": 3,
                "explanation": "Teen drivers need a permit, pass a road test, and complete 6 months of supervised practice driving."
            },
            {
                "question": "When can you drive alone with a learner's permit?",
                "options": ["Immediately", "After 1 month", "After 3 months", "After 6 months", "Never"],
                "correct": 4,
                "explanation": "You cannot drive alone with a learner's permit - you must always have a licensed adult supervisor."
            },
            {
                "question": "What age can you get an unrestricted license in NJ?",
                "options": ["16", "17", "18", "19", "21"],
                "correct": 2,
                "explanation": "You can get an unrestricted license at 18 years old in New Jersey."
            },
            {
                "question": "How often must you take an eye exam for license renewal?",
                "options": ["Every renewal", "Every other renewal", "Only if required", "Never after first test", "Every 10 years"],
                "correct": 0,
                "explanation": "An eye exam is required at every license renewal in New Jersey."
            }
        ]
    },
    2: {
        "title": "Traffic Laws & Right-of-Way",
        "description": "Understanding traffic laws, right-of-way rules, and intersection procedures.",
        "icon": "🚦",
        "questions": [
            {
                "question": "Who has the right-of-way at a four-way stop?",
                "options": ["First to arrive", "Vehicle on the right", "Largest vehicle", "Vehicle going straight", "Emergency vehicles only"],
                "correct": 0,
                "explanation": "At a four-way stop, the first vehicle to arrive has the right-of-way. If vehicles arrive simultaneously, yield to the right."
            },
            {
                "question": "When making a left turn, you must yield to:",
                "options": ["No one", "Oncoming traffic only", "Pedestrians only", "Oncoming traffic and pedestrians", "Vehicles behind you"],
                "correct": 3,
                "explanation": "When making a left turn, you must yield to oncoming traffic and pedestrians in the crosswalk."
            },
            {
                "question": "What does a flashing yellow light mean?",
                "options": ["Stop", "Proceed with caution", "Yield", "Speed up", "Turn only"],
                "correct": 1,
                "explanation": "A flashing yellow light means proceed with caution after checking for cross traffic."
            },
            {
                "question": "When must you stop for a school bus?",
                "options": ["Never", "Only when children are visible", "When red lights are flashing", "Only on school days", "When going same direction only"],
                "correct": 2,
                "explanation": "You must stop when a school bus has its red lights flashing and stop arm extended, regardless of direction."
            },
            {
                "question": "What is the speed limit in a school zone?",
                "options": ["15 mph", "20 mph", "25 mph", "30 mph", "35 mph"],
                "correct": 2,
                "explanation": "The speed limit in school zones is typically 25 mph when children are present."
            },
            {
                "question": "When can you pass on the right?",
                "options": ["Never", "When safe to do so", "On multi-lane roads only", "When vehicle ahead is turning left", "In emergencies only"],
                "correct": 3,
                "explanation": "You may pass on the right when the vehicle ahead is making a left turn and there's sufficient space."
            },
            {
                "question": "What does a solid yellow line mean?",
                "options": ["No passing", "Pass with caution", "Two-way traffic", "Lane change allowed", "Construction zone"],
                "correct": 0,
                "explanation": "A solid yellow line indicates no passing is allowed."
            },
            {
                "question": "Who has right-of-way when entering a highway?",
                "options": ["Merging traffic", "Highway traffic", "Larger vehicles", "Faster vehicles", "No one"],
                "correct": 1,
                "explanation": "Traffic already on the highway has the right-of-way over merging traffic."
            },
            {
                "question": "When must you use headlights?",
                "options": ["At night only", "In rain only", "30 minutes before sunset to 30 minutes after sunrise", "Dawn to dusk", "When visibility is poor"],
                "correct": 2,
                "explanation": "Headlights must be used from 30 minutes before sunset to 30 minutes after sunrise, and during poor visibility."
            },
            {
                "question": "What is the penalty for running a red light?",
                "options": ["Warning", "Fine only", "Fine and points", "License suspension", "Jail time"],
                "correct": 2,
                "explanation": "Running a red light results in both a fine and points added to your license."
            }
        ]
    }
    # Add more sections as needed
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_section' not in st.session_state:
        st.session_state.current_section = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {}

def display_dashboard():
    """Display the main dashboard with all sections"""
    st.title("🚗 New Jersey DMV Practice Test")
    st.markdown("### Master your NJ driving test with comprehensive practice sections")
    
    # Progress overview
    completed_sections = len(st.session_state.user_progress)
    total_sections = len(DMV_SECTIONS)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completed Sections", completed_sections)
    with col2:
        st.metric("Total Sections", total_sections)
    with col3:
        if completed_sections > 0:
            avg_score = sum(st.session_state.user_progress.values()) / completed_sections
            st.metric("Average Score", f"{avg_score:.1f}/10")
        else:
            st.metric("Average Score", "N/A")
    
    st.markdown("---")
    
    # Display sections
    st.subheader("📚 Test Sections")
    
    for section_id, section in DMV_SECTIONS.items():
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col1:
                st.markdown(f"## {section['icon']}")
            
            with col2:
                st.markdown(f"### {section['title']}")
                st.markdown(section['description'])
                
                # Show progress if completed
                if section_id in st.session_state.user_progress:
                    score = st.session_state.user_progress[section_id]
                    st.success(f"✅ Completed - Score: {score}/10")
            
            with col3:
                if st.button(f"Start Section {section_id}", key=f"start_{section_id}"):
                    st.session_state.current_section = section_id
                    st.session_state.current_question = 0
                    st.session_state.answers = {}
                    st.session_state.test_completed = False
                    st.rerun()
        
        st.markdown("---")

def display_test(section_id):
    """Display the test interface"""
    section = DMV_SECTIONS[section_id]
    questions = section['questions']
    current_q = st.session_state.current_question
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"{section['icon']} {section['title']}")
    with col2:
        if st.button("← Back to Dashboard"):
            st.session_state.current_section = None
            st.rerun()
    
    # Progress bar
    progress = (current_q + 1) / len(questions)
    st.progress(progress)
    st.markdown(f"Question {current_q + 1} of {len(questions)}")
    
    if current_q < len(questions):
        question = questions[current_q]
        
        # Question
        st.markdown(f"### {question['question']}")
        
        # Answer options
        answer = st.radio(
            "Select your answer:",
            options=range(len(question['options'])),
            format_func=lambda x: f"{chr(65 + x)}) {question['options'][x]}",
            key=f"q_{current_q}"
        )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_q > 0:
                if st.button("← Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col3:
            if st.button("Next →" if current_q < len(questions) - 1 else "Finish Test"):
                # Save answer
                st.session_state.answers[current_q] = answer
                
                if current_q < len(questions) - 1:
                    st.session_state.current_question += 1
                else:
                    # Complete test
                    st.session_state.test_completed = True
                st.rerun()

def display_results(section_id):
    """Display test results"""
    section = DMV_SECTIONS[section_id]
    questions = section['questions']
    
    st.title(f"📊 Test Results: {section['title']}")
    
    # Calculate score
    correct_answers = 0
    for q_idx, user_answer in st.session_state.answers.items():
        if user_answer == questions[q_idx]['correct']:
            correct_answers += 1
    
    score = correct_answers
    percentage = (score / len(questions)) * 100
    
    # Save progress
    st.session_state.user_progress[section_id] = score
    
    # Display score
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Correct Answers", f"{correct_answers}/{len(questions)}")
    with col2:
        st.metric("Score Percentage", f"{percentage:.1f}%")
    with col3:
        if percentage >= 70:
            st.success("✅ PASSED")
        else:
            st.error("❌ FAILED")
    
    st.markdown("---")
    
    # Detailed results
    st.subheader("📝 Detailed Results")
    
    for q_idx, question in enumerate(questions):
        user_answer = st.session_state.answers.get(q_idx, -1)
        correct_answer = question['correct']
        is_correct = user_answer == correct_answer
        
        with st.expander(f"Question {q_idx + 1}: {'✅' if is_correct else '❌'}"):
            st.markdown(f"**{question['question']}**")
            
            # Show all options with indicators
            for opt_idx, option in enumerate(question['options']):
                if opt_idx == correct_answer:
                    st.success(f"✅ {chr(65 + opt_idx)}) {option} (Correct Answer)")
                elif opt_idx == user_answer and user_answer != correct_answer:
                    st.error(f"❌ {chr(65 + opt_idx)}) {option} (Your Answer)")
                else:
                    st.write(f"{chr(65 + opt_idx)}) {option}")
            
            st.info(f"**Explanation:** {question['explanation']}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Back to Dashboard"):
            st.session_state.current_section = None
            st.rerun()
    with col2:
        if st.button("🔄 Retake Test"):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.test_completed = False
            st.rerun()

def main():
    """Main application function"""
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🚗 DMV Practice")
        st.markdown("### Navigation")
        
        if st.button("🏠 Dashboard"):
            st.session_state.current_section = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Progress")
        for section_id, section in DMV_SECTIONS.items():
            if section_id in st.session_state.user_progress:
                score = st.session_state.user_progress[section_id]
                st.success(f"{section['icon']} {section_id}: {score}/10")
            else:
                st.info(f"{section['icon']} {section_id}: Not started")
    
    # Main content
    if st.session_state.current_section is None:
        display_dashboard()
    elif st.session_state.test_completed:
        display_results(st.session_state.current_section)
    else:
        display_test(st.session_state.current_section)

if __name__ == "__main__":
    main()