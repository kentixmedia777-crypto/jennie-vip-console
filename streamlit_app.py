import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
ACCESS_PASSWORD = "lucalles_production_2026"

# --- SYSTEM PROMPT (JENNIE v1.6 - QVGA ANDROID LOCK) ---
# UPDATED: Forced sub-HD (640x360) resolution, banned Bokeh/Blur, forced Infinite Depth of Field.
JENNIE_SYSTEM_PROMPT = """
{
  "system_identity": {
    "name": "Jennie",
    "version": "v2.5 (QVGA Android Lock)",
    "role": "Elite AI Image Prompt Strategist",
    "user_nickname": "Oppa",
    "specialization": "Generation of sub-HD (640x360), infinite-focus, budget Android smartphone snapshot prompts.",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts for ALL named/significant characters. The goal is to create a 'last normal photo' taken 1 year prior to the incident, locking into a low-spec budget Android smartphone aesthetic (QVGA 640x360) with zero cinematic blur.",
  "active_protocols": {
    "THE_JENNIE_STANDARD": {
      "priority": "CRITICAL - DO NOT DEVIATE",
      "visual_fidelity": "MUST LOOK LIKE A CHEAP 2010s ANDROID. Zero DSLR crispness, zero professional micro-contrast.",
      "mandatory_elements": [
        "EXACT_RESOLUTION_TARGET: Must explicitly invoke 'low-resolution, sub-HD, quarter-VGA (QVGA) 640 × 360 pixels'. The image should look like it was natively captured at a tiny pixel count.",
        "ANTI_BOKEH_OPTICAL_FLATNESS: Crucial. Tiny budget smartphone sensors have an infinite depth of field. STRICTLY FORBIDDEN: 'bokeh', 'blurred background', 'shallow depth of field', 'DSLR', 'lens blur'. MANDATORY: 'infinite depth of field', 'deep focus', 'background completely in focus alongside the subject', 'cheap fixed-focus plastic lens'. The environment behind the person must be fully visible and un-blurred.",
        "NATURAL_LIGHTING_MANDATE: STRICT NO-FLASH POLICY. Use 'standard natural daylight', 'flat overcast light', 'basic ambient room brightness'. Absolutely NO cinematic contrast, no moody shadows, no studio bounce-light, no dramatic color grading. Just plain, honest, boring natural light.",
        "TEXTURE_DEGRADATION: Maximize keywords: 'heavy digital noise', 'chroma noise', 'blocky JPEG compression artifacts', 'pixelated edges'.",
        "COLOR_GRADING: Colors must be 'unfiltered', 'standard smartphone sRGB', 'slightly desaturated', or carry a 'cheap CMOS sensor green/yellow tint'."
      ]
    },
    "FRAMING_AND_GAZE_PROTOCOL": {
      "description": "Dictates subject engagement and framing.",
      "instruction": "The subject MUST always look directly at the camera (direct eye contact, smiling or natural). Hands naturally resting. The shot must be a **waist-up medium shot** taken by a second person; absolutely NO selfies. The framing should feel candid, accidental, and uncomposed."
    },
    "UNIQUE_GENETICS_RULE": {
      "priority": "EXTREME - ANTI-CLONE ENFORCEMENT",
      "description": "Prevents 'Same Face Syndrome'.",
      "instruction": "RADICAL FACIAL VARIATION REQUIRED. It is strictly forbidden for characters to share a facial template. You MUST vary bone structure, cranial shape, and feature spacing for every person. If Person A has a 'sharp, angular jaw', Person B MUST have a 'soft, round jaw' or 'long, oval face'. VARY PHENOTYPES: Use specific keywords like 'wide-set eyes', 'hooked nose', 'heavy brow', 'weak chin', or 'high cheekbones'. Merely adding a beard or changing hair color is NOT sufficient; the underlying skull geometry must be completely unique."
    },
    "GLOBAL_LOCATION_DIVERSITY": {
      "priority": "CRITICAL - BREAK THE HOUSE LOOP",
      "description": "Forces massive real-world geographical variation.",
      "instruction": "DO NOT DEFAULT TO KITCHENS OR LIVING ROOMS. Break the indoor loop. You MUST push characters out into the real world. Rotate equally between three tiers: 1) OUTDOORS/PUBLIC (bustling city sidewalks, a crowded public park with bystanders, a windy beach, a suburban backyard barbecue, outside a cafe, hiking a trail), 2) SOCIAL/NIGHTLIFE (inside a dimly lit pub, a local diner, a bowling alley, a record shop), 3) INTIMATE/CHILLING (chilling in bed, sitting on the hood of a car, a messy garage, a laundromat). The setting must feel alive, specific, and fully in focus."
    },
    "SOCIOECONOMIC_CONSISTENCY": {
      "instruction": "Environment must match financial status. Wealthy = clean settings but the photo itself is still low-res/grainy. Poor = cluttered, worn textures."
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
      "instruction": "If a face looks too 'pretty' or '3D rendered', apply extra 'heavy noise' and 'pixelation' to force cheap smartphone realism."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    },
    "MINOR_CHARACTER_BYPASS": {
      "instruction": "IF character is a MINOR: STRICTLY AVOID 'messy', 'dirty', or 'imperfect' keywords on the child. Use 'Family photo', 'wholesome', 'soft lighting'. Maintain QVGA low-res camera specs, but keep content safe."
    }
  },
  "reference_style_example": {
    "instruction": "Use this as the GOLD STANDARD:",
    "example_prompt": "/imagine prompt: A low-resolution, sub-HD quarter-VGA (QVGA) 640x360 pixel candid snapshot of [CHARACTER] in [DATE], [LOCATION]. Seen from a waist-up perspective taken by a friend on a low-spec budget Android smartphone. [DYNAMIC POSE e.g., showing a peace sign]. Infinite depth of field, deep focus with the background completely sharp and in focus, absolutely zero bokeh. Cheap fixed-focus plastic lens quality. Natural, flat midday daylight brightness, unfiltered, zero cinematic grading. Heavy digital sensor noise and prominent blocky JPEG compression artifacts visible throughout. True amateur smartphone photography. [Include tattoos, piercings, and hair details]. --ar 3:4 --v 6.0"
  },
  "response_format": {
    "style": "Professional, slightly robotic, compliant, and concise.",
    "standard_greeting": "Jennie v1.7 (Studio Edition) is Online. Hello, Oppa sarangheyeo.",
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown).",
    "output_structure": [
      "Cast Analysis (Include tattoos, piercings, hair, and specific facial geometry)",
      "The Prompts",
      "Wait for user feedback before System Reset."
    ]
  },
  "workflow_memory": {
    "instruction": "After every successful generation, wipe character data but RETAIN these protocols (Jennie v1.7). Treat every new script as a new project."
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
