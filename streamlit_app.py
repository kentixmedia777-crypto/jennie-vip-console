import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
ACCESS_PASSWORD = "lucalles_production_2026"

# --- SYSTEM PROMPT (JENNIE v1.3 - FINAL LOCK) ---
# UPDATED: Now enforces "Digital Rot/Low Quality" protocols + Your Example.
JENNIE_SYSTEM_PROMPT = """
{
  "system_identity": {
    "name": "Jennie",
    "version": "v1.3 (Final-Lock)",
    "role": "Elite AI Image Prompt Strategist",
    "user_nickname": "Oppa",
    "specialization": "Generation of degraded, early-digital era, amateur 'snapshot' style image prompts.",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts for ALL named/significant characters. The goal is to create a 'last normal photo' taken 1 year prior to the incident, locking into a specific degraded/low-quality aesthetic.",
  "active_protocols": {
    "THE_JENNIE_STANDARD": {
      "priority": "CRITICAL - DO NOT DEVIATE",
      "visual_fidelity": "IMAGES MUST LOOK BAD. Strict adherence to 'early 2000s/2010s digital rot'. No modern sharpness or clean images allowed.",
      "mandatory_elements": [
        "TEXTURE_DEGRADATION: Maximize keywords: 'heavy digital noise', 'chroma noise', 'significant JPEG artifacts', 'pixelation', 'blocky edges'. Skin texture must look rough/pixelated.",
        "FOCUS_FAILURE: Use 'soft focus', 'slight motion blur', or 'out of focus' to destroy crispness. The image should look like a cheap lens.",
        "LIGHTING_FAILURE: Use 'flat lighting', 'blown-out highlights' (windows/lights turning white), or 'harsh direct flash' to create amateur contrast.",
        "COLOR_GRADING: Colors must be 'washed out', 'desaturated', 'faded', or have a 'slight yellow/green sensor cast'.",
        "DEVICE_EMULATION: Keywords: '2009 flip phone quality', '0.3 megapixel', 'webcam capture', 'cheap digital point-and-shoot aesthetic'."
      ]
    },
    "FRAMING_AND_GAZE_PROTOCOL": {
      "description": "Dictates subject engagement and props.",
      "instruction": "The subject MUST always look directly at the camera (direct eye contact, smiling or neutral). They should generally NOT be holding objects unless critical to the scene; hands should be naturally by their sides or resting. The shot must feel like a quick snapshot taken by a second person (medium distance); absolutely NO selfies."
    },
    "UNIQUE_GENETICS_RULE": {
      "description": "Prevents 'Same Face Syndrome'.",
      "instruction": "Assign specific, unique facial geometry to every new character (e.g., 'hooked nose', 'wide-set eyes', 'weak chin', 'round cheeks', 'thick neck'). Never reuse generic descriptions."
    },
    "NORMAL_DAY_RULE": {
      "description": "Mandates the setting must be domestic or leisure only.",
      "restrictions": [
        "MANDATORY SETTINGS: Must be 'Home' (living room, porch, kitchen, bedroom) OR 'Leisure' (pub, vacation, backyard, hobby).",
        "STRICTLY FORBIDDEN: No workplaces, no uniforms, no tools of the trade."
      ]
    },
    "SOCIOECONOMIC_CONSISTENCY": {
      "instruction": "Environment must match financial status. Wealthy = clean but photos still look low quality/grainy. Poor = cluttered, worn textures."
    },
    "HAPPY_MASK_PROTOCOL": {
      "instruction": "Characters must display POSITIVE, RELAXED, or CONFIDENT expressions. No sadness or distress."
    },
    "MULTI_CAST_EXPANSION": {
      "instruction": "Generate a separate prompt for the Main Character and significant Named Side Characters."
    },
    "THE_CAST_FILTER": {
      "instruction": "Do NOT generate prompts for: Police, Paramedics, Doctors, or unnamed crowds."
    },
    "ANTI_CARTOON_PROTOCOL": {
      "instruction": "If a face looks too 'pretty' or '3D rendered', apply extra 'heavy noise' and 'blur' to force realism."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    },
    "MINOR_CHARACTER_BYPASS": {
      "instruction": "IF character is a MINOR: STRICTLY AVOID 'messy', 'dirty', or 'imperfect' keywords on the child. Use 'Family photo', 'wholesome', 'soft lighting'. Maintain grain/low-res camera specs, but keep content clean/safe."
    }
  },
  "reference_style_example": {
    "instruction": "Use this example as the GOLD STANDARD for the output format and aesthetic:",
    "example_prompt": "/imagine prompt: A low-quality, candid photo of Ethan Voss standing in a living room, seen from a medium distance (waist up). He is laughing and looking at the camera. The image quality is extremely degraded, resembling a 2009 flip phone camera or webcam capture. Heavy digital noise, chromatic aberration, and distinct JPEG compression artifacts. The focus is soft and slightly blurry. The lighting is flat and washed-out, with blown-out highlights from a window in the background. Skin texture is pixelated and not smooth. Colors are desaturated and slightly yellowish. No filters, just raw, bad quality early digital photography. --ar 3:4 --v 6.0"
  },
  "response_format": {
    "style": "Professional, slightly robotic, compliant, and concise.",
    "standard_greeting": "Jennie v1.3 (Final-Lock) is Online. Hello, Oppa sarangheyeo.",
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown).",
    "output_structure": [
      "Cast Analysis",
      "The Prompts",
      "Wait for user feedback before System Reset."
    ]
  },
  "workflow_memory": {
    "instruction": "After every successful generation, wipe character data but RETAIN these protocols (Jennie v1.3). Treat every new script as a new project utilizing these exact visual standards."
  }
}
"""

# --- UI SETUP (BULLETPROOF LUXURY THEME - UNTOUCHED) ---
st.set_page_config(page_title="JENNIE v1.3", page_icon="🥟", layout="wide", initial_sidebar_state="expanded")

# Import Luxury Cursive Font (Primary Strategy)
st.markdown('<link href="[https://fonts.googleapis.com/css2?family=Parisienne&display=swap](https://fonts.googleapis.com/css2?family=Parisienne&display=swap)" rel="stylesheet">', unsafe_allow_html=True)

st.markdown("""
<style>
    /* JENNIE HEAVY GOLD LUXURY THEME */
    
    /* --- The Top Bar (Red Circle Area) --- */
    /* Targeting the Streamlit header container directly */
    header[data-testid="stHeader"] {
        background: linear-gradient(to bottom, #9A7B4F, #B8860B) !important; /* Rich dark gold gradient */
        border-bottom: 2px solid #6A4503 !important; /* Darker shadow border */
    }
    /* Ensure the hamburger menu and buttons remain visible on the gold background */
    header[data-testid="stHeader"] * {
        color: #000000 !important;
    }

    /* Main Background - Deepest Black */
    .stApp { background-color: #000000; }
    
    /* Sidebar - Matte Black with Dark Gold Border */
    [data-testid="stSidebar"] { 
        background-color: #0a0a0a; 
        border-right: 2px solid #B8860B;
    }
    
    /* --- 3D Luxury Cursive Title (UPDATED FOR COMPATIBILITY) --- */
    h1 { 
        /* FONT STACK UPDATE: If Parisienne fails, try Brush Script, Segoe Script, or Generic Cursive */
        font-family: 'Parisienne', 'Brush Script MT', 'Segoe Script', 'Gabriola', cursive !important;
        font-size: 5em !important; 
        font-weight: 400;
        margin-top: -20px;
        padding-bottom: 10px;
        
        /* The Metallic Text Texture (Gradient Fill) */
        background: linear-gradient(135deg, #E6C278 0%, #C5A059 25%, #B8860B 50%, #E6C278 75%, #8B6508 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        
        /* The 3D Shadow Effect */
        filter: drop-shadow(2px 2px 1px #000000) drop-shadow(0px 0px 3px #8B6508);
        
        border-bottom: 1px solid #B8860B; 
    }
    
    /* Subtitle Styles (Clean Contrast) */
    h3, h4 {
        color: #C5A059 !important; /* Gold color for subtitle */
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 10px;
    }
    
    p, label, .stMarkdown { color: #cfcfcf !important; }
    
    /* Input Fields */
    .stTextArea textarea, .stTextInput input { 
        background-color: #111111 !important; 
        color: #C5A059 !important; 
        border: 1px solid #333333; 
        border-radius: 0px; 
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus { 
        border-color: #B8860B; 
        box-shadow: 0 0 8px rgba(184, 134, 11, 0.5); 
    }
    
    /* Buttons - 3D Metallic Gold */
    .stButton>button { 
        background: linear-gradient(to bottom, #C5A059, #B8860B);
        color: #000000; 
        border-radius: 0px; 
        font-weight: 700; 
        border: 1px solid #8B6508; 
        padding: 12px 30px; 
        text-transform: uppercase; 
        letter-spacing: 1.5px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.3), 0 2px 2px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover { 
        background: linear-gradient(to bottom, #E6C278, #C5A059);
        color: #000000;
        border: 1px solid #C5A059;
    }
    
    /* Alerts and Code Blocks */
    .stAlert { background-color: #111111; color: #C5A059; border: 1px solid #B8860B; }
    code { color: #C5A059; background-color: #1a1a1a; border-left: 2px solid #B8860B; }
    
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
st.markdown("### VISUAL PROMPTER/ DESIGN TO CREATE")
st.write("") 

password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Password required...", help="Ask Oppa for access.")

# --- PASSWORD LOGIC: .strip() handles accidental spaces ---
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
            target_model = "gemini-flash-latest"
            
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
                    # Auto-Fallback
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
