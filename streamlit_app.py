"""
NativeEcho v1.4 - AI English Coach
Auto-Auth & Specific Model Edition

A personal AI English coach with:
- Auto-login via pre-configured secrets
- Supabase database persistence
- SiliconFlow LLM API integration
"""

import streamlit as st
import random
import json
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from supabase import create_client, Client

# =============================================================================
# Page Configuration
# =============================================================================
st.set_page_config(
    page_title="NativeEcho - AI English Coach",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# Custom CSS - Compact UI, hide avatars, style chat bubbles
# =============================================================================
st.markdown("""
<style>
/* ============ COMPACT GLOBAL STYLES ============ */
/* Reduce main container padding */
.stMainBlockContainer {
    padding-top: 1rem !important;
    padding-bottom: 0 !important;
}

/* Compact title */
h1 {
    font-size: 1.5rem !important;
    margin-bottom: 0.25rem !important;
}

/* Smaller caption */
.stCaption {
    font-size: 0.75rem !important;
    margin-bottom: 0.5rem !important;
}

/* Reduce block spacing */
.stElementContainer {
    margin-bottom: 0.25rem !important;
}

/* Compact buttons */
.stButton > button {
    padding: 0.25rem 0.75rem !important;
    font-size: 0.85rem !important;
}

/* Compact text inputs */
.stTextInput > div > div > input {
    padding: 0.4rem 0.6rem !important;
    font-size: 0.85rem !important;
}

/* Compact text area */
.stTextArea > div > div > textarea {
    font-size: 0.85rem !important;
}

/* Reduce expander padding */
.streamlit-expanderHeader {
    padding: 0.4rem 0.6rem !important;
    font-size: 0.85rem !important;
}

.streamlit-expanderContent {
    padding: 0.5rem !important;
}

/* ============ SIDEBAR COMPACT ============ */
section[data-testid="stSidebar"] {
    width: 280px !important;
}

section[data-testid="stSidebar"] .stElementContainer {
    margin-bottom: 0.2rem !important;
}

section[data-testid="stSidebar"] h1 {
    font-size: 1.2rem !important;
}

section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stSubheader {
    font-size: 0.9rem !important;
    margin-top: 0.5rem !important;
    margin-bottom: 0.25rem !important;
}

section[data-testid="stSidebar"] hr {
    margin: 0.5rem 0 !important;
}

/* ============ CHAT MESSAGE STYLES ============ */
/* Hide ALL chat message avatars - multiple selectors for compatibility */
[data-testid="stChatMessageAvatarContainer"],
.stChatMessage > div:first-child:has(img),
.stChatMessage > div:first-child:has(svg),
.stChatMessage [data-testid="chatAvatarIcon-user"],
.stChatMessage [data-testid="chatAvatarIcon-assistant"],
.stChatMessage img[alt="user"],
.stChatMessage img[alt="assistant"],
.stChatMessage .stAvatar,
div[data-testid="stChatMessage"] > div:first-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* Compact chat messages */
.stChatMessage {
    padding: 0.5rem 0.75rem !important;
    margin-bottom: 0.4rem !important;
    gap: 0 !important;
    flex-direction: column !important;
}

[data-testid="stChatMessageContent"] {
    margin-left: 0 !important;
    max-width: 100% !important;
}

[data-testid="stChatMessageContent"] p {
    font-size: 0.9rem !important;
    margin-bottom: 0.25rem !important;
}

/* User message bubble */
div[data-testid="stChatMessage"]:has(img[alt="user"]),
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 12px 12px 2px 12px !important;
    margin-left: 15% !important;
}

div[data-testid="stChatMessage"]:has(img[alt="user"]) p,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p {
    color: white !important;
}

/* Assistant message bubble */
div[data-testid="stChatMessage"]:has(img[alt="assistant"]),
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #f0f2f6 !important;
    border-radius: 12px 12px 12px 2px !important;
    margin-right: 15% !important;
}

/* Compact feedback expander inside chat */
.stChatMessage .streamlit-expanderHeader {
    padding: 0.2rem 0.5rem !important;
    font-size: 0.75rem !important;
}

.stChatMessage .streamlit-expanderContent {
    padding: 0.3rem 0.5rem !important;
    font-size: 0.8rem !important;
}

/* ============ ADD BUTTON (POPOVER) ============ */
/* Square button style */
[data-testid="stPopover"] > button {
    border-radius: 6px !important;
    min-width: 32px !important;
    width: 32px !important;
    height: 32px !important;
    padding: 0 !important;
    font-size: 1rem !important;
    line-height: 1 !important;
}

/* Popover content - wider and compact */
[data-testid="stPopoverBody"] {
    min-width: 320px !important;
    padding: 0.4rem !important;
}

[data-testid="stPopoverBody"] .stTextInput {
    margin-bottom: 0 !important;
}

[data-testid="stPopoverBody"] .stTextInput input {
    padding: 0.3rem 0.5rem !important;
    font-size: 0.85rem !important;
}

[data-testid="stPopoverBody"] .stButton button {
    padding: 0.3rem 0.6rem !important;
    font-size: 0.8rem !important;
    height: auto !important;
}

[data-testid="stPopoverBody"] .stElementContainer {
    margin-bottom: 0 !important;
}

/* ============ CHAT INPUT ============ */
[data-testid="stChatInput"] {
    padding: 0.5rem 0 !important;
}

[data-testid="stChatInput"] textarea {
    font-size: 0.9rem !important;
}

/* Prevent password autofill styling on vocab input */
[data-testid="stPopoverBody"] input {
    -webkit-text-security: none !important;
}
</style>

<script>
// Disable autocomplete on vocab input to prevent browser password detection
(function() {
    const observer = new MutationObserver(function(mutations) {
        document.querySelectorAll('[data-testid="stPopoverBody"] input').forEach(function(input) {
            input.setAttribute('autocomplete', 'off');
            input.setAttribute('data-form-type', 'other');
            input.setAttribute('data-lpignore', 'true');
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)

# =============================================================================
# Default Configuration Values
# =============================================================================
DEFAULT_CONFIG = {
    "supabase_url": "https://omanedtxaljaltfmqgov.supabase.co",
    "supabase_key": "sb_publishable_b0XED_AqNr3qecNvPAWZmw_GiNhanD2",
    "siliconflow_api_key": "sk-vlmhbxgjgllzolnsqunigerenwtwdfsutvaecdpgpvxqyncc",
    "siliconflow_base_url": "https://api.siliconflow.cn/v1",
    "siliconflow_model": "deepseek-ai/DeepSeek-V3.2"
}

# =============================================================================
# Configuration Helper Functions
# =============================================================================
def get_config_value(section: str, key: str, default: str = "") -> str:
    """Get configuration value from secrets or session state, with fallback to defaults."""
    # First try st.secrets
    try:
        return st.secrets[section][key]
    except (KeyError, FileNotFoundError):
        pass
    
    # Then try session state
    session_key = f"{section}_{key}"
    if session_key in st.session_state:
        return st.session_state[session_key]
    
    # Finally use default config
    default_key = f"{section}_{key}"
    return DEFAULT_CONFIG.get(default_key, default)

def has_valid_config() -> bool:
    """Check if we have valid configuration (either from secrets or session state)."""
    # Check if secrets exist
    try:
        _ = st.secrets["supabase"]["url"]
        _ = st.secrets["siliconflow"]["api_key"]
        return True
    except (KeyError, FileNotFoundError):
        pass
    
    # Check if session state has config
    if st.session_state.get("config_saved", False):
        return True
    
    return False

def render_setup_page():
    """Render the initial setup page when secrets are not configured."""
    st.title("🗣️ NativeEcho Setup")
    st.markdown("Welcome! Please configure your credentials to get started.")
    
    st.info("""
    **First time here?** You need to configure your database and API credentials.
    
    For **Streamlit Community Cloud** deployment, add these to your app's Secrets in the dashboard.
    For **local development**, create `.streamlit/secrets.toml` with these values.
    """)
    
    with st.form("setup_form"):
        st.subheader("🗄️ Supabase Configuration")
        supabase_url = st.text_input(
            "Supabase URL",
            value=DEFAULT_CONFIG["supabase_url"],
            help="Your Supabase project URL"
        )
        supabase_key = st.text_input(
            "Supabase Key",
            value=DEFAULT_CONFIG["supabase_key"],
            type="password",
            help="Your Supabase anon/public key"
        )
        
        st.subheader("🤖 SiliconFlow API Configuration")
        api_key = st.text_input(
            "API Key",
            value=DEFAULT_CONFIG["siliconflow_api_key"],
            type="password",
            help="Your SiliconFlow API key"
        )
        base_url = st.text_input(
            "Base URL",
            value=DEFAULT_CONFIG["siliconflow_base_url"],
            help="API endpoint URL"
        )
        model = st.text_input(
            "Model",
            value=DEFAULT_CONFIG["siliconflow_model"],
            help="The model to use"
        )
        
        submitted = st.form_submit_button("🚀 Save & Start", type="primary", use_container_width=True)
        
        if submitted:
            # Save to session state
            st.session_state.supabase_url = supabase_url
            st.session_state.supabase_key = supabase_key
            st.session_state.siliconflow_api_key = api_key
            st.session_state.siliconflow_base_url = base_url
            st.session_state.siliconflow_model = model
            st.session_state.config_saved = True
            st.rerun()
    
    # Show secrets.toml template
    with st.expander("📄 View secrets.toml template"):
        st.code(f'''[supabase]
url = "{DEFAULT_CONFIG["supabase_url"]}"
key = "{DEFAULT_CONFIG["supabase_key"]}"

[siliconflow]
api_key = "{DEFAULT_CONFIG["siliconflow_api_key"]}"
base_url = "{DEFAULT_CONFIG["siliconflow_base_url"]}"
model = "{DEFAULT_CONFIG["siliconflow_model"]}"
''', language="toml")
        st.caption("Copy this to `.streamlit/secrets.toml` for local development or add to Streamlit Cloud Secrets.")

# =============================================================================
# Initialize Clients
# =============================================================================
def init_supabase() -> Client:
    """Initialize Supabase client from config."""
    url = get_config_value("supabase", "url")
    key = get_config_value("supabase", "key")
    return create_client(url, key)

def get_openai_client(api_key: str, base_url: str) -> OpenAI:
    """Create OpenAI-compatible client for SiliconFlow."""
    return OpenAI(api_key=api_key, base_url=base_url)

# =============================================================================
# Database Operations
# =============================================================================
def fetch_chat_history(supabase: Client, limit: int = 20) -> list:
    """Fetch the last N messages from chat_logs."""
    try:
        response = supabase.table("chat_logs") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        # Reverse to get chronological order
        return list(reversed(response.data)) if response.data else []
    except Exception as e:
        st.error(f"Error fetching chat history: {e}")
        return []

def save_chat_message(supabase: Client, role: str, content: str):
    """Save a message to chat_logs."""
    try:
        supabase.table("chat_logs").insert({
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        st.error(f"Error saving message: {e}")

def fetch_active_vocab(supabase: Client) -> list:
    """Fetch active vocabulary from vocab_vault."""
    try:
        response = supabase.table("vocab_vault") \
            .select("*") \
            .eq("status", "active") \
            .execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching vocabulary: {e}")
        return []

def save_vocab(supabase: Client, phrase: str, note: str):
    """Save a new phrase to vocab_vault."""
    try:
        supabase.table("vocab_vault").insert({
            "target_phrase": phrase,
            "note": note,
            "status": "active",
            "usage_count": 0
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error saving vocabulary: {e}")
        return False

def update_vocab_usage(supabase: Client, phrase_id: int, new_count: int):
    """Update the usage count for a vocabulary item."""
    try:
        supabase.table("vocab_vault").update({
            "usage_count": new_count
        }).eq("id", phrase_id).execute()
    except Exception as e:
        st.error(f"Error updating vocabulary usage: {e}")

def fetch_feedback_for_input(supabase: Client, user_input: str) -> dict | None:
    """Fetch AI feedback for a specific user input."""
    try:
        response = supabase.table("ai_feedback") \
            .select("*") \
            .eq("user_input", user_input) \
            .limit(1) \
            .execute()
        return response.data[0] if response.data else None
    except Exception:
        return None

def save_ai_feedback(supabase: Client, user_input: str, better_version: str, grammar_point: str):
    """Save AI feedback analysis."""
    try:
        supabase.table("ai_feedback").insert({
            "user_input": user_input,
            "better_version": better_version,
            "grammar_point": grammar_point,
            "is_reviewed": False
        }).execute()
    except Exception as e:
        st.error(f"Error saving feedback: {e}")

def fetch_all_vocab(supabase: Client) -> list:
    """Fetch all vocabulary items."""
    try:
        response = supabase.table("vocab_vault") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching vocabulary: {e}")
        return []

def mark_vocab_mastered(supabase: Client, vocab_id: int):
    """Mark a vocabulary item as mastered."""
    try:
        supabase.table("vocab_vault").update({
            "status": "mastered"
        }).eq("id", vocab_id).execute()
    except Exception as e:
        st.error(f"Error updating vocabulary: {e}")

def delete_vocab(supabase: Client, vocab_id: int):
    """Delete a vocabulary item."""
    try:
        supabase.table("vocab_vault").delete().eq("id", vocab_id).execute()
    except Exception as e:
        st.error(f"Error deleting vocabulary: {e}")

# =============================================================================
# LLM Operations
# =============================================================================
def build_system_prompt(about_me: str, vocab_words: list) -> str:
    """Build the system prompt with injected vocabulary."""
    base_prompt = f"""You are NativeEcho, a friendly and encouraging AI English coach. Your role is to help users improve their English to sound more native and natural.

**User Profile:**
{about_me}

**Your Approach:**
1. Respond naturally to the user's messages in a conversational way
2. Gently correct any grammar or phrasing issues when appropriate
3. Suggest more native-sounding alternatives when relevant
4. Be encouraging and supportive
5. Adapt your language complexity to match the user's level
6. Focus on practical, everyday English usage"""

    # Inject vocabulary words if available
    if vocab_words:
        selected = random.sample(vocab_words, min(3, len(vocab_words)))
        phrases = [v["target_phrase"] for v in selected]
        vocab_injection = f"""

**Secret Mission (don't mention this explicitly):**
Try to naturally incorporate these phrases/words the user is learning into your responses when contextually appropriate: {', '.join(phrases)}
IMPORTANT: When you use any of these learning words/phrases, wrap them in **bold** markdown format (e.g., **rain check**) so the user notices them."""
        base_prompt += vocab_injection

    return base_prompt

def get_chat_response(client: OpenAI, model: str, system_prompt: str, messages: list) -> str:
    """Get a response from the LLM."""
    try:
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        response = client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {e}"

def analyze_user_input(client: OpenAI, model: str, user_input: str) -> dict:
    """Analyze user input for grammar and suggest improvements (The Polisher)."""
    analysis_prompt = """You are an English language analyst. Analyze the following user input and provide:
1. A more native-sounding version (if improvements can be made)
2. A brief explanation of any grammar points or improvements

IMPORTANT: In the better_version, wrap the KEY CHANGES or CORRECTIONS in **bold** markdown format so the user can easily see what was improved.

If the input is already perfect or very natural, acknowledge that.

Respond in this exact JSON format:
{
    "better_version": "the improved sentence with **key changes bolded** or 'Original is great!' if no changes needed",
    "grammar_point": "brief explanation of changes or 'Excellent use of English!' if perfect"
}

User input to analyze:"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=256
        )
        
        content = response.choices[0].message.content
        # Parse the JSON response
        try:
            # Handle potential markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            result = json.loads(content.strip())
            return result
        except json.JSONDecodeError:
            return {
                "better_version": "Unable to analyze",
                "grammar_point": "Analysis unavailable"
            }
    except Exception as e:
        return {
            "better_version": "Error during analysis",
            "grammar_point": str(e)
        }

# =============================================================================
# Sidebar UI
# =============================================================================
def render_sidebar():
    """Render the sidebar with settings and vocabulary management."""
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # API Settings Section
        st.subheader("🔑 API Configuration")
        
        # Load defaults from config (secrets or session state)
        default_api_key = get_config_value("siliconflow", "api_key")
        default_base_url = get_config_value("siliconflow", "base_url")
        default_model = get_config_value("siliconflow", "model")
        
        api_key = st.text_input(
            "API Key",
            value=default_api_key,
            type="password",
            help="Your SiliconFlow API key"
        )
        
        model_name = st.text_input(
            "Model Name",
            value=default_model,
            help="The model to use for chat"
        )
        
        base_url = st.text_input(
            "Base URL",
            value=default_base_url,
            help="API endpoint URL"
        )
        
        st.divider()
        
        # Long-Term Memory Section
        st.subheader("🧠 Long-Term Memory")
        
        about_me = st.text_area(
            "About Me",
            value=st.session_state.get("about_me", "I am an IELTS 7.0 learner. I want to sound like a native American speaker."),
            height=100,
            help="Tell the AI about yourself and your learning goals"
        )
        
        # Store in session state
        st.session_state.about_me = about_me
        
        st.divider()
        
        # Clear Chat Button
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        # Reset Configuration Button
        if st.button("🔄 Reset Configuration", use_container_width=True, type="secondary"):
            st.session_state.config_saved = False
            st.session_state.pop("supabase_url", None)
            st.session_state.pop("supabase_key", None)
            st.session_state.pop("siliconflow_api_key", None)
            st.session_state.pop("siliconflow_base_url", None)
            st.session_state.pop("siliconflow_model", None)
            st.rerun()
        
        return api_key, model_name, base_url, about_me

# =============================================================================
# Main Chat UI
# =============================================================================
def render_chat_interface(supabase: Client, client: OpenAI, model: str, about_me: str):
    """Render the main chat interface."""
    # Initialize messages from database if not in session state
    if "messages" not in st.session_state:
        st.session_state.messages = fetch_chat_history(supabase)
    
    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show feedback for user messages
            if message["role"] == "user":
                feedback = fetch_feedback_for_input(supabase, message["content"])
                if feedback:
                    with st.expander("💡 Language Feedback", expanded=False):
                        st.markdown(f"**Native version:** {feedback.get('better_version', 'N/A')}")
                        st.markdown(f"**Tip:** {feedback.get('grammar_point', 'N/A')}")
    
    # Input area with Add to Learning Plan button
    input_col, add_col = st.columns([12, 1])
    
    with add_col:
        with st.popover("➕"):
            col1, col2 = st.columns([4, 1])
            with col1:
                new_phrase = st.text_input("Add word/phrase", placeholder="rain check", key="vocab_phrase", label_visibility="collapsed")
            with col2:
                if st.button("Add", type="primary", key="add_vocab_btn"):
                    if new_phrase:
                        if save_vocab(supabase, new_phrase, ""):
                            st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Type your message in English..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_chat_message(supabase, "user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get active vocabulary for injection
        active_vocab = fetch_active_vocab(supabase)
        system_prompt = build_system_prompt(about_me, active_vocab)
        
        # Run chat response and feedback analysis in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both tasks
            chat_future = executor.submit(
                get_chat_response, client, model, system_prompt, st.session_state.messages
            )
            analysis_future = executor.submit(
                analyze_user_input, client, model, prompt
            )
            
            # Display chat response as soon as it's ready
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_future.result()
                    st.markdown(response)
            
            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_chat_message(supabase, "assistant", response)
            
            # Get analysis result (should be ready or nearly ready)
            analysis = analysis_future.result()
            save_ai_feedback(
                supabase,
                prompt,
                analysis.get("better_version", ""),
                analysis.get("grammar_point", "")
            )
        
        st.rerun()

def render_vocab_tab(supabase: Client):
    """Render vocabulary management tab."""
    # Add new vocabulary input at top
    col1, col2 = st.columns([5, 1])
    with col1:
        new_phrase = st.text_input("Add new word/phrase", placeholder="e.g., rain check", key="vocab_tab_phrase", label_visibility="collapsed")
    with col2:
        if st.button("Add", type="primary", key="vocab_tab_add_btn"):
            if new_phrase:
                if save_vocab(supabase, new_phrase, ""):
                    st.rerun()
    
    st.divider()
    
    vocab = fetch_all_vocab(supabase)
    
    if not vocab:
        st.info("Your vocabulary vault is empty. Add some phrases to learn!")
    else:
        # Sub-tabs for active and mastered
        active_tab, mastered_tab = st.tabs(["🎯 Active", "✅ Mastered"])
        
        with active_tab:
            active_vocab = [v for v in vocab if v.get("status") == "active"]
            if active_vocab:
                for v in active_vocab:
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"**{v['target_phrase']}**")
                    with col2:
                        if st.button("✅", key=f"master_{v['id']}", help="Mark as mastered"):
                            mark_vocab_mastered(supabase, v['id'])
                            st.rerun()
            else:
                st.info("No active vocabulary items.")
        
        with mastered_tab:
            mastered_vocab = [v for v in vocab if v.get("status") == "mastered"]
            if mastered_vocab:
                for v in mastered_vocab:
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"**{v['target_phrase']}**")
                    with col2:
                        if st.button("🗑️", key=f"delete_{v['id']}", help="Delete"):
                            delete_vocab(supabase, v['id'])
                            st.rerun()
            else:
                st.info("No mastered vocabulary items yet.")

# =============================================================================
# Main App
# =============================================================================
def main():
    """Main application entry point."""
    # Check if configuration is available
    if not has_valid_config():
        render_setup_page()
        return
    
    # Initialize Supabase
    try:
        supabase = init_supabase()
        st.session_state.supabase = supabase
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        st.info("Please check your Supabase credentials.")
        if st.button("🔄 Reconfigure"):
            st.session_state.config_saved = False
            st.rerun()
        st.stop()
    
    # Render sidebar and get settings
    api_key, model_name, base_url, about_me = render_sidebar()
    
    # Initialize OpenAI client
    try:
        client = get_openai_client(api_key, base_url)
    except Exception as e:
        st.error(f"Failed to initialize API client: {e}")
        st.stop()
    
    # Title
    st.title("🗣️ NativeEcho")
    st.caption("Your AI English Coach - Practice natural, native-sounding English")
    
    # Main tabs: Chat and Vocabulary
    chat_tab, vocab_tab = st.tabs(["💬 Chat", "📚 Vocabulary"])
    
    with chat_tab:
        render_chat_interface(supabase, client, model_name, about_me)
    
    with vocab_tab:
        render_vocab_tab(supabase)

if __name__ == "__main__":
    main()
