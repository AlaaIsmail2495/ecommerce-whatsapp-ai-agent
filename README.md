# E-Commerce store WhatsApp AI Agent

An AI-powered e-commerce assistant integrated with WhatsApp via **Neonize**, powered by **Google GenAI** with tool/function calling, and backed by a **FastAPI + SQLAlchemy + SQLite** service. Customers can browse categories and products, manage their shopping cart, complete checkout, and track or cancel orders through natural WhatsApp conversations.

## Tech Stack
- **Backend API:** FastAPI, Uvicorn, SQLAlchemy, SQLite
- **AI Agent:** Google GenAI (`google-genai`) with function/tool calling
- **WhatsApp Client:** Neonize
- **Configuration & Testing:** Python, `python-dotenv`, `stimulate_chat.py`

## Project Structure
```text
ecommerce-whatsapp-agent/
├── backend/
│   ├── database.py          # SQLAlchemy engine & session setup
│   ├── ecommerce.db         # SQLite database file
│   ├── main.py              # FastAPI application entry point & endpoints
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   └── seed_data.py         # Initial categories & products seeding script
├── .env                     # Environment variables (ignored in Git)
├── .gitignore               # Ignored files and folders
├── agent.py                 # AI agent prompt, configuration & tool orchestration
├── bot.py                   # Neonize WhatsApp client & incoming message handler
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── stimulate_chat.py        # Interactive terminal chat simulation script
├── store_bot_session.sqlite # Neonize WhatsApp session database (ignored in Git)
└── tools.py                 # Agent tools calling the FastAPI backend
```

## Setup & Installation

### 1. Clone the repository
```bash
git clone <https://github.com/AlaaIsmail2495/ecommerce-whatsapp-ai-agent.git>
cd ecommerce-whatsapp-agent
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root directory and add your required environment variables:
```env
GEMINI_API_KEY=your_gemini_api_key_here
BACKEND_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
```
*(Adjust variable names if your `agent.py` or `tools.py` uses different environment variable names).*

## Running the Project

### 1. Seed the database
Run the seeding script from inside the `backend` directory:
```bash
cd backend
python seed_data.py
cd ..
```

### 2. Start the FastAPI backend server (Terminal 1)
```bash
uvicorn backend.main:app --reload --port 8000
```
Interactive API documentation will be available at `http://127.0.0.1:8000/docs`.

### 3. Test the agent in the terminal (Optional)
```bash
python stimulate_chat.py
```

### 4. Start the WhatsApp bot (Terminal 2)
```bash
python bot.py
```
Scan the QR code displayed in the terminal using WhatsApp (**Settings -> Linked Devices -> Link a Device**), then send a message from another WhatsApp number to test product browsing, cart management, and checkout.