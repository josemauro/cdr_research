from igraph import Graph

g_mutual = Graph().Read_Ncol('../networks/g_mutual.gml')
communities_multilevel = g_mutual.community_multilevel(return_levels=False)

