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