import os
os.putenv("NLS_LANG", "KOREAN_KOREA.KO16KSC5601")
import cx_Oracle
import pandas as pd
import numpy as np
import matplotlib.font_manager as fm
#%matplotlib inline
import matplotlib.pyplot as plt


conn = cx_Oracle.connect('team/1234@192.168.0.52:32764/xe', encoding='utf-8')

df = pd.read_sql('SELECT article_id, article_category, article_media, result.result_acc FROM article_article article, article_result result WHERE result.result_id = article.article_id', conn)

df.head()
df.describe()
df.ARTICLE_CATEGORY.unique()
df.ARTICLE_MEDIA.unique()
len(df)

grouped = df['RESULT_ACC'].groupby(df['ARTICLE_CATEGORY'])
grouped
grouped.size()
grouped.sum()
grouped.mean()
grouped2 = df['RESULT_ACC'].groupby(df['ARTICLE_MEDIA'])
grouped2
print(grouped2.mean())

#폰트
path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_name = fm.FontProperties(fname=path, size=50).get_name()
#print(font_name)
plt.rc('font', family=font_name)

fig = plt.figure(figsize=(20,20))
plt.bar(grouped2.mean().index,grouped2.mean().values)
plt.xticks(rotation=80)
plt.show()
#plt.savefig('C:/Users/admin/Documents/IMG01.png', bbox_inches='tight')


df['RESULT_ACC']
group_df1 = df.groupby(['ARTICLE_MEDIA','ARTICLE_CATEGORY']).mean()
group_df1
print(group_df1.loc['프레시안'])