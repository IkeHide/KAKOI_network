import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy

class mk_KAKOI_netowrk:
    def __init__(self, nodes, edges, pos):
        self.nodes = nodes
        self.edges = edges
        self.pos = pos

        self.network = nx.Graph()  # ネットワークの作成
        self.network.add_nodes_from(self.nodes)  # ネットワークにノードを追加
        self.network.add_edges_from(self.edges)  # ネットワークにエッジを追加
    
    # ネットワークの描画
    def output_network(self, network):
        plt.figure(figsize=(8,6))
        # nx.draw(G)でネットワークGを出力する。引数は右を参照：https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html
        nx.draw(network, self.pos, with_labels=True, node_color = "burlywood", node_size = 2000, width=5, font_size=20, font_weight="bold", font_family="Yu Gothic")
        plt.subplots_adjust(left=0.4, right=0.6, bottom=0.4, top=0.6)
        plt.show()


    # 以下はネットワークの特徴量の出力
    def output_average_shortest_path_length(self):  #（最大クラスタ）平均距離
        new_network = copy.deepcopy(self.network)  # 最大クラスタのネットワークの作成
        # 今回、部分ネットワークが2つ以上できる囲いはなかったので、次数が0のノードを除く という操作を行う。
        remove_nodes = [nodes for nodes in self.network if self.network.degree(nodes) == 0]
        new_network.remove_nodes_from(remove_nodes)
        print(nx.average_shortest_path_length(new_network))

    def output_average_degree(self):  # 平均次数を出力
        # networkxで直接出力する関数がないので自作する。
        # nx.degree(G)[node]でネットワークGにおけるあるnodeの次数を取得できるので、各ノードの次数をリストに格納し その平均を得る。
        print(np.average([nx.degree(self.network)[node] for node in self.nodes]))

    def output_average_clustering(self):  # 平均クラスタ係数
        print(nx.average_clustering(self.network))

    def get_density(self,edges,nodes):  # 密度を返す
        return 2*edges/(nodes*(nodes-1))

    def output_degree_density(self):  # 密度を出力
        E = self.network.number_of_edges()  # エッジ数を取得
        N = self.network.number_of_nodes()  # ノード数を取得
        degree_density = self.get_density(E, N)
        print(degree_density)

    def output_degree_assortativity_coefficient(self):  # 次数相関を出力
        print(nx.degree_assortativity_coefficient(self.network))
    
    def get_SMC(self, G):  # 最大クラスタのノード数を返す
        largest_cc = max(nx.connected_components(G), key=len)
        max_cluster = G.subgraph(largest_cc).copy()  # 最大クラスタのグラフ
        return len(max_cluster)  

    def output_robustness(self):  # 頑健性を出力
        import copy
        new_network = copy.deepcopy(self.network)         # ネットワークのコピー
        target_piece = '金'          # 狙われやすい駒の設定
        new_network.remove_node(target_piece)  # ノードの削除
        self.output_network(new_network)

        if nx.is_connected(new_network):
            G1_diam = nx.diameter(self.network)
            G2_diam = nx.diameter(new_network)
            print('直径の変化率：{}[%]'.format((G2_diam-G1_diam)/G1_diam*100))

        G1_SMC = self.get_SMC(self.network)
        G2_SMC = self.get_SMC(new_network)
        print('最大クラスタサイズの変化率：{}[%]'.format((G2_SMC-G1_SMC)/G1_SMC*100))

        G1_dens = self.get_density(self.network.number_of_edges(),self.network.number_of_nodes())
        G2_dens = self.get_density(new_network.number_of_edges(),new_network.number_of_nodes())
        print('密度の変化率：{}[%]'.format((G2_dens-G1_dens)/G1_dens*100))

        G1_average_degree = np.average([nx.degree(self.network)[node] for node in self.network.nodes])
        G2_average_degree = np.average([nx.degree(new_network)[node] for node in new_network.nodes])
        print('平均次数の変化率：{}[%]'.format((G2_average_degree-G1_average_degree)/G1_average_degree*100))

    

        
        

#   ９ ８ ７ ６ ５ ４ ３ ２ １
# +---------------------------+
# | ・ ・ ・ ・ ・ ・ ・ ・ ・|一
# | ・ ・ ・ ・ ・ ・ ・ ・ ・|二
# | ・ ・ ・ ・ ・ ・ ・ ・ ・|三
# | ・ ・ ・ ・ ・ ・ ・ ・ ・|四
# | ・ ・ ・ ・ ・ ・ ・ ・ ・|五
# | ・ ・ ・ ・ ・ ・ ・ ・ 歩|六
# | ・ ・ ・ ・ 歩 歩 歩 歩 ・|七
# | ・ ・ ・ ・ 金 ・ 銀 玉 ・|八
# | ・ ・ ・ ・ ・ 金 ・ 桂 香|九
# +---------------------------+
# 上の美濃囲いの例を参考に、ノード（駒の種類）、エッジ（駒の利き）、ポジション（駒の位置）を入力する
mino_kakoi = mk_KAKOI_netowrk(['歩', '歩2', '歩3', '歩4', '歩5', '金', '銀', '玉', '金2', '桂', '香'],
                              [('香', '歩'), ('金', '歩2'), ('金', '歩3'), ('銀', '歩3'), ('銀', '歩4'), ('玉', '歩4'), 
                               ('桂', '歩4'), ('銀', '歩5'), ('玉', '歩5'), ('金2', '金'), ('玉', '銀'), ('金2', '銀'), 
                               ('銀', '金2'), ('銀', '桂'), ('玉', '桂'), ('玉', '香')],
                               {'歩': (9, 4), '歩2': (5, 3), '歩3': (6, 3), '歩4': (7, 3), '歩5': (8, 3), '金': (5, 2),
                                '銀': (7, 2), '玉': (8, 2), '金2': (6, 1), '桂': (8, 1), '香': (9, 1)}
                              )
mino_kakoi.output_network(mino_kakoi.network)
mino_kakoi.output_degree_density()
mino_kakoi.output_average_clustering()
mino_kakoi.output_robustness()
