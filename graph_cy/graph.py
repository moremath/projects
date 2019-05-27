class Graph:
    nodes =dict()
    def addNode(self,nodeName):
        if nodeName not in Graph.nodes:
            Graph.nodes[nodeName] = dict()

    def addLink(self,startNodeName,endNodeName,relationshipDict=dict()):
        self.addNode(startNodeName)
        self.addNode(endNodeName)
        _relationshipDict = Graph.nodes[startNodeName].get(endNodeName,dict())
        # todo
        # relationshipDict.update(_relationshipDict)
        for k in _relationshipDict:
            if k in relationshipDict:
                if '__add__' in dir(relationshipDict[k]):
                    relationshipDict[k] += _relationshipDict[k]
                elif isinstance(relationshipDict[k],set):
                    relationshipDict[k] |= _relationshipDict[k]
        Graph.nodes[startNodeName][endNodeName] = relationshipDict
        if startNodeName not in Graph.nodes[endNodeName]:
            Graph.nodes[endNodeName][startNodeName]=dict()

    def __getitem__(self, item):
        return Graph.nodes.get(item)

    def __repr__(self):
        linksNum=sum([
            len(Graph.nodes[nodeName])
            for nodeName in Graph.nodes
        ])//2
        nodesNum = len(Graph.nodes)
        return (nodesNum,linksNum)
        # return "{} nodes and {} bilateral links on this Graph".format(nodesNum,linksNum)

    def shortestPath(self,nodeName1,nodeName2):
        searched = { nodeName1,}
        resultPath=list()
        paths = [ [nodeName1],]
        flag = True
        while flag:
            newPaths =[]
            for path in paths:
                lastNodeName = path[-1]
                print([k for k in Graph.nodes])
                nextNodeNames = [
                    e
                    for e in Graph.nodes[lastNodeName]
                    if e not in searched
                ]
                # print('path',path,'nextNodeNames',nextNodeNames)
                _searched= set()
                for nodeName in nextNodeNames:
                    nextPath = path+[ nodeName ]
                    if nodeName == nodeName2:
                        resultPath.append(nextPath)
                        flag = False
                    else:
                        _searched.add(nodeName)
                    newPaths.append(nextPath)
                    # print('nextPath',nextPath)
                    # _searched.add(nodeName)
                searched.update(_searched)
                # print('searched',searched)
            paths = newPaths
            if len(paths) == 0:
                flag= False
        return resultPath


def sum_user_property(_dict,user,key):
    vals = []
    for k in _dict[user]:
        v = _dict[user][k]
        # if key not in v:
        #     return
        # print('=====v',v)
        vals.append(v[key])
    val_0 = vals[0]
    for val in vals[1:]:
        if '__add__' in dir(val_0):
            val_0 +=val
        elif isinstance(val_0,set):
            val_0 |= val
    return val_0


def test():
    g=Graph()
    g.addNode('a')
    g.addNode('d')
    g.addNode('b')
    g.addNode('c')
    g.addLink('a','b')
    g.addLink('b','c')
    g.addLink('a','e')
    g.addLink('e','c')
    # print(g)
    print(g.shortestPath('a','c'))
# test()