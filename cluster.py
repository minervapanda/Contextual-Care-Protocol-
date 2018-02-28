import pandas as pd
import math

keywords=[
	('corpscular','ferratin'),
	('corpuscul5ar','erythrocyte'),
	]

def to_key(fb1):
	if fb1.empty:
		return -1
	keys=list(pd.read_csv("Decision Trees Data/"+str(fb1.iloc[0]['tree'])+".csv"))
	# print(keys[int(fb1.iloc[0]['feature'])].split()[0].lower())
	return keys[int(fb1.iloc[0]['feature'])].split()[0].lower()

def diff_fid(df,fid):
	df.is_copy=False
	df2=df[df['feedback id']==fid]
	cid=df['cluster_id'].max()
	# print(fid)
	if math.isnan(cid):
		cid=0
	cid=int(cid)
	# print("cid",cid,fid)
	for c in range(1,cid+1):
		to_check=df2[df2['is changed']=='Y']
		for row in range(len(to_check.index)):
			# print(to_check,fid,c)
			changes=to_check.iloc[[row]]
			# print(df[df['cluster_id']==c])
			if sim(df,changes,df[df['cluster_id']==c].iloc[[0]]):
				df.loc[df['feedback id']==fid,'cluster_id']=int(c)
				return
	# print("cid",cid,fid)
	df.loc[df['feedback id']==fid,'cluster_id']=int(cid+1)
	# print(df)

def main(df):
	# print(df)
	fss=df[df['cluster_id'].isnull()]
	# print(fss)
	fs=list(set(fss['feedback id']))
	done=[]
	for a in fs:
		diff_fid(df,a)
		done.append(a)
		# left=set(fs)-set(done)
		# for b in left:
		# 	diff_fid(df,a,b)

def sim(df,fb1,fb2):
	# print(fb1,"fb1")
	# print(fb2,"fb2")
	# print("fb12",str(fb1.iloc[0]['tree']),"fb22",str(fb2.iloc[0]['tree']))
	if str(fb1.iloc[0]['tree'])==str(fb2.iloc[0]['tree']):
		pos1=df[df['new position']==int(fb1.iloc[0]['new position']-1)]
		pos2=df[df['new position']==int(fb2.iloc[0]['new position']-1)]
		# print(pos1,pos2)
		# if (pos1==pos2):
		# 	return 1
		feature_sim=((to_key(fb1),to_key(fb2)) in keywords) or ((to_key(fb2),to_key(fb1)) in keywords)
		prev_sim=(to_key(pos1),to_key(pos2) in keywords) or (to_key(pos2),to_key(pos1) in keywords)
		if feature_sim and prev_sim:
			return 1
	return 0

if __name__ == '__main__':
	df=pd.read_csv("feedback.csv")
	# replaced=df[(df['feedback id']==fid and df['new position']=='-1' and df['is changed']=='Y')]
	# new_stuff=df[(df['feedback id']==fid and df['is new']=='True' and df['is changed']=='Y')]
	main(df)
	df.to_csv("feedback2.csv")
	print(df)
	# main(new_stuff)
	# print(new_stuff)
