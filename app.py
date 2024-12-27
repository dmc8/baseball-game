import streamlit as st
import random

st.title("⚾️ Streamlit Baseball Game ⚾️")

if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "inning": 1,
        "outs": 0,
        "home_score": 0,
        "away_score": 0,
        "message": "Start of the game!",
        "pitcher_choice": None,
        "batter_choice": None,
        "game_over": False,
        "bases": [False, False, False] # Represents 1st, 2nd, and 3rd base
    }

game_state = st.session_state.game_state

def handle_at_bat(batter_choice, pitcher_choice):
  if game_state["game_over"]:
    return

  outcomes = {
      "Fastball": {"Swing": "Hit", "Wait": "Ball"},
      "Curveball": {"Swing": "Miss", "Wait": "Strike"},
      "Changeup": {"Swing": "Hit", "Wait": "Ball"},
  }
  
  outcome = outcomes[pitcher_choice][batter_choice]
  game_state["message"] = f"Pitcher throws a {pitcher_choice}! Batter {batter_choice}s. It's a {outcome}!"
  
  if outcome == "Out":
    game_state["outs"] += 1
  elif outcome == "Hit":
    advance_bases()
  elif outcome == "Strike":
      # Simplified strike logic (3 strikes = out)
      if "strikes" not in game_state:
          game_state["strikes"] = 0
      game_state["strikes"]+=1
      if game_state["strikes"] == 3:
          game_state["message"] += " Batter is out!"
          game_state["outs"] += 1
          game_state["strikes"] = 0
  elif outcome == "Ball":
      if "balls" not in game_state:
          game_state["balls"] = 0
      game_state["balls"] += 1
      if game_state["balls"] == 4:
          game_state["message"] += " Batter walks!"
          advance_bases()
          game_state["balls"] = 0
  if game_state["outs"] == 3:
      game_state["inning"] += 1
      game_state["outs"] = 0
      game_state["bases"] = [False, False, False]
      game_state["strikes"] = 0
      game_state["balls"] = 0
      game_state["message"] = f"Start of Inning {game_state['inning']}!"

def advance_bases():
    # Start from 3rd base and move players
    if game_state["bases"][2]: #3rd base
        game_state["home_score"] += 1
        game_state["bases"][2] = False

    if game_state["bases"][1]: #2nd base
        game_state["bases"][2] = True #move to 3rd
        game_state["bases"][1] = False
    
    if game_state["bases"][0]: #1st base
        game_state["bases"][1] = True #move to 2nd
        game_state["bases"][0] = False

    game_state["bases"][0] = True

def reset_game():
    st.session_state.game_state = {
        "inning": 1,
        "outs": 0,
        "home_score": 0,
        "away_score": 0,
        "message": "New Game Started!",
        "pitcher_choice": None,
        "batter_choice": None,
        "game_over": False,
        "bases": [False, False, False]
    }

st.write(f"Inning: {game_state['inning']}")
st.write(f"Outs: {game_state['outs']}")
st.write(f"Score: Home {game_state['home_score']} - Away {game_state['away_score']}")

st.write(game_state["message"])

pitcher_choices = ["Fastball", "Curveball", "Changeup"]
batter_choices = ["Swing", "Wait"]

col1, col2 = st.columns(2)
with col1:
    game_state["pitcher_choice"] = st.selectbox("Pitcher throws:", pitcher_choices)
with col2:
    game_state["batter_choice"] = st.selectbox("Batter:", batter_choices)

if st.button("Play Ball!"):
    handle_at_bat(game_state["batter_choice"], game_state["pitcher_choice"])
    st.experimental_rerun()

if st.button("New Game"):
    reset_game()
    st.experimental_rerun()
