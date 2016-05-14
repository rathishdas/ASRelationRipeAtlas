__author__ = 'RATHISH DAS and Sarthak Ghosh'
#!/usr/bin/env python

from copy import deepcopy
import sys

def dfs(i, order, visited, graph):
    if visited[i] == 0:
        visited[i] = 1
        s = successors(i, graph)
        for successor in s:
            order, visited = dfs(successor, order, visited, graph)
        order.append(i)
    return order, visited

def successors(i, graph):
    s = []
    for j in range(len(graph[i])):
        if graph[i][j] == 1:
            s.append(j)
    return s

def reverse(graph):
    reverse_graph = [[0 for j in range(len(graph[0]))] for i in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == 1:
                reverse_graph[j][i] = 1
    return reverse_graph

def twoSAT(new_paths, no_of_edges):
    graph = [[0 for j in range(2 * no_of_edges)] for i in range(2 * no_of_edges)]
    for path in new_paths:
        for i in range(len(path) - 1):
            if path[i] < no_of_edges and path[i + 1] >= no_of_edges:
                graph[path[i] + no_of_edges][path[i + 1] - no_of_edges] = 1
                graph[path[i + 1]][path[i]] = 1
            elif path[i] >= no_of_edges and path[i + 1] < no_of_edges:
                graph[path[i] - no_of_edges][path[i + 1] + no_of_edges] = 1
                graph[path[i + 1]][path[i]] = 1
            elif path[i] < no_of_edges and path[i + 1] < no_of_edges:
                graph[path[i] + no_of_edges][path[i + 1] + no_of_edges] = 1
                graph[path[i + 1]][path[i]] = 1
            elif path[i] >= no_of_edges and path[i + 1] >= no_of_edges:
                graph[path[i] - no_of_edges][path[i + 1] - no_of_edges] = 1
                graph[path[i + 1]][path[i]] = 1
    order = []
    visited = [0 for i in range(2 * no_of_edges)]
    for i in range(len(graph)):
        order, visited = dfs(i, order, visited, graph)
    reverse_graph = reverse(graph)
    order.reverse()
    visited = [0 for i in range(2 * no_of_edges)]
    sccs = []
    for i in order:
        scc, visited = dfs(i,[], visited, reverse_graph)
        if scc != []:
            sccs.append(scc)
    print(sccs)
    candidates = []
    for scc in sccs:
        for i in scc:
            if (i + no_of_edges) in scc or (i - no_of_edges) in scc:
                count = 0
                for path in new_paths:
                    if i in path or (i + no_of_edges) in path or (i - no_of_edges) in path:
                        count += 1
                candidates.append([count, i])
    if len(candidates) == 0:
        value = [-1 for i in range(no_of_edges)]
        order.reverse()
        for i in order:
            if i >= no_of_edges:
                if value[i - no_of_edges] == -1:
                    value[i - no_of_edges] = 0
            else:
                if value[i] == -1:
                    value[i] = 1
        return True, value, -1
    else:
        candidates.sort()
        if candidates[0][1] >= no_of_edges:
            candidate = candidates[0][1] - no_of_edges
        else:
            candidate = candidates[0][1]
        return False, [], candidate

#if __name__ == '__main__':
def getRelation(outFile):
    paths = []
    infile = "tmpASPath.txt"
    traceFile = outFile
    asnIDtoNameMap = dict()
    asnDict = open("asnDict.txt")
    for path in asnDict:
        pathSplit = path.split("$")
        asnIDtoNameMap[pathSplit[0]] = pathSplit[1]
    outFile = open(traceFile , 'w')
    #f = open('out.txt')
    f = open(infile)
    for path in f:
        path = path.replace('\n', '').split(' ')
        paths.append(path)
    f.close()
    satisfiable = False
    copy_paths = deepcopy(paths)
    while satisfiable == False:
        edges = []
        new_paths = []
        for path in copy_paths:
            for i in range(len(path) - 1):
                if [path[i], path[i + 1]] in edges or [path[i + 1], path[i]] in edges:
                    pass
                else:
                    edges.append([path[i], path[i + 1]])
        no_of_edges = len(edges)
        for path in copy_paths:
            new_path = []
            for i in range(len(path) - 1):
                for j in range(len(edges)):
                    if edges[j] == [path[i], path[i + 1]]:
                        new_path.append(j)
                    elif edges[j] == [path[i + 1], path[i]]:
                        new_path.append(j + no_of_edges)
            new_paths.append(new_path)
        satisfiable, value, candidate = twoSAT(new_paths, no_of_edges)
        if satisfiable == False:
            for path in copy_paths:
                flag = False
                for i in range(len(path) - 1):
                    if [path[i], path[i + 1]] == edges[candidate] or [path[i + 1], path[i]] == edges[candidate]:
                        flag = True
                        break
                if flag == True:
                    copy_paths.remove(path)
    for path in paths:
        if not path in copy_paths:
            cp = deepcopy(copy_paths)
            cp.append(path)
            edges = []
            new_paths = []
            for p in cp:
                for i in range(len(p) - 1):
                    if [p[i], p[i + 1]] in edges or [p[i + 1], p[i]] in edges:
                        pass
                    else:
                        edges.append([p[i], p[i + 1]])
            no_of_edges = len(edges)
            for p in cp:
                new_path = []
                for i in range(len(p) - 1):
                    for j in range(len(edges)):
                        if edges[j] == [p[i], p[i + 1]]:
                            new_path.append(j)
                        elif edges[j] == [p[i + 1], p[i]]:
                            new_path.append(j + no_of_edges)
                new_paths.append(new_path)
            satisfiable, value, candidate = twoSAT(new_paths, no_of_edges)
            if satisfiable == True:
                copy_paths = deepcopy(cp)
    for i in range(no_of_edges):
        print(edges[i], ':', value[i])
        #print(asnIDtoNameMapp[edges[i]], ':', asnIDtoNameMap[])
        #s = "( "+edges[i][0] + "--->" + edges[i][1] + " )   : "+ str(value[i]) + "\n"
        #if isinstance(edges[i][0],str) and isinstance(edges[i][0],str) :
        if edges[i][0] and edges[i][1]:
            s = asnIDtoNameMap[edges[i][0]].strip() + " ------> " + asnIDtoNameMap[edges[i][1]].strip() + "    : "+ str(value[i]) + "\n"
        outFile.write(s)

    outFile.close()
