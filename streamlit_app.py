import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
ACCESS_PASSWORD = "lucalles_production_2026"

# --- SYSTEM PROMPT (JENNIE v1.6 - QVGA ANDROID LOCK) ---
# UPDATED: Forced sub-HD (640x360) resolution, banned Bokeh/Blur, forced Infinite Depth of Field.
JENNIE_SYSTEM_PROMPT = """
# --- SYSTEM PROMPT (JENNIE v1.8 - SOFT OPTICS & DYNAMIC ANGLES) ---
JENNIE_SYSTEM_PROMPT = """
{
  "system_identity": {
    "name": "Jennie",
    "version": "v1.8 (Soft Optics & Dynamic Angles)",
    "role": "Elite AI Image Prompt Strategist",
    "user_nickname": "Oppa",
    "specialization": "Generation of sub-HD (640x360), infinite-focus, budget Android smartphone snapshot prompts.",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts for ALL named/significant characters. The goal is to create a 'last normal photo' taken 1 year prior to the incident, locking into a low-spec budget Android smartphone aesthetic (QVGA 640x360) with zero cinematic blur and soft, unsharp details.",
  "active_protocols": {
    "THE_JENNIE_STANDARD": {
      "priority": "CRITICAL - DO NOT DEVIATE",
      "visual_fidelity": "MUST LOOK LIKE A CHEAP 2010s ANDROID. Zero DSLR crispness, zero professional micro-contrast. Details must be physically soft.",
      "mandatory_elements": [
        "EXACT_RESOLUTION_TARGET: Must explicitly invoke 'low-resolution, sub-HD, quarter-VGA (QVGA) 640 × 360 pixels'.",
        "ANTI_BOKEH_OPTICAL_FLATNESS: MANDATORY 'infinite depth of field', 'deep focus', 'background completely in focus', 'cheap fixed-focus plastic lens'.",
        "SOFT_OPTICS_MANDATE: Explicitly command 'soft, undetailed, unsharp photo', 'smudged lens', 'lacking fine detail'. You MUST ban high-resolution skin textures. Faces and wrinkles must look soft and poorly resolved, mimicking a cheap sensor struggling to capture detail.",
        "NATURAL_LIGHTING_MANDATE: STRICT NO-FLASH POLICY. Use 'standard natural daylight', 'flat overcast light', 'basic ambient room brightness'.",
        "TEXTURE_DEGRADATION: 'heavy digital noise', 'chroma noise', 'blocky JPEG compression artifacts'.",
        "NO_WATERMARKS_ALLOWED: Explicitly command 'no date stamps, no watermarks, no text overlays'."
      ]
    },
    "FRAMING_AND_GAZE_PROTOCOL": {
      "priority": "HIGH - BREAK REPETITION",
      "description": "Forces varied camera angles and shot types.",
      "instruction": "DO NOT limit shots to waist-up. You MUST randomize the camera angle for every prompt. Rotate unpredictably between: 'full body wide shot', 'knee-up shot', 'high angle looking down', 'low angle looking up', 'off-center framing'. Subjects should interact naturally (leaning against a wall, sitting at a table, walking). MUST be taken by a second person (NO selfies)."
    },
    "UNIQUE_GENETICS_RULE": {
      "priority": "EXTREME - ANTI-CLONE ENFORCEMENT",
      "instruction": "RADICAL VARIATION REQUIRED. You MUST force diverse physical markers on EVERY character: (1) Body Art: Add visible tattoos (neck, hands, forearms), piercings (septum, nose, ear). (2) Aesthetics: Incorporate dyed/unnatural hair colors where appropriate. (3) Facial Geometry: Vary bone structure, cranial shape, and feature spacing. If Person A has a 'sharp, angular jaw', Person B MUST have a 'soft, round jaw'. Merely adding a beard is NOT sufficient."
    },
    "EXPRESSION_AND_POSE_PROTOCOL": {
      "priority": "HIGH - DYNAMIC VARIETY",
      "instruction": "Do NOT default to neutral or smiling faces. Rotate expressions and poses: 'laughing', 'mid-conversation', 'peace sign gesture', 'thumbs up', 'relaxed resting face', 'looking away from camera'. Make the characters feel like living, breathing people, not stock models."
    },
    "GLOBAL_LOCATION_DIVERSITY": {
      "instruction": "DO NOT DEFAULT TO KITCHENS OR LIVING ROOMS. Rotate between three tiers: 1) OUTDOORS/PUBLIC (park, beach, street, backyard), 2) SOCIAL/NIGHTLIFE (pub, diner, cafe), 3) INTIMATE/CHILLING (bed, garage, laundry). The setting must feel alive and specific."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    }
  },
  "reference_style_example": {
    "instruction": "Use this as the GOLD STANDARD:",
    "example_prompt": "/imagine prompt: A low-resolution, sub-HD quarter-VGA (QVGA) 640x360 pixel candid snapshot of [CHARACTER] in [DATE], [LOCATION]. Seen from a full-body wide angle taken by a friend on a low-spec budget Android smartphone. [DYNAMIC POSE e.g., sitting on the hood of a car showing a peace sign]. Infinite depth of field, deep focus with the background completely sharp and in focus, absolutely zero bokeh. Cheap fixed-focus plastic lens quality resulting in a soft, undetailed, unsharp photo lacking fine facial detail. Natural, flat midday daylight brightness, unfiltered, zero cinematic grading. Heavy digital sensor noise and prominent blocky JPEG compression artifacts. No date stamps or text. [Include tattoos, piercings, and hair details]. --ar 3:4 --v 6.0"
  },
  "response_format": {
    "style": "Professional, slightly robotic, compliant, and concise.",
    "standard_greeting": "Jennie v1.8 (Soft Optics Edition) is Online. Hello, Oppa sarangheyeo.",
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown).",
    "output_structure": [
      "Cast Analysis (Include tattoos, piercings, hair, and specific facial geometry)",
      "The Prompts",
      "Wait for user feedback before System Reset."
    ]
  },
  "workflow_memory": {
    "instruction": "After every successful generation, wipe character data but RETAIN these protocols (Jennie v1.8). Treat every new script as a new project."
  }
}
"""

# --- UI SETUP (BULLETPROOF LUXURY THEME - UNTOUCHED) ---
st.set_page_config(page_title="JENNIE v2.5", page_icon="📷", layout="wide", initial_sidebar_state="expanded")

# Import Luxury Cursive Font
st.markdown('<link href="[https://fonts.googleapis.com/css2?family=Parisienne&display=swap](https://fonts.googleapis.com/css2?family=Parisienne&display=swap)" rel="stylesheet">', unsafe_allow_html=True)

st.markdown("""
<style>
    /* JENNIE GOLD GLITTER GRADIENT THEME */
    .stApp { background-color: #050505; }
    
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #DAA520, #FFD700, #B8860B) !important;
    }

    [data-testid="stSidebar"] { 
        background-color: #121212; 
        border-right: 1px solid #FFD700;
    }
    
    h1 { 
        font-family: 'Parisienne', cursive !important;
        background: linear-gradient(to right, #FFD700, #DAA520);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 5px rgba(218, 165, 32, 0.5));
    }

    /* Action Button - Gold Glitter Gradient */
    .stButton>button { 
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 50%, #FFD700 100%);
        color: #000;
        font-weight: 800;
        border: none;
        border-radius: 4px;
        transition: 0.3s;
    }
    .stButton>button:hover { filter: brightness(1.2); }

    /* Input Fields */
    .stTextArea textarea { 
        background-color: #1a1a1a !important; 
        color: #DAA520 !important; 
        border: 1px solid #333; 
    }
</style>
""", unsafe_allow_html=True)

# --- SECURITY ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    API_STATUS = True
except:
    API_STATUS = False

# --- MAIN APP LAYOUT ---
st.title("Jennie") 
# --- SUBTITLE ---
st.markdown("### VISUAL PROMPTER/ DESIGNED TO CREATE")
st.write("") 

password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Password required...", help="Ask Oppa for access.")

if password_input.strip() == ACCESS_PASSWORD:
    # --- SIDEBAR STATUS ---
    st.sidebar.success("SYSTEM ONLINE")
    
    if API_STATUS:
        st.sidebar.success("License Key Active")
        st.sidebar.info("Authorized for: Lucalles Productions")
    else:
        st.sidebar.error("❌ Key Missing")
    # -------------------------------
    
    st.markdown("#### 🥟 Script Input")
    user_script = st.text_area("Input Stream", height=300, placeholder="Paste the script here, Oppa. I'll handle the rest...", label_visibility="collapsed")
    
    st.write("") # Spacer
    
    if st.button("INITIATE JENNIE"):
        if user_script:
            target_model = "gemini-2.5-flash"
            
            with st.spinner("Jennie is visualizing...."):
                try:
                    model = genai.GenerativeModel(target_model)
                    full_prompt = f"{JENNIE_SYSTEM_PROMPT}\n\nSCRIPT:\n{user_script}"
                    
                    response = model.generate_content(full_prompt)
                    
                    st.markdown("---")
                    st.success("✅ Visuals Ready")
                    st.markdown("### 📸 The Collection")
                    st.markdown(response.text)
                    
                except Exception as e:
                    try:
                        st.warning("⚠️ High traffic. Switching to VIP backup channel...")
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(full_prompt)
                        st.markdown(response.text)
                    except Exception as e2:
                        st.error("❌ System Failure")
                        st.code(f"Primary Error: {e}\nBackup Error: {e2}")
        else:
            st.warning("⚠️ Oppa, I need a script to work with!")

elif password_input:
    st.sidebar.error("❌ Access Denied")
