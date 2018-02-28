import pandas as pd
import numpy as np
import dateutil.parser
from sklearn.neural_network import MLPClassifier
import warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)

def load_csv(filename,remove_head=True):
	data_frama=pd.read_csv(filename)
	dataset=data_frama.values.tolist()
	if remove_head:
		dataset=dataset[1:]
	return dataset

main = 'main_table.csv'
dataset = np.array(load_csv(main,remove_head=False))

new = 'new.csv'
new_data = np.array(load_csv(new,remove_head=False))

# feedback = '/home/pranshu/Dropbox/GE/Dataset/feedback.csv'
# feed = load_csv(feed)

roll='B114061'

print("Train for ",roll)
train_X,train_y,test_X=[],[],[]
X,y,x=[],[],[]
for i in dataset:
	d = dateutil.parser.parse(i[2])
	i[2] = d.month + (d.year-2015)*12
	X.append(i[2:-1].astype(float))	
	y.append(i[-1].astype(float))
	if i[1]==roll:
		train_X.append(i[2:-1].astype(float))
		train_y.append(i[-1].astype(float))
		print("Data to train :",train_X[-1],"Disease :",train_y[-1])

print("\nTest for ",roll)
for i in new_data:
	d = dateutil.parser.parse(i[2])
	i[2] = d.month + (d.year-2015)*12
	x.append(i[2:].astype(float))
	if i[1]==roll: 
		test_X.append(i[2:].astype(float))
	print("New Entry :",test_X[-1])
clf = MLPClassifier(solver='sgd', alpha=1e-5,hidden_layer_sizes=(10,10), random_state=1)

c=0
p=0

if len(train_X)!=0 and len(test_X)!=0:
	clf.fit(train_X	, train_y)
	p=clf.predict_proba(test_X)
	c=clf.predict(test_X)
	#print(clf.score(test_X,train_y[:6]))
else:
	clf.fit(X, y)
	p=clf.predict_proba(x)
	c=clf.predict(x)

print("\nProbabilities :",p,"\nMax :",c,"\n")
#pd.DataFrame(np.array([len(dataset)+1,roll,x,c])).to_csv("/home/pranshu/Dropbox/GE/Dataset/main_table.csv",mode='a',index=False,header=False)
