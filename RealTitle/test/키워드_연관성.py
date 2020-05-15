import numpy as np
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

mpl.rcParams['axes.unicode_minus'] = False

path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_name = fm.FontProperties(fname=path, size=50).get_name()
print(font_name)
plt.rc('font', family=font_name)

print('# 설정되어있는 폰트 사이즈')
print(plt.rcParams['font.size'])
print('# 설정되어있는 폰트 글꼴')
print(plt.rcParams['font.family'])

df = pd.read_excel('C:/Users/admin/Desktop/fp_test (2)/data/sample.xlsx')

df.head()

lines = df['제목']
lines

from konlpy.tag import Hannanum
hannanum = Hannanum()

dataset = []
for line in lines:
    dataset.append(hannanum.nouns(re.sub('[^가-힣a-zA-Z\s]', '', line)))
dataset[:5]

# !pip install apyori

from apyori import apriori

result = (list(apriori(dataset, min_support=0.01)))
df2 = pd.DataFrame(result)
df2['length'] = df2['items'].apply(lambda x: len(x))
df2 = df2[(df2['length'] == 2) & (df2['support'] >= 0.01)].sort_values(by='support', ascending=False)
df2.head()

G = nx.Graph()
ar = (df2['items'])
G.add_edges_from(ar)

pr = nx.pagerank(G)
nsize = np.array([v for v in pr.values()])
nsize = 2000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))

pos = nx.random_layout(G)
#pos = nx.planar_layout(G)

plt.figure(figsize=(16, 12))
plt.axis('off')
nx.draw_networkx(G, 
                 pos=pos,
                 font_family=font_name,
                 font_size=16,
                 node_color=list(pr.values()), 
                 node_size=nsize, 
                 alpha=0.7,
                 edge_color='.5', 
                 cmap=plt.cm.YlGn)
plt.savefig('C:/Users/admin/Desktop/fp_test (2)/data/result.png', bbox_inches='tight')