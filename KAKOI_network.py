import python_shogi_master.shogi as psm
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class mk_KAKOI_netowrk:
    def __init__(self, nodes, edges, pos):
        self.nodes = nodes
        self.edges = edges
        self.pos = pos

        self.network = nx.Graph()  # ネットワークの作成
        self.network.add_nodes_from(self.nodes)  # ネットワークにノードを追加
        self.network.add_edges_from(self.edges)  # ネットワークにエッジを追加
    
    # ネットワークの描画
    def output_network(self):
        plt.figure(figsize=(8,6))
        nx.draw(self.network, self.pos, with_labels=True, node_color = "burlywood", node_size = 2000, width=5, font_size=20, font_weight="bold", font_family="Yu Gothic")
        # plt.savefig("output.eps")
        plt.subplots_adjust(left=0.4, right=0.6, bottom=0.4, top=0.6)
        plt.show()


    # 以下はネットワークの特徴量の出力
    def output_average_shortest_path_length(self):  #（最大クラスター）平均距離
        new_network = self.network  # 最大クラスターのネットワークの作成
        remove_nodes = [nodes for nodes in self.network if self.network.degree(nodes) == 0]
        new_network.remove_nodes_from(remove_nodes)
        print(nx.average_shortest_path_length(new_network))

    def output_average_degree(self):  # 平均次数
        # networkxで直接出力する関数がないので自作する。
        # nx.degree(G)[node]でネットワークGにおけるあるnodeの次数を取得できるので、各ノードの次数をリストに格納し その平均を得る。
        print(np.average(nx.degree(self.network)[node] for node in self.nodes))

    def output_average_clustering(self):  # 平均クラスタ係数
        print(nx.average_clustering(self.network))

    def output_degree_density(self):  # 次数密度
        E = self.network.number_of_edges()  # エッジ数を取得
        N = self.network.number_of_nodes()  # ノード数を取得
        degree_density = 2*E/(N*(N-1))
        print(degree_density)

    def output_degree_assortativity_coefficient(self):
        print(nx.degree_assortativity_coefficient(self.network))
        
        
        
mino_kakoi = mk_KAKOI_netowrk(['歩', '歩2', '歩3', '歩4', '歩5', '金', '銀', '王', '金2', '桂', '香'],
                              [('香', '歩'), ('金', '歩2'), ('金', '歩3'), ('銀', '歩3'), ('銀', '歩4'), ('王', '歩4'), 
                               ('桂', '歩4'), ('銀', '歩5'), ('王', '歩5'), ('金2', '金'), ('王', '銀'), ('金2', '銀'), 
                               ('銀', '金2'), ('銀', '桂'), ('王', '桂'), ('王', '香')],
                               {'歩': (9, 4), '歩2': (5, 3), '歩3': (6, 3), '歩4': (7, 3), '歩5': (8, 3), '金': (5, 2),
                                '銀': (7, 2), '王': (8, 2), '金2': (6, 1), '桂': (8, 1), '香': (9, 1)}
                              )
mino_kakoi.output_network()
mino_kakoi.output_degree_density()
mino_kakoi.output_average_clustering()
