import streamlit as st
import ollama

# Page Configuration
st.set_page_config(
    page_title="ClearDoc: Local Plain-Language Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Accessibility & Contrast
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextArea textarea {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "ai_draft" not in st.session_state:
    st.session_state["ai_draft"] = ""
if "is_approved" not in st.session_state:
    st.session_state["is_approved"] = False
if "current_input" not in st.session_state:
    st.session_state["current_input"] = ""
if "sample_dropdown" not in st.session_state:
    st.session_state["sample_dropdown"] = "-- Select a test case --"
if "do_reset" not in st.session_state:
    st.session_state["do_reset"] = False

# Handle Reset Flag at the Top (Before Widget Instantiation)
if st.session_state["do_reset"]:
    st.session_state["sample_dropdown"] = "-- Select a test case --"
    st.session_state["current_input"] = ""
    st.session_state["ai_draft"] = ""
    st.session_state["is_approved"] = False
    st.session_state["do_reset"] = False
    st.rerun()

# App Header
st.title("🛡️ ClearDoc")
st.caption("Privacy-First, 100% Offline Plain-Language Assistant for Dense Text (Powered by Local Gemma 4)")

# Sidebar Information
with st.sidebar:
    st.header("About ClearDoc")
    st.write(
        "Designed for elderly users (such as our persona, Arthur) who require "
        "absolute data privacy. All text processing runs **100% locally on-device** "
        "via Ollama (`gemma4:e2b`). No cloud APIs or external data transfers are used."
    )
    st.markdown("---")
    st.info("💡 **HCI Design Note:** Small models can hallucinate or omit critical details. Our interface enforces a mandatory human review gate before text can be approved and saved.")

# Layout: Two Columns (Source Document vs. AI Draft & Review Gate)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 Source Document")
    
    # Official Test Case Selector linked to session state key
    sample_choice = st.selectbox(
        "Load an official test case (Cases 1-3):",
        [
            "-- Select a test case --", 
            "Case 1: Rheumatoid Arthritis & Joints", 
            "Case 2: Legal Liability & Arbitration", 
            "Case 3: Warfarin / Coumadin & Vitamin K"
        ],
        key="sample_dropdown"
    )
    
    if sample_choice == "Case 1: Rheumatoid Arthritis & Joints":
        st.session_state["current_input"] = (
            "Rheumatoid arthritis (RA) is a chronic systemic inflammatory disease characterized by persistent synovitis affecting peripheral joints. "
            "Structural joint damage manifests as classic deformities including boutonniere deformity of the fingers, swan-neck deformity, and Z-thumb. "
            "The pathogenesis involves pro-inflammatory cytokines such as tumor necrosis factor-alpha (TNF-alpha) and Interleukin-1 (IL-1), which drive "
            "synovial hyperproliferation and cartilage degradation. Regarding dietary adjuncts, polyunsaturated fatty acids like eicosapentaenoic acid (EPA) "
            "from Omega-3 sources and gamma-linolenic acid (GLA) from Omega-6 plant oils modulate inflammatory pathways to help alleviate joint pain."
        )
    elif sample_choice == "Case 2: Legal Liability & Arbitration":
        st.session_state["current_input"] = (
            "TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL THE COMPANY, ITS AFFILIATES, AGENTS, DIRECTORS, EMPLOYEES, "
            "SUPPLIERS OR LICENSORS BE LIABLE FOR ANY INDIRECT, PUNITIVE, INCIDENTAL, SPECIAL, CONSEQUENTIAL OR EXEMPLARY DAMAGES, INCLUDING WITHOUT "
            "LIMITATION DAMAGES FOR LOSS OF PROFITS, GOODWILL, USE, DATA OR OTHER INTANGIBLE LOSSES, ARISING OUT OF OR RELATING TO THE USE OF, OR "
            "INABILITY TO USE, THIS SERVICE. UNDER NO CIRCUMSTANCES WILL THE COMPANY BE RESPONSIBLE FOR ANY DAMAGE, LOSS OR INJURY RESULTING FROM "
            "HACKING, TAMPERING OR OTHER UNAUTHORIZED ACCESS OR USE OF THE SERVICE. ANY DISPUTE MUST BE RESOLVED EXCLUSIVELY THROUGH BINDING, "
            "INDIVIDUAL ARBITRATION, AND YOU WAIVE THE RIGHT TO PARTICIPATE IN A CLASS ACTION LAWSUIT OR CLASS-WIDE ARBITRATION."
        )
    elif sample_choice == "Case 3: Warfarin / Coumadin & Vitamin K":
        st.session_state["current_input"] = (
            "The anticoagulant effect of COUMADIN is mediated by the inhibition of VKORC1, which limits the available active vitamin K1. "
            "Therefore, dietary vitamin K1 can reduce the anticoagulant effect of COUMADIN. Patients should maintain a consistent vitamin K intake. "
            "High vitamin K intake (e.g., from green leafy vegetables like spinach, kale, and turnip greens) can reduce the clinical efficacy of COUMADIN, "
            "leading to a subtherapeutic INR and increased risk of thromboembolism. Conversely, a sudden decrease in vitamin K intake can increase the INR, "
            "putting the patient at risk for severe hemorrhage. Botanical medicines such as garlic, ginkgo, and ginseng may also alter bleeding risk and should be closely monitored."
        )
    elif sample_choice == "-- Select a test case --":
        st.session_state["current_input"] = ""

    source_text = st.text_area(
        "Or paste custom dense medical, legal, or technical text here:",
        value=st.session_state["current_input"],
        height=260,
        placeholder="Paste your complex contract, terms of service, or drug label text here..."
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        simplify_clicked = st.button("✨ Simplify with Gemma", type="primary", use_container_width=True)
    with col_btn2:
        clear_clicked = st.button("🗑️ Clear All & Reset", use_container_width=True)

    if clear_clicked:
        st.session_state["do_reset"] = True
        st.rerun()

    if simplify_clicked:
        if not source_text.strip():
            st.warning("⚠️ Please paste some source text before running the simplification model.")
        else:
            with st.status("🧠 Running local Gemma 4 (e2b) offline...", expanded=True) as status:
                try:
                    system_prompt = (
                        "Rewrite this complex text into plain, easy-to-understand bullet points "
                        "suitable for an older adult. Keep it concise, preserve all numerical thresholds "
                        "accurately, and do NOT invent new facts or medical claims."
                    )
                    
                    stream = ollama.chat(
                        model='gemma4:e2b',
                        messages=[
                            {'role': 'system', 'content': system_prompt},
                            {'role': 'user', 'content': source_text}
                        ],
                        options={'temperature': 0.1},
                        stream=True
                    )
                    
                    accumulated_text = ""
                    for chunk in stream:
                        if 'message' in chunk and 'content' in chunk['message']:
                            accumulated_text += chunk['message']['content']
                    
                    st.session_state["ai_draft"] = accumulated_text.replace("**", "")
                    st.session_state["is_approved"] = False
                    
                    status.update(label="✅ Simplification complete!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    status.update(label="❌ Generation failed", state="error", expanded=True)
                    st.error(f"Connection Error: {e}")

with col2:
    st.subheader("✍️ AI Draft & Human Review Gate")
    
    edited_draft = st.text_area(
        "Review and refine the AI draft side-by-side:",
        value=st.session_state["ai_draft"],
        height=260
    )
    
    st.markdown("### 🔍 Human Verification Checklist")
    st.write("To prevent blind trust in small-model outputs, verify the points below:")
    
    check_numbers = st.checkbox("I have verified that all key numbers, percentages, and timeframes match the source.")
    check_risks = st.checkbox("I have checked for and corrected any safety warnings or direction errors (e.g., risk directions).")
    
    can_approve = check_numbers and check_risks and bool(edited_draft.strip())
    
    if st.button("✅ Approve & Save Verified Text", disabled=not can_approve, use_container_width=True):
        st.session_state["is_approved"] = True
        st.success("Verified! Text is officially reviewed, locked, and cleared for safe use.")
        st.balloons()

    if st.session_state["is_approved"]:
        st.markdown("---")
        st.download_button(
            label="📥 Download Verified Output (.txt)",
            data=edited_draft,
            file_name="cleardoc_verified_output.txt",
            mime="text/plain",
            use_container_width=True
        )