#판다스, 표
from pandas import DataFrame
from datetime import datetime
import numpy as np


#시각화
import matplotlib as mpl
import seaborn as sns; sns.set(style='darkgrid', font='malgun', font_scale=1.5)
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

#표
import pandas as pd
import csv

#폰트 
# %config InlineBackend.figure_format = 'retina'
 
# !apt -qq -y install fonts-nanum
 
import matplotlib.font_manager as fm
# fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
# font = fm.FontProperties(fname=fontpath, size=9)
# plt.rc('font', family='NanumBarunGothic') 
# mpl.font_manager._rebuild()

# 창희 폰트
# path = 'C:\\Windows\\Fonts\\malgun.ttf'
# font_name = fm.FontProperties(fname=path, size=50).get_name()
# print(font_name)
# plt.rc('font', family=font_name)

# print('# 설정되어있는 폰트 사이즈')
# print(plt.rcParams['font.size'])
# print('# 설정되어있는 폰트 글꼴')
# print(plt.rcParams['font.family'])

#뉴스 파일가져오기
df = pd.read_excel('C:\\Users\\admin\\Downloads\\NewsResult.xlsx')

#timestamp 추가
df['timestamp'] = pd.to_datetime(df["일자"],format='%Y%m%d', errors='ignore')
df['timestamp']


#timestamp 3개로 나누기
df['year'] = df["timestamp"].dt.year
df['month'] = df["timestamp"].dt.month
df['day'] = df["timestamp"].dt.day


#날짜 > int로 바꾸기
df['year'] = df['year'].astype(int)
df['month'] = df['month'].astype(int)
df['day'] = df['day'].astype(int)

#작은 테이블 만들기

new_df = df[['본문','키워드','year', 'day', 'month']]


new1 = new_df[new_df['본문'].str.match('총선') | new_df['키워드'].str.match('매일신문') ]
df_date = new1[(df["month"] >= 3) & (df["month"] <= 4) & (df["day"] >= 1)& (df["day"] <= 30)]


# **가 언급된 날짜별 기사건수 

graph = df_date.groupby(df_date["day"]).count()

x = graph.index
y = graph['본문']

f, ax = plt.subplots(figsize=(16,8)); plt.xticks(x, rotation=0)


ax = f.add_subplot(1,1,1) # Get the figure and the axes

ax.set(title='날짜별 기사건수', xlabel='날짜별', ylabel='기사량')

ax.errorbar(x, y, fmt = "ro-" ,capsize=2 ) 

plot = ax.bar(x, y)

for rect in plot:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height, '%d' %int(height), ha='center', va='bottom')
    plt.savefig('C:/Users/admin/Documents/IMG02.png', bbox_inches='tight')
print(plot)

######################################################################
def graph(query):
    
    %matplotlib notebook
    import matplotlib.pyplot as plt
    import numpy
    from numpy import sin
    from numpy import cos
    import pandas as pd
    import cx_Oracle as oci
    from datetime import datetime
    
    #DB Connecion    
    conn = oci.connect("test/1234@192.168.0.52:32764/xe", charset='utf8')
    cursor.execute("selet count(*) from article")
    
    #timestamp 추가
    df['timestamp'] = pd.to_datetime(df["일자"],format='%Y%m%d', errors='ignore')
    df['timestamp']

    #timestamp 3개로 나누기
    df['year'] = df["timestamp"].dt.year
    df['month'] = df["timestamp"].dt.month
    df['day'] = df["timestamp"].dt.day

    #날짜 str로 바꾸기 왠지몰라
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['day'] = df['day'].astype(int)

    #DB Connecion 해서 가져오기
    keyword = SELECT * FROM article WHERE article_content LIKE "%이명박%" 
    period = SELECT * FROM article WHERE month < %s% AND month > %% ORDER BY DATE;
    SELECT hire_date, article_date, EXTRACT(YEAR FROM (SYSDATE-hire_date) YEAR TO MONTH) "Years" 
  2  FROM employees WHERE ROWNUM <= 5;
    SELECT article_date FROM v$nls_parameters WHERE REGEXP_LIKE(parameter, 'NLS_(DATE|TIME).*');
    
    
    for row in cursor:
        total = row[0]
    t=np.arrange(total)
    cursor.execute("select article_content, article_date from article")
    keyword = []
    period = []
    
    for row in cursor:
        keyword.append(row[0])
        period.append(row[1])
    bar_with = 0.3
    try:
        with conn.cursor() as curs:
            #디비에서 article_sample 가져오기
            sql = "'select * from article_sample'"
            #화면에 출력
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                print(row)
    finally:
        conn.close()

        

        