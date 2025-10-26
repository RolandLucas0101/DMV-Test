import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter
from datetime import datetime

st.set_page_config(page_title="AI Career Analysis", layout="wide", page_icon="🤖")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Career data
career_data = [
    {
        "field": "NICU Nurse",
        "student": "Vernil",
        "category": "Healthcare",
        "concerns": "Job displacement due to AI automation; Loss of over 100 million jobs predicted; Reliance on technology may reduce human element in care",
        "solutions": "Learn to use AI analytics for patient monitoring; Stay current with AI-assisted medical technologies; Automate administrative tasks to free time for direct patient care",
        "effectiveness": "HIGHLY EFFECTIVE - Solutions demonstrate strong understanding that healthcare requires empathy and critical judgment AI cannot replace. Strategic use of AI for monitoring and admin while preserving human care element is well-aligned with healthcare AI trends.",
        "considerations": "Need continuous upskilling in medical AI tools; Must preserve empathy and critical clinical judgment as key differentiators; Balance technical proficiency with compassionate care; Stay informed about ethical implications of AI in neonatal care",
        "projections": "FUTURE: AI-enhanced neonatal monitoring with predictive analytics; Automated vital sign tracking and early warning systems; AI-assisted diagnosis; Smart documentation. FORMAL EDUCATION: BSN programs with health informatics and AI coursework; Certifications in medical data analytics; Continuing education in AI-assisted medical technologies; Master's in nursing informatics. INFORMAL EDUCATION: Practice with digital health platforms; Join nursing informatics communities; Follow medical AI research; Hands-on training with hospital AI systems during clinical rotations."
    },
    {
        "field": "Marketing",
        "student": "Ajanay",
        "category": "Business & Science",
        "concerns": "AI expected to eliminate 100 million jobs within next decade; Automation of marketing tasks could reduce need for human marketers; Risk of job displacement in data analysis and campaign management",
        "solutions": "Use AI to improve efficiency, creativity, and customer satisfaction; Leverage AI for data analysis to identify customer trends; Use AI for automated tasks (emails, scheduling); Implement AI chatbots for 24/7 customer service; Focus on ethical AI use",
        "effectiveness": "HIGHLY EFFECTIVE - Marketing is already highly data-driven. Solutions show strong grasp of AI's complementary role. Using AI for personalization, automation, and analytics while maintaining ethical standards positions marketers excellently for AI-enhanced industry.",
        "considerations": "Must learn advanced analytics and AI-powered marketing tools; Develop expertise in prompt engineering for AI content generation; Understand data privacy and ethical AI marketing practices; Focus on creative strategy and emotional intelligence AI cannot replicate",
        "projections": "FUTURE: Hyper-personalized consumer experiences using AI prediction models; AI-generated content with human creative direction; Real-time campaign optimization; Predictive customer behavior modeling. FORMAL EDUCATION: Marketing degrees with AI and data analytics concentrations; Google Analytics and AI marketing platform certifications; Consumer psychology and data science courses. INFORMAL EDUCATION: Master AI marketing tools (HubSpot AI, Jasper, Copy.ai); Build portfolio using AI-assisted campaigns; Take online courses in marketing analytics; Practice social listening with AI tools; Join digital marketing AI communities."
    },
    {
        "field": "Pediatric Surgeon",
        "student": "Cleajah",
        "category": "Healthcare",
        "concerns": "Risk of over-reliance on automated diagnostic and surgical tools; Concern about accuracy when depending on AI analysis; Potential for technology to miss nuances in pediatric cases",
        "solutions": "Use AI tools to analyze medical scans (MRIs, X-rays) faster and catch problems; Utilize robotic tools powered by AI for precise movements in delicate areas; Leverage AI to create personalized treatment plans; Focus on using AI to save lives and improve outcomes",
        "effectiveness": "HIGHLY EFFECTIVE - Shows excellent understanding of AI as augmentation tool. Recognizes AI's strengths in imaging analysis and precision while maintaining need for surgical expertise. Approach aligns perfectly with surgical robotics trends and AI-assisted diagnosis.",
        "considerations": "Must maintain surgical skills while learning to operate AI-enabled robotic devices; Need expert oversight of AI recommendations - cannot fully automate surgical decisions; Develop proficiency in interpreting AI-generated imaging analysis; Stay current with evolving surgical robotics",
        "projections": "FUTURE: AI-assisted robotic surgical systems with haptic feedback; Digital twin simulations for surgical planning; Intraoperative AI guidance for complex procedures; Predictive models for surgical outcomes; AI-enhanced preoperative imaging and 3D modeling. FORMAL EDUCATION: Medical school with surgical robotics electives; Specialized fellowship training in minimally invasive pediatric surgery; Certifications in robotic surgical systems (da Vinci); CME in AI surgical applications. INFORMAL EDUCATION: Practice with surgical simulation software; Attend surgical robotics conferences; Follow pediatric surgical AI research; Participate in cadaver labs with robotic systems; Network with surgeons using AI-assisted techniques."
    },
    {
        "field": "Nursing (General)",
        "student": "Diana",
        "category": "Healthcare",
        "concerns": "Fear that AI will replace human jobs in nursing; Concern that AI cannot replace human connection needed in nursing; Worry about over-reliance on automated systems for patient care",
        "solutions": "Use AI databases to help with diagnosis quickly; Implement AI to automate treatment administration based on patient needs; Leverage AI for inserting patient data to speed diagnosis; Maintain focus on human connection as irreplaceable element",
        "effectiveness": "MODERATELY EFFECTIVE - Solutions correctly identify that nursing requires human connection AI cannot provide. However, could expand on specific AI tools and skills development. Good foundation but needs more detail on technical literacy and advanced AI applications in nursing.",
        "considerations": "Develop strong technical literacy in nursing informatics and AI systems; Focus on communication and patient advocacy as differentiators; Learn to critically evaluate AI recommendations; Understand limitations of AI in complex patient scenarios; Build expertise in both high-tech and high-touch nursing care",
        "projections": "FUTURE: AI triage systems for emergency departments; Clinical decision support systems integrated into EHRs; Predictive analytics for patient deterioration; Automated medication administration with AI safety checks; Virtual nursing assistants for patient education. FORMAL EDUCATION: Nursing programs with health informatics tracks; Certifications in nursing informatics (RN-BC); Graduate degrees in healthcare technology. INFORMAL EDUCATION: Learn digital patient care platforms and EHR systems; Practice with clinical decision support tools; Join nursing informatics professional organizations; Follow evidence-based practice research on AI in nursing; Volunteer to pilot new AI systems."
    },
    {
        "field": "Cybersecurity",
        "student": "Robert",
        "category": "Technology",
        "concerns": "AI-driven threats making cyber attacks more sophisticated and complex; Need to stay ahead of rapidly evolving threat landscape; Risk of being overwhelmed by volume and complexity of AI-powered attacks",
        "solutions": "Use AI to analyze large amounts of data and spot unusual activity; Automate routine work like malware scanning and tracking suspicious behavior; Leverage AI to learn from past attacks and predict new ones; Focus on solving bigger problems while AI handles routine tasks",
        "effectiveness": "VERY EFFECTIVE - Excellent understanding that AI-driven threats require AI defenses. Solutions demonstrate strategic thinking about automation vs. human expertise. Recognizes cybersecurity professionals must become AI experts to combat AI-powered attacks. Well-aligned with industry trends.",
        "considerations": "Must develop AI-specific threat detection and response skills; Learn machine learning techniques used by attackers to better defend; Stay current with AI security tools and platforms; Understand adversarial AI and how attackers manipulate AI systems; Build skills in AI model security and validation",
        "projections": "FUTURE: Autonomous defensive systems with real-time threat response; AI-powered threat intelligence platforms; Behavioral analytics for zero-day threat detection; Automated incident response and remediation; AI vs. AI security scenarios. FORMAL EDUCATION: Cybersecurity degrees with AI/ML specializations; Certifications: CISSP, CEH, GIAC Security Analytics; Graduate programs in AI security. INFORMAL EDUCATION: Complete security analytics bootcamps; Learn Python and machine learning frameworks for security; Practice on platforms like TryHackMe and HackTheBox; Participate in CTF competitions; Build personal AI security projects; Follow threat intelligence feeds and security AI research."
    },
    {
        "field": "Cosmetic Science",
        "student": "Natally",
        "category": "Business & Science",
        "concerns": "Need to ensure product safety while innovating quickly; Staying current with rapidly changing cosmetic trends; Pressure to speed up product development cycles; Risk of falling behind competitors using advanced technology",
        "solutions": "Use AI to analyze ingredient data and predict formulation performance; Leverage AI to identify new ingredient combinations; Use AI to track trends through social media and market reports; Run simulations before physical experiments to save time and materials",
        "effectiveness": "HIGHLY EFFECTIVE - Solutions demonstrate strong understanding of AI's role in accelerating innovation while maintaining safety. Using AI for predictive formulation, trend analysis, and simulation is well-aligned with cosmetic science industry direction. Shows good balance of creativity and data-driven decision making.",
        "considerations": "Must learn digital lab tools and chemistry database software; Develop skills in computational chemistry and molecular modeling; Understand regulatory requirements for AI-assisted product development; Stay informed about AI ethics in beauty and personal care; Build expertise in data analysis and interpretation",
        "projections": "FUTURE: AI-driven personalized cosmetic formulation; Virtual skin testing and simulation; Predictive modeling for product stability and efficacy; AI-powered ingredient discovery and optimization; Consumer preference prediction through data analytics. FORMAL EDUCATION: Chemistry or biochemistry degrees with data science minors; Cosmetic science programs incorporating AI and computational chemistry; Certifications in formulation science. INFORMAL EDUCATION: Learn AI formulation software and molecular modeling tools; Practice with chemistry databases; Follow cosmetic science journals and AI research; Join Society of Cosmetic Chemists; Experiment with AI-assisted formulation tools; Build understanding of consumer behavior analytics."
    },
    {
        "field": "Dermatology Physician Assistant",
        "student": "Thania",
        "category": "Healthcare",
        "concerns": "Fear of being replaced by automated image analysis systems; Concern about AI eliminating jobs in diagnostic imaging; Worry about reduced need for human practitioners with AI diagnosis",
        "solutions": "Think of AI as assistant/helping hand, not competitor; Use AI image analysis to catch skin changes early; Leverage AI for predictions to personalize treatment; Use AI for documentation to free time for patient interaction; Learn AI tools to make oneself harder to replace; Treat AI as asset to thrive",
        "effectiveness": "HIGHLY EFFECTIVE - Demonstrates exceptional mindset shift from viewing AI as threat to leveraging it as tool. Solutions show mature understanding that AI enhances rather than replaces dermatology care. Strong focus on preserving human elements (interaction, empathy) while building technical skills. Very well-aligned with dermatology AI trends.",
        "considerations": "Maintain strong interpersonal care skills and bedside manner; Develop expertise in interpreting AI-generated diagnostic suggestions; Understand ethical considerations in AI-assisted dermatology; Learn to explain AI recommendations to patients in accessible terms; Build skills in complex case analysis requiring human judgment",
        "projections": "FUTURE: Routine AI skin lesion analysis and classification; Predictive modeling for treatment outcomes; AI-assisted dermoscopy and image enhancement; Personalized skincare recommendations through AI; Telederm with AI pre-screening. FORMAL EDUCATION: PA programs with dermatology focus; Training in dermatology imaging technologies; Courses in AI-aided diagnostic systems; Continuing education in digital dermatology. INFORMAL EDUCATION: Practice with dermatology AI platforms (DermEngine, etc.); Learn imaging software and analysis tools; Follow dermatology AI research; Attend digital health conferences; Join teledermatology communities; Build patient communication skills for explaining AI tools."
    },
    {
        "field": "Electrical Engineering",
        "student": "Dunsin",
        "category": "Engineering",
        "concerns": "Rapid technology evolution could make skills outdated quickly; Risk of falling behind peers who adopt AI tools; Concern about being less valuable without AI proficiency; Fear that refusing to learn new technology will limit career opportunities",
        "solutions": "Use AI for circuit design to work faster; Leverage machine learning to predict equipment failures; Use AI to optimize power distribution in buildings; Keep learning about new AI software for simulations and testing; See AI as something that enhances work, not replaces engineers; Stay curious and practice with AI tools throughout career",
        "effectiveness": "VERY EFFECTIVE - Demonstrates excellent understanding of AI as efficiency multiplier and differentiator. Strong recognition that continuous learning is essential. Solutions show practical applications (circuit design, failure prediction, optimization) that align perfectly with electrical engineering AI trends. Mature attitude about adaptation.",
        "considerations": "Need continuous learning of AI-enabled engineering design software; Develop proficiency in machine learning for predictive maintenance; Learn to integrate AI into existing engineering workflows; Build skills in IoT and smart systems that rely on AI; Understand limitations and verification needs for AI-generated designs; Focus on creative problem-solving and innovation AI cannot replicate",
        "projections": "FUTURE: AI-driven smart grid management and optimization; Automated circuit design and PCB layout; Predictive maintenance through IoT sensors and ML; AI-powered simulation and testing; Smart building and infrastructure systems. FORMAL EDUCATION: Electrical engineering degrees with AI/ML coursework; Power systems certifications; Graduate studies in smart systems or AI engineering. INFORMAL EDUCATION: Master ML-enabled CAD and simulation software; Learn Python for engineering applications; Build IoT projects using AI platforms; Join robotics clubs and maker spaces; Participate in engineering competitions; Follow smart grid and renewable energy AI innovations; Practice with industry-standard AI engineering tools."
    },
    {
        "field": "Civil Engineering",
        "student": "Pamela",
        "category": "Engineering",
        "concerns": "Risk of falling behind peers using advanced AI tools; Structural safety concerns with AI-generated designs; Need to keep up with rapidly evolving engineering technology; Pressure to work faster while maintaining quality and safety",
        "solutions": "Use AI to design safer and stronger buildings; Leverage AI to analyze data quickly and spot problems early; Use AI to save time and reduce mistakes; Make better decisions on projects through AI insights; Stay up to date to avoid falling behind",
        "effectiveness": "HIGHLY EFFECTIVE - Solutions show good understanding of AI for error prevention and optimization. Focus on safety and early problem detection is crucial in civil engineering. Could be strengthened with more specific AI tool mentions, but demonstrates solid grasp of AI's role in enhancing design quality and project management.",
        "considerations": "Learn to use BIM (Building Information Modeling) with AI integrations; Develop skills in structural analysis software with AI optimization; Understand how to verify and validate AI-generated designs; Stay informed about building codes and regulations for AI-assisted design; Build expertise in sustainable design aided by AI; Learn project management platforms enhanced with AI; Maintain strong fundamentals in structural engineering principles",
        "projections": "FUTURE: Automated structural optimization and generative design; AI-powered project planning and resource allocation; Smart city infrastructure design; Predictive maintenance for infrastructure; AI-assisted environmental impact analysis; Construction site safety monitoring through AI. FORMAL EDUCATION: Civil engineering degrees with construction technology focus; BIM certifications with AI components; Graduate programs in smart infrastructure; Professional Engineer (PE) licensure. INFORMAL EDUCATION: Master AutoCAD, Revit, and other BIM software with AI features; Learn structural analysis programs (SAP2000, ETABS with AI); Take online courses in smart city design; Join civil engineering professional organizations; Practice with project management AI tools; Participate in sustainable design competitions; Follow infrastructure AI innovations and case studies."
    },
    {
        "field": "Pediatrician",
        "student": "Samessa",
        "category": "Healthcare",
        "concerns": "Fear of AI handling diagnoses and reducing physician role; Concern about AI making medical decisions without human oversight; Worry about losing relevance as medical field advances technologically",
        "solutions": "Use AI for symptom detection to help identify illnesses; Submit symptoms into AI tools like ChatGPT for diagnostic assistance; Use AI to track patient data and dates; Leverage AI to make faster decisions in critical moments; Use AI at full potential to stay relevant with technological advancement",
        "effectiveness": "MODERATELY EFFECTIVE - Shows basic understanding of AI applications but relies too heavily on consumer tools (ChatGPT) rather than medical-grade AI systems. Solutions need more depth about medical oversight requirements and limitations. Good recognition of speed benefits but needs stronger emphasis on human judgment and verification.",
        "considerations": "Must use FDA-approved medical AI, not general consumer chatbots; Develop strong diagnostic reasoning that AI complements but doesn't replace; Build excellent patient and family communication skills; Understand pediatric-specific considerations AI may miss; Learn to critically evaluate AI recommendations; Stay current with evidence-based medicine and pediatric guidelines; Focus on developmental and behavioral aspects AI cannot assess",
        "projections": "FUTURE: AI-assisted diagnostic decision support systems; Personalized pediatric treatment protocols through ML; Early detection of developmental disorders through AI screening; Predictive models for childhood diseases; Virtual health assistants for routine pediatric questions; Growth and development tracking with AI analytics. FORMAL EDUCATION: Medical school with focus on pediatrics and health informatics; Residency with exposure to AI clinical tools; CME courses in pediatric AI applications; Certifications in pediatric subspecialties using AI. INFORMAL EDUCATION: Develop AI literacy specific to healthcare; Learn pediatric EHR systems and clinical decision support; Follow pediatric medical AI research; Join pediatric informatics interest groups; Practice with clinical simulation software; Build strong evidence-based medicine skills; Attend conferences on digital health in pediatrics."
    },
    {
        "field": "Software Developer",
        "student": "Josue",
        "category": "Technology",
        "concerns": "AI could automate coding, risking job loss for developers; Fear that AI will completely solve programming problems; Concern about job displacement in software development field",
        "solutions": "Use AI solely for advice and ideas, not complete solutions; Learn to efficiently modify and control AI systems; Become asset who can participate in making AI; Minimize odds of job loss by learning to build AI, not just use it; Recognize AI will create new jobs requiring AI development skills",
        "effectiveness": "HIGHLY EFFECTIVE - Excellent strategic thinking - shift from AI user to AI builder/controller. Strong recognition that developers who create AI remain competitive. Mature understanding that AI creates new opportunities while transforming old ones. Well-aligned with industry reality that prompt engineering and AI development are growing fields.",
        "considerations": "Focus on AI development skills (ML, deep learning, NLP); Learn prompt engineering and AI fine-tuning; Develop creative problem-solving abilities AI lacks; Build skills in system architecture and complex design; Understand AI limitations and edge cases; Stay current with rapidly evolving AI frameworks and tools; Develop domain expertise in specific industries; Focus on problems requiring human creativity and judgment",
        "projections": "FUTURE: AI-assisted coding (GitHub Copilot, etc.) becomes standard; Automated testing and debugging with AI; Natural language to code generation; AI-powered code review and optimization; Automated documentation generation; Low-code/no-code platforms with AI. FORMAL EDUCATION: Computer Science degrees with AI/ML specializations; Courses in machine learning, deep learning, NLP; Graduate programs in AI engineering; Certifications in cloud AI platforms (AWS, Azure, Google). INFORMAL EDUCATION: Master Python, TensorFlow, PyTorch; Learn prompt engineering techniques; Build AI/ML projects and contribute to open source; Practice on Kaggle and AI competition platforms; Stay current with latest AI models and frameworks; Join AI developer communities; Create portfolio of AI-integrated applications; Learn about AI ethics and responsible development."
    }
]

# Convert to DataFrame
df = pd.DataFrame(career_data)

# Title and header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Future Career Analysis</h1>
    <p>Student Perspectives on AI Integration Across 11 Career Fields</p>
</div>
""", unsafe_allow_html=True)

# Statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Career Fields", "11")
with col2:
    st.metric("Student Responses", "12")
with col3:
    st.metric("Healthcare Fields", len(df[df['category'] == 'Healthcare']))
with col4:
    st.metric("Technology Fields", len(df[df['category'] == 'Technology']))

# Filters
st.sidebar.header("Filters")
category_filter = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df['category'].unique().tolist())
)

effectiveness_filter = st.sidebar.multiselect(
    "Filter by Effectiveness",
    ["HIGHLY EFFECTIVE", "VERY EFFECTIVE", "MODERATELY EFFECTIVE"],
    default=[]
)

# Apply filters
filtered_df = df.copy()
if category_filter != "All":
    filtered_df = filtered_df[filtered_df['category'] == category_filter]

if effectiveness_filter:
    filtered_df = filtered_df[filtered_df['effectiveness'].str.contains('|'.join(effectiveness_filter))]

# Display data
st.subheader(f"Showing {len(filtered_df)} of {len(df)} Career Fields")

# Display as expandable cards
for idx, row in filtered_df.iterrows():
    with st.expander(f"**{row['field']}** - {row['student']} ({row['category']})"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("### 🚨 Issues/Concerns")
            st.write(row['concerns'])
            
            st.markdown("### 💡 Student Solutions")
            st.write(row['solutions'])
            
            st.markdown("### ⚖️ Effectiveness Analysis")
            st.write(row['effectiveness'])
        
        with col_b:
            st.markdown("### 🎯 Additional Considerations")
            st.write(row['considerations'])
            
            st.markdown("### 🔮 Future Projections & Preparation")
            st.write(row['projections'])

# Download buttons
st.sidebar.markdown("---")
st.sidebar.header("Download Options")

# Excel download
@st.cache_data
def create_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_export = df[['field', 'student', 'category', 'concerns', 'solutions', 'effectiveness', 'considerations', 'projections']]
        df_export.to_excel(writer, sheet_name='AI Career Analysis', index=False)
        
        workbook = writer.book
        worksheet = writer.sheets['AI Career Analysis']
        
        # Format
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#667eea',
            'font_color': 'white',
            'border': 1
        })
        
        # Apply header format
        for col_num, value in enumerate(df_export.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Set column widths
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:H', 40)
    
    return output.getvalue()

excel_data = create_excel()
st.sidebar.download_button(
    label="📥 Download Excel",
    data=excel_data,
    file_name=f"AI_Career_Analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# CSV download
csv = df.to_csv(index=False)
st.sidebar.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name=f"AI_Career_Analysis_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Summary statistics
st.markdown("---")
st.subheader("📊 Summary Statistics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### By Category")
    category_counts = df['category'].value_counts()
    st.bar_chart(category_counts)

with col2:
    st.markdown("### Effectiveness Distribution")
    effectiveness_levels = []
    for eff in df['effectiveness']:
        if 'HIGHLY EFFECTIVE' in eff or 'VERY EFFECTIVE' in eff:
            effectiveness_levels.append('High')
        else:
            effectiveness_levels.append('Moderate')
    
    eff_df = pd.DataFrame({'Effectiveness': effectiveness_levels})
    st.bar_chart(eff_df['Effectiveness'].value_counts())

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>AI Future Career Analysis | Prepared for Educational Use</p>
    <p>Data based on student responses about AI integration in their future careers</p>
</div>
""", unsafe_allow_html=True)
