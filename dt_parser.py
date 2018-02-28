class decisionnode:
	def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
		self.col=col
		self.value=value
		self.results=results
		self.tb=tb
		self.fb=fb
		self.cb=None

# def ident_level(l,levels=1):
#     return int((len(l)-len(l.strip()))/levels)

def get_start_node(line):
	start=0
	tf=line.strip().split(':',1)
	# print(line,"ok",tf)
	i_s=tf[1].split('?')
	if i_s[1]=='>':
		start=decisionnode(col=int(tf[0].strip()),value=int(i_s[0].strip()))
	else:
		start=decisionnode(col=int(tf[0].strip()),value=i_s[0])
	return (start,None)

def get_node(line2):
	is_further=line2.split('>',1)
	# print(line2,is_further,"po")
	start=0
	if is_further[1][0]=="{":
		result=eval(is_further[1])
		start=decisionnode(results=result)
	else:
		line=is_further[1]
		start=get_start_node(line)[0]
	return (start,is_further[0][0])

def parse_tree(treefile):
	# treefile=open(treefilename,"r")
	treefile.seek(0)
	start=0
	levels=[]
	for line in treefile:
		# print(line)
		line=line.strip()
		if not line:
			continue
		if not levels:
			levels.append(get_start_node(line))
		else:
			node_prop=get_node(line.strip())
			if node_prop[1]=='T':
				if not levels[-1][0].tb:
					levels[-1][0].tb=node_prop[0]
				else:
					print("This already has a true value,",printnode(levels[-1][0].tb)," went wrong, tried to replace",printnode(node_prop[0]))
					exit(-3)
			elif node_prop[1]=='F':
				if not levels[-1][0].fb:
					levels[-1][0].fb=node_prop[0]
				else:
					print("This already has a false value,",printnode(levels[-1][0].fb)," went wrong, tried to replace",printnode(node_prop[0]))
					exit(-3)
			else:
				print(printnode(node_prop[0]))
				print("Invalid Truth/False value, denote with 'T'/'F' only")
				exit(-1)
			if not node_prop[0].results:
				levels.insert(len(levels),node_prop)
			if node_prop[1]=='F' and node_prop[0].results:
				# print(levels)
				while levels and levels[-1][1] and levels[-1][0].fb:
					# print("popping",printnode(levels[-1][0]),levels[-1][1])
					levels.pop()
					# print(levels[-1])
				# print(levels)
				if not levels:
					print(levels)
					print("Invalid Format, Always put the true branch before False branch only")
					exit(-2)
				elif not levels[-1][1] and levels[-1][0].fb:
					return levels[0][0]
	return levels[0][0]

def printnode(tree):
	if tree.results!=None:
		return str(tree.results)
	else:
		if isinstance(tree.value,int) or isinstance(tree.value,float):
			return str(tree.col)+':'+str(tree.value)+'?> '
		else:
			return str(tree.col)+':'+str(tree.value)+'?= '


def printtree(tree,begindent='\t',endindent='\t'):
	# Is this a leaf node?
	if not tree:
		print("Something was replaced")
		exit(-4)
	if tree.results!=None:
		print(str(tree.results))
	else:
		if isinstance(tree.value,int) or isinstance(tree.value,float):
			print(str(tree.col)+':'+str(tree.value)+'?> ')
		else:
			print(str(tree.col)+':'+str(tree.value)+'?= ')
		print(begindent+'T->',end="")
		printtree(tree.tb,begindent+endindent,endindent)
		print(begindent+'F->', end="")
		printtree(tree.fb,begindent+endindent,endindent)

def classify(observation,tree):
	if tree.results!=None:
		return tree.results
	else:
		v=observation[tree.col]
		branch=None
	if isinstance(v,int) or isinstance(v,float):
		if v>=tree.value: branch=tree.tb
		else: branch=tree.fb
	else:
		if v==tree.value: branch=tree.tb
		else: branch=tree.fb
	return classify(observation,branch)
	

if __name__ == '__main__':
	test_dt=open("/home/yash/Dropbox/GE/Metadata/gd.txt")
	tree=parse_tree(test_dt)
	printtree(tree)
