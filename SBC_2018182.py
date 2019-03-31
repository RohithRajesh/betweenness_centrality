#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "Rohith Rajesh"
    email = "rohith18182@iiitd.ac.in"
    roll_num = "2018182"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        self.validate()

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

   
    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''


        dicto={}
        i=1
        dicto[0]=[]
        dicto[0].append(start_node)
        while i<=len(self.vertices)-1:
            for x in dicto[i-1]:
                for h in self.vertices:
                    if h !=start_node :
                        if ((h,x) in self.edges) or ((x,h) in self.edges):
                            if i in dicto.keys():
                                if not(h in dicto[i]):
                                    dicto[i].append(h)
                            else:
                                dicto[i]=[h]
            i+=1
        for x in dicto.values():
            if end_node in x:
                return list(dicto.values()).index(x)
    def min_dist_1(self, start_node, end_node):
        #prepared for use in other function
        dicto={}
        i=1
        dicto[0]=[]
        dicto[0].append(start_node)
        while i<=len(self.vertices)-1:
            for x in dicto[i-1]:
                for h in self.vertices:
                    if h !=start_node :
                        if ((h,x) in self.edges) or ((x,h) in self.edges):
                            if i in dicto.keys():
                                if not(h in dicto[i]):
                                    dicto[i].append(h)
                            else:
                                dicto[i]=[h]
            i+=1
        for x in dicto.values():
            if end_node in x:
                return list(dicto.values()).index(x),dicto

    def all_shortest_paths(self,start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        return self.all_paths(start_node,end_node,self.min_dist(start_node,end_node),[])
        

    
    def all_paths(self,node, destination, dist, path):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """



        x,y=self.min_dist_1(node,destination)

        temp=[]
        backup=[]
        i=0
        for g in y[1]:
            temp.append([node])
            temp[i].append(g)
            i+=1
        for k in temp:
            if destination in k:
                path.append(temp[temp.index(k)])
                temp.pop(temp.index(k))
        w=1
        backup=temp
        while w< len(self.vertices):
            
            for s in temp:
                for q in y[w]:
                    
                    if ((s[-1],q) in self.edges) or ((q,s[-1]) in self.edges):
                        if not(q in s) and not([s+[q]] in backup):
                            backup.extend([s+[q]])
            for k in temp:
                if k[-1]==destination:
                    path.append(temp[temp.index(k)])
                    temp.pop(temp.index(k))
            temp=backup
            w+=1
        final_path=[]
        for i in path:
            if not(i in final_path):
                final_path.append(i)
        mega_path=[]
        for i in final_path:
            flag=0
            for x in i:
                if i.count(x)!=1:
                    flag=1
            if (flag==0) and(len(i)==dist+1):
                mega_path.append(i)
        
        return mega_path

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """




        sums=0
        for x in self.vertices:
            for y in self.vertices:
                if (x!=y) and x!=node and y!=node:
                    k=len(self.all_shortest_paths(x,y))
                    g=0
                    for d in self.all_shortest_paths(x,y):
                        if node in d:
                            g+=1
                    sums=sums+(g/k)

        return sums/2

    def standardised_centrality(self,node):
        '''returns the standardised betweenness centrality for a node.'''


        return (self.betweenness_centrality(node)*2)/((len(self.vertices)-1)*(len(self.vertices)-2))

    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """



        pre={}
        for x in self.vertices:
            pre[x]=self.betweenness_centrality(x)
        m=max(list(pre.values()))
        felina=[]
        for y in pre.keys():
            if pre[y]==m:
                felina.append(y)
        return felina



if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6),(3,6)]
    graph = Graph(vertices, edges)