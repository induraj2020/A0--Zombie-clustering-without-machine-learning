import unittest
from ast import literal_eval
import matplotlib.pyplot as plt
import networkx as nx

"""
    Algorithm using networkx library to cluster the zombies and non Zombies
"""
def clustering_using_library(z,matrix,plt_size):
    conn_list=[]                                                #list of connected elements
    N = len(matrix)
    G=nx.Graph()                                                # initializing graph
    result = [(i, j) for i in range(N) for j in range(N)]
    for i,j in result:
        if(matrix[i][j]==1):
            conn_list.append((i,j))
    G.add_edges_from(conn_list)                                 # Building Graph

    plt.figure(z)
    nx.draw_networkx(G)
    cluster_list=list(nx.connected_components(G))
    plt.title("example={} \n cluster_number={}".format(z+1,len(cluster_list)))

    return(len(cluster_list))


"""
    own algorithm
"""
def zombieCluster(matrix):
    i_list=[]
    N= len(matrix)
    result = [(i,j) for i in range(N) for j in range(N) if(j>i)]

    """ Function connection finder basically finds the connection between any zombies"""
    def connection_finder(result):
        for i,j in result:
            if(matrix[i][j]==1):
                i_list.append([i,j])
        u_set=set([item for sublist in i_list for item in sublist])
        g_list= [item for sublist in i_list for item in sublist]
        return  (u_set,g_list)

    """ Function Path Builder buids the Connection between zombies as tuples"""
    def path_builder(u_set,g_list):
        d_dict={}
        for element in u_set:
            d_dict[element]=set()
            for i,x in enumerate(g_list):
                if((x==element)):
                    if(i%2==0):
                        if(x not in d_dict[element]):
                            d_dict[element].add(x)
                        if(g_list[i+1] not in d_dict[element]):
                            d_dict[element].add(g_list[i+1])
                    else:
                        d_dict[element].add(x)
                        d_dict[element].add(g_list[i-1])
        return d_dict
    """ Function cluster finder finds the clusters of zombies and Non Zomies """
    def cluster_finder(d_dict):
        k_vist = []
        key_list = [element for element in d_dict.keys()]
        for key in list(d_dict):
            if (key in list(d_dict) and (key not in k_vist)):
                for j in key_list:
                    if j!=key_list[0] and j in d_dict and j not in k_vist and key in d_dict and j!=key and (d_dict[key].isdisjoint(d_dict[j]) == False) :
                        d_dict[key] = (d_dict[key].union(d_dict[j]))
                        del [d_dict[j]]
                        k_vist.append(j)
        return d_dict


    u_set,g_list =connection_finder(result)                            # calling the functions
    d_dict= path_builder(u_set,g_list)
    d_dict=cluster_finder(d_dict)
    d_dict=cluster_finder(d_dict)
    clus1_numb= len(d_dict)
    lis=[]
    for elem in d_dict.values():
        lis.extend(list(elem))
    final_cluster= len(set(range(N))-set(lis))+clus1_numb           # calculating the final cluster
    return final_cluster


class test_problem(unittest.TestCase):
    """
    Class to test the values provided by zombieCluster if an integration is done
    """
    def setUp(self):
        self.matrices = []
        self.values = []
        with open('problem1_test.txt', 'r') as file:
            line = file.readline()
            while (line):
                if ('example' in line):
                    temp = ''
                elif ('[' in line):
                    temp += line
                elif ('result' in line):
                    self.matrices.append(literal_eval(temp))
                    self.values.append(int(line.split(' = ')[1]))
                line = file.readline()
        self.n_tests = len(self.values)
        assert self.n_tests==len(self.matrices), "problem reading file, check it has not been modified or corrupted"

    def test_zombieCluster(self):
        msg = 'wrong value computed. zombieCluster returned {} when expected {}'
        found_cluster1 = []  # list of clusters found by my own algorithm
        found_cluster2 = []  # list of clusters found by using library
        for i in range(self.n_tests):

            computed_res = zombieCluster(self.matrices[i])
            computed_res = zombieCluster(self.matrices[i])  # calling custom clustering code
            found_cluster1.append(computed_res)
            computed_res1 = clustering_using_library(i, self.matrices[i], self.n_tests)
            found_cluster2.append(computed_res1)

            with(self.subTest(i=i)):
                self.assertEqual(computed_res, self.values[i], msg.format(computed_res, self.values[i]))
        print("Actual Cluster = \t\t\t\t\t\t\t {} ".format(self.values))
        print("Own Algorithm Cluster=\t\t\t\t\t\t {} ".format(found_cluster1))
        print("Clustering by library networkx =\t\t\t {} ".format(found_cluster2))
        plt.show()
if __name__ == '__main__':
    unittest.main()
    plt.show()