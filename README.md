# Cinematic Reading Engine (Cinei-read)

[![CI](https://github.com/OWNER/Storyboard/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/Storyboard/actions/workflows/ci.yml)

This repository contains the early scaffolding for **Cinei-read**, an MVP
that enhances traditional ebooks with subtle cinematic effects.

## Project Structure
- `backend/` – FastAPI service for uploading EPUBs and generating
  Cinematic Markup.
- `client/` – React Native application for reading enhanced books.
- `legacy/` – Historical prototypes not used by the MVP.


A revolutionary digital reading platform that enhances traditional ebooks with intelligent cinematic effects—kinetic typography, atmospheric audio, and thematic visuals—while preserving the fundamental joy of reading.

## 🎯 Vision & Philosophy

### Core Vision
Create a new media format that bridges traditional literature and modern interactive entertainment by integrating subtle, tasteful, and dynamic theatrical elements into digital books.

### Core Philosophy
**The book is the star.** All effects serve as subconscious enhancements to the reader's imagination, never as distractions. Built on "less is more," the most impactful effects are reserved for critical story moments, deepening immersion without disrupting the reading experience.

### Target Audience
- Avid readers who are technologically curious
- Younger audiences accustomed to dynamic digital media
- Anyone seeking a more immersive reading experience

## 🏗️ System Architecture

### Client-Server Model
The system separates intensive processing from real-time rendering for optimal performance:

#### 📱 Mobile Client (The Reader)
- **Platform**: React Native (Android first, iOS planned)
- **Purpose**: Upload books, manage library, experience enhanced content
- **Responsibilities**: Parse Cinematic Markup, render effects in real-time

#### ⚙️ Backend (The Conversion Engine)
- **Framework**: Python with FastAPI
- **Purpose**: Complete analysis and enhancement processing
- **Responsibilities**: Receive ebooks, parse content, apply effects, return enhanced versions

## 📋 Requirements

### Functional Requirements
- ✅ User account creation and management
- ✅ Secure EPUB upload and processing
- ✅ Personal library management
- ✅ Immersive Reader with playback controls
- ✅ Adjustable text size and brightness
- ✅ Global effect intensity settings
- ✅ Effect enable/disable options

### Non-Functional Requirements
- **Performance**: Process average novels in <2 minutes, maintain 60fps animations
- **Scalability**: Handle concurrent book processing as user base grows
- **Security**: Secure storage and private processing of user content

## 🧠 The Algorithmic Rulebook

### Guiding Principles
1. **Thematic Design**: Determine book's overall theme for Base Theme selection
2. **Effects Hierarchy**: Operate on strict layering system (no effect overload)
3. **Climactic Emphasis**: Reserve powerful effects for narrative climaxes
4. **Subtlety First**: All effect parameters default to low values

### Processing Pipeline

#### Step 1: Structural Analysis
**Action**: Parse EPUB to understand basic structure using XML parser
**Output**: Structured text map (Document Object Model for books)
**Example**: Separates character dialogue and identifies chapter/scene structure

#### Step 2: Thematic & Genre Analysis
**Action**: Use NLP libraries (spaCy/NLTK) for text classification
**Output**: Primary theme tag (e.g., `theme: sci-fi`, `theme: historical`)
**Example**: "Romeo and Juliet" → `theme: historical` → worn manuscript Base Theme

#### Step 3: Character & Dialogue Analysis
**Action**: 
- Create character profiles
- Perform sentiment analysis on dialogue
- Track emotional shifts throughout narrative
**Output**: Character profiles with evolving emotional signatures
**Example**: Tybalt → `emotion: aggressive`, Benvolio → `emotion: calm`

#### Step 4: Narrative Climax Detection
**Action**: Analyze pacing and emotional intensity for key moments
**Output**: Flags marking climactic sections
**Example**: "Have at thee, coward!" + "They fight" → climax flag → Critical Effect permission

#### Step 5: Effects Mapping & Output
**Action**:
- Apply Base Theme to entire book
- Apply Character Effects to corresponding dialogue
- Sparingly apply Secondary Effects in non-climactic sections
- Apply single Critical Effect in climactic sections
**Output**: Enhanced file in Cinematic Markup JSON format

## 📄 Cinematic Markup Format

The system outputs a structured JSON format that the mobile client parses:

```json
{
  "bookTitle": "Romeo and Juliet",
  "theme": "historical_manuscript",
  "chapters": [
    {
      "chapterTitle": "Act 1, Scene 1",
      "content": [
        {
          "type": "dialogue",
          "speaker": "Tybalt",
          "text": "What, drawn, and talk of peace! I hate the word...",
          "effects": [
            { "type": "text_style", "style": "fiery_sharp" },
            { "type": "word_effect", "word": "hate", "effect": "burn" }
          ]
        },
        {
          "type": "action",
          "text": "*They fight*",
          "effects": [
            { "type": "sound", "sound": "swords_clash.mp3", "volume": 0.3 }
          ]
        }
      ]
    }
  ]
}
```

## 🗂️ Project Structure

```
Storyboard/
├── backend/           # FastAPI service for EPUB processing
│   ├── app/
│   │   ├── models/    # Data models
│   │   ├── routers/   # API endpoints
│   │   └── services/  # Business logic
│   └── requirements.txt
├── client/            # React Native mobile app
│   ├── App.js
│   └── package.json
├── model/             # Legacy prototype code (to be refactored)
├── storyboard.py      # Original experiment script
└── README.md
```

## 🚀 Development Roadmap

### Phase 1: Core Engine & Reader (3 Months)
- [ ] Develop backend service with basic EPUB parsing
- [ ] Build initial Android client with functional library and reader
- [ ] Create manual Cinematic Markup file for "Romeo and Juliet" testing

### Phase 2: The Learning Algorithm (4 Months)
- [ ] Integrate NLP and sentiment analysis libraries
- [ ] Develop thematic, character, and climax detection logic
- [ ] Begin algorithm training on public domain books

### Phase 3: Closed Beta & Refinement (2 Months)
- [ ] Invite small user group for full pipeline testing
- [ ] Gather feedback on effect quality and subtlety
- [ ] Refine algorithm based on user feedback

### Phase 4: Public Launch & Iteration (Ongoing)
- [ ] Release on Google Play Store
- [ ] Continuous algorithm improvement
- [ ] New effects library expansion

## 🛠️ Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- React Native development environment

### Installation
```bash
# Backend setup
cd backend
pip install -r requirements.txt

# Client setup
cd client
npm install
```

## Testing

Run the test suite and verify Python syntax with:

```bash
pytest
python -m py_compile $(git ls-files '*.py')
```

The CI workflow executes these commands on every push.

### Development
```bash
# Start backend server
cd backend
uvicorn app.main:app --reload

# Start React Native app
cd client
npx react-native run-android
```

## 🤝 Contributing

This project is in early development. Contributions are welcome! Please see our contributing guidelines for more details.

## 📄 License

[License information to be added]

---

**Cinei-read** - Where literature meets cinematic magic ✨

