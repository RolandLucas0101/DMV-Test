import streamlit as st
import json
from typing import List, Dict, Optional
from dataclasses import dataclass

# Configure page
st.set_page_config(
    page_title="New Jersey DMV Practice Test",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class Question:
    id: int
    section_id: int
    question_text: str
    options: List[str]
    correct_answer: int
    explanation: str
    order: int

@dataclass
class TestSection:
    id: int
    title: str
    description: str
    icon: str
    order: int

# Initialize session state
if "user_progress" not in st.session_state:
    st.session_state.user_progress = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "current_answers" not in st.session_state:
    st.session_state.current_answers = {}
if "test_completed" not in st.session_state:
    st.session_state.test_completed = False
if "current_section" not in st.session_state:
    st.session_state.current_section = None
if "overall_stats" not in st.session_state:
    st.session_state.overall_stats = {"completed": 0, "passed": 0, "total_questions": 0, "total_correct": 0}

# Define test sections
TEST_SECTIONS = [
    TestSection(1, "Vehicle Registration & Age Requirements", "Learn about registration requirements and age limits for driving in New Jersey.", "📋", 1),
    TestSection(2, "Traffic Laws & Signals", "Understanding traffic signals, signs, and basic driving laws.", "🚦", 2),
    TestSection(3, "Speed Limits & School Zones", "Speed regulations and special zones requiring reduced speeds.", "🏫", 3),
    TestSection(4, "Right of Way & Turning", "Rules for yielding right of way and making safe turns.", "↩️", 4),
    TestSection(5, "Parking & Vehicle Positioning", "Proper parking techniques and vehicle positioning rules.", "🅿️", 5),
    TestSection(6, "Following Distance & Safety", "Maintaining safe distances and defensive driving practices.", "🛡️", 6),
    TestSection(7, "License Requirements & Restrictions", "Driver license types, requirements, and restrictions.", "🆔", 7),
    TestSection(8, "Alcohol & Drug Laws", "Laws regarding impaired driving and substance use.", "🚫", 8),
    TestSection(9, "Child Safety & Seat Belts", "Child restraint systems and seat belt requirements.", "👶", 9),
    TestSection(10, "Emergency Vehicles & Procedures", "Responding to emergency vehicles and emergency situations.", "🚨", 10),
    TestSection(11, "School Buses & Pedestrians", "Rules for school buses and pedestrian right of way.", "🚌", 11),
    TestSection(12, "Road Sharing & Motorcycles", "Sharing the road with motorcycles, trucks, and other vehicles.", "🏍️", 12),
    TestSection(13, "Weather & Road Conditions", "Driving in adverse weather and road conditions.", "🌧️", 13),
    TestSection(14, "Railroad Crossings & Hazards", "Safety at railroad crossings and handling road hazards.", "🚂", 14),
    TestSection(15, "Night Driving & Vision", "Safe practices for night driving and vision requirements.", "🌙", 15)
]

# Load questions from the questions_data.json file we created
@st.cache_data
def load_questions():
    try:
        with open('questions_data.json', 'r') as f:
            questions_data = json.load(f)
        
        questions = []
        for q_data in questions_data:
            question = Question(
                id=q_data["id"],
                section_id=q_data["sectionId"],
                question_text=q_data["questionText"],
                options=q_data["options"],
                correct_answer=q_data["correctAnswer"],
                explanation=q_data["explanation"],
                order=q_data["order"]
            )
            questions.append(question)
        return questions
    except FileNotFoundError:
        # Fallback questions if file not found
        return []

ALL_QUESTIONS = load_questions()

def get_questions_for_section(section_id: int) -> List[Question]:
    """Get all questions for a specific section"""
    return [q for q in ALL_QUESTIONS if q.section_id == section_id]

def calculate_score(answers: Dict[int, int], questions: List[Question]) -> Dict:
    """Calculate the test score"""
    correct = sum(1 for q_id, answer in answers.items() 
                  if any(q.id == q_id and q.correct_answer == answer for q in questions))
    total = len(questions)
    percentage = (correct / total * 100) if total > 0 else 0
    return {
        "correct": correct,
        "total": total,
        "percentage": percentage,
        "passed": percentage >= 80
    }

def update_overall_stats():
    """Update overall statistics based on completed sections"""
    completed = 0
    passed = 0
    total_questions = 0
    total_correct = 0
    
    for section_id in range(1, 16):
        if section_id in st.session_state.user_progress:
            completed += 1
            progress = st.session_state.user_progress[section_id]
            total_questions += progress.get("total", 0)
            total_correct += progress.get("correct", 0)
            if progress.get("passed", False):
                passed += 1
    
    st.session_state.overall_stats = {
        "completed": completed,
        "passed": passed,
        "total_questions": total_questions,
        "total_correct": total_correct
    }

def main():
    st.title("🚗 New Jersey DMV Practice Test")
    st.markdown("---")
    
    # Check if questions are loaded
    if not ALL_QUESTIONS:
        st.error("Questions could not be loaded. Please make sure the questions_data.json file is present.")
        st.stop()
    
    # Update overall stats
    update_overall_stats()
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_section = None
            st.session_state.current_question = 0
            st.session_state.current_answers = {}
            st.session_state.test_completed = False
            st.rerun()
        
        # Overall Progress
        st.markdown("### Overall Progress")
        stats = st.session_state.overall_stats
        st.metric("Sections Completed", f"{stats['completed']}/15")
        st.metric("Sections Passed", f"{stats['passed']}/15")
        if stats["total_questions"] > 0:
            overall_percentage = (stats["total_correct"] / stats["total_questions"]) * 100
            st.metric("Overall Score", f"{stats['total_correct']}/{stats['total_questions']} ({overall_percentage:.1f}%)")
        
        st.markdown("### Test Sections")
        
        # Display progress for each section
        for section in TEST_SECTIONS:
            section_progress = st.session_state.user_progress.get(section.id, {})
            if section_progress:
                score = section_progress.get("correct", 0)
                total = section_progress.get("total", 10)
                percentage = section_progress.get("percentage", 0)
                status = "✅" if percentage >= 80 else "❌"
                st.write(f"{section.icon} Section {section.id} {status} ({score}/{total})")
            else:
                st.write(f"{section.icon} Section {section.id} ⭕")

    # Main content area
    if st.session_state.current_section is None:
        # Home page - section selection
        st.header("Choose a Test Section")
        st.markdown("Select a section below to start practicing. Each section contains 10 questions.")
        
        # Display overall progress summary
        if st.session_state.overall_stats["completed"] > 0:
            st.markdown("### Your Progress Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Completed", f"{st.session_state.overall_stats['completed']}/15")
            with col2:
                st.metric("Passed", f"{st.session_state.overall_stats['passed']}/15")
            with col3:
                if st.session_state.overall_stats["total_questions"] > 0:
                    overall_pct = (st.session_state.overall_stats["total_correct"] / st.session_state.overall_stats["total_questions"]) * 100
                    st.metric("Overall %", f"{overall_pct:.1f}%")
            with col4:
                st.metric("Total Q&A", f"{st.session_state.overall_stats['total_correct']}/{st.session_state.overall_stats['total_questions']}")
            st.markdown("---")
        
        # Display sections in a grid
        cols = st.columns(3)
        for i, section in enumerate(TEST_SECTIONS):
            with cols[i % 3]:
                section_progress = st.session_state.user_progress.get(section.id, {})
                
                # Create section card
                with st.container():
                    st.markdown(f"### {section.icon} Section {section.id}")
                    st.markdown(f"**{section.title}**")
                    st.markdown(section.description)
                    
                    if section_progress:
                        score = section_progress.get("correct", 0)
                        total = section_progress.get("total", 10)
                        percentage = section_progress.get("percentage", 0)
                        status_color = "green" if percentage >= 80 else "red"
                        st.markdown(f"**Last Score:** :{status_color}[{score}/{total} ({percentage:.0f}%)]")
                    
                    if st.button(f"Start Section {section.id}", key=f"start_{section.id}", use_container_width=True):
                        st.session_state.current_section = section.id
                        st.session_state.current_question = 0
                        st.session_state.current_answers = {}
                        st.session_state.test_completed = False
                        st.rerun()
                
                st.markdown("---")
    
    else:
        # Test taking interface
        current_section_id = st.session_state.current_section
        current_section = next(s for s in TEST_SECTIONS if s.id == current_section_id)
        questions = get_questions_for_section(current_section_id)
        
        if not questions:
            st.error(f"No questions found for section {current_section_id}")
            return
        
        if not st.session_state.test_completed:
            # Display current question
            if st.session_state.current_question < len(questions):
                question = questions[st.session_state.current_question]
                
                # Progress bar
                progress = (st.session_state.current_question + 1) / len(questions)
                st.progress(progress)
                st.markdown(f"**Question {st.session_state.current_question + 1} of {len(questions)}**")
                
                # Section header
                st.header(f"{current_section.icon} Section {current_section.id}: {current_section.title}")
                
                # Question
                st.markdown(f"### {question.question_text}")
                
                # Answer options
                answer_key = f"answer_{question.id}"
                selected_answer = st.radio(
                    "Choose your answer:",
                    options=list(range(len(question.options))),
                    format_func=lambda x: f"{chr(65+x)}. {question.options[x]}",
                    key=answer_key,
                    index=st.session_state.current_answers.get(question.id, 0)
                )
                
                # Navigation buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.session_state.current_question > 0:
                        if st.button("← Previous"):
                            # Save current answer before moving
                            st.session_state.current_answers[question.id] = selected_answer
                            st.session_state.current_question -= 1
                            st.rerun()
                
                with col2:
                    if st.button("Submit Answer", type="primary"):
                        # Save answer
                        st.session_state.current_answers[question.id] = selected_answer
                        
                        if st.session_state.current_question < len(questions) - 1:
                            st.session_state.current_question += 1
                            st.rerun()
                        else:
                            # Test completed
                            st.session_state.test_completed = True
                            st.rerun()
                
                with col3:
                    if st.session_state.current_question < len(questions) - 1:
                        if st.button("Next →"):
                            # Save current answer before moving
                            st.session_state.current_answers[question.id] = selected_answer
                            st.session_state.current_question += 1
                            st.rerun()
        
        else:
            # Test results
            st.header(f"🎉 Test Complete: Section {current_section.id}")
            st.markdown(f"**{current_section.icon} {current_section.title}**")
            
            # Calculate score
            score_data = calculate_score(st.session_state.current_answers, questions)
            
            # Save progress
            st.session_state.user_progress[current_section_id] = score_data
            
            # Update overall stats
            update_overall_stats()
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Correct Answers", f"{score_data['correct']}/{score_data['total']}")
            
            with col2:
                st.metric("Percentage", f"{score_data['percentage']:.1f}%")
            
            with col3:
                status = "PASSED" if score_data["passed"] else "FAILED"
                color = "green" if score_data["passed"] else "red"
                st.markdown(f"**Status:** :{color}[{status}]")
            
            # Show detailed results
            st.markdown("### Detailed Results")
            
            for i, question in enumerate(questions):
                user_answer = st.session_state.current_answers.get(question.id, 0)
                is_correct = user_answer == question.correct_answer
                
                with st.expander(f"Question {i+1}: {'✅' if is_correct else '❌'}"):
                    st.markdown(f"**{question.question_text}**")
                    
                    # Show all options with indicators
                    for j, option in enumerate(question.options):
                        if j == question.correct_answer:
                            st.markdown(f"✅ **{chr(65+j)}. {option}** (Correct Answer)")
                        elif j == user_answer:
                            st.markdown(f"❌ **{chr(65+j)}. {option}** (Your Answer)")
                        else:
                            st.markdown(f"⭕ {chr(65+j)}. {option}")
                    
                    st.markdown(f"**Explanation:** {question.explanation}")
            
            # Overall progress after completion
            st.markdown("### Updated Overall Progress")
            stats = st.session_state.overall_stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Sections Completed", f"{stats['completed']}/15")
            with col2:
                st.metric("Sections Passed", f"{stats['passed']}/15")
            with col3:
                if stats["total_questions"] > 0:
                    overall_percentage = (stats["total_correct"] / stats["total_questions"]) * 100
                    st.metric("Overall Score", f"{overall_percentage:.1f}%")
            with col4:
                st.metric("Total Correct", f"{stats['total_correct']}/{stats['total_questions']}")
            
            # Action buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Retake Section", use_container_width=True):
                    st.session_state.current_question = 0
                    st.session_state.current_answers = {}
                    st.session_state.test_completed = False
                    st.rerun()
            
            with col2:
                if st.button("Back to Sections", use_container_width=True):
                    st.session_state.current_section = None
                    st.session_state.current_question = 0
                    st.session_state.current_answers = {}
                    st.session_state.test_completed = False
                    st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("### About This Test")
    st.info("""
    This practice test is based on the New Jersey DMV manual and contains 150 questions across 15 sections. 
    Each section has 10 questions, and you need 80% or higher to pass. 
    
    **Note:** This is a practice test only. For the official test, visit your local DMV office.
    """)

if __name__ == "__main__":
    main()