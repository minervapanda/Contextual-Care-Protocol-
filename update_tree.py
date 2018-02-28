import decision_trees
import pandas as pd

def update_tree_replace(cid,old_tree,repl2,pos):
	tree_file=open("Metadata/"+old_tree+".txt","r")
	repl=repl2[repl2['is changed']=='Y']
	start=decision_trees.parse_tree(tree_file)
	# print(type(repl))
	repl_sort=repl2.sort('orignal position')
	repl_sort=repl_sort[repl_sort["cluster_id"]==cid]
	prev=start
	decision_trees.printtree(start)
	print(len(repl_sort.index),pos)
	for node in range(len(repl_sort.index)):
		if node==0:
			continue
		elif node==pos:
			prev.col=repl_sort.iloc[node]['feature']
			main_table=pd.read_csv("Decision Trees Data/"+repl_sort.iloc[node]['tree']+".csv")
			exist_features=list(main_table)
			if repl_sort.iloc[node]['is new']==1:
				main_table[repl_sort.iloc[node]['feature name']]=repl_sort.iloc[node]['value']
				prev.col=len(main_table.columns)
			else:
				prev.col=repl_sort.iloc[node]['feature']
			prev.value=repl_sort.iloc[node]['value']
			decision_trees.printtree(start)
			main_table.to_csv("main_table2.csv")
		if prev.tb and repl_sort.iloc[node]['feature']==prev.tb.col:
			prev=prev.tb
		else:
			prev=prev.fb

def to_update(df):
	trees_list=[]
	to_change=df[df['incorporated']==0]
	# print(to_change)
	to_change=to_change[to_change['acceptance']==1]
	# print(to_change)
	cid=list(set(to_change['cluster_id']))
	new_stuff=[]
	replaced=[]
	repls=[]
	# print("ok",cid)
	for clus in cid:
		repl=to_change[(to_change['cluster_id']==clus)]
		# print(repl)
		repls.append(repl)
		if repl.size:
			replaced.append(repl[repl['is changed']=='Y'])
		newer=to_change[(to_change['cluster_id']==clus) & (to_change['is new']==1)]
		if newer.size:
			new_stuff.append(newer.iloc[[0]])
	for rep in range(len(replaced)):
		fb1=replaced[rep]
		pos1=df[(df['new position']==int(fb1.iloc[0]['new position']-1))]
		# pos2=replaced['new position'==str(int(fb2['new position'])-1)]
		# print(pos1,"ps1")
		if pos1.iloc[0]['new position']>=0:
			if pos1.iloc[0]['tree']==fb1.iloc[0]['tree']:
				update_tree_replace(cid[rep],pos1.iloc[0]['tree'],repls[rep],pos1.iloc[0]['new position'])



# if __name__ == '__main__':
df=pd.read_csv("/home/pranshu/Dropbox/GE/Prototype/feedback2.csv")
# print(df)
to_update(df)