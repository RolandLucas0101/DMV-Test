import streamlit as st
from typing import List, Dict
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

# All 150 questions embedded directly in the app
@st.cache_data
def load_questions():
    questions_data = [
        {
            "id": 1,
            "sectionId": 1,
            "questionText": 'To register a vehicle in New Jersey, you must be age ____ or older.',
            "options": ['16', '17', '18', '19', '21'],
            "correctAnswer": 1,
            "explanation": 'To register a motor vehicle in New Jersey, you must be at least 17 years old. You must have proof of identity and proof of vehicle ownership.',
            "order": 1
        },
        {
            "id": 2,
            "sectionId": 1,
            "questionText": "What is the fee for a Learner's Permit in New Jersey?",
            "options": ['$5', '$10', '$15', '$20', '$24'],
            "correctAnswer": 1,
            "explanation": "The fee for a Learner's Permit in New Jersey is $10.",
            "order": 2
        },
        {
            "id": 3,
            "sectionId": 1,
            "questionText": "What is the fee for an Initial Auto Driver's License in New Jersey?",
            "options": ['$10', '$18', '$24', '$30', '$35'],
            "correctAnswer": 2,
            "explanation": "The fee for an Initial Auto Driver's License in New Jersey is $24.",
            "order": 3
        },
        {
            "id": 4,
            "sectionId": 1,
            "questionText": "What is the fee for Changes/Duplicates of a driver's license?",
            "options": ['$5', '$8', '$11', '$15', '$20'],
            "correctAnswer": 2,
            "explanation": "The fee for changes or duplicates of a driver's license in New Jersey is $11.",
            "order": 4
        },
        {
            "id": 5,
            "sectionId": 1,
            "questionText": 'A driver who is age 21 or older and operating on a GDL must practice supervised driving for at least ____.',
            "options": ['One month', 'Two months', 'Three months', 'Six months', 'One year'],
            "correctAnswer": 2,
            "explanation": 'A driver who is age 21 or older and operating on a Graduated Driver License (GDL) must practice supervised driving for a minimum of three months before taking the official road test.',
            "order": 5
        },
        {
            "id": 6,
            "sectionId": 1,
            "questionText": 'A driver who is under the age of 21 and operating on a GDL must practice supervised driving for at least ____.',
            "options": ['One month', 'Three months', 'Four months', 'Six months', 'One year'],
            "correctAnswer": 3,
            "explanation": 'A driver who is under the age of 21 and operating on a Graduated Driver License (GDL) must practice supervised driving for a minimum of six months before taking the official road test.',
            "order": 6
        },
        {
            "id": 7,
            "sectionId": 1,
            "questionText": 'How many questions are on the New Jersey knowledge test?',
            "options": ['40', '45', '50', '60', '75'],
            "correctAnswer": 2,
            "explanation": 'The New Jersey knowledge test consists of 50 questions. Applicants must correctly answer at least 40 questions to receive a passing score.',
            "order": 7
        },
        {
            "id": 8,
            "sectionId": 1,
            "questionText": 'How many questions must you answer correctly to pass the New Jersey knowledge test?',
            "options": ['35', '38', '40', '42', '45'],
            "correctAnswer": 2,
            "explanation": 'Applicants must correctly answer at least 40 out of 50 questions to receive a passing score on the New Jersey knowledge test.',
            "order": 8
        },
        {
            "id": 9,
            "sectionId": 1,
            "questionText": 'A driver is required to practice driving on a probationary license for up to:',
            "options": ['Six months', 'Nine months', 'One year', 'Eighteen months', 'Two years'],
            "correctAnswer": 2,
            "explanation": 'Once obtaining a probationary license, a driver must practice unsupervised driving for at least one year before they can get their basic driver license.',
            "order": 9
        },
        {
            "id": 10,
            "sectionId": 1,
            "questionText": 'During the probationary period, how many points can a new driver accumulate before being enrolled in a Probationary Driver Program?',
            "options": ['Two', 'Three', 'Four', 'Five', 'Six'],
            "correctAnswer": 2,
            "explanation": 'During a two-year period after receiving a special learner permit, a new driver may not be convicted of two or more moving traffic violations totaling in four or more points against their license before they are required to enroll in a Probationary Driver Program.',
            "order": 10
        },
        {
            "id": 11,
            "sectionId": 2,
            "questionText": 'You may avoid a traffic signal by driving on public or private property:',
            "options": ['Never', 'If an officer directs you to do so', 'In emergency situations only', 'If traffic is heavy', 'During construction'],
            "correctAnswer": 1,
            "explanation": 'It is a traffic violation to operate a motor vehicle on public or private property to avoid a traffic control signal or sign unless an officer directs traffic to do so.',
            "order": 1
        },
        {
            "id": 12,
            "sectionId": 2,
            "questionText": 'You may turn right on red:',
            "options": ['Never', 'Always', 'After coming to a complete stop and yielding to pedestrians and vehicles', 'Only during off-peak hours', 'Only if no sign prohibits it'],
            "correctAnswer": 2,
            "explanation": 'You may turn right on a red light after coming to a full stop. You may only turn if it is safe to do so and if there is no sign prohibiting the turn on a red light. Be watchful for pedestrians crossing in front of your vehicle.',
            "order": 2
        },
        {
            "id": 13,
            "sectionId": 2,
            "questionText": 'You should signal to turn ____ before beginning the turn.',
            "options": ['50 feet', '100 feet', '150 feet', '200 feet', '250 feet'],
            "correctAnswer": 1,
            "explanation": 'When you wish to change lanes or make a turn, signal to inform other motorists of your intention. Signals should be activated at least 100 feet before you make the turn. Continue signaling until you have completed the turn or lane change.',
            "order": 3
        },
        {
            "id": 14,
            "sectionId": 2,
            "questionText": 'The Implied Consent Law:',
            "options": ['Requires all drivers to carry insurance', 'Means drivers consent to a breath test when suspected of drinking and driving', 'Applies only to commercial drivers', 'Requires annual vehicle inspections', 'Mandates seat belt use'],
            "correctAnswer": 1,
            "explanation": 'The Implied Consent Law means that, by driving on New Jersey roads, you are giving your consent to undergo a breath test if you are arrested for an alcohol-related offense.',
            "order": 4
        },
        {
            "id": 15,
            "sectionId": 2,
            "questionText": 'When making a left turn, you must yield to:',
            "options": ['Vehicles turning right only', 'Pedestrians only', 'All approaching vehicles and pedestrians', 'Vehicles already in the intersection', 'Emergency vehicles only'],
            "correctAnswer": 2,
            "explanation": 'When making a left turn, you must yield to pedestrians, bicyclists, or other vehicles moving on their green light.',
            "order": 5
        },
        {
            "id": 16,
            "sectionId": 2,
            "questionText": 'A red arrow pointing right means:',
            "options": ['Turn right with caution', 'Stop until the light turns green', 'Yield to oncoming traffic', 'Turn right after yielding', 'No right turn allowed'],
            "correctAnswer": 1,
            "explanation": "A red arrow means 'stop.' You must remain stopped until a green light or green arrow appears. Do not turn against a red arrow.",
            "order": 6
        },
        {
            "id": 17,
            "sectionId": 2,
            "questionText": 'You should not enter an intersection unless:',
            "options": ['You have a green light', 'Traffic is light', 'You can get completely across before the light turns red', 'Other drivers are waiting', 'You are making a right turn'],
            "correctAnswer": 2,
            "explanation": 'Even if the signal is green, you must not enter an intersection unless you can get completely across before the light turns red. If you block the intersection, you can be cited.',
            "order": 7
        },
        {
            "id": 18,
            "sectionId": 2,
            "questionText": 'A solid yellow line next to a broken yellow line means:',
            "options": ['No passing in either direction', 'Vehicles next to the broken line may pass', 'Vehicles next to the solid line may pass', 'Passing allowed in both directions', 'Construction zone ahead'],
            "correctAnswer": 1,
            "explanation": 'Yellow lines separate lanes of traffic moving in opposite directions. A broken yellow line next to your driving lane means that you may pass. A solid yellow line means no passing.',
            "order": 8
        },
        {
            "id": 19,
            "sectionId": 2,
            "questionText": "When a pedestrian is crossing in the middle of the street after the 'Don't Walk' signal begins flashing, you should:",
            "options": ['Honk your horn', 'Drive around the pedestrian', 'Wait until the pedestrian crosses completely', 'Proceed slowly', 'Flash your headlights'],
            "correctAnswer": 2,
            "explanation": 'At a green light, you must give the right-of-way to any vehicle, bicyclist, or pedestrian in the intersection. If a pedestrian begins crossing the street after the traffic signal light starts flashing, wait until they have crossed the street before proceeding.',
            "order": 9
        },
        {
            "id": 20,
            "sectionId": 2,
            "questionText": 'If a green arrow turns into a solid green light, you:',
            "options": ['Must stop immediately', 'May still turn, but must yield to oncoming traffic', 'Have the right of way', 'Cannot turn anymore', 'Must wait for another green arrow'],
            "correctAnswer": 1,
            "explanation": 'If a green arrow turns into a solid green light, you may still turn in the direction that the arrow was pointing but you must first yield to pedestrians and oncoming traffic.',
            "order": 10
        },
        {
            "id": 21,
            "sectionId": 3,
            "questionText": 'The speed limit in school zones is:',
            "options": ['15 mph', '20 mph', '25 mph', '30 mph', '35 mph'],
            "correctAnswer": 2,
            "explanation": 'Unless otherwise posted, drivers in school zones should not drive at speeds faster than 25 mph. You should always exercise caution when driving in a school zone.',
            "order": 1
        },
        {
            "id": 22,
            "sectionId": 3,
            "questionText": 'Unless otherwise posted, the speed limit in residential districts is:',
            "options": ['20 mph', '25 mph', '30 mph', '35 mph', '40 mph'],
            "correctAnswer": 1,
            "explanation": 'Unless otherwise posted, the speed limit in residential districts is 25 mph. If a different speed limit is posted, you should follow that speed limit.',
            "order": 2
        },
        {
            "id": 23,
            "sectionId": 3,
            "questionText": 'Unless otherwise posted, the speed limit on rural roadways is:',
            "options": ['35 mph', '40 mph', '45 mph', '50 mph', '55 mph'],
            "correctAnswer": 3,
            "explanation": 'Unless otherwise posted, the speed limit on unmarked rural roadways is 50 mph. If a different speed limit is posted, you should follow that speed limit.',
            "order": 3
        },
        {
            "id": 24,
            "sectionId": 3,
            "questionText": 'If you drive more slowly than the flow of traffic, you will most likely:',
            "options": ['Be safer', 'Save fuel', 'Interfere with traffic and receive a ticket', 'Be ignored by other drivers', 'Help traffic flow'],
            "correctAnswer": 2,
            "explanation": 'You must drive more slowly than usual when there is heavy traffic or bad weather. However, if you block the normal and reasonable movement of traffic by driving too slowly, you may be cited.',
            "order": 4
        },
        {
            "id": 25,
            "sectionId": 3,
            "questionText": 'When merging onto a freeway, you should be driving:',
            "options": ['Slower than traffic', 'Much faster than traffic', 'At or near the speed of traffic on the freeway', 'At exactly the speed limit', 'As fast as possible'],
            "correctAnswer": 2,
            "explanation": 'When merging onto a freeway, you should enter at or near the speed of traffic.',
            "order": 5
        },
        {
            "id": 26,
            "sectionId": 3,
            "questionText": 'Slower-moving traffic on a multilane highway should:',
            "options": ['Drive in the left lane', 'Drive in the right lane', 'Drive in any lane', 'Drive in the center lane', 'Change lanes frequently'],
            "correctAnswer": 1,
            "explanation": 'If you are driving more slowly than surrounding traffic on a multilane road, use the right lane. The left-hand lane is intended for use by faster-moving traffic that is passing slower-moving traffic.',
            "order": 6
        },
        {
            "id": 27,
            "sectionId": 3,
            "questionText": 'A tractor-trailer could take up to ____ percent longer to stop under poor weather conditions.',
            "options": ['15', '20', '25', '30', '35'],
            "correctAnswer": 2,
            "explanation": 'When driving near a tractor-trailer, be aware of how its size will affect the way it is driven. Under poor weather conditions, the larger vehicle may take up to 25 percent longer to come to a complete stop than it would if being driven under ideal conditions.',
            "order": 7
        },
        {
            "id": 28,
            "sectionId": 3,
            "questionText": 'A driver may pass a school bus at a speed no faster than ____ if the school bus is stopped in front of a school.',
            "options": ['5 mph', '10 mph', '15 mph', '20 mph', '25 mph'],
            "correctAnswer": 1,
            "explanation": 'If a school bus is stopped in front of a school to drop off or pick up students, other drivers may pass the stopped bus from either direction at speeds no faster than 10 mph, if it is safe to do so.',
            "order": 8
        },
        {
            "id": 29,
            "sectionId": 3,
            "questionText": 'When approaching a school zone during school hours, you should:',
            "options": ['Maintain normal speed', 'Speed up to get through quickly', 'Reduce speed and be extra cautious', 'Honk your horn to warn children', 'Change lanes frequently'],
            "correctAnswer": 2,
            "explanation": 'When driving through a school zone, especially during school hours, you should reduce your speed to the posted limit (usually 25 mph) and be extra cautious for children who may be crossing the street.',
            "order": 9
        },
        {
            "id": 30,
            "sectionId": 3,
            "questionText": 'If you are driving significantly slower than other traffic, you should:',
            "options": ['Stay in the left lane', 'Use the right lane or pull over safely', 'Speed up to match traffic', 'Turn on hazard lights', 'Ignore other drivers'],
            "correctAnswer": 1,
            "explanation": 'If you must drive significantly slower than other traffic, use the right lane or pull over safely when possible to allow faster traffic to pass.',
            "order": 10
        },
        {
            "id": 31,
            "sectionId": 4,
            "questionText": 'When two vehicles arrive at a four-way stop intersection at the same time, which vehicle has the right of way?',
            "options": ['The vehicle on the left', 'The vehicle on the right', 'The larger vehicle', 'The vehicle going straight', 'The first vehicle to honk'],
            "correctAnswer": 1,
            "explanation": 'When two vehicles arrive at a four-way stop at the same time, the vehicle on the right has the right of way. This is a basic rule of right-of-way at intersections.',
            "order": 1
        },
        {
            "id": 32,
            "sectionId": 4,
            "questionText": 'When making a left turn at an intersection, you must yield to:',
            "options": ['No one', 'Vehicles turning right only', 'Oncoming traffic and pedestrians', 'Vehicles behind you', 'Emergency vehicles only'],
            "correctAnswer": 2,
            "explanation": 'When making a left turn, you must yield to oncoming traffic and pedestrians crossing the intersection. Wait for a safe gap before completing your turn.',
            "order": 2
        },
        {
            "id": 33,
            "sectionId": 4,
            "questionText": 'At a yield sign, you must:',
            "options": ['Come to a complete stop', 'Slow down and proceed if safe', 'Speed up to merge quickly', 'Honk your horn', 'Stop only if other vehicles are present'],
            "correctAnswer": 1,
            "explanation": 'At a yield sign, you must slow down and be prepared to stop if necessary. You may proceed if the way is clear, but you must yield the right-of-way to other vehicles and pedestrians.',
            "order": 3
        },
        {
            "id": 34,
            "sectionId": 4,
            "questionText": 'When entering a highway from an on-ramp, you should:',
            "options": ['Stop at the end of the ramp', 'Yield to traffic already on the highway', 'Force your way into traffic', 'Use your hazard lights', 'Drive slowly until you find a gap'],
            "correctAnswer": 1,
            "explanation": 'When entering a highway from an on-ramp, you must yield to traffic already on the highway. Accelerate to match the speed of highway traffic and merge when safe.',
            "order": 4
        },
        {
            "id": 35,
            "sectionId": 4,
            "questionText": 'At an intersection with no traffic control devices, who has the right of way?',
            "options": ['The vehicle on the left', 'The vehicle on the right', 'The larger vehicle', 'The vehicle that arrives first', 'No one has right of way'],
            "correctAnswer": 1,
            "explanation": 'At an intersection with no traffic control devices, the vehicle on the right has the right of way when two vehicles arrive at approximately the same time.',
            "order": 5
        },
        {
            "id": 36,
            "sectionId": 4,
            "questionText": 'When turning right at an intersection, you must yield to:',
            "options": ['No one', 'Vehicles turning left', 'Pedestrians crossing your path', 'Vehicles behind you', 'Only emergency vehicles'],
            "correctAnswer": 2,
            "explanation": 'When turning right, you must yield to pedestrians crossing in front of your vehicle. Always check for pedestrians before completing your turn.',
            "order": 6
        },
        {
            "id": 37,
            "sectionId": 4,
            "questionText": 'A vehicle turning left from a driveway onto a road must:',
            "options": ['Have the right of way', 'Yield to all traffic on the road', 'Honk before turning', 'Flash headlights', 'Stop completely'],
            "correctAnswer": 1,
            "explanation": 'A vehicle turning left from a driveway onto a road must yield to all traffic on the road. The vehicle on the road has the right of way.',
            "order": 7
        },
        {
            "id": 38,
            "sectionId": 4,
            "questionText": 'When making a U-turn, you must:',
            "options": ['Have the right of way', 'Yield to all other traffic', 'Use your hazard lights', 'Honk your horn', 'Speed through quickly'],
            "correctAnswer": 1,
            "explanation": 'When making a U-turn, you must yield to all other traffic and pedestrians. Make sure you can complete the turn safely without interfering with other traffic.',
            "order": 8
        },
        {
            "id": 39,
            "sectionId": 4,
            "questionText": 'At a T-intersection, the vehicle on the:',
            "options": ['Left has right of way', 'Right has right of way', 'Through street has right of way', 'Larger vehicle has right of way', 'First to arrive has right of way'],
            "correctAnswer": 2,
            "explanation": 'At a T-intersection, traffic on the through street (the street that continues straight) has the right of way over traffic that must turn from the dead-end street.',
            "order": 9
        },
        {
            "id": 40,
            "sectionId": 4,
            "questionText": 'Before making any turn, you should:',
            "options": ['Speed up', 'Signal at least 100 feet before the turn', 'Honk your horn', 'Flash your lights', 'Change lanes'],
            "correctAnswer": 1,
            "explanation": 'Before making any turn, you should signal at least 100 feet before the turn to warn other drivers of your intention to turn.',
            "order": 10
        },
        {
            "id": 41,
            "sectionId": 5,
            "questionText": 'You may not park within ____ feet of a fire hydrant.',
            "options": ['5', '10', '15', '20', '25'],
            "correctAnswer": 1,
            "explanation": 'You may not park within 10 feet of a fire hydrant. This ensures that firefighters have adequate access to the hydrant in case of emergency.',
            "order": 1
        },
        {
            "id": 42,
            "sectionId": 5,
            "questionText": 'You may not park within ____ feet of a crosswalk.',
            "options": ['10', '15', '20', '25', '30'],
            "correctAnswer": 3,
            "explanation": 'You may not park within 25 feet of a crosswalk. This ensures visibility for pedestrians and other drivers.',
            "order": 2
        },
        {
            "id": 43,
            "sectionId": 5,
            "questionText": 'When parking on a hill with a curb, you should:',
            "options": ['Always turn wheels left', 'Always turn wheels right', 'Turn wheels toward the curb when facing downhill', 'Leave wheels straight', 'Use parking brake only'],
            "correctAnswer": 2,
            "explanation": 'When parking on a hill with a curb, turn your wheels toward the curb when facing downhill, and away from the curb when facing uphill. Always use your parking brake.',
            "order": 3
        },
        {
            "id": 44,
            "sectionId": 5,
            "questionText": 'You may not park within ____ feet of a stop sign.',
            "options": ['15', '20', '25', '30', '50'],
            "correctAnswer": 4,
            "explanation": 'You may not park within 50 feet of a stop sign. This ensures that the sign remains visible to approaching drivers.',
            "order": 4
        },
        {
            "id": 45,
            "sectionId": 5,
            "questionText": 'Double parking is:',
            "options": ['Legal if under 5 minutes', 'Legal with hazard lights on', 'Never legal', 'Legal in business districts', 'Legal on weekends'],
            "correctAnswer": 2,
            "explanation": 'Double parking is never legal. It blocks traffic flow and creates dangerous conditions for other drivers.',
            "order": 5
        },
        {
            "id": 46,
            "sectionId": 5,
            "questionText": 'When parallel parking, your vehicle should be no more than ____ inches from the curb.',
            "options": ['6', '8', '10', '12', '18'],
            "correctAnswer": 0,
            "explanation": 'When parallel parking, your vehicle should be no more than 6 inches from the curb. This leaves adequate room for traffic while not taking up too much of the roadway.',
            "order": 6
        },
        {
            "id": 47,
            "sectionId": 5,
            "questionText": 'You may not park:',
            "options": ['On a one-way street', 'In a residential area', 'In front of a driveway', 'On the right side of the road', 'During daylight hours'],
            "correctAnswer": 2,
            "explanation": 'You may not park in front of a driveway as it blocks access for the property owner and may create emergency access issues.',
            "order": 7
        },
        {
            "id": 48,
            "sectionId": 5,
            "questionText": 'When leaving a parallel parking space, you should:',
            "options": ['Back out quickly', 'Signal and check mirrors and blind spots', 'Honk your horn', 'Turn on hazard lights', 'Exit without signaling'],
            "correctAnswer": 1,
            "explanation": 'When leaving a parallel parking space, you should signal your intention, check your mirrors and blind spots, and proceed carefully into traffic.',
            "order": 8
        },
        {
            "id": 49,
            "sectionId": 5,
            "questionText": 'You may not park within ____ feet of an intersection.',
            "options": ['10', '15', '20', '25', '50'],
            "correctAnswer": 3,
            "explanation": 'You may not park within 25 feet of an intersection. This ensures adequate visibility and turning radius for vehicles.',
            "order": 9
        },
        {
            "id": 50,
            "sectionId": 5,
            "questionText": 'Parking is prohibited:',
            "options": ['On all bridges', 'On narrow roads only', 'In tunnels and on bridges', 'Only during rush hour', 'Only in urban areas'],
            "correctAnswer": 2,
            "explanation": 'Parking is prohibited in tunnels and on bridges because these locations can create serious safety hazards and traffic obstructions.',
            "order": 10
        },
        {
            "id": 51,
            "sectionId": 6,
            "questionText": 'The safe following distance behind another vehicle is:',
            "options": ['1 second', '2 seconds', '3 seconds', '4 seconds', '5 seconds'],
            "correctAnswer": 2,
            "explanation": 'A safe following distance is at least 3 seconds behind the vehicle in front of you under normal driving conditions. This gives you enough time to react and stop safely.',
            "order": 1
        },
        {
            "id": 52,
            "sectionId": 6,
            "questionText": 'In poor weather conditions, you should increase your following distance to:',
            "options": ['4 seconds', '5 seconds', '6 seconds', '8 seconds', '10 seconds'],
            "correctAnswer": 2,
            "explanation": 'In poor weather conditions such as rain, snow, or fog, you should increase your following distance to at least 6 seconds to account for reduced visibility and longer stopping distances.',
            "order": 2
        },
        {
            "id": 53,
            "sectionId": 6,
            "questionText": 'When following a large truck, you should:',
            "options": ['Follow closely to save space', 'Increase your following distance', 'Change lanes immediately', 'Use high beams', 'Honk to signal your presence'],
            "correctAnswer": 1,
            "explanation": 'When following a large truck, you should increase your following distance because trucks have larger blind spots and require more stopping distance.',
            "order": 3
        },
        {
            "id": 54,
            "sectionId": 6,
            "questionText": 'Tailgating is dangerous because:',
            "options": ['It saves fuel', 'It reduces reaction time', "It's more efficient", "It's courteous", 'It helps traffic flow'],
            "correctAnswer": 1,
            "explanation": 'Tailgating is dangerous because it reduces your reaction time and stopping distance, increasing the risk of rear-end collisions.',
            "order": 4
        },
        {
            "id": 55,
            "sectionId": 6,
            "questionText": 'The 3-second rule helps you:',
            "options": ['Calculate speed', 'Maintain safe following distance', 'Time traffic lights', 'Measure fuel efficiency', 'Count lane changes'],
            "correctAnswer": 1,
            "explanation": 'The 3-second rule helps you maintain a safe following distance by ensuring you have adequate time to react to the vehicle ahead.',
            "order": 5
        },
        {
            "id": 56,
            "sectionId": 6,
            "questionText": 'If someone is tailgating you, you should:',
            "options": ['Speed up', 'Brake suddenly', 'Pull over when safe to let them pass', 'Ignore them', 'Tailgate the car in front'],
            "correctAnswer": 2,
            "explanation": 'If someone is tailgating you, you should pull over when safe to let them pass, or increase your following distance to create a buffer zone.',
            "order": 6
        },
        {
            "id": 57,
            "sectionId": 6,
            "questionText": 'When driving at night, your following distance should be:',
            "options": ['The same as daytime', 'Reduced by half', 'Increased', 'Based on traffic', 'At least 10 seconds'],
            "correctAnswer": 2,
            "explanation": 'When driving at night, your following distance should be increased because visibility is reduced and it takes longer to see and react to hazards.',
            "order": 7
        },
        {
            "id": 58,
            "sectionId": 6,
            "questionText": 'Anti-lock brakes (ABS) help prevent:',
            "options": ['Speeding', 'Tire wear', 'Wheel lockup during braking', 'Engine problems', 'Lane drifting'],
            "correctAnswer": 2,
            "explanation": 'Anti-lock brakes (ABS) help prevent wheel lockup during hard braking, allowing you to maintain steering control while stopping.',
            "order": 8
        },
        {
            "id": 59,
            "sectionId": 6,
            "questionText": 'The best way to avoid a collision is to:',
            "options": ['Drive faster', 'Maintain awareness and safe following distance', 'Use horn frequently', 'Change lanes often', 'Drive in the left lane'],
            "correctAnswer": 1,
            "explanation": 'The best way to avoid a collision is to maintain awareness of your surroundings and keep a safe following distance from other vehicles.',
            "order": 9
        },
        {
            "id": 60,
            "sectionId": 6,
            "questionText": 'When you see brake lights ahead, you should:',
            "options": ['Speed up to pass', 'Immediately apply brakes', 'Check mirrors and gradually slow down', 'Change lanes', 'Honk your horn'],
            "correctAnswer": 2,
            "explanation": 'When you see brake lights ahead, you should check your mirrors and gradually slow down while being prepared to stop.',
            "order": 10
        },
        {
            "id": 61,
            "sectionId": 7,
            "questionText": 'A probationary driver license restricts driving between:',
            "options": ['10 PM and 6 AM', '11 PM and 5 AM', '12 AM and 6 AM', '11 PM and 6 AM', '12 AM and 5 AM'],
            "correctAnswer": 3,
            "explanation": 'A probationary driver license restricts driving between 11:01 PM and 5:59 AM, with certain exceptions for work, school, or religious activities.',
            "order": 1
        },
        {
            "id": 62,
            "sectionId": 7,
            "questionText": 'How many passengers can a probationary driver have in the car?',
            "options": ['No restrictions', '1 passenger', 'Only family members', '1 passenger plus parents/guardian', '2 passengers maximum'],
            "correctAnswer": 3,
            "explanation": 'A probationary driver may have only one passenger (plus parents or guardian) unless additional passengers are immediate family members.',
            "order": 2
        },
        {
            "id": 63,
            "sectionId": 7,
            "questionText": 'To obtain a basic driver license, you must:',
            "options": ['Be 18 years old', 'Complete probationary period', 'Pass another road test', 'Pay additional fees', 'Take defensive driving course'],
            "correctAnswer": 1,
            "explanation": 'To obtain a basic driver license, you must successfully complete the probationary period without violations.',
            "order": 3
        },
        {
            "id": 64,
            "sectionId": 7,
            "questionText": 'A Special Learner Permit allows you to drive:',
            "options": ['Alone', 'Only with a licensed instructor', 'With any licensed adult', 'With parents only', 'With a licensed adult 21 or older'],
            "correctAnswer": 4,
            "explanation": 'A Special Learner Permit allows you to drive only when accompanied by a licensed adult who is 21 years of age or older.',
            "order": 4
        },
        {
            "id": 65,
            "sectionId": 7,
            "questionText": 'The minimum age to get a Special Learner Permit in New Jersey is:',
            "options": ['15', '16', '17', '18', '21'],
            "correctAnswer": 1,
            "explanation": 'The minimum age to get a Special Learner Permit in New Jersey is 16 years old.',
            "order": 5
        },
        {
            "id": 66,
            "sectionId": 7,
            "questionText": 'If you receive a traffic violation during the probationary period:',
            "options": ['Nothing happens', 'License is automatically suspended', 'You may face additional restrictions', 'You must retake the road test', 'You pay a fine only'],
            "correctAnswer": 2,
            "explanation": 'If you receive traffic violations during the probationary period, you may face additional restrictions, extended probationary periods, or license suspension.',
            "order": 6
        },
        {
            "id": 67,
            "sectionId": 7,
            "questionText": 'A license examination includes:',
            "options": ['Written test only', 'Road test only', 'Vision, written, and road tests', 'Vision test only', 'Written and vision tests only'],
            "correctAnswer": 2,
            "explanation": 'A license examination includes a vision test, written knowledge test, and road test to demonstrate driving ability.',
            "order": 7
        },
        {
            "id": 68,
            "sectionId": 7,
            "questionText": 'You must notify MVC of an address change within:',
            "options": ['1 week', '2 weeks', '1 month', '2 months', '6 months'],
            "correctAnswer": 0,
            "explanation": 'You must notify MVC of an address change within 1 week of moving to ensure you receive important correspondence.',
            "order": 8
        },
        {
            "id": 69,
            "sectionId": 7,
            "questionText": 'A driver license must be renewed every:',
            "options": ['2 years', '4 years', '5 years', '6 years', '10 years'],
            "correctAnswer": 1,
            "explanation": 'A New Jersey driver license must be renewed every 4 years to maintain driving privileges.',
            "order": 9
        },
        {
            "id": 70,
            "sectionId": 7,
            "questionText": 'Commercial driver license holders must report traffic violations to their employer within:',
            "options": ['24 hours', '48 hours', '1 week', '30 days', '60 days'],
            "correctAnswer": 3,
            "explanation": 'Commercial driver license holders must report traffic violations to their employer within 30 days of conviction.',
            "order": 10
        },
        {
            "id": 71,
            "sectionId": 8,
            "questionText": 'The legal blood alcohol limit for drivers 21 and older is:',
            "options": ['.05%', '.08%', '.10%', '.12%', '.15%'],
            "correctAnswer": 1,
            "explanation": 'The legal blood alcohol limit for drivers 21 and older is .08%. Driving with a BAC of .08% or higher is illegal.',
            "order": 1
        },
        {
            "id": 72,
            "sectionId": 8,
            "questionText": 'The legal blood alcohol limit for drivers under 21 is:',
            "options": ['0%', '.01%', '.02%', '.05%', '.08%'],
            "correctAnswer": 1,
            "explanation": 'The legal blood alcohol limit for drivers under 21 is .01%. New Jersey has a zero tolerance policy for underage drinking and driving.',
            "order": 2
        },
        {
            "id": 73,
            "sectionId": 8,
            "questionText": 'If you refuse a breath test, your license will be suspended for:',
            "options": ['3 months', '6 months', '7 months', '1 year', '2 years'],
            "correctAnswer": 2,
            "explanation": "If you refuse a breath test, your license will be suspended for 7 months for a first offense under New Jersey's Implied Consent Law.",
            "order": 3
        },
        {
            "id": 74,
            "sectionId": 8,
            "questionText": 'Alcohol affects your:',
            "options": ['Vision only', 'Reaction time only', 'Judgment only', 'All driving abilities', 'Coordination only'],
            "correctAnswer": 3,
            "explanation": 'Alcohol affects all driving abilities including vision, reaction time, judgment, coordination, and concentration.',
            "order": 4
        },
        {
            "id": 75,
            "sectionId": 8,
            "questionText": 'The only way to sober up is:',
            "options": ['Coffee', 'Cold shower', 'Fresh air', 'Time', 'Exercise'],
            "correctAnswer": 3,
            "explanation": 'The only way to sober up is time. The liver can only process about one drink per hour, and no other method can speed up this process.',
            "order": 5
        },
        {
            "id": 76,
            "sectionId": 8,
            "questionText": 'Driving under the influence of drugs is:',
            "options": ['Legal if prescribed', 'Less dangerous than alcohol', 'Just as illegal as drunk driving', 'Only illegal for certain drugs', 'Legal in small amounts'],
            "correctAnswer": 2,
            "explanation": 'Driving under the influence of drugs is just as illegal as drunk driving, whether the drugs are illegal, prescription, or over-the-counter.',
            "order": 6
        },
        {
            "id": 77,
            "sectionId": 8,
            "questionText": 'A first DWI conviction can result in license suspension for:',
            "options": ['30 days', '3 months', '6 months', '1 year', '2 years'],
            "correctAnswer": 1,
            "explanation": 'A first DWI conviction can result in license suspension for 3 months, along with fines and possible jail time.',
            "order": 7
        },
        {
            "id": 78,
            "sectionId": 8,
            "questionText": 'When taking prescription medication, you should:',
            "options": ['Drive normally', 'Check with your doctor about driving safety', 'Only drive short distances', 'Drive slower', 'Avoid highways'],
            "correctAnswer": 1,
            "explanation": 'When taking prescription medication, you should check with your doctor about potential effects on driving ability before getting behind the wheel.',
            "order": 8
        },
        {
            "id": 79,
            "sectionId": 8,
            "questionText": 'Mixing alcohol with other drugs:',
            "options": ['Reduces impairment', 'Has no effect', 'Increases impairment', 'Only affects reaction time', 'Is safe in small amounts'],
            "correctAnswer": 2,
            "explanation": 'Mixing alcohol with other drugs increases impairment and can be extremely dangerous, often having unpredictable and severe effects.',
            "order": 9
        },
        {
            "id": 80,
            "sectionId": 8,
            "questionText": 'If convicted of DWI, you may be required to:',
            "options": ['Pay fines only', 'Install an ignition interlock device', 'Attend traffic school only', 'Retake the written test', 'Change insurance companies'],
            "correctAnswer": 1,
            "explanation": 'If convicted of DWI, you may be required to install an ignition interlock device, which prevents the vehicle from starting if alcohol is detected.',
            "order": 10
        },
        {
            "id": 81,
            "sectionId": 9,
            "questionText": 'Children under age 8 and under 57 inches tall must be secured in:',
            "options": ['Seat belts', 'Booster seats', 'Child safety seats', 'Front seat only', 'No special requirements'],
            "correctAnswer": 2,
            "explanation": 'Children under age 8 and under 57 inches tall must be secured in child safety seats or booster seats appropriate for their age and size.',
            "order": 1
        },
        {
            "id": 82,
            "sectionId": 9,
            "questionText": 'Seat belts must be worn by:',
            "options": ['Driver only', 'Front seat passengers only', 'All occupants', 'Adults only', 'Back seat passengers only'],
            "correctAnswer": 2,
            "explanation": 'Seat belts must be worn by all occupants of the vehicle, both front and back seat passengers.',
            "order": 2
        },
        {
            "id": 83,
            "sectionId": 9,
            "questionText": 'The safest place for children under 13 is:',
            "options": ['Front seat', 'Back seat', 'Middle front seat', 'Any seat with airbag', "Driver's lap"],
            "correctAnswer": 1,
            "explanation": 'The safest place for children under 13 is in the back seat, away from airbags and the point of impact in frontal crashes.',
            "order": 3
        },
        {
            "id": 84,
            "sectionId": 9,
            "questionText": 'A rear-facing car seat should be placed:',
            "options": ['In the front seat only', 'Never in front of an airbag', 'Facing forward', 'In the center only', 'Without securing straps'],
            "correctAnswer": 1,
            "explanation": 'A rear-facing car seat should never be placed in front of an active airbag, as airbag deployment can cause serious injury to the child.',
            "order": 4
        },
        {
            "id": 85,
            "sectionId": 9,
            "questionText": 'When should a child move from a car seat to a booster seat?',
            "options": ['At age 3', 'When they outgrow the car seat', 'At 40 pounds', 'When they can walk', 'At age 5'],
            "correctAnswer": 1,
            "explanation": 'A child should move from a car seat to a booster seat when they outgrow the weight or height limits of their current car seat.',
            "order": 5
        },
        {
            "id": 86,
            "sectionId": 9,
            "questionText": 'The driver is responsible for ensuring:',
            "options": ['Their own seat belt only', 'Front passengers are buckled', 'All passengers under 18 are properly secured', 'Adult passengers buckle themselves', 'Only child passengers are secured'],
            "correctAnswer": 2,
            "explanation": 'The driver is responsible for ensuring that all passengers under 18 are properly secured with seat belts or appropriate child restraints.',
            "order": 6
        },
        {
            "id": 87,
            "sectionId": 9,
            "questionText": 'Airbags are designed to work with:',
            "options": ['Nothing else needed', 'Seat belts', 'Only for adults', 'Large passengers', 'Front seat passengers only'],
            "correctAnswer": 1,
            "explanation": 'Airbags are designed to work with seat belts as part of a complete restraint system, not as a replacement for seat belts.',
            "order": 7
        },
        {
            "id": 88,
            "sectionId": 9,
            "questionText": 'If your seat belt is twisted or frayed, you should:',
            "options": ['Use it anyway', 'Not wear it', 'Replace it immediately', 'Only use the lap portion', 'Tie it in place'],
            "correctAnswer": 2,
            "explanation": 'If your seat belt is twisted or frayed, you should replace it immediately as it may not provide proper protection in a crash.',
            "order": 8
        },
        {
            "id": 89,
            "sectionId": 9,
            "questionText": 'Pregnant women should wear seat belts:',
            "options": ['Never', 'Only the shoulder belt', 'Only the lap belt', 'Both lap and shoulder belts properly positioned', 'Loosely for comfort'],
            "correctAnswer": 3,
            "explanation": 'Pregnant women should wear both lap and shoulder belts with the lap belt positioned under the belly and the shoulder belt between the breasts.',
            "order": 9
        },
        {
            "id": 90,
            "sectionId": 9,
            "questionText": 'The fine for not wearing a seat belt is:',
            "options": ['$25', '$46', '$100', '$200', '$500'],
            "correctAnswer": 1,
            "explanation": 'The fine for not wearing a seat belt in New Jersey is $46 for each unrestrained occupant.',
            "order": 10
        },
        {
            "id": 91,
            "sectionId": 10,
            "questionText": 'When you hear an emergency vehicle siren, you should:',
            "options": ['Speed up', 'Stop immediately', 'Pull to the right and stop', 'Continue driving', 'Change lanes left'],
            "correctAnswer": 2,
            "explanation": 'When you hear an emergency vehicle siren, you should pull to the right side of the road and stop to allow the emergency vehicle to pass.',
            "order": 1
        },
        {
            "id": 92,
            "sectionId": 10,
            "questionText": 'You must move over or slow down when passing:',
            "options": ['Any parked car', 'Stopped emergency vehicles', 'Slow-moving vehicles', 'Construction workers', 'All of the above'],
            "correctAnswer": 4,
            "explanation": "New Jersey's Move Over law requires you to move over or slow down when passing stopped emergency vehicles, construction workers, and other hazardous situations.",
            "order": 2
        },
        {
            "id": 93,
            "sectionId": 10,
            "questionText": 'If you cannot move over for an emergency vehicle, you should:',
            "options": ['Maintain speed', 'Speed up', 'Slow down significantly', 'Stop in your lane', 'Change lanes quickly'],
            "correctAnswer": 2,
            "explanation": 'If you cannot move over for an emergency vehicle due to traffic or road conditions, you should slow down significantly and proceed with caution.',
            "order": 3
        },
        {
            "id": 94,
            "sectionId": 10,
            "questionText": 'Emergency vehicles include:',
            "options": ['Police only', 'Fire trucks only', 'Ambulances only', 'Police, fire, and ambulance vehicles', 'Tow trucks only'],
            "correctAnswer": 3,
            "explanation": 'Emergency vehicles include police cars, fire trucks, ambulances, and other authorized emergency response vehicles displaying flashing lights and/or sirens.',
            "order": 4
        },
        {
            "id": 95,
            "sectionId": 10,
            "questionText": 'If your vehicle breaks down on the highway, you should:',
            "options": ['Stay in the vehicle', 'Stand behind the vehicle', 'Move to a safe location away from traffic', 'Wave at passing cars', 'Try to fix it immediately'],
            "correctAnswer": 2,
            "explanation": 'If your vehicle breaks down on the highway, you should move to a safe location away from traffic, preferably beyond barriers or guardrails.',
            "order": 5
        },
        {
            "id": 96,
            "sectionId": 10,
            "questionText": 'When approaching a stopped emergency vehicle with flashing lights, you must:',
            "options": ['Maintain normal speed', 'Move over one lane if possible', 'Stop completely', 'Use your horn', 'Flash your lights'],
            "correctAnswer": 1,
            "explanation": 'When approaching a stopped emergency vehicle with flashing lights, you must move over one lane if possible, or slow down if you cannot change lanes.',
            "order": 6
        },
        {
            "id": 97,
            "sectionId": 10,
            "questionText": 'If you are involved in an accident, you should:',
            "options": ['Leave immediately', 'Move vehicles out of traffic if possible', 'Wait for police regardless', 'Exchange information only', 'Admit fault'],
            "correctAnswer": 1,
            "explanation": 'If you are involved in an accident, you should move vehicles out of traffic if possible and safe to do so, then call police and exchange information.',
            "order": 7
        },
        {
            "id": 98,
            "sectionId": 10,
            "questionText": 'Emergency flashers should be used:',
            "options": ['When parking illegally', 'During heavy rain', 'When your vehicle is disabled', 'While driving slowly', 'In construction zones'],
            "correctAnswer": 2,
            "explanation": 'Emergency flashers should be used when your vehicle is disabled or creating a hazard to warn other drivers of the dangerous situation.',
            "order": 8
        },
        {
            "id": 99,
            "sectionId": 10,
            "questionText": 'The Move Over law applies to:',
            "options": ['Police vehicles only', 'All emergency and service vehicles', 'Fire trucks only', 'Ambulances only', 'Tow trucks only'],
            "correctAnswer": 1,
            "explanation": 'The Move Over law applies to all emergency and service vehicles including police, fire, ambulance, tow trucks, and highway maintenance vehicles.',
            "order": 9
        },
        {
            "id": 100,
            "sectionId": 10,
            "questionText": 'When emergency vehicles approach from behind, you should NOT:',
            "options": ['Pull to the right', 'Stop', 'Slow down', 'Speed up to get out of the way', 'Signal your intentions'],
            "correctAnswer": 3,
            "explanation": 'When emergency vehicles approach from behind, you should NOT speed up to get out of the way. Instead, pull to the right and stop safely.',
            "order": 10
        },
        {
            "id": 101,
            "sectionId": 11,
            "questionText": 'You must stop for a school bus when:',
            "options": ['The bus is loading or unloading children', 'The bus is parked', 'You see children near the bus', 'The bus has flashing red lights', 'All of the above'],
            "correctAnswer": 3,
            "explanation": 'You must stop for a school bus when it displays flashing red lights and extends its stop sign, indicating children are boarding or exiting.',
            "order": 1
        },
        {
            "id": 102,
            "sectionId": 11,
            "questionText": 'You may pass a stopped school bus when:',
            "options": ['Never', 'When the red lights stop flashing', 'When driving slowly', 'When no children are visible', 'When honking your horn'],
            "correctAnswer": 1,
            "explanation": "You may pass a stopped school bus only when the red lights stop flashing and the stop sign is retracted, indicating it's safe to proceed.",
            "order": 2
        },
        {
            "id": 103,
            "sectionId": 11,
            "questionText": 'When a school bus has flashing yellow lights, you should:',
            "options": ['Stop immediately', 'Prepare to stop', 'Speed up to pass', 'Change lanes', 'Honk your horn'],
            "correctAnswer": 1,
            "explanation": 'When a school bus has flashing yellow lights, you should prepare to stop as the bus is preparing to load or unload children.',
            "order": 3
        },
        {
            "id": 104,
            "sectionId": 11,
            "questionText": 'The penalty for illegally passing a school bus can include:',
            "options": ['Warning only', 'Fine and points', 'License suspension', 'Community service', 'All of the above'],
            "correctAnswer": 4,
            "explanation": 'The penalty for illegally passing a school bus can include fines, points on your license, license suspension, and community service.',
            "order": 4
        },
        {
            "id": 105,
            "sectionId": 11,
            "questionText": 'When should you stop for pedestrians in a crosswalk?',
            "options": ['Never', 'Only at traffic lights', 'Always when they are crossing', 'Only if they wave', 'Only during school hours'],
            "correctAnswer": 2,
            "explanation": 'You must always stop for pedestrians who are crossing in a crosswalk, whether marked or unmarked.',
            "order": 5
        },
        {
            "id": 106,
            "sectionId": 11,
            "questionText": 'Pedestrians have the right of way:',
            "options": ['Never', 'In crosswalks only', 'At all intersections', 'Only with traffic signals', 'Everywhere on the road'],
            "correctAnswer": 2,
            "explanation": 'Pedestrians have the right of way at all intersections, whether marked or unmarked, and drivers must yield to them.',
            "order": 6
        },
        {
            "id": 107,
            "sectionId": 11,
            "questionText": 'When turning at an intersection, you must yield to:',
            "options": ['Vehicles only', 'Pedestrians only', 'Both vehicles and pedestrians', 'Emergency vehicles only', 'No one'],
            "correctAnswer": 2,
            "explanation": 'When turning at an intersection, you must yield to both vehicles and pedestrians who have the right of way.',
            "order": 7
        },
        {
            "id": 108,
            "sectionId": 11,
            "questionText": 'A blind pedestrian carrying a white cane or using a guide dog:',
            "options": ['Should be ignored', 'Always has the right of way', 'Must stay on sidewalks', 'Should be honked at', 'Can be passed closely'],
            "correctAnswer": 1,
            "explanation": 'A blind pedestrian carrying a white cane or using a guide dog always has the right of way and must be given extra caution and space.',
            "order": 8
        },
        {
            "id": 109,
            "sectionId": 11,
            "questionText": 'School zones have reduced speed limits during:',
            "options": ['All day', 'School hours and when children are present', 'Morning only', 'Afternoon only', 'Weekdays only'],
            "correctAnswer": 1,
            "explanation": 'School zones have reduced speed limits during school hours and when children are present, requiring extra caution from drivers.',
            "order": 9
        },
        {
            "id": 110,
            "sectionId": 11,
            "questionText": 'When children are playing near the road, you should:',
            "options": ['Maintain normal speed', 'Speed up to pass quickly', 'Slow down and be extra alert', 'Honk to warn them', 'Change lanes immediately'],
            "correctAnswer": 2,
            "explanation": 'When children are playing near the road, you should slow down and be extra alert as children can be unpredictable and may dart into the street.',
            "order": 10
        },
        {
            "id": 111,
            "sectionId": 12,
            "questionText": 'When following a motorcycle, you should:',
            "options": ['Follow closely', 'Maintain the same following distance as for cars', 'Increase your following distance', 'Use high beams', 'Change lanes immediately'],
            "correctAnswer": 2,
            "explanation": 'When following a motorcycle, you should increase your following distance because motorcycles can stop more quickly than cars.',
            "order": 1
        },
        {
            "id": 112,
            "sectionId": 12,
            "questionText": 'Motorcycles are entitled to:',
            "options": ['Half a lane', 'The full width of a traffic lane', 'Share lanes with cars', 'Use only the shoulder', 'Ride between cars'],
            "correctAnswer": 1,
            "explanation": 'Motorcycles are entitled to the full width of a traffic lane, just like any other vehicle.',
            "order": 2
        },
        {
            "id": 113,
            "sectionId": 12,
            "questionText": 'When passing a cyclist, you should:',
            "options": ['Pass as close as possible', 'Leave at least 3 feet of space', 'Honk your horn', 'Speed up quickly', 'Use your high beams'],
            "correctAnswer": 1,
            "explanation": 'When passing a cyclist, you should leave at least 3 feet of space to ensure their safety.',
            "order": 3
        },
        {
            "id": 114,
            "sectionId": 12,
            "questionText": 'Large trucks have:',
            "options": ['Better visibility than cars', 'Smaller blind spots', 'Larger blind spots', 'No blind spots', 'The same visibility as cars'],
            "correctAnswer": 2,
            "explanation": 'Large trucks have larger blind spots than passenger vehicles, especially on the right side and directly behind the truck.',
            "order": 4
        },
        {
            "id": 115,
            "sectionId": 12,
            "questionText": 'When sharing the road with farm equipment, you should:',
            "options": ['Pass immediately', 'Be patient and pass when safe', 'Honk continuously', 'Tailgate to pressure them', 'Use high beams'],
            "correctAnswer": 1,
            "explanation": 'When sharing the road with farm equipment, you should be patient and pass only when it is safe to do so, as they may be wide and slow-moving.',
            "order": 5
        },
        {
            "id": 116,
            "sectionId": 12,
            "questionText": "A truck's blind spot is called:",
            "options": ['Dead zone', 'No-zone', 'Danger zone', 'Hidden area', 'Shadow zone'],
            "correctAnswer": 1,
            "explanation": "A truck's blind spot is called the 'No-Zone' - areas around the truck where the driver cannot see other vehicles.",
            "order": 6
        },
        {
            "id": 117,
            "sectionId": 12,
            "questionText": 'When driving near motorcycles, you should be aware that they:',
            "options": ['Are easier to see', 'Can stop more quickly', 'Are always speeding', "Don't follow traffic laws", "Can't be affected by weather"],
            "correctAnswer": 1,
            "explanation": 'When driving near motorcycles, you should be aware that they can stop more quickly than cars and may be harder to see, especially in adverse weather.',
            "order": 7
        },
        {
            "id": 118,
            "sectionId": 12,
            "questionText": "You should never drive in a truck's:",
            "options": ['Left lane', 'Right lane', 'No-zone', 'Passing lane', 'Exit lane'],
            "correctAnswer": 2,
            "explanation": "You should never drive in a truck's No-Zone (blind spot) as the truck driver cannot see you and may change lanes or turn.",
            "order": 8
        },
        {
            "id": 119,
            "sectionId": 12,
            "questionText": 'When a motorcycle is turning, you should:',
            "options": ['Pass on the right', 'Follow closely', 'Give them extra space', 'Honk your horn', 'Flash your lights'],
            "correctAnswer": 2,
            "explanation": 'When a motorcycle is turning, you should give them extra space as they may need to adjust their position in the lane.',
            "order": 9
        },
        {
            "id": 120,
            "sectionId": 12,
            "questionText": 'Horse-drawn vehicles on the road:',
            "options": ['Must stay on shoulders', 'Have the same rights as motor vehicles', 'Are not allowed', 'Must use bike lanes', 'Only allowed at night'],
            "correctAnswer": 1,
            "explanation": 'Horse-drawn vehicles have the same rights as motor vehicles and must be treated with respect and caution on the roadway.',
            "order": 10
        },
        {
            "id": 121,
            "sectionId": 13,
            "questionText": 'In rainy conditions, you should:',
            "options": ['Drive faster to get out of rain', 'Use cruise control', 'Reduce speed and increase following distance', 'Turn on hazard lights', 'Drive in the left lane only'],
            "correctAnswer": 2,
            "explanation": 'In rainy conditions, you should reduce speed and increase following distance because wet roads reduce traction and increase stopping distance.',
            "order": 1
        },
        {
            "id": 122,
            "sectionId": 13,
            "questionText": 'Hydroplaning occurs when:',
            "options": ['Tires lose contact with the road surface', 'Brakes overheat', 'Engine overheats', 'Steering wheel locks', 'Transmission fails'],
            "correctAnswer": 0,
            "explanation": 'Hydroplaning occurs when tires lose contact with the road surface due to a layer of water, causing loss of traction and control.',
            "order": 2
        },
        {
            "id": 123,
            "sectionId": 13,
            "questionText": 'If your vehicle starts to hydroplane, you should:',
            "options": ['Brake hard', 'Accelerate', 'Ease off the gas and steer straight', 'Turn the wheel sharply', 'Use the parking brake'],
            "correctAnswer": 2,
            "explanation": 'If your vehicle starts to hydroplane, you should ease off the gas and steer straight until you regain traction with the road.',
            "order": 3
        },
        {
            "id": 124,
            "sectionId": 13,
            "questionText": 'In foggy conditions, you should use:',
            "options": ['High beam headlights', 'Low beam headlights', 'Hazard lights', 'Parking lights only', 'No lights'],
            "correctAnswer": 1,
            "explanation": 'In foggy conditions, you should use low beam headlights as high beams can reflect off the fog and reduce visibility further.',
            "order": 4
        },
        {
            "id": 125,
            "sectionId": 13,
            "questionText": 'Black ice is most likely to form:',
            "options": ['In direct sunlight', 'On bridges and overpasses', 'In parking lots', 'On dry roads', 'During summer'],
            "correctAnswer": 1,
            "explanation": 'Black ice is most likely to form on bridges and overpasses because these surfaces freeze first due to cold air circulation above and below.',
            "order": 5
        },
        {
            "id": 126,
            "sectionId": 13,
            "questionText": 'When driving in snow, you should:',
            "options": ['Use cruise control', 'Brake hard to stop quickly', 'Accelerate slowly and brake gently', 'Drive at normal speed', 'Use high beams constantly'],
            "correctAnswer": 2,
            "explanation": 'When driving in snow, you should accelerate slowly and brake gently to maintain traction and avoid skidding.',
            "order": 6
        },
        {
            "id": 127,
            "sectionId": 13,
            "questionText": 'If your vehicle skids on ice, you should:',
            "options": ['Brake immediately', 'Accelerate hard', 'Steer in the direction you want to go', 'Turn the wheel opposite to the skid', 'Use the parking brake'],
            "correctAnswer": 2,
            "explanation": 'If your vehicle skids on ice, you should steer in the direction you want to go and avoid sudden movements that could worsen the skid.',
            "order": 7
        },
        {
            "id": 128,
            "sectionId": 13,
            "questionText": 'Wind can affect your vehicle by:',
            "options": ['Improving fuel economy', 'Reducing stopping distance', 'Pushing it off course', 'Increasing traction', 'Cooling the engine'],
            "correctAnswer": 2,
            "explanation": 'Wind can affect your vehicle by pushing it off course, especially high-profile vehicles, and requiring steering corrections to maintain your lane.',
            "order": 8
        },
        {
            "id": 129,
            "sectionId": 13,
            "questionText": 'When driving through a puddle, you should:',
            "options": ['Speed up to get through quickly', 'Brake while going through', 'Slow down before entering', 'Use cruise control', 'Turn on hazard lights'],
            "correctAnswer": 2,
            "explanation": 'When driving through a puddle, you should slow down before entering to reduce the risk of hydroplaning and maintain control.',
            "order": 9
        },
        {
            "id": 130,
            "sectionId": 13,
            "questionText": 'After driving through deep water, you should:',
            "options": ['Accelerate quickly', 'Test your brakes gently', 'Turn on hazard lights', 'Stop immediately', 'Change lanes'],
            "correctAnswer": 1,
            "explanation": 'After driving through deep water, you should test your brakes gently to make sure they are working properly, as water can affect braking performance.',
            "order": 10
        },
        {
            "id": 131,
            "sectionId": 14,
            "questionText": 'When approaching a railroad crossing with flashing red lights, you must:',
            "options": ['Slow down and proceed with caution', 'Stop completely', 'Speed up to cross quickly', 'Look both ways and proceed', 'Honk your horn'],
            "correctAnswer": 1,
            "explanation": "When approaching a railroad crossing with flashing red lights, you must stop completely and not proceed until the lights stop flashing and it's safe to cross.",
            "order": 1
        },
        {
            "id": 132,
            "sectionId": 14,
            "questionText": 'You must stop at least ____ feet from railroad tracks when a train is approaching.',
            "options": ['10', '15', '20', '25', '50'],
            "correctAnswer": 1,
            "explanation": 'You must stop at least 15 feet from railroad tracks when a train is approaching to ensure safety and avoid being struck by the train.',
            "order": 2
        },
        {
            "id": 133,
            "sectionId": 14,
            "questionText": 'If your vehicle stalls on railroad tracks, you should:',
            "options": ['Try to restart it immediately', 'Get out and move away from the tracks', 'Stay in the vehicle', 'Call for help from inside the car', 'Push the car off the tracks'],
            "correctAnswer": 1,
            "explanation": 'If your vehicle stalls on railroad tracks, you should immediately get out and move away from the tracks and the vehicle, then call for help.',
            "order": 3
        },
        {
            "id": 134,
            "sectionId": 14,
            "questionText": 'Railroad crossings that have no warning devices:',
            "options": ['Are always safe to cross', 'Require you to stop anyway', 'Mean no trains use these tracks', 'Require extra caution', 'Are illegal'],
            "correctAnswer": 3,
            "explanation": 'Railroad crossings that have no warning devices require extra caution - you must look and listen carefully for approaching trains before crossing.',
            "order": 4
        },
        {
            "id": 135,
            "sectionId": 14,
            "questionText": 'A train traveling 55 mph can take ____ to stop.',
            "options": ['100 feet', '500 feet', '1 mile or more', '50 feet', '200 feet'],
            "correctAnswer": 2,
            "explanation": 'A train traveling 55 mph can take a mile or more to stop completely, which is why you must never try to beat a train across the tracks.',
            "order": 5
        },
        {
            "id": 136,
            "sectionId": 14,
            "questionText": 'When waiting at a railroad crossing, you should:',
            "options": ['Rev your engine', 'Turn off your engine', 'Keep your engine running', 'Get out of the vehicle', 'Open all windows'],
            "correctAnswer": 2,
            "explanation": 'When waiting at a railroad crossing, you should keep your engine running so you can move quickly if necessary.',
            "order": 6
        },
        {
            "id": 137,
            "sectionId": 14,
            "questionText": 'You may drive around lowered railroad crossing gates:',
            "options": ['If no train is visible', 'Never', "If you're in a hurry", 'If the gates seem broken', 'If traffic is backing up'],
            "correctAnswer": 1,
            "explanation": 'You may never drive around lowered railroad crossing gates. This is illegal and extremely dangerous as a train may be approaching.',
            "order": 7
        },
        {
            "id": 138,
            "sectionId": 14,
            "questionText": 'At a railroad crossing, you should:',
            "options": ['Speed up to cross quickly', 'Stop, look, and listen', 'Rely only on warning signals', 'Cross immediately if gates are up', 'Honk your horn before crossing'],
            "correctAnswer": 1,
            "explanation": 'At a railroad crossing, you should always stop, look both ways, and listen for approaching trains, even if warning signals are not active.',
            "order": 8
        },
        {
            "id": 139,
            "sectionId": 14,
            "questionText": 'Large trucks and buses must:',
            "options": ['Never cross railroad tracks', 'Stop at all railroad crossings', 'Cross quickly without stopping', 'Only cross at designated points', 'Honk before crossing'],
            "correctAnswer": 1,
            "explanation": 'Large trucks and buses must stop at all railroad crossings to ensure they can cross safely without getting stuck or being struck by a train.',
            "order": 9
        },
        {
            "id": 140,
            "sectionId": 14,
            "questionText": 'If you see a train approaching but think you can beat it across:',
            "options": ["Go for it if you're fast", 'Wait for the train to pass', 'Speed up and cross quickly', 'Flash your lights at the train', 'Honk your horn'],
            "correctAnswer": 1,
            "explanation": 'If you see a train approaching, you should always wait for it to pass completely. Never try to beat a train across the tracks - trains are larger and faster than they appear.',
            "order": 10
        },
        {
            "id": 141,
            "sectionId": 15,
            "questionText": 'When driving at night, you should:',
            "options": ['Use high beams constantly', 'Reduce speed', 'Follow closer to see better', 'Turn on interior lights', 'Drive in the left lane'],
            "correctAnswer": 1,
            "explanation": 'When driving at night, you should reduce speed because visibility is limited and you need more time to react to hazards.',
            "order": 1
        },
        {
            "id": 142,
            "sectionId": 15,
            "questionText": 'Your headlights should be used:',
            "options": ['Only when completely dark', 'From sunset to sunrise', 'Only in bad weather', 'Only on highways', 'Only when raining'],
            "correctAnswer": 1,
            "explanation": 'Your headlights should be used from sunset to sunrise and whenever visibility is reduced, such as in rain, fog, or snow.',
            "order": 2
        },
        {
            "id": 143,
            "sectionId": 15,
            "questionText": 'High beam headlights should be dimmed when:',
            "options": ['Never', 'Within 500 feet of oncoming traffic', 'Only in the city', 'Only on highways', "When it's foggy"],
            "correctAnswer": 1,
            "explanation": 'High beam headlights should be dimmed when within 500 feet of oncoming traffic or when following another vehicle within 300 feet.',
            "order": 3
        },
        {
            "id": 144,
            "sectionId": 15,
            "questionText": 'If an oncoming vehicle has bright headlights, you should:',
            "options": ['Flash your high beams', 'Look directly at the lights', 'Look to the right edge of the road', 'Speed up to pass quickly', 'Turn on your high beams'],
            "correctAnswer": 2,
            "explanation": 'If an oncoming vehicle has bright headlights, you should look to the right edge of the road to avoid being blinded while maintaining your lane position.',
            "order": 4
        },
        {
            "id": 145,
            "sectionId": 15,
            "questionText": 'Driving at night is more dangerous because:',
            "options": ['There are more drunk drivers', 'Visibility is reduced', 'Roads are more crowded', 'Speed limits are higher', 'Police patrol less'],
            "correctAnswer": 1,
            "explanation": 'Driving at night is more dangerous because visibility is reduced, making it harder to see pedestrians, animals, and road hazards.',
            "order": 5
        },
        {
            "id": 146,
            "sectionId": 15,
            "questionText": 'When following another vehicle at night, you should:',
            "options": ['Use high beams', 'Follow more closely', 'Use low beams', 'Turn off headlights', 'Flash your lights'],
            "correctAnswer": 2,
            "explanation": 'When following another vehicle at night, you should use low beams to avoid blinding the driver ahead through their mirrors.',
            "order": 6
        },
        {
            "id": 147,
            "sectionId": 15,
            "questionText": 'Your headlights must be on from sunset to sunrise and when visibility is less than:',
            "options": ['100 feet', '200 feet', '300 feet', '500 feet', '1000 feet'],
            "correctAnswer": 3,
            "explanation": 'Your headlights must be on from sunset to sunrise and when visibility is less than 500 feet due to weather conditions.',
            "order": 7
        },
        {
            "id": 148,
            "sectionId": 15,
            "questionText": 'If you become drowsy while driving, you should:',
            "options": ['Drink coffee and continue', 'Open windows for fresh air', 'Pull over and rest', 'Drive faster to get home quickly', 'Turn up the radio'],
            "correctAnswer": 2,
            "explanation": 'If you become drowsy while driving, you should pull over in a safe place and rest. Drowsy driving can be as dangerous as drunk driving.',
            "order": 8
        },
        {
            "id": 149,
            "sectionId": 15,
            "questionText": 'At night, you can see a vehicle approaching from behind by:',
            "options": ['Turning around', 'Using your rearview mirror', 'Rolling down windows', 'Stopping periodically', 'Using peripheral vision'],
            "correctAnswer": 1,
            "explanation": "At night, you can see a vehicle approaching from behind by using your rearview mirror, which will show the vehicle's headlights.",
            "order": 9
        },
        {
            "id": 150,
            "sectionId": 15,
            "questionText": 'Parking lights should be used:',
            "options": ['Instead of headlights at night', 'Only when parking', 'Never while driving', 'In bad weather only', 'On highways only'],
            "correctAnswer": 2,
            "explanation": 'Parking lights should never be used instead of headlights while driving. They are only for when the vehicle is parked and do not provide adequate illumination for driving.',
            "order": 10
        }
    ]

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
                
                correct_emoji = "✅" if is_correct else "❌"
                with st.expander(f"Question {i+1}: {correct_emoji}"):
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
