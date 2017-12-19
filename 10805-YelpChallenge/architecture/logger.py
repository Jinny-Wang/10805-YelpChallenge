
import pickle
class logger(object):
	"""docstring for logger"""
	def __init__(self):
		self.log_path = "/Users/yuyanzhang/Desktop/CMU/10605/yelp/10805-YelpChallenge/log/"

	def log_model(self,model_name,model,result,info=None):
		pickle.dump(model, open("".join([self.log_path,model_name,".pickle"]), 'wb'))
		result_log = open("../log/model_log.csv","a")
		if info ==None:
			result_log.write(result) 
		else:
			result_log.write("".join([(str)(result),"info: ",info,"\n"]))