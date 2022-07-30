class dfs():
    def depthFirstPrint(self, graph, source):
        stack=[]
        stack.append(source)
        while (len(stack)>0):
            cur=stack.pop()
            print(cur,"\n")
            for i in graph[cur]:
                stack.append(i)

    def dfsrecursion(self, graph, source):
        print(source)
        for neighbor in graph[source]:
            self.dfsrecursion(graph, neighbor)

    def sourcedestination(self, graph, source, destination):
        if source==destination:
            return True
        for neigh in graph[source]:
            if self.sourcedestination(graph, neigh, destination)==True:
                return True
        return False



class bfs():
    def breadthFirstPrint(self, graph, source):
        queue=[]
        queue.append(source)
        while (len(queue)>0):
            cur=queue.pop(0)
            print(cur,"\n")
            for i in graph[cur]:
                queue.append(i)

    def sourcedestination(self, graph, source, destination):
        if source==destination:
            return True
        queue=[]
        queue.append(source)
        while (len(queue)>0):
            cur=queue.pop(0)
            if cur==destination:
                return True
            for i in graph[cur]:
                queue.append(i)
        return False   

        

    

graph={
    'a':['b','c'],
    'b':['d'],
    'c':['e'],
    'd':['f'],
    'e':[],
    'f':[]
}
#obj=bfs()
# obj.breadthFirstPrint(graph,'a')
obj=bfs()
print(obj.sourcedestination(graph, 'a', 'f'))





