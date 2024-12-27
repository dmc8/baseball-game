import streamlit as st
import random

MLB_TEAMS = [
    "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox",
    "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians",
    "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals",
    "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers",
    "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics",
    "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants",
    "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers",
    "Toronto Blue Jays", "Washington Nationals"
]

DIVISIONS = {
    "AL East": ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", "Toronto Blue Jays"],
    "AL Central": ["Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"],
    "AL West": ["Los Angeles Angels", "Houston Astros", "Oakland Athletics", "Seattle Mariners", "Texas Rangers"],
    "NL East": ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies", "Washington Nationals"],
    "NL Central": ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates", "St. Louis Cardinals"],
    "NL West": ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants"]
}

PLAYER_NAMES = [
    "Liam O'Connell", "Ava Rodriguez", "Noah Dubois", "Isabella Moreau", "Ethan Silva",
    "Mia Dubois", "Lucas Martin", "Charlotte Bernard", "Jackson Thomas", "Amelia Petit",
    "Aiden Richard", "Harper Durand", "Elijah Garcia", "Evelyn Leroy", "Grayson White",
    "Abigail Fontaine", "Oliver Nguyen", "Emily Lopez", "Caleb Hernandez", "Madison Clement",
    "Henry Wilson", "Sofia Anderson", "Owen Taylor", "Scarlett Moore", "James Jackson",
    "Victoria Thompson", "Benjamin Harris", "Eleanor Perez", "Daniel Sanchez", "Grace Clark",
    "Joseph Martinez", "Chloe Davis", "Samuel Brown", "Penelope Wilson", "David Garcia",
    "Elizabeth Rodriguez", "Matthew Smith", "Sofia Johnson", "Andrew Williams", "Natalie Jones"
]

def generate_player_name():
    return random.choice(PLAYER_NAMES)

def simulate_game(team1, team2):
    score1 = random.randint(1, 10)
    score2 = random.randint(1, 10)
    return (team1, score1), (team2, score2)

def simulate_season(teams):
    standings = {team: {"wins": 0, "losses": 0, "division": None, "mvp_candidate": None} for team in teams}
    for division, division_teams in DIVISIONS.items():
        for team in division_teams:
            standings[team]["division"] = division
    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                for _ in range(3):
                    (t1, s1), (t2, s2) = simulate_game(team1, team2)
                    if s1 > s2:
                        standings[t1]["wins"] += 1
                        standings[t2]["losses"] += 1
                    else:
                        standings[t1]["losses"] += 1
                        standings[t2]["wins"] += 1

    mvp_candidates = {}
    for team in teams:
        player_name = generate_player_name()
        mvp_candidates[player_name] = random.randint(100, 200)
        standings[team]["mvp_candidate"] = player_name
    regular_season_mvp_player = max(mvp_candidates, key=mvp_candidates.get)
    regular_season_mvp_team = next((team for team, data in standings.items() if data["mvp_candidate"] == regular_season_mvp_player), None)

    return standings, regular_season_mvp_player, regular_season_mvp_team

def determine_playoff_teams(standings):
    division_winners = {}
    wildcard_teams = []

    for division, division_teams in DIVISIONS.items():
        best_record = None
        best_team = None
        for team in division_teams:
            record = standings[team]
            if best_record is None or record["wins"] > best_record["wins"]:
                best_record = record
                best_team = team
        division_winners[division] = best_team

    remaining_teams = [team for team in standings if team not in division_winners.values()]
    sorted_remaining = sorted(remaining_teams, key=lambda team: (standings[team]["wins"]/(standings[team]["wins"]+standings[team]["losses"])) if (standings[team]["wins"]+standings[team]["losses"]) > 0 else 0, reverse=True)
    wildcard_teams = sorted_remaining[:2]

    playoff_teams = list(division_winners.values()) + wildcard_teams
    return playoff_teams

def simulate_playoff_series(team1, team2):
    wins1 = 0
    wins2 = 0
    while wins1 < 4 and wins2 < 4:
        (t1, s1), (t2, s2) = simulate_game(team1, team2)
        if s1 > s2:
            wins1 += 1
        else:
            wins2 += 1
    return team1 if wins1 == 4 else team2

def simulate_playoffs(playoff_teams, standings):
    quarterfinal_winners = []
    for i in range(0, len(playoff_teams), 2):
        winner = simulate_playoff_series(playoff_teams[i], playoff_teams[i+1])
        quarterfinal_winners.append(winner)

    semifinal_winners = []
    for i in range(0, len(quarterfinal_winners), 2):
        winner = simulate_playoff_series(quarterfinal_winners[i], quarterfinal_winners[i+1])
        semifinal_winners.append(winner)

    champion = simulate_playoff_series(semifinal_winners[0], semifinal_winners[1])

    ws_mvp_candidates = {}
    for team in semifinal_winners:
        player_name = standings[team]["mvp_candidate"]
        ws_mvp_candidates[player_name] = random.randint(50, 100)
    world_series_mvp_player = max(ws_mvp_candidates, key=ws_mvp_candidates.get)
    world_series_mvp_team = next((team for team, data in standings.items() if data["mvp_candidate"] == world_series_mvp_player), None)

    return champion, world_series_mvp_player, world_series_mvp_team, semifinal_winners

st.title("⚾️ MLB Season Simulator ⚾️")

if "season_simulated" not in st.session_state:
    st.session_state.season_simulated = False
if "playoffs_simulated" not in st.session_state:
    st.session_state.playoffs_simulated = False

if st.button("Simulate Regular Season"):
    with st.spinner("Simulating season..."):
        standings, regular_season_mvp_player, regular_season_mvp_team = simulate_season(MLB_TEAMS)
        st.session_state.standings = standings
        st.session_state.regular_season_mvp_player = regular_season_mvp_player
        st.session_state.regular_season_mvp_team = regular_season_mvp_team
        st.session_state.season_simulated = True
        st.session_state.playoffs_simulated = False

if st.session_state.season_simulated:
    st.subheader("Regular Season Standings (Top Teams):")
    sorted_standings = sorted(st.session_state.standings.items(), key=lambda item: item[1]["wins"] / (item[1]["wins"] + item[1]["losses"]) if (item[1]["wins"] + item[1]["losses"]) > 0 else 0, reverse=True)
    for team, record in sorted_standings[:10]:
        win_percentage = (record["wins"] / (record["wins"] + record["losses"])) if (record["wins"] + record["losses"]) > 0 else 0
        st.write(f"{team}: {record['wins']} Wins - {record['losses']} Losses - {win_percentage:.3f} Win% - Division: {record['division']}")
    st.write(f"Regular Season MVP: {st.session_state.regular_season_mvp_player} of the {st.session_state.regular_season_mvp_team}")

    playoff_teams = determine_playoff_teams(st.session_state.standings)
    st.subheader("Playoff Teams:")
    st.write(playoff_teams)

    if st.button("Simulate Playoffs"):
        with st.spinner("Simulating Playoffs..."):
            champion, world_series_mvp_player, world_series_mvp_team, semifinal_winners = simulate_playoffs(playoff_teams, st.session_state.standings)
            st.session_state.champion = champion
            st.session_state.world_series_mvp_player = world_series_mvp_player
            st.session_state.world_series_mvp_team = world_series_mvp_team
            st.session_state.semifinal_winners = semifinal_winners
            st.session_state.playoffs_simulated = True

if st.session_state.playoffs_simulated:
    st.subheader(f"🏆 The {st.session_state.champion} are the World Series Champions! 🏆")
    st.write(f"World Series MVP: {st.session_state.world_series_mvp_player} of the {st.session_state.world_series_mvp_team}")