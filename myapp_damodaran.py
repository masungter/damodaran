import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rc('font', family='Gulim') # 한글폰트 선택

conn = sqlite3.connect('KRX_FS_lite.sqlite3')
curs = conn.cursor()
df_krx = pd.read_sql(f"SELECT * FROM 'df_krx'", conn, index_col = 'Symbol')
final_company_df = pd.read_sql(f"SELECT * FROM 'final_company_df'", conn, index_col = "symbol")



### 변수 선언
input_PER = -1
input_PBR = -1
input_ROE = -1
input_DEBT = -1
input_DIVIDEND = -1
input_DIVIDEND_ratio = -1
input_EPS_growth = -1
input_EPS_stable = -1
input_PEG = -1
input_BETA = -1
input_SALES_growth = -1
input_PER_KOSPI = -1
input_EPS_KOSPI = -1
input_PER_SECTOR = -1
input_EPS_SECTOR = -1



### 함수 ###
def screen(input_per=-1, input_pbr=-1, input_roe=-1, input_debt=-1, input_beta=-1,
           input_dividen=-1, input_dividen_ratio=-1, input_eps_ratio=-1,
           input_eps_stable=-1, input_per_sector=False, input_peg=-1,
           input_esp_sector=False, input_sales=-1):

    company_df_temp = final_company_df

    if input_per >= 0:
        company_df_temp = company_df_temp[(company_df_temp['PER'] < input_per)&(company_df_temp['PER']>0)]
    if input_pbr >= 0:
        company_df_temp = company_df_temp[company_df_temp['PBR'] < input_pbr]
    if input_roe >= 0:
        company_df_temp = company_df_temp[company_df_temp['ROE'] > input_roe]
    if input_debt >= 0:
        company_df_temp = company_df_temp[company_df_temp['부채비율'] < input_debt]
    if input_beta >= 0:
        company_df_temp = company_df_temp[company_df_temp['beta'] < input_beta]
    if input_dividen >= 0:
        company_df_temp = company_df_temp[company_df_temp['배당수익률'] > input_dividen]
    if input_dividen_ratio >= 0:
        company_df_temp = company_df_temp[company_df_temp['배당성향'] < input_dividen_ratio]
    if input_eps_ratio >= 0:
        company_df_temp = company_df_temp[company_df_temp['EPS성장률'] > input_eps_ratio]
    if input_eps_stable == 1:
        company_df_temp = company_df_temp[company_df_temp['EPS안정성'] == 1]
    if input_per_sector:
        company_df_temp = company_df_temp[company_df_temp['PER'] < company_df_temp['PER_KOSPI']]
        company_df_temp = company_df_temp[company_df_temp['PER'] < company_df_temp['per_sector']]
    if input_peg >= 0:
        company_df_temp = company_df_temp[(company_df_temp['PEG'] < input_peg) & (company_df_temp['PEG'] > 0)]
    if input_esp_sector:
        company_df_temp = company_df_temp[company_df_temp['EPS성장률'] > company_df_temp['EPS_KOSPI']]
        company_df_temp = company_df_temp[company_df_temp['EPS성장률'] > company_df_temp['eps_sector']]
    if input_sales >= 0:
        company_df_temp = company_df_temp[company_df_temp['매출성장률'] > input_sales]

    company_df_screened = company_df_temp

    return company_df_screened

def screen_graph(names):
    # data_optimation
    for name in names:
        x = screen_df[name].values
        x_upper_lim = np.percentile(x,[90])[0]
        x_lower_lim = np.percentile(x,[10])[0]
        a = x[(x<x_upper_lim )& (x>x_lower_lim)]

        # graph
        fig = plt.figure(figsize=(12, 2))
        plt.hist(a, bins=8, color='gray', edgecolor='black')
        plt.axvline(x=one_company[name].values, color='red')
        plt.title(name)
        st.pyplot(fig)




### 사이드바 ###
#st.sidebar.header('')
input_stock = st.sidebar.text_input("종목 :")
if input_stock in df_krx['Name'].values.tolist():
    per_kospi = final_company_df[final_company_df['회사명']==input_stock]['PER_KOSPI'].values[0]
    eps_kospi = final_company_df[final_company_df['회사명'] == input_stock]['EPS_KOSPI'].values[0]
    per_sector = final_company_df[final_company_df['회사명'] == input_stock]['per_sector'].values[0]
    eps_sector = final_company_df[final_company_df['회사명'] == input_stock]['eps_sector'].values[0]

select_type = st.sidebar.selectbox('분석 :',
                ('1) 고배당주', '2) 저PER', '3) 저PBR', '4) 이익이 안정적인',
                 '5) 성장주', '0) 모든필터'))

if select_type == '1) 고배당주':
    input_DIVIDEND = st.sidebar.number_input('배당수익률', step=0.1, value=2.38)
    input_DIVIDEND_ratio = st.sidebar.number_input('배당성향', step=0.1, value=80.0)
    input_EPS_growth = st.sidebar.number_input('EPS성장률', step=0.1, value=4.0)
elif select_type == '2) 저PER':
    input_PER = st.sidebar.number_input('PER', step=0.1, value=12.0)
    input_DEBT = st.sidebar.number_input('부채비율', step=0.1, value=50.0)
    input_BETA = st.sidebar.number_input('BETA', step=0.1, value=1.0)
    input_EPS_growth = st.sidebar.number_input('EPS성장률', step=0.1, value=5.0)
elif select_type == '3) 저PBR':
    input_PBR = st.sidebar.number_input('PBR', step=0.1, value=0.8)
    input_ROE = st.sidebar.number_input('ROE', step=0.1, value=8.0)
    input_DEBT = st.sidebar.number_input('부채비율', step=0.1, value=70.0)
    input_BETA = st.sidebar.number_input('BETA', step=0.1, value=1.5)
elif select_type == '4) 이익이 안정적인':
    input_PER = st.sidebar.number_input('PER', step=0.1, value=15.0)
    input_BETA = st.sidebar.number_input('BETA', step=0.1, value=1.25)
    input_EPS_growth = st.sidebar.number_input('EPS성장률', step=0.1, value=10.0)
    input_EPS_stable = st.sidebar.number_input('EPS안정성', step=0.1, value=1.0)
elif select_type == '5) 성장주':
    input_ROE = st.sidebar.number_input('ROE', step=0.1, value=15.0)
    input_BETA = st.sidebar.number_input('BETA', step=0.1, value=1.25)
    input_EPS_growth = st.sidebar.number_input('EPS성장률', step=0.1, value=15.0)
    input_SALES_growth = st.sidebar.number_input('매출성장률', step=0.1, value=10.0)




### 본문 ###
one_company = final_company_df[final_company_df['회사명']==input_stock]
if input_stock in df_krx['Name'].values.tolist():
    st.write(input_stock)
    st.dataframe(one_company)
else:
    st.write('회사명을 입력해주세요')


#####################################################
if select_type == '1) 고배당주':
    names = ["배당수익률", '배당성향', 'EPS성장률']
    screen_df = screen(input_dividen=input_DIVIDEND, input_dividen_ratio=input_DIVIDEND_ratio,
                       input_eps_ratio=input_EPS_growth)
elif select_type == '2) 저PER':
    names = ["PER", '부채비율', 'beta', 'EPS성장률']
    screen_df = screen(input_per=input_PER, input_debt=input_DEBT, input_beta=input_BETA,
                       input_eps_ratio=input_EPS_growth, input_per_sector=True, input_esp_sector=True)
elif select_type == '3) 저PBR':
    names = ["PBR", 'ROE', '부채비율', 'beta']
    screen_df = screen(input_pbr=input_PBR, input_roe=input_ROE,
                       input_debt=input_DEBT, input_beta=input_BETA)
elif select_type == '4) 이익이 안정적인':
    names = ["PER", 'beta', 'EPS성장률', 'EPS안정성']
    screen_df = screen(input_per=input_PER, input_beta=input_BETA,
                       input_eps_ratio=input_EPS_growth, input_eps_stable=input_EPS_stable)
elif select_type == '5) 성장주':
    names = ["ROE", 'beta', 'EPS성장률', '매출성장률']
    screen_df = screen(input_roe=input_ROE, input_beta=input_BETA,
                       input_eps_ratio=input_EPS_growth,input_sales=input_SALES_growth)

st.write('------')
st.write('분석방법 : ', select_type)
st.write('분류된 회사수 : ', screen_df.shape[0])
screen_graph(names)
st.dataframe(screen_df)


