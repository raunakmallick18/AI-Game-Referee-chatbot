import os
import random
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai.types import Content, Part
from dotenv import load_dotenv

load_dotenv()

def resolve_round(user_move: str, tool_context: ToolContext) -> dict:
    state = tool_context.state
    round_num = state.get("round", 1)
    user_score = state.get("user_score", 0)
    bot_score = state.get("bot_score", 0)
    user_bomb_used = state.get("user_bomb_used", False)
    bot_bomb_used = state.get("bot_bomb_used", False)

    valid_moves = ["rock", "paper", "scissors", "bomb"]
    user_move = user_move.lower()
    outcome = ""
    winner = None
    bot_move = None

    if user_move not in valid_moves:
        outcome = f"Invalid move '{user_move}'. You lose this round."
        winner = "Bot"
    elif user_move == "bomb" and user_bomb_used:
        outcome = "You already used your bomb. Invalid move."
        winner = "Bot"
    else:
        if user_move == "bomb":
            user_bomb_used = True
        bot_options = ["rock", "paper", "scissors"]
        if not bot_bomb_used:
            bot_options.append("bomb")
        bot_move = random.choice(bot_options)
        if bot_move == "bomb":
            bot_bomb_used = True

        if user_move == "bomb" and bot_move == "bomb":
            outcome = "Both used bomb. It's a draw."
            winner = "Draw"
        elif user_move == "bomb":
            outcome = f"Your bomb beats Bot's {bot_move}."
            winner = "User"
        elif bot_move == "bomb":
            outcome = f"Bot's bomb beats your {user_move}."
            winner = "Bot"
        elif user_move == bot_move:
            outcome = f"Both played {user_move}. It's a draw."
            winner = "Draw"
        elif (user_move == "rock" and bot_move == "scissors") or \
             (user_move == "scissors" and bot_move == "paper") or \
             (user_move == "paper" and bot_move == "rock"):
            outcome = f"{user_move} beats {bot_move}. You win this round."
            winner = "User"
        else:
            outcome = f"{bot_move} beats {user_move}. Bot wins this round."
            winner = "Bot"

    if winner == "User":
        user_score += 1
    elif winner == "Bot":
        bot_score += 1

    tool_context.actions.state_delta = {
        "round": round_num + 1,
        "user_score": user_score,
        "bot_score": bot_score,
        "user_bomb_used": user_bomb_used,
        "bot_bomb_used": bot_bomb_used
    }

    return {
        "round": round_num,
        "user_move": user_move,
        "bot_move": bot_move,
        "outcome": outcome,
        "winner": winner,
        "user_score": user_score,
        "bot_score": bot_score
    }

referee = LlmAgent(
    name="rps_referee",
    model="models/gemini-pro",
    description="Rock-Paper-Scissors-Plus Game Referee Agent",
    tools=[resolve_round],
    instruction=(
        "You are a game referee for Rock-Paper-Scissors-Plus. Explain the rules briefly, then prompt user each round. "
        "Valid moves: rock, paper, scissors, bomb (once per game). Bomb beats all; bomb vs bomb = draw. "
        "Call resolve_round() every round and summarize the results. End after 3 rounds with a final winner."
    )
)

session_service = InMemorySessionService()
runner = Runner(agent=referee, app_name="rps_app", session_service=session_service)

async def main():
    user_id = "user123"
    session_id = "session_rps"
    session = await session_service.create_session(
        app_name="rps_app",
        user_id=user_id,
        session_id=session_id
    )

    print("Welcome to Rock–Paper–Scissors–Plus!")
    print("Rules: Best of 3. Valid moves: rock, paper, scissors, bomb (once per game). Invalid input loses round.")

    while session.state.get("round", 1) <= 3:
        user_input = input("Enter your move: ")
        msg = Content(parts=[Part(text=user_input)])
        for event in runner.run(user_id=user_id, session_id=session_id, new_message=msg):
            if event.is_final_response():
                print(event.content.parts[0].text)
                break
        session = await session_service.get_session(
            app_name="rps_app",
            user_id=user_id,
            session_id=session_id
        )

    us = session.state.get("user_score", 0)
    bs = session.state.get("bot_score", 0)
    print("\nFinal Score — You:", us, "| Bot:", bs)
    if us > bs:
        print("🏆 You win the game!")
    elif bs > us:
        print("🤖 Bot wins the game!")
    else:
        print("🤝 It's a draw!")

if __name__ == "__main__":
    asyncio.run(main())
