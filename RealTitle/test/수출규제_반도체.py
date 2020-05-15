import pandas as pd
import seaborn as sns; sns.set(style='darkgrid', font='malgun', font_scale=1.5)
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

#폰트
path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_name = fm.FontProperties(fname=path, size=50).get_name()
print(font_name)
plt.rc('font', family=font_name)

# 수출규제 기사건수 
df = pd.read_excel('C:/Users/admin/Documents/export.xlsx', sheet_name='sheet', index_col='일자', parse_dates=True)
df1 = df.groupby(df.index.month).size()
f, ax = plt.subplots(figsize=(16,8)); plt.xticks(df1.index, rotation=90)
plot = ax.bar(df1.index, df1.values)
for rect in plot:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height, '%d' %int(height), ha='center', va='bottom')
    plt.savefig('C:/Users/admin/Documents/IMG01.png', bbox_inches='tight')


# 반도체가 언급된 깃대종 기사건수 
df2 = df[df['제목'].str.contains('반도체')| df['본문'].str.contains('반도체')]
df2 = df2.groupby(df2.index.month).size()
f, ax = plt.subplots(figsize=(16,8)); plt.xticks(df1.index, rotation=90)
plot = ax.bar(df2.index, df2.values)
for rect in plot:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height, '%d' %int(height), ha='center', va='bottom')
    plt.savefig('C:/Users/admin/Documents/IMG02.png', bbox_inches='tight')


# 수출규제 기사건수, 반도체가 언급된 수출규제 기사건수
pd.concat([df1, df2], axis=1).plot(kind='line',figsize=(16,8))
plt.legend(['수출규제 기사건수','반도체가 언급된 수출규제 기사건수'])
plt.savefig('C:/Users/admin/Documents/IMG03.png', bbox_inches='tight')

print('수출규제 기사 ' + str(df1.sum()) + '건 중 반도체가 언급된 수출규제 기사는 '
     + str(df2.sum()) + '건: ' + str(format(df2.sum()/ df1.sum()*100, ".1f")) +'%차지')


# 형태소 분석: 한나눔 불러오기 
from konlpy.tag import Hannanum
hannanum = Hannanum()

#기사 제목만 따로 저장한 뒤, 불러오기
df[['제목']].to_csv('C:/Users/admin/Documents/export1.txt', index=False, header=False)
f = open('C:/Users/admin/Documents/export1.txt', 'r', encoding='UTF-8')
lines = f.readlines()
f.close()

# 단어 빈도 분석 
word = []
for I in range(len(lines)):
    word.append(hannanum.nouns(lines[I]))

def flatten(I):
    flatList = []
    for elem in I:
        if type(elem) == list:
            for e in elem:
                flatList.append(e)
        else:
            flatList.append(elem)
    return flatList

word_list = flatten(word)
word_list = pd.Series([x for x in word_list if len(x)>1])
word_list.value_counts().head(20)

# 단어구름
from wordcloud import WordCloud
from collections import Counter

font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
wordcloud = WordCloud(font_path=font_path, width=800, height=800, background_color='white')

count = Counter(word_list)
wordcloud = wordcloud.generate_from_frequencies(count)
array = wordcloud.to_array()

fig = plt.figure(figsize=(10,10))
plt.imshow(array, interpolation='bilinear')
plt.axis("off")
plt.savefig('C:/Users/admin/Documents/IMG04.png', bbox_inches='tight')


#연습중