def undirected(edges, nodeA, nodeB):
    graph=buildgraph(edges)
    return (haspath(graph, nodeA, nodeB, visited=[]))
    
def haspath(graph, nodeA, nodeB, visited):
    if nodeA==nodeB:
        return True
    visited.append(nodeA)
    for neigh in graph[nodeA]:
        if neigh not in visited: 
            if haspath(graph, neigh, nodeB, visited):
                return True
    return False
    
def buildgraph(edges):
    graph={}
    for edge in edges:
        a,b= edge
        if a not in graph:
            graph[a]=[]
        if b not in graph:
            graph[b]=[]
        graph[a].append(b)
        graph[b].append(a)
    return graph
        

edges=[
    ['i','j'],
    ['k','i'],
    ['m','k'],
    ['k','l'],
    ['o','n']
]
print(undirected(edges, 'j', 'k'))


