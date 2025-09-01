import streamlit as st
import time
from dotenv import load_dotenv
from graph.orchestrator import build_graph
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Startup Intelligence Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
        margin-top: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.6rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        line-height: 1.4;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    .result-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .step-container {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #1f77b4;
    }
    /* Center the main content */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    /* Center the form elements */
    .stForm {
        max-width: 800px;
        margin: 0 auto;
    }
    /* Center the example ideas */
    .stButton {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Startup Intelligence Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered market research and pitch generation for your startup idea</p>', unsafe_allow_html=True)
    
    
    # Main content area - using full width for better centering
    st.markdown('<h2 style="text-align: center;">Enter Your Startup Idea</h2>', unsafe_allow_html=True)
    
    # Input form
    with st.form("startup_form"):
        startup_topic = st.text_area(
            "Describe your startup idea or target market:",
            placeholder="e.g., AI-powered fitness app for busy professionals, sustainable food delivery service, fintech solution for small businesses...",
            height=100
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            submit_button = st.form_submit_button("🚀 Generate Intelligence Report", use_container_width=True)
    
    
    # Use example if selected
    if 'example_selected' in st.session_state:
        startup_topic = st.session_state.example_selected
        del st.session_state.example_selected
    
    # Process the request
    if submit_button and startup_topic:
        if not tavily_key:
            st.error("❌ Please set your TAVILY_API_KEY in the .env file to proceed.")
            return
            
        st.header("🔄 Processing Your Startup Idea...")
        
        # Progress tracking with real-time updates
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Initialize (no artificial delay)
            status_text.text("🚀 Initializing AI agents...")
            progress_bar.progress(15)
            
            # Step 2: Research (most time-consuming step)
            status_text.text("🔍 Conducting market research...")
            progress_bar.progress(25)
            
            # Build and execute the graph
            graph = build_graph(startup_topic)
            
            # Step 3: Analysis and generation
            status_text.text("📊 Analyzing data and generating insights...")
            progress_bar.progress(60)
            
            # Execute the graph
            result = graph.invoke({})
            
            # Step 4: Complete
            status_text.text("✅ Intelligence report generated successfully!")
            progress_bar.progress(100)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.header("📈 Intelligence Report")
            
            # Create tabs for different sections
            tab1, tab2, tab3 = st.tabs(["📝 Generated Pitch", "🔍 Research Insights", "💡 Recommendations"])
            
            with tab1:
                st.markdown(f"""
                <div class="result-container">
                <h3>🎯 Investor-Ready Pitch Outline</h3>
                <p><strong>Topic:</strong> {startup_topic}</p>
                <hr>
                {result.get('pitch', 'No pitch generated')}
                </div>
                """, unsafe_allow_html=True)
                
                # Download button
                pitch_content = f"Startup Idea: {startup_topic}\n\n{result.get('pitch', '')}"
                st.download_button(
                    label="📥 Download Pitch as Text",
                    data=pitch_content,
                    file_name=f"pitch_{startup_topic.replace(' ', '_')[:20]}.txt",
                    mime="text/plain"
                )
            
            with tab2:
                st.markdown("""
                <div class="result-container">
                <h3>🔍 Research Data</h3>
                <p>This section contains the raw insights gathered during the research phase.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if 'research_data' in result:
                    st.text_area("Research Findings:", result['research_data'], height=200)
                else:
                    st.info("Research data not available in current result format.")
            
            with tab3:
                st.markdown("""
                <div class="result-container">
                <h3>💡 Next Steps & Recommendations</h3>
                <ul>
                <li>Validate your market assumptions with potential customers</li>
                <li>Research the identified competitors more deeply</li>
                <li>Develop a minimum viable product (MVP)</li>
                <li>Consider the regulatory environment for your industry</li>
                <li>Build a financial model based on the market size insights</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your configuration and try again.")
            
            # Debug information
            with st.expander("🐛 Debug Information"):
                st.text(f"Error details: {str(e)}")
                st.text("Make sure:")
                st.text("1. Ollama is running locally")
                st.text("2. Gemma:2b model is installed")
                st.text("3. TAVILY_API_KEY is set in .env file")
                st.text("4. Check the console for detailed error messages")
    
    elif submit_button and not startup_topic:
        st.warning("⚠️ Please enter your startup idea or select an example.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
    🚀 Startup Intelligence Agent | Powered by AI | Built with Streamlit & LangChain
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()