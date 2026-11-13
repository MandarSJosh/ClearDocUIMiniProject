import streamlit as st
import ollama

# Page setup for a clean, modern aesthetic
st.set_page_config(
    page_title="ClearDoc: Local Plain-Language Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS styling to make the app look polished and professional
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🛡️ ClearDoc")
st.markdown("**Local Plain-Language Assistant** — *Privacy-First On-Device Text Simplification*")

st.markdown("---")

# Initialize session state for draft persistence
if 'draft' not in st.session_state:
    st.session_state['draft'] = ""
if 'raw_input' not in st.session_state:
    st.session_state['raw_input'] = ""

# Main two-column layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 1. Source Document")
    st.markdown("Paste any dense articles, technical manuals, policy documents, or complex text below.")
    
    original_text = st.text_area(
        "Original Text Input", 
        height=380, 
        placeholder="Paste dense, complex text here...",
        value=st.session_state['raw_input'],
        label_visibility="collapsed"
    )
    
    # Action buttons for column 1
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        simplify_btn = st.button("✨ Simplify with Gemma", type="primary")
    with b_col2:
        clear_btn = st.button("🗑️ Clear Text")
        if clear_btn:
            st.session_state['raw_input'] = ""
            st.session_state['draft'] = ""
            st.rerun()

with col2:
    st.subheader("🔍 2. Human-in-the-Loop Review")
    st.markdown("Review the local AI model's draft. Edit errors or missing caveats before approval.")
    
    if simplify_btn and original_text:
        st.session_state['raw_input'] = original_text
        with st.spinner("Running Gemma 4 locally on-device..."):
            try:
                response = ollama.chat(model='gemma4:e2b', messages=[
                    {
                        'role': 'system', 
                        'content': 'Rewrite this complex text into plain, easy-to-understand language as clear bullet points. Keep it brief. Do NOT invent new facts.'
                    },
                    {
                        'role': 'user', 
                        'content': original_text
                    }
                ])
                st.session_state['draft'] = response['message']['content']
            except Exception as e:
                st.error(f"Local Model Error: {e}")
                st.info("💡 Mitigation Tip: Ensure Ollama is running in your terminal (`ollama run gemma4:e2b`)")

    # Editable review area (Critical HCI mitigation component)
    edited_draft = st.text_area(
        "Editable AI Draft", 
        value=st.session_state['draft'], 
        height=380,
        placeholder="Simplified draft will appear here for human review...",
        label_visibility="collapsed"
    )
    
    # Approval action button
    if st.button("✅ Approve & Save Verified Text", type="secondary"):
        if edited_draft:
            st.success("🎉 Verified! Text successfully approved and locked for use.")
            st.balloons()
        else:
            st.warning("⚠️ Cannot approve an empty document. Please process or enter text first.")

# Footer info
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6c757d; font-size: 0.85rem;'>"
    "ClearDoc UI Mini Project • Designed for Small-Model Failure Mitigation & Local Data Privacy"
    "</div>", 
    unsafe_allow_html=True
)