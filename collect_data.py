from werwolf_main import run_streamed_game

NUM_GAMES = 20 

for i in range(NUM_GAMES):
    print(f"Running game {i + 1} of {NUM_GAMES}...")
    
    # Instanțiază un meci nou
    game_generator = run_streamed_game()
    
    # Parcurge generatorul pentru a lăsa mediul să execute pașii
    for step_data in game_generator:
        pass 
        
    print(f"Game {i + 1} was completed and saved.")