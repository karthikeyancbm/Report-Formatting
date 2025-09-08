import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu
import io
import openpyxl

st._config.set_option('themebase','dark')

st.set_page_config(layout='wide')

title_txt = '''<h1 style='font-size : 55px;text-align:center;color:purple;background-color:lightgrey;'>BHIMA JEWELLERY</h1>'''
st.markdown(title_txt,unsafe_allow_html=True)

file =st.file_uploader('Upload the file',type=['xlsx','xlsm','xls'])

if file is not None:

    file_path = file

    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(file_path,sheet_name= xls.sheet_names[0],header=None)

    df.dropna(how='all',axis=0,inplace=True)
    df.dropna(how='all',axis=1,inplace=True)
    df.reset_index(drop=True)
    df.iloc[:,0] = df.iloc[:,0].astype(str).str.replace(r"[\n\t]+","",regex=True).str.strip()
    df = df.set_index(0)

    st.session_state.df = df

labels = ["Opening_wt", "Arrival", "Barcode", "Pending_wt", "Remarks"]

branch_names = ['MADURAI','RAJAPALAYAM','DINDIGUL','TRICHY','SALEM','THIRUNELVELI']

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:

       
    if st.button(":rainbow[Gold] :beginner:",use_container_width=True):
        if 'df' in st.session_state:
            df= st.session_state.df    
            gold_df = df.loc['GOLD'].reset_index().T
            gold_df.drop([0],axis=0,inplace=True)
            gold_df.columns = branch_names
            gold_df.index = ["Opening_wt", "Arrival", "Barcode", "Pending_wt", "Remarks"]
            gold_df.index.name = 'Particulars'
            gold_df = gold_df.reset_index()
            gold_df = gold_df.fillna('NIL')   
            gold_df.insert(0, "Metal", "GOLD")
            st.session_state.gold_df = gold_df
            st.dataframe(gold_df)
            csv = gold_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 :rainbow[Download GOLD as CSV]",
                data=csv,
                file_name="GOLD.csv",
                mime="text/csv",
            )


with col2:

    if st.button(":rainbow[Silver] :beginner:",use_container_width=True):        
            if 'df' in st.session_state:
                df = st.session_state.df
                silver_df = df.loc['SILVER'].reset_index().T
                silver_df.drop([0],axis=0,inplace=True)
                silver_df.columns = branch_names
                silver_df.index = ["Opening_wt", "Arrival", "Barcode", "Pending_wt", "Remarks"]
                silver_df.index.name = 'Particulars'
                silver_df = silver_df.fillna('NIL')
                silver_df = silver_df.reset_index()
                silver_df.insert(0, "Metal", "SILVER")
                st.session_state.silver_df = silver_df
                st.dataframe(silver_df)
                csv = silver_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 :rainbow[Download SILVER as CSV]",
                    data=csv,
                    file_name="SILVER.csv",
                    mime="text/csv",
                )

    
with col3:
     
     if st.button(":rainbow[Platinum] :beginner:",use_container_width=True):
        if 'df' in st.session_state:
            df = st.session_state.df
            plat_df = df.loc['PLATINUM'].reset_index().T
            plat_df.drop([0],axis=0,inplace=True)
            plat_df.columns = branch_names
            plat_df.index = ["Opening_wt", "Arrival", "Barcode", "Pending_wt", "Remarks"]
            plat_df.index.name = "Particulars"
            plat_new_df = plat_df.reset_index()
            plat_new_df = plat_new_df.fillna('NIL')
            plat_new_df.insert(0, "Metal", "PLATINUM")
            st.session_state.plat_new_df = plat_new_df
            st.dataframe(plat_new_df)
            csv = plat_new_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 :rainbow[Download PLATINUM as CSV]",
                data=csv,
                file_name="PLATINUM.csv",
                mime="text/csv",
            )
        
with col4:
     
    try:
     
     if st.button(":rainbow[Coin] :beginner:",use_container_width=True):
        if 'df' in st.session_state:
            df = st.session_state.df
            coin_df = df.loc['COIN'].reset_index().T
            coin_df.drop([0],axis=0,inplace=True)
            coin_df.columns = branch_names
            coin_df.index = ["Opening_wt", "Arrival", "Barcode", "Pending_wt", "Remarks"]
            coin_df.index.name = 'Particulars'
            coin_new_df = coin_df.reset_index()
            coin_new_df = coin_new_df.fillna('NIL')
            coin_new_df.insert(0, "Metal", "GOLD_COIN")
            st.session_state.coin_new_df = coin_new_df
            st.dataframe(coin_new_df)
            csv = coin_new_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 :rainbow[Download COIN as CSV]",
                data=csv,
                file_name="COIN.csv",
                mime="text/csv",
            )
    except:
        st.error('Start fron Beginning')
     
with col5:
    try:     
        if st.button(":rainbow[Diamond] :beginner:",use_container_width=True):          
            if 'df' in st.session_state:
                df = st.session_state.df
                diamond_df = df.loc['DIAMOND'].reset_index()
                diamond_df_lst = diamond_df['DIAMOND'].tolist()
                diamond_df_1 = pd.DataFrame(index=labels, columns=branch_names)
                diamond_df_1['MADURAI'] = diamond_df_lst
                diamond_df_1 = diamond_df_1.fillna('NIL')
                diamond_df_1.index.name = 'Particulars'
                diamond_df_1 = diamond_df_1.reset_index()
                diamond_df_1.insert(0, "Metal", "DIAMOND")
                st.session_state.diamond_df_1 = diamond_df_1
                st.dataframe(diamond_df_1)

                csv = diamond_df_1.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 :rainbow[Download DIAMOND as CSV]",
                    data=csv,
                    file_name="DIAMOND.csv",
                    mime="text/csv",
                )

    except:
        st.error('Start from Beginning')

     
with col6:
    try:     
        if st.button(":rainbow[Summary] :beginner:",use_container_width=True):
            if 'df' in st.session_state:
                df =st.session_state.df
                metals   = ['GOLD','SILVER','DIAMOND','PLATINUM','COIN']
                summary_df = pd.concat([st.session_state.gold_df,st.session_state.silver_df,st.session_state.plat_new_df,st.session_state.coin_new_df,st.session_state.diamond_df_1],axis=0,ignore_index=True)
                summary_df['Metal'] = summary_df['Metal'].drop_duplicates()
                summary_df['Metal'] = summary_df['Metal'].fillna('')
                st.session_state.summary_df = summary_df
                st.dataframe(summary_df)

                csv = summary_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 :rainbow[Download Summary as CSV]",
                    data=csv,
                    file_name="summary.csv",
                    mime="text/csv",
                )

                # --- Download as Excel ---
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    summary_df.to_excel(writer, index=False, sheet_name="Summary")
                st.download_button(
                    label="📥 Download Summary as Excel",
                    data=output.getvalue(),
                    file_name="summary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
    except Exception as e:
        st.error('Start from Beginning')





