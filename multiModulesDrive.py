import ckbot.logical as L

class MultiModulesDrive():
	"""control multimodules to its desired position"""
	def __init__(self, arg):
		super(MultiModulesDrive, self).__init__()
		self.arg = arg
