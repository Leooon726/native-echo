# 🗣️ NativeEcho v1.4

**Your Personal AI English Coach** - Practice natural, native-sounding English with intelligent feedback and personalized learning.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nativeecho.streamlit.app/)

## Features

### 🎯 Core Capabilities
- **AI-Powered Conversations**: Practice English with a friendly AI coach powered by DeepSeek-V3.2
- **Auto-Authentication**: Zero-friction startup with pre-configured API keys
- **Persistent Learning**: Your conversations and vocabulary are saved automatically

### 📚 Active Learning System
- **Vocabulary Vault**: Save words and phrases you want to learn
- **Smart Injection**: The AI naturally incorporates your learning vocabulary into conversations
- **Progress Tracking**: Track your vocabulary from "active" to "mastered"

### 💡 The Polisher
- **Background Analysis**: Every message you send is analyzed for improvements
- **Native Suggestions**: Get more natural-sounding alternatives to your phrases
- **Grammar Tips**: Understand why certain phrasings work better

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Streamlit     │────▶│   SiliconFlow   │────▶│  DeepSeek-V3.2  │
│   Frontend      │     │      API        │     │      LLM        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│    Supabase     │
│   PostgreSQL    │
│   ─────────     │
│  • chat_logs    │
│  • vocab_vault  │
│  • ai_feedback  │
└─────────────────┘
```

## Database Schema

### `chat_logs` - Conversation History
| Column | Type | Description |
|--------|------|-------------|
| id | int8 | Primary Key |
| created_at | timestamptz | Auto-generated timestamp |
| role | text | 'user' or 'assistant' |
| content | text | The message text |

### `vocab_vault` - Active Learning
| Column | Type | Description |
|--------|------|-------------|
| id | int8 | Primary Key |
| created_at | timestamptz | Auto-generated timestamp |
| target_phrase | text | The phrase to learn |
| note | text | User's note |
| status | text | 'active' or 'mastered' |
| usage_count | int4 | Times used in conversation |

### `ai_feedback` - Language Analysis
| Column | Type | Description |
|--------|------|-------------|
| id | int8 | Primary Key |
| created_at | timestamptz | Auto-generated timestamp |
| user_input | text | Original user sentence |
| better_version | text | Native rewrite |
| grammar_point | text | Explanation |
| is_reviewed | boolean | Review status |

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nativeecho
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure secrets**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   [supabase]
   url = "your-supabase-url"
   key = "your-supabase-key"

   [siliconflow]
   api_key = "your-api-key"
   base_url = "https://api.siliconflow.cn/v1"
   model = "deepseek-ai/DeepSeek-V3.2"
   ```

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment on Streamlit Community Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Add your secrets in the Streamlit Cloud dashboard under **Settings > Secrets**
4. Deploy!

## Configuration

All settings can be customized in the sidebar:

- **API Key**: Your SiliconFlow API key (auto-filled from secrets)
- **Model Name**: The LLM model to use (default: `deepseek-ai/DeepSeek-V3.2`)
- **Base URL**: API endpoint (default: `https://api.siliconflow.cn/v1`)
- **About Me**: Personal profile to customize AI responses

## Usage Tips

1. **Start Conversations**: Just type naturally in English - the AI will respond and help you improve
2. **Add Vocabulary**: Use the "Add to Learning Plan" expander to save phrases you want to learn
3. **Review Feedback**: Click on "Language Feedback" expanders under your messages to see improvement suggestions
4. **Track Progress**: Use the Vocabulary Vault in the sidebar to manage your learning words

## License

See [LICENSE](LICENSE) for details.
