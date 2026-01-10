
import sys
sys.modules.pop("utils.evaluator", None)

import os
from dotenv import load_dotenv
import streamlit as st
import random
from utils.evaluator import AnswerEvaluator
from utils.vector_store import initialize_vector_store

# Load environment variables
load_dotenv()

# Initialize components
evaluator = AnswerEvaluator()
vector_store = initialize_vector_store()

# Page config
st.set_page_config(
    page_title="Electronics Interview Coach",
    page_icon="🔌",
    layout="wide"
)

# Enhanced questions database
QUESTIONS = [
    {
        "id": 1,
        "category": "digital_design",
        "difficulty": "medium",
        "question": "Explain setup and hold time in flip-flops with timing diagrams.",
        "model_answer": """
Setup time is the minimum time before the active clock edge during which the data input must remain stable for reliable sampling. Hold time is the minimum time after the active clock edge during which the data input must remain unchanged.

**Timing Diagram Explanation:**
1. Clock signal with rising/falling edges marked
2. Data signal showing:
   - Setup window (before clock edge)
   - Hold window (after clock edge)
   - Violation case: data changes within setup/hold windows
   - Correct operation: data stable throughout both windows

**Consequences of Violation:**
- Metastability (unpredictable output)
- Data corruption
- System failure in synchronous circuits

**Typical Values:** Setup: 0.1-1ns, Hold: 0.05-0.5ns (varies by technology)
""",
        "key_points": ["definition", "timing windows", "violation consequences", "metastability"],
        "follow_up": "What happens during setup time violation and how can it be prevented?"
    },
    {
        "id": 2,
        "category": "analog_circuits",
        "difficulty": "hard",
        "question": "Compare BJT and MOSFET transistors.",
        "model_answer": """
**BJT (Bipolar Junction Transistor):**
- Current-controlled device (base current controls collector current)
- Lower input impedance (typically kΩ range)
- Higher transconductance (gm)
- Prone to thermal runaway
- Better for linear/analog applications

**MOSFET (Metal-Oxide-Semiconductor FET):**
- Voltage-controlled device (gate voltage controls drain current)
- Very high input impedance (near infinite, GΩ range)
- Lower power consumption in static state
- No gate current (except leakage)
- Preferred for digital circuits and switching applications

**Key Differences:**
1. Control mechanism: Current vs Voltage
2. Input impedance: Low vs Very High
3. Switching speed: MOSFET generally faster
4. Power consumption: MOSFET lower in static state
5. Cost: MOSFET generally cheaper in IC form
""",
        "key_points": ["current vs voltage control", "input impedance", "applications", "power consumption"],
        "follow_up": "Why is MOSFET preferred in digital circuits?"
    },
    {
        "id": 3,
        "category": "digital_design",
        "difficulty": "easy",
        "question": "What is the difference between combinational and sequential circuits?",
        "model_answer": """
**Combinational Circuits:**
- Output depends only on current inputs
- No memory elements
- Examples: Adders, Multiplexers, Decoders
- Timing determined by propagation delay

**Sequential Circuits:**
- Output depends on current inputs AND previous states
- Contains memory elements (flip-flops, latches)
- Examples: Counters, Registers, Finite State Machines
- Requires clock signal for synchronization

**Key Characteristics:**
- Combinational: Stateless, no feedback
- Sequential: Stateful, uses feedback
- Sequential circuits build upon combinational circuits by adding memory
""",
        "key_points": ["memory elements", "state dependency", "clock requirement", "examples"],
        "follow_up": "Give an example of a sequential circuit and explain its operation."
    },
    {
        "id": 4,
        "category": "analog_circuits",
        "difficulty": "medium",
        "question": "Explain the working principle of an operational amplifier.",
        "model_answer": """
**Operational Amplifier (Op-Amp) Basics:**
- Differential amplifier with very high gain (typically 100,000+)
- High input impedance (MΩ to GΩ)
- Low output impedance (typically < 100Ω)
- Two inputs: Inverting (-) and Non-inverting (+)

**Ideal Op-Amp Characteristics:**
1. Infinite open-loop gain
2. Infinite input impedance
3. Zero output impedance
4. Infinite bandwidth
5. Zero offset voltage

**Key Configurations:**
1. **Inverting Amplifier:** Vout = -(Rf/Rin) × Vin
2. **Non-inverting Amplifier:** Vout = (1 + Rf/R1) × Vin
3. **Voltage Follower:** Unity gain buffer
4. **Summing Amplifier:** Weighted sum of inputs
5. **Integrator/Differentiator:** For calculus operations

**Golden Rules (Negative Feedback):**
1. Input terminals draw no current
2. Voltage difference between inputs is zero (virtual short)
""",
        "key_points": ["differential amplification", "ideal characteristics", "configurations", "feedback rules"],
        "follow_up": "What is the significance of virtual short concept in op-amp analysis?"
    },
    {
        "id": 5,
        "category": "digital_design",
        "difficulty": "hard",
        "question": "What is clock skew and how does it affect synchronous circuits?",
        "model_answer": """
**Clock Skew Definition:**
Clock skew is the difference in arrival times of the clock signal at different flip-flops in a synchronous circuit.

**Causes of Clock Skew:**
1. Unequal wire lengths in clock distribution network
2. Buffer delays in clock tree
3. Process variations in manufacturing
4. Temperature gradients across chip

**Types of Clock Skew:**
- **Positive Skew:** Clock arrives later at receiving flip-flop
- **Negative Skew:** Clock arrives earlier at receiving flip-flop

**Effects on Timing:**
1. **Setup Time Violations:** May occur with positive skew
2. **Hold Time Violations:** May occur with negative skew
3. **Reduced Clock Frequency:** Limits maximum operating speed
4. **Race Conditions:** Can cause incorrect data capture

**Mitigation Techniques:**
1. Balanced clock tree synthesis
2. Buffer insertion for delay matching
3. Clock mesh distribution
4. Proper placement and routing

**Timing Margin Calculation:**
Available time = Clock period - Setup time - Clock skew - Jitter
""",
        "key_points": ["definition", "types", "timing effects", "mitigation techniques"],
        "follow_up": "How would you design a clock distribution network to minimize skew?"
    },
    {
        "id": 6,
        "category": "analog_circuits",
        "difficulty": "medium",
        "question": "What is the Barkhausen criteria for oscillation?",
        "model_answer": """
**Barkhausen Criteria** (for sustained oscillations):

**Two Conditions:**
1. **Loop Gain Condition:** |Aβ| = 1
   - The magnitude of loop gain must be exactly unity
   - Aβ < 1: oscillations die out
   - Aβ > 1: oscillations grow (unstable)

2. **Phase Condition:** ∠Aβ = 0° or 360°n (where n is integer)
   - Total phase shift around the loop must be zero or multiples of 360°
   - Ensures positive feedback

**Where:**
- A = Amplifier gain
- β = Feedback network transfer function
- Aβ = Loop gain

**Practical Considerations:**
- In practice, initial Aβ > 1 to start oscillations, then settles to Aβ = 1
- Automatic gain control (AGC) often used to maintain unity gain
- Phase shift oscillators use RC networks for 180° phase shift
- LC oscillators use resonant tanks for frequency selectivity

**Common Oscillator Types:**
1. RC Phase Shift Oscillator
2. Wien Bridge Oscillator
3. Colpitts Oscillator
4. Hartley Oscillator
5. Crystal Oscillator (most stable)
""",
        "key_points": ["loop gain condition", "phase condition", "practical considerations", "oscillator types"],
        "follow_up": "How does a crystal oscillator achieve better frequency stability than RC oscillators?"
    },
    {
        "id": 7,
        "category": "digital_design",
        "difficulty": "medium",
        "question": "Explain different types of finite state machines (FSM).",
        "model_answer": """
**Finite State Machine (FSM) Definition:**
A mathematical model of computation with a finite number of states, transitions between states, and actions.

**Two Main Types:**

**1. Moore Machine:**
- Output depends ONLY on current state
- Output = f(current state)
- Simpler timing, output changes with state transition
- Typically requires more states than Mealy

**2. Mealy Machine:**
- Output depends on current state AND current input
- Output = f(current state, current input)
- Can be more compact (fewer states)
- Output can change asynchronously with input changes

**Comparison:**
| Aspect | Moore | Mealy |
|--------|-------|-------|
| Output dependency | State only | State + Input |
| States required | More | Fewer |
| Output timing | Synchronous | Can be asynchronous |
| Implementation | Often simpler | More complex timing |

**FSM Design Steps:**
1. State diagram development
2. State minimization
3. State encoding (binary, one-hot, gray code)
4. Next-state logic design
5. Output logic design

**Applications:**
- Digital controllers
- Communication protocols
- Sequence detectors
- Game AI
- Traffic light controllers
""",
        "key_points": ["moore vs mealy", "output dependencies", "design steps", "applications"],
        "follow_up": "When would you choose a Mealy machine over a Moore machine?"
    },
    {
        "id": 8,
        "category": "analog_circuits",
        "difficulty": "hard",
        "question": "What is the Miller effect and its impact on amplifier bandwidth?",
        "model_answer": """
**Miller Effect Definition:**
The Miller effect describes the increase in equivalent input capacitance of an inverting voltage amplifier due to capacitance between input and output nodes.

**Miller Theorem:**
A capacitor C connected between input and output of an inverting amplifier with gain -A appears as:
- Input capacitance: C_in = C × (1 + A)
- Output capacitance: C_out = C × (1 + 1/A) ≈ C (for large A)

**Impact on Amplifier Performance:**
1. **Bandwidth Reduction:** 
   - Dominant pole frequency decreases
   - Bandwidth ∝ 1/(C_in × R_source)
   - High gain stages affected most severely

2. **Frequency Response:**
   - Creates a dominant pole at input
   - Reduces unity-gain bandwidth
   - Can cause instability in feedback amplifiers

**Mathematical Analysis:**
For an amplifier with voltage gain -A and feedback capacitor C_f:
- Input Miller capacitance: C_M = C_f × (1 + A)
- Dominant pole frequency: f_p = 1/(2π × R_s × C_M)
- Where R_s is source resistance

**Mitigation Techniques:**
1. **Cascode Configuration:** Isolates input from output
2. **Miller Compensation:** Intentional use for stability
3. **Neutralization:** Adding opposite phase signal
4. **Reducing Gain:** Lower A reduces Miller multiplication

**Practical Example:**
In common-emitter/common-source amplifiers, C_bc/C_gd creates significant Miller capacitance, limiting high-frequency response.
""",
        "key_points": ["definition", "capacitance multiplication", "bandwidth impact", "mitigation techniques"],
        "follow_up": "How does cascode configuration help mitigate the Miller effect?"
    },
    {
        "id": 9,
        "category": "digital_design",
        "difficulty": "easy",
        "question": "What are the differences between latches and flip-flops?",
        "model_answer": """
**Key Differences:**

**Latch:**
- Level-sensitive device
- Transparent when enable is active
- Can change output multiple times during transparency
- Simpler design (fewer transistors)
- Prone to glitches and timing issues
- Examples: SR latch, D latch

**Flip-flop:**
- Edge-triggered device
- Changes state only at clock edges
- Output changes once per clock cycle
- More complex design (master-slave, etc.)
- Better for synchronous design
- Examples: D flip-flop, JK flip-flop

**Detailed Comparison:**
| Characteristic | Latch | Flip-flop |
|----------------|-------|-----------|
| Triggering | Level-sensitive | Edge-triggered |
| Transparency | Transparent when enabled | Opaque between edges |
| Timing Control | Less precise | Precise (clock edges) |
| Metastability | More susceptible | Less susceptible |
| Area/Power | Smaller/lower | Larger/higher |
| Applications | Asynchronous circuits | Synchronous circuits |

**Timing Behavior:**
- Latch: Output follows input when enable=1
- Flip-flop: Samples input at clock edge, holds until next edge

**Design Guidelines:**
- Use flip-flops for synchronous digital design
- Use latches for specific applications like pulse capture
- Avoid latches in general-purpose logic due to timing complexity
""",
        "key_points": ["level vs edge triggering", "transparency", "applications", "timing behavior"],
        "follow_up": "Why are flip-flops preferred over latches in synchronous digital design?"
    },
    {
        "id": 10,
        "category": "analog_circuits",
        "difficulty": "medium",
        "question": "Explain the concept of negative feedback in amplifiers.",
        "model_answer": """
**Negative Feedback Concept:**
A portion of output signal is fed back 180° out of phase with input, reducing overall gain but improving other characteristics.

**Basic Configuration:**
Input → [Amplifier A] → Output
        ↑            ↓
        └──[Feedback Network β]──┘

**Closed-Loop Gain:**
A_f = A / (1 + Aβ)
Where:
- A = Open-loop gain
- β = Feedback factor
- Aβ = Loop gain

**Advantages of Negative Feedback:**

1. **Gain Stability:**
   - Reduces sensitivity to parameter variations
   - Gain depends mainly on passive components (β network)

2. **Bandwidth Extension:**
   - Gain-bandwidth product remains constant
   - Lower gain → Higher bandwidth

3. **Noise Reduction:**
   - Improves signal-to-noise ratio
   - Reduces distortion and non-linearities

4. **Impedance Modification:**
   - Increases input impedance (series feedback)
   - Decreases output impedance (shunt feedback)

**Types of Negative Feedback:**
1. **Voltage Series (Series-Shunt):** Increases R_in, decreases R_out
2. **Voltage Shunt (Shunt-Shunt):** Decreases both R_in and R_out
3. **Current Series (Series-Series):** Increases both R_in and R_out
4. **Current Shunt (Shunt-Series):** Decreases R_in, increases R_out

**Trade-offs:**
- Reduced gain (designed sacrifice)
- Potential stability issues (phase margins)
- Requires careful compensation
""",
        "key_points": ["closed-loop gain", "advantages", "feedback types", "trade-offs"],
        "follow_up": "What are the stability criteria for negative feedback amplifiers?"
    }
]

# Initialize session state
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = False

# Main app
st.title("🔌 Electronics Interview Coach")
st.markdown("Practice electronics interview questions with AI feedback")
st.markdown("---")

# Progress indicator
total_questions = len(QUESTIONS)
current_q_num = st.session_state.current_index + 1
progress = current_q_num / total_questions
st.progress(progress, text=f"Question {current_q_num} of {total_questions}")

# Get current question
current_q = QUESTIONS[st.session_state.current_index]

st.subheader("❓ Question")
st.write(f"**{current_q['question']}**")
st.caption(f"Category: {current_q['category'].replace('_', ' ').title()}   •   Difficulty: {current_q['difficulty'].title()}")

user_answer = st.text_area(
    "✏️ Your Answer:", 
    height=150, 
    placeholder="Type your detailed answer here...\n\nTip: Include definitions, explanations, and examples for best results.",
    key=f"answer_{st.session_state.current_index}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit_btn = st.button("📤 Submit Answer", type="primary", use_container_width=True)
with col2:
    feedback_btn = st.button("🤖 Get AI Feedback", use_container_width=True, disabled=not st.session_state.get('answer_submitted', False))
with col3:
    next_btn = st.button("⏭️ Next Question", use_container_width=True)

# Handle buttons
# Handle buttons
if submit_btn:
    if len(user_answer.strip()) >= 20:
        st.session_state.answer_submitted = True
        st.success("✅ Answer submitted! Click 'Get AI Feedback' for evaluation.")
        st.session_state.feedback_given = False
    else:
        st.warning("⚠️ Please write a more detailed answer (minimum 20 characters).")

if feedback_btn and st.session_state.get('answer_submitted', False):
    if len(user_answer.strip()) >= 20:
        with st.spinner("🤖 AI is evaluating your answer..."):
            
            # ============================================
            # SMART FEEDBACK GENERATOR
            # ============================================
            
            # Initialize feedback components
            score = 5  # Start with average score
            strengths = []
            improvements = []
            
            # Convert to lowercase for analysis
            answer_lower = user_answer.lower()
            question_lower = current_q['question'].lower()
            
            # ============================================
            # SCORING LOGIC
            # ============================================
            
            # 1. LENGTH SCORING (0-3 points)
            word_count = len(user_answer.split())
            if word_count > 100:
                score += 3
                strengths.append("Comprehensive answer with good detail")
            elif word_count > 60:
                score += 2
                strengths.append("Good answer length")
            elif word_count > 30:
                score += 1
                strengths.append("Adequate answer length")
            else:
                score -= 2
                improvements.append("Answer is too brief - aim for at least 50 words")
            
            # 2. QUESTION-SPECIFIC SCORING
            
            # Setup/Hold Time Question
            if 'setup' in question_lower and 'hold' in question_lower:
                # Check for correct concepts
                has_setup = 'setup' in answer_lower
                has_hold = 'hold' in answer_lower
                has_clock = 'clock' in answer_lower
                has_stable = 'stable' in answer_lower or 'constant' in answer_lower
                has_before = 'before' in answer_lower
                has_after = 'after' in answer_lower
                
                # Check for MAJOR ERROR: Reversed concepts
                reversed_error = False
                if ('setup' in answer_lower and 'after' in answer_lower and 
                    'hold' in answer_lower and 'before' in answer_lower):
                    # User said "setup after" and "hold before" - REVERSED!
                    reversed_error = True
                    score = 2  # Very low score for major conceptual error
                    improvements.append("❌ **MAJOR CONCEPT ERROR:** You reversed setup and hold time!")
                    improvements.append("✓ Setup time is BEFORE clock edge")
                    improvements.append("✓ Hold time is AFTER clock edge")
                
                # If not reversed, normal scoring
                if not reversed_error:
                    if has_setup and has_hold:
                        score += 3
                        strengths.append("Correctly identified both setup and hold time")
                    elif has_setup or has_hold:
                        score += 1
                        strengths.append(f"Mentioned {'setup' if has_setup else 'hold'} time")
                        improvements.append(f"Missing {'hold' if has_setup else 'setup'} time definition")
                    else:
                        score -= 2
                        improvements.append("Missing both setup and hold time concepts")
                    
                    if has_clock:
                        score += 1
                        strengths.append("Related timing to clock edges")
                    else:
                        improvements.append("Should mention clock signal relationship")
                    
                    if has_stable:
                        score += 1
                        strengths.append("Correctly mentioned data stability requirement")
                    
                    # Check for timing diagram mention
                    if 'diagram' in answer_lower or 'timing' in answer_lower or 'waveform' in answer_lower:
                        score += 1
                        strengths.append("Considered timing diagrams as requested")
                    else:
                        improvements.append("Include description of timing diagrams")
                    
                    # Check for violation consequences
                    if any(word in answer_lower for word in ['violat', 'metastab', 'error', 'fail', 'problem']):
                        score += 1
                        strengths.append("Discussed consequences of timing violations")
                    else:
                        improvements.append("Mention what happens during setup/hold violations")
            
            # BJT vs MOSFET Question
            elif 'bjt' in question_lower and 'mosfet' in question_lower:
                has_current = 'current' in answer_lower
                has_voltage = 'voltage' in answer_lower
                has_impedance = 'impedance' in answer_lower or 'resistance' in answer_lower
                
                if has_current and has_voltage:
                    score += 3
                    strengths.append("Correctly identified control mechanism difference")
                elif has_current or has_voltage:
                    score += 1
                    improvements.append(f"Missing {'voltage' if has_current else 'current'} control aspect")
                
                if has_impedance:
                    score += 1
                    strengths.append("Mentioned input impedance difference")
                
                if 'digital' in answer_lower or 'switch' in answer_lower:
                    score += 1
                    strengths.append("Correctly identified MOSFET preference in digital circuits")
            
            # ============================================
            # FINAL SCORE ADJUSTMENT (1-10 scale)
            # ============================================
            score = max(1, min(10, score))
            
            # ============================================
            # QUALITY-BASED FEEDBACK
            # ============================================
            if score >= 9:
                feedback_title = "🎉 Excellent Answer!"
                strengths.append("Comprehensive and technically accurate")
            elif score >= 7:
                feedback_title = "✅ Good Answer"
                if not improvements:
                    improvements.append("Add more examples for even better answer")
            elif score >= 5:
                feedback_title = "📚 Average Answer"
                if not improvements:
                    improvements.append("Review key concepts and add more detail")
            else:
                feedback_title = "⚠️ Needs Improvement"
                if not strengths:
                    strengths.append("You attempted the question - good starting point")
            
            # ============================================
            # DISPLAY RESULTS
            # ============================================
            st.markdown("---")
            st.subheader(f"📊 {feedback_title}")
            
            # Score display with color
            col_a, col_b, col_c = st.columns([1, 1, 2])
            with col_a:
                if score >= 8:
                    st.metric("🎯 **Score**", f"{score}/10", delta="Good")
                elif score >= 6:
                    st.metric("🎯 **Score**", f"{score}/10", delta="Average")
                else:
                    st.metric("🎯 **Score**", f"{score}/10", delta="Needs Work")
            
            with col_b:
                st.metric("📝 **Words**", word_count)
            
            # Strengths section
            st.write("**✅ Strengths:**")
            for strength in strengths[:3]:  # Show top 3 strengths
                st.success(f"• {strength}")
            
            # Improvements section
            st.write("**📈 Areas for Improvement:**")
            for improvement in improvements[:3]:  # Show top 3 improvements
                st.warning(f"• {improvement}")
            
            # Show more detailed feedback if score is low
            if score < 6:
                with st.expander("🔍 Detailed Analysis"):
                    st.write(f"**Answer Analysis:**")
                    st.write(f"- Keywords found: {[word for word in ['setup', 'hold', 'clock', 'stable'] if word in answer_lower]}")
                    st.write(f"- Answer relevance: {'High' if word_count > 50 else 'Medium' if word_count > 25 else 'Low'}")
                    st.write(f"**Tip:** Try to structure your answer with: 1) Definition 2) Explanation 3) Example 4) Importance")
            
            # Model Answer
            with st.expander("📘 View Model Answer"):
                st.markdown(current_q['model_answer'])
                st.caption("Compare your answer with this model answer to identify gaps.")
            
            # Follow-up Question
            st.write("**💭 Follow-up Question (for deeper understanding):**")
            st.info(current_q['follow_up'])
            
    else:
        st.warning("⚠️ Please write a more detailed answer (minimum 20 characters) to get feedback.")
if next_btn:
    st.session_state.current_index = (st.session_state.current_index + 1) % len(QUESTIONS)
    st.session_state.answer_submitted = False
    st.session_state.feedback_given = False
    st.rerun()

# Sidebar with additional features
with st.sidebar:
    st.header("📚 Question Bank")
    
    # Category filter
    categories = list(set([q["category"] for q in QUESTIONS]))
    selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    # Difficulty filter
    difficulties = list(set([q["difficulty"] for q in QUESTIONS]))
    selected_difficulty = st.selectbox("Filter by Difficulty", ["All"] + difficulties)
    
    # Filtered questions list
    filtered_questions = QUESTIONS
    if selected_category != "All":
        filtered_questions = [q for q in filtered_questions if q["category"] == selected_category]
    if selected_difficulty != "All":
        filtered_questions = [q for q in filtered_questions if q["difficulty"] == selected_difficulty]
    
    # Question selector
    st.write(f"**Available Questions: {len(filtered_questions)}**")
    for idx, q in enumerate(filtered_questions):
        if st.button(f"Q{q['id']}: {q['question'][:50]}...", key=f"select_{q['id']}"):
            st.session_state.current_index = QUESTIONS.index(q)
            st.session_state.answer_submitted = False
            st.session_state.feedback_given = False
            st.rerun()
    
    st.markdown("---")
    st.header("📈 Progress")
    st.metric("Questions Completed", f"{current_q_num-1}/{total_questions}")
    
    if st.button("🔄 Restart Practice"):
        st.session_state.current_index = 0
        st.session_state.answer_submitted = False
        st.session_state.feedback_given = False
        st.session_state.user_score = 0
        st.rerun()

# Footer
st.markdown("---")
st.caption("Electronics Interview Coach v1.0 • Built with Streamlit & OpenAI • Practice makes perfect! 🚀")
