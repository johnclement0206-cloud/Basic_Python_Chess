import chess
import chess.engine
import os

def main():
    stockfish_path = r"PythonChess\stockfish\stockfish-windows-x86-64-avx2.exe"
    
    if not os.path.exists(stockfish_path):
        print(f"Stockfish not found at: {stockfish_path}")
        print("Please download Stockfish from: https://stockfishchess.org/download/")
        print("Extract it and update the 'stockfish_path' variable.")
        return
    
    try:
        board = chess.Board()
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        
        print("Chess with Stockfish - Ready!")
        
        while not board.is_game_over():
            print("\nCurrent board:")
            print(board)
            
            if board.turn == chess.WHITE:
                while True:
                    move_input = input("Your move (e.g., e2e4 or Nf3): ").strip()
                    
                    if move_input.lower() == 'quit':
                        print("Game ended by user.")
                        engine.quit()
                        return

                    try:
                        move = None
                        try:
                            move = chess.Move.from_uci(move_input)
                        except Exception:
                            move = None

                        if move is None:
                            try:
                                move = board.parse_san(move_input)
                            except Exception:
                                move = None

                        if move is None:
                            print("Invalid move format! Use UCI (e.g., e2e4) or algebraic notation (e.g., Nf3)")
                            continue

                        if move in board.legal_moves:
                            board.push(move)
                            break
                        else:
                            print("Illegal move! Try again.")
                    except Exception as e:
                        print(f"Error parsing move: {e}")
            else:
                print("Stockfish thinking...")
                result = engine.play(board, chess.engine.Limit(time=2.0))
                
                move_san = board.san(result.move)
                print(f"Stockfish played: {move_san}")
                
                board.push(result.move)
        
        print("\nFinal board:")
        print(board)
        print("Game over!")
        
        if board.is_checkmate():
            winner = "White" if board.turn == chess.BLACK else "Black"
            print(f"Checkmate! {winner} wins!")
        elif board.is_stalemate():
            print("Stalemate! Game is drawn.")
        elif board.is_insufficient_material():
            print("Draw due to insufficient material.")
        elif board.is_fifty_moves():
            print("Draw by fifty-move rule.")
        elif board.is_repetition():
            print("Draw by repetition.")
        
        engine.quit()
        
    except Exception as e:
        print(f"Error: {e}")
        try:
            engine.quit()
        except:
            pass

if __name__ == "__main__":
    main()