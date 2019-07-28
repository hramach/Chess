from chess import *
import time

def main():
	board = genBoard()
	done = False
	White = 10
	Black = 20

	while not(done):
		# Displaying the board state
		print(printBoard(convPrintBoard(board)))
		print("Score: " + str(evalBoard(board)))	
		legal = False

		if inCheck(board, White):
			if isCheckmate(board, White):
				print("Checkmate. Black wins.")
				return True
			else:
				print("White is in check!")

		# Getting a legal White move
		while not(legal):
			move = input("White, enter a move [L#L#]: ")
			if len(move) == 4:
				startStr = move[0:2]
				endStr = move[2:4]
				start = convToPos(startStr)
				end = convToPos(endStr)
				
				legal = start != -1 and end != -1
				if legal:
					legal = isValidPiece(board[start] - White)
			else:
				legal = False

			if legal:
				legalMoves = GetPieceValidMoves(board, start)
				legal = end in legalMoves

			if not(legal):
				print("Illegal move. Try again.")

		print()

		# Moving White
		board[end] = board[start]
		board[start] = 0

		# Displaying new board state
		print(printBoard(convPrintBoard(board)))
		print("Score: " + str(evalBoard(board)))
		legal = False

		if inCheck(board, Black):
			if isCheckmate(board, Black):
				print("Checkmate. White wins.")
				return True
			else:
				print("Black is in check!")

		# Getting a legal Black move
		print("The computer is thinking...")

		startTime = time.time()
		
		[start, end] = chessPlayer(board, Black)[1]

		endTime = time.time()

		print("Black moves " + convToStr(start) + " to " + convToStr(end) + ".")
		print("Elapsed time: " + str(endTime - startTime))
		print()

		# Moving Black
		board[end] = board[start]
		board[start] = 0

main()