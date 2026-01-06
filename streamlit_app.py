import streamlit as st
import time
from models.analyzer import CodeReviewModel
from engine.syntax_checker import SyntaxChecker

# Page Config
st.set_page_config(
    page_title="RefineCode AI",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextArea textarea {
        font-family: 'Consolas', 'Courier New', monospace;
    }
    .bug-high {
        color: #ff4b4b;
        font-weight: bold;
    }
    .bug-low {
        color: #2e7bcf;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐛 RefineCode AI: Automatic Code Review")
st.markdown("### Powered by CodeBERT & DistilBERT")

# Sidebar
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Select Model", ["CodeBERT (Bug Prediction)", "DistilBERT (Style Check)"])
    language = st.selectbox("Language", ["Python", "Java", "C++", "JavaScript"])
    st.info("This system uses pre-trained Transformer models to detect bugs and analyze code quality.")

# Load Models (Cached)
@st.cache_resource
def load_engine():
    return CodeReviewModel(use_cuda=False), SyntaxChecker()

with st.spinner("Loading AI Models..."):
    model_engine, syntax_engine = load_engine()

# Main Input
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Source Code")
    code_input = st.text_area("Paste your code here:", height=300, value="def example():\n    return 1 / 0")
    analyze_btn = st.button("Analyze Code", type="primary")

with col2:
    st.subheader("Analysis Results")
    
    if analyze_btn:
        if not code_input.strip():
            st.warning("Please enter some code to analyze.")
        else:
            # Progress bar simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Checking syntax...")
            progress_bar.progress(30)
            time.sleep(0.5)
            
            # Syntax Check
            syntax_res = syntax_engine.check_syntax(code_input, language)
            
            status_text.text(f"Running {model_choice} inference...")
            progress_bar.progress(70)
            
            # Model Prediction
            bug_prob = model_engine.predict_bug_probability(code_input)
            
            progress_bar.progress(100)
            status_text.text("Analysis Complete!")
            time.sleep(0.5)
            status_text.empty()
            progress_bar.empty()
            
            # Display Results
            st.markdown("#### Syntax Status")
            if syntax_res['valid']:
                st.success("✅ Syntax Valid")
            else:
                st.error(f"❌ Syntax Error: {syntax_res['error']}")
            
            st.markdown("---")
            st.markdown("#### Bug Probability")
            
            if bug_prob > 0.5:
                st.markdown(f"<span class='bug-high'>High Risk: {bug_prob:.2%}</span>", unsafe_allow_html=True)
                st.error("⚠️ Potential bugs detected! Review logic carefully.")
            else:
                st.markdown(f"<span class='bug-low'>Low Risk: {bug_prob:.2%}</span>", unsafe_allow_html=True)
                st.success("✨ Code looks relatively safe.")
            
            with st.expander("Detailed Insights"):
                st.write(f"Model used: {model_choice}")
                st.write(f"Language: {language}")
                st.write("Tokenizer tokens count:", len(code_input.split()))
