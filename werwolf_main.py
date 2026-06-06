import os
import json
import textarena as ta
from rotating_client import RotatingOpenAIClient
from rotating_agent import RotatingOpenAIAgent
import time

def run_streamed_game():
    logs = []

    api_keys = [
        "bc315679fc9b7675265b194d420449a0",
        "de905758b4bf5da0bc26ec7555c2cd92",
    ]

    openai_client = RotatingOpenAIClient(
        api_keys=api_keys,
        base_url="https://chat-ai.academiccloud.de/v1", 
        model="llama-3.3-70b-instruct",             
    )

    agents = {
        i: RotatingOpenAIAgent(client=openai_client)
        for i in range(6)
    }

    # Initialize the environment
    env = ta.make(env_id="SecretMafia-v0")

    # wrap it for additional visualizations
    env = ta.wrappers.SimpleRenderWrapper(env=env)

    env.reset(num_players=len(agents))
    
    # Send initial game state and roles to the UI
    yield {
    "type": "init",
    "actual_roles": env.player_roles  
    }

    # Main game loop
    step=0
    done = False
    while not done:
        player_id, observation = env.get_observation() # Get the current player's ID and observation
        action = agents[player_id](observation)["action"] # Get the action from the corresponding agent based on the player ID
        done, step_info = env.step(action=action) # Take a step in the environment with the chosen action and receive the new state and reward
       
        player_data = {
            "step": step,
            "player_id": player_id,
            "observation": observation,
            "action": action,
            "step_info": step_info,
            "alive_ids": env.state.game_state["alive_players"]
        }
        logs.append(player_data)
        yield player_data # Send the step data to the UI for real-time visualization

        step += 1

    rewards, game_info = env.close() # Get final rewards and game info after the game is done
    

    winner_ids = [player_id for player_id, reward in rewards.items() if reward > 0]
    
    # Determine the winning team based on the first winner's role
    if len(winner_ids) > 0 and env.player_roles[winner_ids[0]] == "Mafia":
        winners = "Mafia"
    else:
        winners = "Villagers"

    game_log = {
        "num_players": len(agents),
        "steps": logs,
        "rewards": rewards,
        "game_info": game_info,
        "winners": winners
    }

    timestamp = int(time.time())
    filename = f"mafia_game_log_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(game_log, f, indent=2)

    yield { # Final game summary to the UI
        "type": "final",
        "rewards": rewards,
        "game_info": game_info,
        "logs": logs,
        "winners": winners
    }
