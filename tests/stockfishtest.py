import chess
import time
import chess.engine

def play_chess(color):
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish-windows-x86-64-sse41-popcnt.exe")

    if color == "white":
        player_color = chess.WHITE
    else:
        player_color = chess.BLACK

    while not board.is_game_over():
        if board.turn == player_color:
            # Player's turn
            move = input("Enter your move: ")
            print("\n")
            try:
                move = board.parse_san(move)
                board.push(move)
            except ValueError:
                print("Invalid move. Try again.")
        else:
            # Engine's turn
            result = engine.play(board, chess.engine.Limit(time=2.0))
            board.push(result.move)
            print("Engine's move:", result.move)

        print(board)
        
    time.sleep(10)
    engine.quit()

# Specify your color: "white" or "black"
play_chess("black")