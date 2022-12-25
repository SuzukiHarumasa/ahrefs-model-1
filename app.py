import streamlit as st
import pandas as pd
from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
import pandas as pd
import os
import io
import csv
from PIL import Image
import glob
from selenium.webdriver.chrome.service import Service # 1) Serviceのインポート

IMG_PATH = './tmp_dir'

data = st.file_uploader("ファイルアップロード", type='csv')
# if data is not None:
#     # To read file as bytes:
#     stringio = io.StringIO(data.getvalue().decode("utf-8"))
#     st.dataframe(stringio)

USERNAME = "media_general@joint.works"
PASSWORD = "Jointinc"

# first_image = Image.open('./img/harumake2.png')

# st.image(first_image,width=300)

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

if data:
    second_image = Image.open('./img/harumasamama mogumogu.png')

    st.image(second_image,width=300)
    data = pd.read_csv(data)
    st.dataframe(data)

    options = webdriver.chrome.options.Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    profile_path = './Profile ahrefs'
    options.add_argument('--user-data-dir=' + profile_path)
    l=glob.glob("./*")
    print(l)
    # driver_path ='./chromedriver.exe'
    
    # service = Service(executable_path=driver_path) # 2) executable_pathを指定
    driver = webdriver.Chrome(options=options) # 3) serviceを渡す

    target_url = "https://app.ahrefs.com/user/login"
    driver.get(target_url)
    sleep(5)

    username_input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[1]/div/input')

    username_input.send_keys(USERNAME)
    sleep(1)

    password_input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[2]/div/div/input')
    password_input.send_keys(PASSWORD)
    sleep(1)

    login_burron = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/button/div')
    login_burron.submit()
    sleep(5)

    df = pd.DataFrame()

    for domain in data['ドメイン'].to_list():
        ahrefs_url = "https://app.ahrefs.com/positions-explorer/top-subfolders/subdomains/jp/all/all/all/all/all/all/all/1/traffic_desc?target="+domain+"%2F"

        driver.get(ahrefs_url)
        sleep(5)

        df_tmp = driver.find_element(By.XPATH,'//*[@id="main_se_data_table"]')

        html = df_tmp.get_attribute('outerHTML')
        df_tmp = pd.read_html(html)

        df_tmp = df_tmp[0].head(1)

        df_tmp = df_tmp[['トラフィック', '価値', 'キーワード']]
        df_tmp.insert(0,'ドメイン',domain)
        df_tmp.insert(4,'ahrefs上位ページ取得URL',ahrefs_url)

        df = pd.concat([df, df_tmp], join='outer')
    driver.quit()
    st.success('Done!!!', icon="✅")
    df.to_csv('./output/output.csv',
            index=False)

    st.dataframe(df)
    df = convert_df(df)
    button = st.download_button(
        label="Download",
        data=df,
        file_name='output.csv',
        mime='text/csv',
    )

    if button:
        third_image = Image.open('./img/harumake6.png')
        st.image(third_image,width=300)