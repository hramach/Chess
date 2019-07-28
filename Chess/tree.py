from queue import *
from chess import *

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