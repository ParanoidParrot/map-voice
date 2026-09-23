# MapVoice

**MapVoice** is a navigation pronunciation engine that improves the pronunciation of Indian street names in GPS navigation systems.

This project demonstrates how mixed-language street names (e.g., English + Indian languages) can be normalized and converted into natural-sounding speech for navigation instructions. The system transforms raw navigation instructions into speech-friendly text before generating audio. Aim is to improve TTS output for Indian place names by combining:

- map-derived linguistic data
- suffix-aware normalization
- word splitting
- speech synthesis using Sarvam AI

It also translates normalized English navigation instructions into selected Indian languages and generates native-language speech using Sarvam Translate + Bulbul TTS.


## Problem

Navigation systems often mispronounce Indian street names due to:

- abbreviations (Rd, Dr, St)
- mixed-language tokens
- transliterated names
- acronyms (BDA, NIT)


## Tech Stack

| Technology | Use Case |
| :--- | :--- |
| Python | FastAPI, data processing |
| OpenStreetMap | Geospatial data |
| Sarvam AI | Text-to-Speech |


## How to Run
-  Setup environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install dependencies
```bash
python -m pip install -r requirements.txt
```

- Run demo
```bash
python -m scripts.voice_demo
```

Audio files will be generated in:
scripts/audio_outputs/

```bash
python -m uvicorn backend_api.main:app --reload
```

Open http://127.0.0.1:8000/ to see webpage and demo



## Audio Comparison

MapVoice can generate before / after speech samples for the same navigation instruction:

- **Raw**: original navigation text
- **Normalized**: text after MapVoice expansion and suffix-aware processing

Try it out: [TryItHere](https://nav-pronunciation-engine-production.up.railway.app)


## Key Highlights

- Data-driven linguistic modeling using real map data
- Handles Indian multilingual naming patterns
- Improves TTS without modifying the speech model
- Modular pipeline (normalization → parsing → TTS)
- Spells common navigation acronyms such as MG, JP, BTM, NH, and HSR before TTS.
- Supports Sarvam AI Pronunciation Dictionary via `SARVAM_PRONUNCIATION_DICT_ID`.
- Uses configurable TTS model, speaker, pace, and temperature for pronunciation experiments.
- Android MVP tested via APK / internal Play Console track.

## Future Work

- Multi-language script injection (e.g, Kannada, Hindi, Tamil)
- Route playback simulation (real-time navigation)
- Expanded linguistic lexicon with regional metadata
- Android / iOS prototype integration



## System Architecture

```mermaid
flowchart TD 
    %% Runtime pipeline
    A[Raw Navigation Instruction] --> B[Tokenizer]
    B --> C[Rule-based Normalizer]
    C --> D[Number & Distance Expansion]
    D --> E[Abbreviation & Acronym Expansion]
    E --> F[Suffix Detector]
    F --> G[Word Splitter]
    G --> H[Normalized Navigation Text]

    %% English pronunciation path
    H --> I[Pronunciation Hint Layer]
    I --> J[Speech-friendly English Text]
    A --> K[Raw English TTS]
    J --> L[Normalized English TTS]

    %% Native-language path
    H --> M{Native Language Selected?}
    M -- Yes --> N[Sarvam Translate API]
    N --> O[Native-script Navigation Text]
    O --> P[Sarvam TTS<br/>Selected Language Code]
    M -- No --> Q[Skip Native Translation]

    %% Audio outputs
    K --> R[Raw English Audio]
    L --> S[Normalized English Audio]
    P --> T[Native-language Audio]

    R --> U[Web Demo / API Response]
    S --> U
    T --> U
    Q --> U

    %% Data pipeline
    V[OpenStreetMap India Dataset Offline Source Data] --> W[Named Road Extraction]
    W --> X[Suffix Mining]
    X --> Y[Suffix Cleaning & Clustering]
    Y --> Z[Lexicon Builder]
    Z --> AA[lexicon.json]

    %% Lexicon feeds runtime suffix processing
    AA --> F

MapVoice uses an OpenStreetMap-derived Indian road-name lexicon to support suffix detection and word splitting during normalization. At runtime, normalized navigation text can follow either the pronunciation-aware English TTS path or, when a native language is selected, a translation path that generates native-script text and speech using Sarvam Translate and TTS. OpenStreetMap India data is used offline to derive road-name suffix patterns and build lexicon.json. The deployed runtime depends on the generated lexicon, not on the raw OSM/PBF/GeoJSON files.