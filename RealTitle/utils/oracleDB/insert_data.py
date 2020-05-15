from sqlalchemy import create_engine
import cx_Oracle
import pandas as pd
import logging
from tqdm import tqdm 

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

def insertData():
    conn = create_engine('oracle://team:1234@192.168.0.52:32764/xe?encoding=utf-8')
    # conn = cx_Oracle.connect("team/1234@192.168.0.52:32764/xe")

    df = pd.read_sql('select article_id from article_article group by article_id', conn)

    df.columns = ['article_id']
    df['check'] = 1

    file_name = 'total_article_ver1_20200427'
    df2 = pd.read_csv('RealTitle/data/' + file_name + '.csv')

    df_merge = pd.merge(df, df2, how='outer')

    df_result = df_merge[df_merge['check'].isna()]
    df_result.drop('check', axis=1, inplace=True)

    print(df_result.head())
    print(df_result.columns)
    print(df_result.shape)

    print('insert start..')
    df_result.to_sql('article_article', conn, if_exists='append', index=False)
    print('insert complete..')

    # df1 = df[['article_id', 'article_url', 'article_category', 'article_media', 'article_date', 'article_title', 'article_content']]
    # rows = [tuple(x) for x in df1.to_records(index=False)]

    # for line in rows:
        # print(line)
        # article_id = line[0]
        # article_url = line[1]
        # article_category = line[2]
        # article_media = line[3]
        # article_date = line[4]
        # article_title = line[5]
        # article_content = line[6]

        # con = conn.cursor()

        # con.excutemany('insert into article_article values(:1,:2,:3,:4,:5,:6,:7)', rows)
        # con.commit()

        # print(article_id, 'insert complete')

insertData()