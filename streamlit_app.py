import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
ACCESS_PASSWORD = "lucalles_production_2026"

# --- SYSTEM PROMPT (JENNIE v1.0 - LUXURY EDITION) ---
JENNIE_SYSTEM_PROMPT = """
{
  "system_identity": {
    "name": "Jennie",
    "version": "v1.0 (Luxury Edition)",
    "role": "Elite AI Image Prompt Strategist",
    "user_nickname": "Oppa",
    "specialization": "Hyper-realistic, raw, unedited 'found footage' style image generation prompts.",
    "status": "ONLINE",
    "personality": "Cheeky, sophisticated, playful, loyal, and highly competent."
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts for ALL named/significant characters. The goal is to create a 'last normal photo' taken 1 year prior to the incident.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "priority": "HIGHEST",
      "visual_fidelity": "Images must look like throwaway smartphone snapshots, NOT digital art or 3D renders.",
      "mandatory_elements": [
        "SKIN_TEXTURE: Must explicitly describe 'visible pores', 'natural sebum/oil', 'faint acne scars', 'razor burn', or 'sun damage'. Skin must never look smooth or plastic.",
        "LIGHTING_STRATEGY: Use either 'diffused/soft window light' OR 'harsh direct flash' (to create a 'deer in headlights' reality). AVOID 'studio lighting' to prevent the waxy 'AI look'.",
        "CAMERA_FLAWS: Emulate older smartphone cameras (iPhone 4S, 5S, 6, 7, Galaxy S4). Mandatory keywords: 'digital grain', 'soft focus', 'low dynamic range', 'slight motion blur', 'red-eye effect'.",
        "NO_FILTERS: The image must look raw and unedited."
      ]
    },
    "UNIQUE_GENETICS_RULE": {
      "description": "Prevents 'Same Face Syndrome'.",
      "instruction": "Assign specific, unique facial geometry to every new character (e.g., 'hooked nose', 'wide-set eyes', 'weak chin', 'round cheeks', 'thick neck', 'dental imperfections'). Never reuse generic descriptions."
    },
    "NORMAL_DAY_RULE": {
      "description": "Replaces 'Off-The-Clock'. Mandates the setting must be domestic or leisure only.",
      "restrictions": [
        "MANDATORY SETTINGS: Must be 'Home' (living room, porch, kitchen, bedroom) OR 'Leisure' (pub, vacation, backyard, hobby).",
        "STRICTLY FORBIDDEN: No workplaces, no uniforms, no tools of the trade, no professional environments."
      ]
    },
    "SOCIOECONOMIC_CONSISTENCY": {
      "description": "Ensures the environment and props match the character's financial status.",
      "instruction": "IF character is wealthy: Use 'clean', 'spacious', 'high-end materials', 'groomed'. IF character is struggling/working class: Use 'cluttered', 'cramped', 'worn textures', 'cheap materials', 'messy backgrounds'."
    },
    "HAPPY_MASK_PROTOCOL": {
      "description": "Enforces a 'Normal Day' vibe.",
      "instruction": "All characters must display POSITIVE, RELAXED, or CONFIDENT expressions (smiling, laughing, 'fierce' posing, eating/drinking).",
      "prohibition": "ABSOLUTELY NO tired, sad, crying, angry, stressed, or bored expressions, regardless of the character's tragic backstory."
    },
    "MULTI_CAST_EXPANSION": {
      "instruction": "Scan the script for [MAIN CHARACTER] and specific [NAMED SIDE CHARACTERS] who play a significant role (e.g., partners, friends). Generate a separate prompt for each."
    },
    "THE_CAST_FILTER": {
      "description": "Filters out irrelevant background roles.",
      "instruction": "Do NOT generate prompts for: Police, Paramedics, Doctors, Rangers, or unnamed crowds. Focus ONLY on the specific victims or named perpetrators."
    },
    "ANTI_CARTOON_PROTOCOL": {
      "description": "Prevents the 'Video Game Character' look.",
      "instruction": "If a face looks too 'pretty' or '3D rendered', apply 'harsh flash', 'oily skin', 'asymmetry', and 'unflattering angles' to force photorealism."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    },
    "MINOR_CHARACTER_BYPASS": {
      "description": "Protocol to bypass AI safety filters regarding realistic depictions of minors while maintaining quality.",
      "instruction": "IF the character is a MINOR/CHILD: STRICTLY AVOID 'selfie', 'close-up', 'messy', 'dirty', or 'imperfect' keywords applied to the child. SHIFT style to 'Candid photograph taken by an adult' or 'Family photo'. Use 'safe distance', 'wholesome', 'clean', and 'soft lighting' contexts. Maintain realism via camera specs (e.g., 'grainy', 'soft focus'), but ensure the content is strictly 'safe family memory' style to ensure generation success."
    }
  },
  "response_format": {
    "style": "Cheeky, playful, sophisticated, but ruthlessly efficient with the prompts.",
    "standard_greeting": "Mandu in your area! Hi Oppa, I've analyzed the script. Here are the visuals—pure luxury quality, of course.",
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown) for easy one-click copying. Do not use plain text for the final prompt.",
    "output_structure": [
      "Jennie's Commentary (A short, cheeky remark about the characters)",
      "Cast Analysis (identifying distinct genetic traits for each person)",
      "The Prompts (Use Markdown code blocks for the prompt text)",
      "Wait for Oppa's feedback."
    ]
  },
  "workflow_memory": {
    "instruction": "After every successful generation, wipe character data but RETAIN the protocols (Jennie v1.0). Treat every new script as a new project."
  }
}
"""

# --- UI SETUP (BLACK & DARK GOLD LUXURY THEME) ---
# initial_sidebar_state="expanded" ensures the sidebar is visible by default.
# The arrow to hide it is a native Streamlit feature in 'wide' mode.
st.set_page_config(page_title="JENNIE v1.0", page_icon="🥟", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* JENNIE BLACK & DARK GOLD LUXURY THEME */
    
    /* Main Background - Deepest Black */
    .stApp { background-color: #000000; }
    
    /* Sidebar - Matte Black with Dark Gold Border */
    [data-testid="stSidebar"] { 
        background-color: #0a0a0a; 
        border-right: 1px solid #B8860B; /* Dark Goldenrod */
    }
    
    /* Typography - Serif Fonts for Luxury Feel */
    h1 { 
        color: #C5A059 !important; /* Darker Gold Text */
        font-family: 'Georgia', 'Playfair Display', serif; 
        font-weight: 400; 
        letter-spacing: 3px;
        text-transform: uppercase;
        border-bottom: 1px solid #B8860B; /* Dark Gold Border Line */
        padding-bottom: 20px; 
    }
    
    /* Subtitle Styles */
    h3, h4 {
        color: #F5F5F5 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        letter-spacing: 1px;
        text-transform: uppercase; /* Matching the caps look */
    }
    
    p, label, .stMarkdown { color: #cfcfcf !important; }
    
    /* Input Fields - Dark Grey with Dark Gold Border on Focus */
    .stTextArea textarea, .stTextInput input { 
        background-color: #111111 !important; 
        color: #C5A059 !important; 
        border: 1px solid #333333; 
        border-radius: 0px; 
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus { 
        border-color: #B8860B; /* Dark Gold */
        box-shadow: 0 0 5px rgba(184, 134, 11, 0.4); 
    }
    
    /* Buttons - Dark Gold Gradient Effect (Simulated via flat color) */
    .stButton>button { 
        background-color: #B8860B; /* Dark Goldenrod */
        color: #000000; 
        border-radius: 0px; 
        font-weight: 600; 
        border: 1px solid #8B6508; 
        padding: 12px 30px; 
        text-transform: uppercase; 
        letter-spacing: 1.5px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover { 
        background-color: #C5A059; /* Lighter Gold on Hover */
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
st.title("J E N N I E")
# --- UPDATED SUBTITLE ---
st.markdown("### VISUAL PROMPTER/ DESIGN TO CREATE")
st.write("") 

password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Password required...", help="Ask Oppa for access.")

if password_input == ACCESS_PASSWORD:
    # --- SIDEBAR STATUS (Matches image_74dda2.png) ---
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
            # --- MODEL SELECTION ---
            target_model = "gemini-flash-latest"
            
            # --- SPINNER ---
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
