import streamlit as st
import time
from dotenv import load_dotenv
from graph.orchestrator import build_graph
import os
from config import get_config
from vectorstore.chat_store import list_sessions, get_session, create_session


load_dotenv()


st.set_page_config(
    page_title="Startup Intelligence Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- Custom CSS for better styling ----------------------
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


# ---------------------- Main method to show all stuff ----------------------
def main():
    
    cfg = get_config()
    tavily_key = cfg.get("TAVILY_API_KEY")

    if "selected_session_id" not in st.session_state:
        st.session_state["selected_session_id"] = None
    if "new_chat_clicked" not in st.session_state:
        st.session_state["new_chat_clicked"] = False

# ---------------------- Sidebar: chat history ----------------------
    with st.sidebar:
        st.subheader("@Startup Intelligence Agent/")
        sessions = list_sessions()
        titles = [s.get("title", "Untitled") for s in sessions]
        ids = [s.get("id") for s in sessions]
        
        new_chat = st.button("+ New Chat", use_container_width=True)
        if new_chat:
            st.session_state["selected_session_id"] = None
            st.session_state["new_chat_clicked"] = True
            st.rerun()  
    
        if ids:
            current_idx = None
            if st.session_state["selected_session_id"] in ids:
                current_idx = ids.index(st.session_state["selected_session_id"])
            
            selected_idx = st.selectbox(
                "Chats", 
                list(range(len(ids))), 
                index=current_idx,
                format_func=lambda i: titles[i],
                key="chat_selector"
            )
            
            if selected_idx is not None and selected_idx != current_idx:
                st.session_state["selected_session_id"] = ids[selected_idx]
                st.session_state["new_chat_clicked"] = False
                st.rerun()  

# ---------------------- Header ----------------------
    st.markdown('<h1 class="main-header"> Startup Intelligence Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered market research and pitch generation for your startup idea</p>', unsafe_allow_html=True)
    
    
    if st.session_state.get("new_chat_clicked", False):
        st.markdown('<h2 style="text-align: center;">✨ New Chat - Enter Your Startup Idea</h2>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="text-align: center;">Enter Your Startup Idea</h2>', unsafe_allow_html=True)
    
    selected_session = None
    if st.session_state["selected_session_id"] and not st.session_state["new_chat_clicked"]:
        selected_session = get_session(st.session_state["selected_session_id"])

    form_key = f"startup_form_{st.session_state.get('selected_session_id', 'new')}"
    with st.form(form_key):
        prefill = ""
        if selected_session and selected_session.get("messages"):
            user_msgs = [m for m in selected_session.get("messages", []) if m.get("role") == "user"]
            if user_msgs:
                prefill = user_msgs[-1].get("content", "")

        startup_topic = st.text_area(
            "Describe your startup idea or target market:",
            value=prefill,
            placeholder="e.g., AI-powered fitness app for busy professionals, sustainable food delivery service, fintech solution for small businesses...",
            height=100,
            key=f"startup_topic_{st.session_state.get('selected_session_id', 'new')}"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            submit_button = st.form_submit_button("🚀 Generate Intelligence Report", use_container_width=True)
    
    
    if 'example_selected' in st.session_state:
        startup_topic = st.session_state.example_selected
        del st.session_state.example_selected
    
    if not submit_button and st.session_state["selected_session_id"] and not st.session_state["new_chat_clicked"]:
        if selected_session:
            result_loaded = (selected_session.get("extra", {}) or {}).get("result", {})
            if result_loaded:
                st.header("📈 Intelligence Report")
                tab1, tab2, tab3 = st.tabs(["📝 Generated Pitch", "🔍 Research Insights", "💡 Recommendations"])
                with tab1:
                    topic = "N/A"
                    if selected_session.get("messages"):
                        user_msgs = [m for m in selected_session.get("messages", []) if m.get("role") == "user"]
                        if user_msgs:
                            topic = user_msgs[-1].get("content", "N/A")
                    
                    st.markdown(f"""
                    <div class="result-container">
                    <h3>🎯 Investor-Ready Pitch Outline</h3>
                    <p><strong>Topic:</strong> {topic}</p>
                    <hr>
                    {result_loaded.get('pitch', 'No pitch stored')}
                    </div>
                    """, unsafe_allow_html=True)
                with tab2:
                    st.markdown("""
                    <div class="result-container">
                    <h3>🔍 Research Data</h3>
                    <p>This section contains the raw insights gathered during the research phase.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if 'research_data' in result_loaded:
                        st.text_area("Research Findings:", result_loaded['research_data'], height=200)
                    else:
                        st.info("Research data not available in stored session.")
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

    
    if submit_button and startup_topic:
        st.session_state["new_chat_clicked"] = False
        
        if not tavily_key:
            st.error("❌ Please set your TAVILY_API_KEY in the .env file to proceed.")
            return
            
        st.header("🔄 Processing Your Startup Idea...")
        
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🚀 Initializing AI agents...")
            progress_bar.progress(15)
            
            status_text.text("🔍 Conducting market research...")
            progress_bar.progress(25)
            
            graph = build_graph(startup_topic)
            
            status_text.text("📊 Analyzing data and generating insights...")
            progress_bar.progress(60)

            result = graph.invoke({})
            
            status_text.text("✅ Intelligence report generated successfully!")
            progress_bar.progress(100)
            
            progress_bar.empty()
            status_text.empty()
            
            st.header("📈 Intelligence Report")
            
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
                
# ---------------------- Pitch Download Button ----------------------
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
            
            try:
                title = startup_topic.strip()[:60] or "Untitled"
                session_id = create_session(title=title, user_prompt=startup_topic, result=result)
                st.session_state["selected_session_id"] = session_id
            except Exception as e:
                st.warning(f"⚠️ Failed to save chat session: {e}")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your configuration and try again.")
            
            with st.expander("🐛 Debug Information"):
                st.text(f"Error details: {str(e)}")
                st.text("Make sure:")
                st.text("1. Ollama is running locally")
                st.text("2. Gemma:2b model is installed")
                st.text("3. TAVILY_API_KEY is set in .env file")
                st.text("4. Check the console for detailed error messages")
    
    elif submit_button and not startup_topic:
        st.warning("⚠️ Please enter your startup idea or select an example.")
    
# ---------------------- Footer ----------------------
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
    🚀 Startup Intelligence Agent | Powered by AI | Built with Streamlit & LangChain
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()