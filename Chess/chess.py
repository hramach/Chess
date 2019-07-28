import time

class AlphaBeta:
    def __init__(self, gametree):
        self.gametree = gametree
        return
        
    def alpha_beta_search(self, tree):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        
        successors = tree.GetSuccessors()
        best_state = None
        for successor in successors:
            value = self.min_value(successor, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = successor
                
        return best_state
        
    def max_value(self, tree, alpha, beta):
        if self.isTerminal(tree):
            return self.getUtility(tree)
        infinity = float('inf')
        value = -infinity
        
        successors = self.getSuccessors(tree)
        for successor in successors:
            value = max(value, self.min_value(successor, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value
        
    def min_value(self, tree, alpha, beta):
        if self.isTerminal(tree):
            return self.getUtility(tree)
        infinity = float('inf')
        value = infinity
        
        successors = self.getSuccessors(tree)
        for successor in successors:
            value = min(value, self.max_value(successor, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
            
        return value
            
    
    def getSuccessors(self, tree):
        return tree.GetSuccessors()
        
    def isTerminal(self, tree):
        return len(tree.GetSuccessors()) == 0
        
    def getUtility(self, tree):
        return tree.GetScore()

class queue:
	def __init__(self, val):
		self.store = [val]

	def enqueue(self, val):
		self.store += [val]

	def dequeue(self):
		if self.isEmpty():
			return False
		else:
			val = self.store[0]
			self.store = self.store[1:len(self.store)]
			return val

	def isEmpty(self):
		return len(self.store) == 0

class tree:
	def __init__(self, move, score, turn):
		self.store = [[move, score, turn], []]

	def GetMove(self):
		return self.store[0][0]

	def GetScore(self):
		return self.store[0][1]

	def GetTurn(self):
		return self.store[0][2]

	def GetSuccessors(self):
		return self.store[1]

	def AddSuccessor(self, t):
		self.store[1] = self.store[1] + [t]
		return True

	def Get_LevelOrder(self):
		lst = []

		q = queue(self)
		while not q.isEmpty():
			t = q.dequeue()
			lst += [t.store[0][0:2]]
			for subtree in t.store[1]:
				q.enqueue(subtree)
		
		return lst

	def updateScores(self, player):
		if len(self.store[1]) > 0:
			for successor in self.store[1]:
				successor.updateScores(player)

			extVal = self.store[1][0].GetScore()
			bestMove = self.store[1][0].GetMove()
			for successor in self.store[1]:
				if (player == 10 and successor.GetTurn() == 10) \
				or (player == 20 and successor.GetTurn() == 10):
					if successor.GetScore() > extVal:
						extVal = successor.GetScore()
						bestMove = successor.GetMove()
				elif (player == 10 and successor.GetTurn() == 20) \
				or (player == 20 and successor.GetTurn() == 20):
					if successor.GetScore() < extVal:
						extVal = successor.GetScore()
						bestMove = successor.GetMove()

			if len(self.store[0][0]) == 0:
				self.store[0][0] = bestMove
			self.store[0][1] = extVal

			return True
		else:
			return False

def GetPlayerPositions(board, player):
	occupied = []
	offset = player
	i = 0

	for pos in board:
		piece = pos - offset
		if isValidPiece(piece):
			occupied += [i]
		i = i + 1

	return occupied

def GetPieceLegalMoves(board, position):
	moves = []
	player = 0
	opponent = 0

	if not isValidPosition(position):
		return []

	if isValidPiece(board[position] - 10):
		player = 10
		opponent = 20
	elif isValidPiece(board[position] - 20):
		player = 20
		opponent = 10
	else:
		return []

	piece = board[position] - player

	if piece == getPiece("pawn"):
		if player == 10:
			factor = +1
		else:
			factor = -1
		if isValidPosition(position + factor * 8):
			if board[position + factor * 8] == 0:
				moves += [position + factor * 8]
		if isValidPosition(position + factor * 7):
			if isValidPiece(board[position + factor * 7] - opponent):
				moves += [position + factor * 7]
		if isValidPosition(position + factor * 9):
			if isValidPiece(board[position + factor * 9] - opponent):
				moves += [position + factor * 9]
	elif piece == getPiece("knight"):
		absolute = [position + 17, position + 15, position - 17, \
			 position - 15, position + 10, position + 6, position - 10, position - 6]
		for pos in absolute:
			if isValidPosition(pos):
				if not (abs(col(pos) - col(position)) >= 2 and abs(row(pos) - row(position)) >= 2):
					if isValidPiece(board[pos] - opponent) or (board[pos] == 0):
						moves += [pos]
	elif piece == getPiece("bishop"):
		moves = genBishopMoves(board, position, player, opponent)
	elif piece == getPiece("rook"):
		moves = genRookMoves(board, position, player, opponent) 
	elif piece == getPiece("queen"):
		moves = genBishopMoves(board, position, player, opponent) \
			+ genRookMoves(board, position, player, opponent)
	elif piece == getPiece("king"):
		absolute = [position + 9, position + 8, position + 7, position + 1, \
			position - 9, position - 8, position - 7, position - 1]
		for pos in absolute:
			if isValidPosition(pos):
				if isValidPiece(board[pos] - opponent) or (board[pos] == 0):
					moves += [pos]
	
	return moves

def GetPieceValidMoves(board, position):	
	if isValidPiece(board[position] - 10):
		player = 10
		opponent = 20
	elif isValidPiece(board[position] - 20):
		player = 20
		opponent = 10
	else:
		return []

	moves = GetPieceLegalMoves(board, position)
	
	validMoves = []
	for move in moves:
		nBoard = list(board)
		nBoard[move] = nBoard[position]
		nBoard[position] = 0
		if not(inCheck(nBoard, player)):
			validMoves += [move]

	return validMoves

def IsPositionUnderThreat(board, position, player):
	if player == 10:
		opponent = 20
	elif player == 20:
		opponent = 10
	else:
		return False

	opponentPieces = GetPlayerPositions(board, opponent)

	opponentMoves = []
	for piece in opponentPieces:
		opponentMoves += GetPieceLegalMoves(board, piece)

	return position in opponentMoves

def printBoard(board):
	accum = "---- BLACK SIDE ----\n"
	maxI = 63
	for j in range(0, 8, 1):
		for i in range(maxI - j * 8, maxI - j * 8 - 8, -1):
			accum = accum + '{0: <5}'.format(board[i])
		accum = accum + " |" + str(8 - j) +  "\n"
	accum = accum + "|-A-||-B-||-C-||-D-||-E-||-F-||-G-||-H-|\n"
	accum = accum + "---- WHITE SIDE ----"
	return accum

def getChar(piece):
	if piece == 0:
		return 'p'
	elif piece == 1:
		return 'N'
	elif piece == 2:
		return 'B'
	elif piece == 3:
		return 'R'
	elif piece == 4:
		return 'Q'
	elif piece == 5:
		return 'K'
	else:
		return -1

def getPiece(name):
	if name == "pawn" or name == 'p':
		return 0
	elif name == "knight" or name == 'N':
		return 1
	elif name == "bishop" or name == 'B':
		return 2
	elif name == "rook" or name == 'R':
		return 3
	elif name == "queen" or name == 'Q':
		return 4
	elif name == "king" or name == 'K':
		return 5
	else:
		return -1

def genBoard():
	r = [0] * 64
	White = 10
	Black = 20
	for i in [ White, Black ]:
		if i == White:
			factor = +1
			shift = 0
		else:
			factor = -1
			shift = 63

		r[shift + factor * 7] = r[shift + factor * 0] = i + getPiece("rook")
		r[shift + factor * 6] = r[shift + factor * 1] = i + getPiece("knight")
		r[shift + factor * 5] = r[shift + factor * 2] = i + getPiece("bishop")

		if i == White:
			r[shift + factor * 4] = i + getPiece("queen")
			r[shift + factor * 3] = i + getPiece("king")
		else:
			r[shift + factor * 3] = i + getPiece("queen")
			r[shift + factor * 4] = i + getPiece("king")

		for j in range(0, 8, 1):
			r[shift + factor * (j + 8)] = i + getPiece("pawn")

	return r

def convPrintBoard(board):
	pBoard = list(board)
	for i in range(0, len(board), 1):
		if board[i] != 0:
			if isValidPiece(board[i] - 10):
				pBoard[i] = 'w' + getChar(board[i] - 10)
			elif isValidPiece(board[i] - 20):
				pBoard[i] = 'b' + getChar(board[i] - 20)
			else:
				return -1

	return pBoard

def convToStr(position):
	if not(isValidPosition(position)):
		return ""

	c = 0
	r = 0

	c = col(position)
	letters = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
	c = letters[c]

	r = row(position)
	r = r + 1

	return c + str(r)

def convToPos(string):
	if len(string) != 2:
		return -1

	col = string[0]
	row = int(string[1])

	letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
	cols = [7, 6, 5, 4, 3, 2, 1, 0]

	done = False
	i = 0
	while not(done):
		if col == letters[i]:
			col = cols[i]
			done = True
			i = i - 1
		i = i + 1

		if i >= len(letters):
			done = True
			i = -1

	if i == -1:
		return -2

	row = row - 1
	if not(row >= 0 and row < 8):
		return -3

	return row * 8 + col
	
def isValidPosition(position):
	return (position >= 0) and (position < 64)

def isValidPiece(piece):
	return (piece >= 0) and (piece < 6)

def col(position):
	return position % 8

def row(position):
	return position // 8

def genBishopMoves(board, position, player, opponent):
	moves = []

	# adding -> left, top
	accum = []
	nPos = position + 9
	while nPos < 64 and col(nPos) > col(position):
		accum += [nPos]
		nPos = nPos + 9

	moves += checkSeqPositions(board, accum, player, opponent)
	
	# adding -> right, top
	accum = []
	nPos = position + 7
	while nPos < 64 and col(nPos) < col(position):
		accum += [nPos]
		nPos = nPos + 7

	moves += checkSeqPositions(board, accum, player, opponent)

	# adding -> left, bottom
	accum = []
	nPos = position - 7
	while nPos > 0 and col(nPos) > col(position):
		accum += [nPos]
		nPos = nPos - 7

	moves += checkSeqPositions(board, accum, player, opponent)

	# adding -> right, bottom
	accum = []
	nPos = position - 9
	while nPos > 0 and col(nPos) < col(position):
		accum += [nPos]
		nPos = nPos - 9

	moves += checkSeqPositions(board, accum, player, opponent)

	return moves

def genRookMoves(board, position, player, opponent):
	moves = []

	# adding -> left
	accum = []
	nPos = position + 1
	while nPos < 64 and col(nPos) > col(position):
		accum += [nPos]
		nPos = nPos + 1

	moves += checkSeqPositions(board, accum, player, opponent)
	
	# adding -> top
	accum = []
	nPos = position + 8
	while nPos < 64 and row(nPos) > row(position):
		accum += [nPos]
		nPos = nPos + 8

	moves += checkSeqPositions(board, accum, player, opponent)

	# adding -> right
	accum = []
	nPos = position - 1
	while nPos > 0 and col(nPos) < col(position):
		accum += [nPos]
		nPos = nPos - 1
	
	moves += checkSeqPositions(board, accum, player, opponent)

	# adding -> bottom
	accum = []
	nPos = position - 8
	while nPos > 0 and row(nPos) < row(position):
		accum += [nPos]
		nPos = nPos - 8

	moves += checkSeqPositions(board, accum, player, opponent)

	return moves

def checkSeqPositions(board, ordList, player, opponent):
	i = 0
	valid = []	
	pieceFound = i >= len(ordList)

	while not pieceFound:
		if isValidPiece(board[ordList[i]] - player):
			valid = ordList[0:i]
			pieceFound = True
		elif isValidPiece(board[ordList[i]] - opponent):
			valid = ordList[0:i+1]
			pieceFound = True
		i = i + 1
		if not(pieceFound):
			pieceFound = i >= len(ordList)
			valid = list(ordList)

	return valid

def chooseSafeMove(board, player):
	accum = []
	L = GetPlayerPositions(board, player)
	for pos in L:
		moves = GetPieceValidMoves(board, pos)
		for i in moves:
			candBoard = list(board)
			candBoard[i] = candBoard[pos]
			candBoard[pos] = 0
			if not(IsPositionUnderThreat(candBoard, i, player)):
				accum = accum + [[pos, i]]

	if len(accum) > 0:
		moveIndex = random.randint(0, len(accum) - 1)
		return accum[moveIndex]
	else:
		moveIndex = random.randint(0, len(moves) - 1)
		return accum[moveIndex]

def shortSightedMove(board, player):
	if not(player == 10 or player == 20):
		return []

	accum = []
	initScore = evalBoard(board)
	L = GetPlayerPositions(board, player)
	for pos in L:
		moves = GetPieceValidMoves(board, pos)
		for i in moves:
			candBoard = list(board)
			candBoard[i] = candBoard[pos]
			candBoard[pos] = 0
			accum = accum + [[[pos, i], evalBoard(candBoard) - initScore]]

	if len(accum) == 0:
		return []
	else:
		moveIndex = 0
		extVal = accum[0][1]
		for i in range(0, len(accum), 1):
			if player == 10:
				if accum[i][1] > extVal:
					moveIndex = i
					extVal = accum[i][1]
			else:
				if accum[i][1] < extVal:
					moveIndex = i
					extVal = accum[i][1]

	return accum[moveIndex][0]

def moveWithForesight(board, player, depth):
	t = genTree(board, player, depth)
	t.updateScores(player)
	return [t.GetMove(), t]
	
def moveWithForesightv2(board, player, depth):
	t = genTree(board, player, depth)
	moveFinder = AlphaBeta(t)
	bestMoveTree = moveFinder.alpha_beta_search(t)
	return [bestMoveTree.GetMove(), t]

def findKing(board, player):
	king = player + 5
	for i in range(0, len(board), 1):
		if board[i] == king:
			return i
	return -1

def inCheck(board, player):
	king = findKing(board, player)
	return IsPositionUnderThreat(board, king, player)

def isCheckmate(board, player):
	if not(inCheck(board, player)):
		return False

	# checking whether the king can escape check
	playerPositions = GetPlayerPositions(board, player)
	for pos in playerPositions:
		moves = GetPieceLegalMoves(board, pos)
		for move in moves:
			nBoard = list(board)
			nBoard[move] = nBoard[pos]
			nBoard[pos] = 0
			if not(inCheck(board, player)):
				return False

	return True

def getPieceSquare(piece): # bottom to top, right to left, white on bottom
	if piece == getPiece("queen"):
		return \
		[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0, \
		 -1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, -1.0, \
		 -1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, -1.0, \
		 -0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, \
		 -0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5, \
		 -1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0, \
		 -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, \
		 -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
	elif piece == getPiece("bishop"):
		return \
		[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0, \
 		-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0, \
 		-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, \
 		-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, \
 		-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0, \
 		-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0, \
 		-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, \
 		-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
	elif piece == getPiece("pawn"):
		return \
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, \
 		0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5, \
 		0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5, \
 		0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0, \
 		0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5, \
 		1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, \
 		5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, \
 		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	elif piece == getPiece("king"):
		return \
		[2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0, \
		2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, \
 		-1.0,-2.0,-2.0,-2.0,-2.0,-2.0,-2.0,1.0, \
 		-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0, \
		-3.0, -4.0, -4.0, -5.0, -5.0, -4.0 ,-4.0, -3.0, \
 		-3.0, -4.0, -4.0, -5.0, -5.0, -4.0 ,-4.0, -3.0, \
 		-3.0, -4.0, -4.0, -5.0, -5.0, -4.0 ,-4.0, -3.0, \
 		-3.0, -4.0, -4.0, -5.0, -5.0, -4.0 ,-4.0, -3.0]
	elif piece == getPiece("rook"):
		return \
		[0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, \
 		-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, \
 		-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, \
 		-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, \
 		-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, \
 		-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, \
 		0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, \
 		0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	elif piece == getPiece("knight"):
		return \
		[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0, \
 		-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0, \
 		-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0, \
 		-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0, \
 		-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0, \
 		-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0, \
 		-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0, \
 		-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
	else:
		return False

def evalPositions(board):	
	whitePositions = GetPlayerPositions(board, 10)
	blackPositions = GetPlayerPositions(board, 20)

	score = 0
	
	for pos in whitePositions:
		piece = board[pos] - 10
		pieceSquare = getPieceSquare(piece)
		score += 10 * pieceSquare[pos]

	for pos in blackPositions:
		piece = board[pos] - 20
		pieceSquare = getPieceSquare(piece)
		score -= 10 * pieceSquare[63 - pos]

	return score

def evalMaterial(board):
	whitePositions = GetPlayerPositions(board, 10)
	blackPositions = GetPlayerPositions(board, 20)

	whitePieces = []
	blackPieces = []

	for pos in whitePositions:
		whitePieces += [board[pos] - 10]

	for pos in blackPositions:
		blackPieces += [board[pos] - 20]

	score = 0

	for piece in whitePieces:
		if piece == getPiece("pawn"):
			score += 100
		elif piece == getPiece("knight"):
			score += 320
		elif piece == getPiece("bishop"):
			score += 330
		elif piece == getPiece("rook"):
			score += 500
		elif piece == getPiece("queen"):
			score += 900
		elif piece == getPiece("king"):
			score += 20000
		else:
			return -1
	
	for piece in blackPieces:
		if piece == getPiece("pawn"):
			score -= 100
		elif piece == getPiece("knight"):
			score -= 320
		elif piece == getPiece("bishop"):
			score -= 330
		elif piece == getPiece("rook"):
			score -= 500
		elif piece == getPiece("queen"):
			score -= 900
		elif piece == getPiece("king"):
			score -= 20000
		else:
			return -1

	return score

def evalMobility(board):	
	whitePositions = GetPlayerPositions(board, 10)
	blackPositions = GetPlayerPositions(board, 20)

	numWhiteMoves = 0
	numBlackMoves = 0

	for pos in whitePositions:
		validMoves = GetPieceValidMoves(board, pos)
		numWhiteMoves += len(validMoves)

	for pos in blackPositions:
		validMoves = GetPieceValidMoves(board, pos)
		numBlackMoves += len(validMoves)

	return 5 * (numWhiteMoves - numBlackMoves)

def evalBoard(board):
	return evalPositions(board) + evalMaterial(board)

def switch(player):
	if player == 10:
		return 20
	elif player == 20:
		return 10
	else:
		return -1

def genTree(board, player, depth):
	if depth >= 0:
	    score = evalBoard(board)
	    
	    if player == 20:
            score = -1 * score
	    
		t = tree([], score, 0)
		grow(board, player, depth - 1, t)
		return t
	else:
		return False

def grow(board, player, depth, t):
	if depth >= 0:
		if t.GetMove() != []:
			board = list(board)
			board[t.GetMove()[1]] = board[t.GetMove()[0]]
			board[t.GetMove()[0]] = 0
				
		candidates = []
		playerPositions = GetPlayerPositions(board, player)
		for pos in playerPositions:
			legalMoves = GetPieceValidMoves(board, pos)
			for move in legalMoves:
				candBoard = list(board)
				candBoard[move] = candBoard[pos]
				candBoard[pos] = 0
				score = evalBoard(board)
				
				if player == 20:
                    score = -1 * score
				
				candidate = tree([pos, move], score, player)
				del(candBoard)
				grow(board, switch(player), depth - 1, candidate)
				candidates += [candidate]

		for candidate in candidates:
			t.AddSuccessor(candidate)

		return True
	else:
		return False

def chessPlayer(board, player):
	[move, t] = moveWithForesightv2(board, player, 3)
	candidateMoves = []
	successors = t.GetSuccessors()
	for candidate in successors:
		candidateMoves += [[candidate.GetMove(), candidate.GetScore()]]
	evalTree = t.Get_LevelOrder()
	return [True, move, candidateMoves, evalTree]