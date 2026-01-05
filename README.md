# Rock–Paper–Scissors–Plus Referee Bot 🎮🤖

This is a minimal conversational AI referee for a game of **Rock–Paper–Scissors–Plus**, built using **Google ADK**. It tracks rounds, enforces rules, and provides natural language responses in a CLI-style game against the user.

## 🧠 Game Rules

- Best of **3 rounds**
- Valid moves: `rock`, `paper`, `scissors`, `bomb`
- `bomb` beats any move (but can be used only **once per player**)
- `bomb` vs `bomb` is a **draw**
- Invalid input loses the round
- Game ends automatically after 3 rounds

## 🧰 Tech Stack

- Python 3.10+
- [Google ADK (Agent Development Kit)](https://github.com/google-deepmind/adk)
- Gemini via Google AI Studio (API Key)

## 🚀 How to Run

### 1. Clone this repo and enter the folder

```
git clone https://github.com/your-username/rpsgame_bot.git
cd rpsgame_bot
```
### 2. Create and activate a virtual environment
```
python -m venv .venv
.venv\Scripts\Activate.ps1  # For Windows PowerShell
```
### 3. Install dependencies
```
pip install --upgrade pip
pip install google-adk[extensions]
pip install google-genai
```
### 4. Set up your .env file
Create a .env file in the root with the following content (get your API key from Google AI Studio):
```
GOOGLE_API_KEY="your-api-key-here"
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```
### 5. Run the bot
```
python rps_game_referee.py
```
## 🎮 Example Gameplay
```
Welcome to Rock–Paper–Scissors–Plus!
Rules: Best of 3. Valid moves: rock, paper, scissors, bomb (once per game). Invalid input loses round.

Enter your move: rock
Round 1: You played rock. Bot played scissors. You win the round!

Enter your move: bomb
Round 2: You used bomb! Bot played paper. You win again!

Enter your move: scissors
Round 3: Bot played bomb! Bot wins the round!

Final score: You 2 – Bot 1. You win! 🎉
```

## 📦 File Structure
```
rpsgame_bot/
├── rps_game_referee.py   # Main game script
├── README.md             # This file
└── .env                  # API key and config
```

## 🧠 Design Overview
Stateful Game Logic: Tracks scores, rounds, and bomb usage in tool_context.state.

LLM Agent: Handles dialogue and interaction flow.

ADK Tool: resolve_round processes the rules and updates state.

Separation of Concerns: Game logic and response generation are modular and testable.
