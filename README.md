# ZentroMart Chatbot

ZentroMart Chatbot is a Streamlit customer-support assistant for a synthetic e-commerce dataset. It combines retrieval-augmented generation (RAG), Azure OpenAI, customer CSV data, and  speech input/output.

The project is an educational prototype. The order lookup and ticket tools are offline simulations and are not production authentication, payment, or customer-support systems.

## Features

- Answers policy and help questions from the Markdown knowledge base.
- Uses multilingual sentence-transformer embeddings and a local Chroma vector store.
- Supports order-specific lookup behind verification using either the registered phone suffix or delivery pincode.
- Creates synthetic human-handover tickets in `tools/tickets_created.csv`.
- Supports text chat and microphone-based voice interaction.
- Includes synthetic customers, orders, products, pincodes, holidays, support logs, and practice/evaluation data.

## How it works

1. `build_index.py` reads the Markdown files in `kb/`, parses their front matter, splits them by `##` sections, embeds them, and stores them in the `zentromart_kb` Chroma collection under `chroma_db/`.
2. `src/retreiver.py` retrieves up to five relevant sections using maximal marginal relevance.
3. `src/agent.py` sends the question, retrieved context, system prompt, conversation state, and available tools to the configured Azure OpenAI model.
4. The Streamlit UI in `run.py` gives chatbot interface which displays the question/reply.

## Project structure

```text
ZentroMart_Chatbot/
├── run.py                    # Streamlit application entry point
├── build_index.py            # Builds/rebuilds the Chroma knowledge-base index
├── requirements.txt          # Python dependencies
├── .env_example              # Environment-variable template
├── batch_audio.py            # converts audio files to required outputs
├── data/                     # Synthetic commerce and support data
├── kb/                       # Policy, FAQ, help, agent-guide, and marketing documents
├── practice/                 # Practice questions and multi-turn conversations
├── sample_output/            # Example generated/evaluation JSONL outputs
├── sample_reply/             # Runtime-generated assistant WAV replies
├── sample_voice/             # Runtime-generated recorded WAV questions
├── src/
│   ├── agent.py              # LangChain/LangGraph agent and memory
│   ├── llm.py                # Azure OpenAI client configuration
│   ├── prompt.py             # Safety, privacy, verification, and response rules
│   ├── retreiver.py          # RAG retrieval and agent invocation
│   ├── rec_play.py           # Microphone recording and audio playback
│   └── voice.py              # Gnani STT/TTS integration
├── tools/
│   ├── tools.py              # Offline order lookup and ticket creation
│   └── tickets_created.csv   # Ticket log created by the tool
└── chroma_db/                # Local generated vector index (ignored by Git)
```

## Requirements

- Python 3.11 or newer is recommended.
- Azure OpenAI access and a deployed chat model.
- Gnani credentials for speech-to-text and text-to-speech features.
- A working microphone and audio output device for voice mode.
- Internet access for api calling.

## Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env_example .env
```

Set the values in `.env`:

```dotenv
GNANI_API_KEY=your_gnani_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-project-name.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

`.env` and `chroma_db/` are excluded by `.gitignore`.

## Build the knowledge-base index

Run this from the repository root so the Knowledge-base `chroma_db/` from kb/ can be created:

```powershell
python build_index.py
```

## Run the application

```powershell
streamlit run run.py
```

Open the local URL printed by Streamlit. Type a question in the chat box or select `Voice Assist` to record a question. The current UI plays the generated WAV reply for both typed and spoken questions.

Example questions:

- `How long do refunds to the ZentroMart Wallet take?`
- `Can I return electronics delivered before 1 August 2026?`
- `I want a human agent to help with my order.`

For an order-specific question, the assistant requests the order ID and exactly one verification value: the last four registered-phone digits or the six-digit delivery pincode. Order details should only be disclosed after successful verification.

## Batch-process customer audio

`batch_audio.py` is a small wrapper around the existing `STT`, `TTS`, and `retrieve_context` functions. Pass the input and output folders in the terminal:

```powershell
python batch_audio.py .\customer_audio_file --output-dir .\batch_output_file
```

It scans `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, and `.aac` files. For every input from `customer_audio_file/` it saves four files in `batch_output_file/`:

```text
batch_output_file/
├── customer_001_transcript.txt
├── customer_001_reply.txt
├── customer_001_reply.wav
└── customer_001_chunks.txt
```

`*_chunks.txt` contains the retrieved document chunks returned by the existing RAG function.

## Data and knowledge base

The bundled data is synthetic and includes:

- 300 customers and 1,000 orders.
- 1,783 order-item rows and 70 products.
- 36 pincode/serviceability rows, four warehouse holidays, and 244 support logs.
- 21 Markdown knowledge-base documents covering current policies, FAQs, help articles, agent guidance, marketing content, and one explicitly superseded returns policy.
- Practice files containing 52 questions and 96 conversation rows.

The knowledge-base reference date is 20 October 2026. Current policy documents take precedence over agent guides, help documents, FAQs, and marketing documents; the prompt also handles the explicitly superseded electronics policy.

## Tools

`tools.tools.lookup_order(order_id, verification_value=None)` returns a verification-required response until one valid verification value is supplied. It discloses order data only after verification.

`tools.tools.create_ticket(summary, order_id=None, reason=None, intent=None)` appends a synthetic ticket to `tools/tickets_created.csv`. Summaries must contain at least 20 characters.
