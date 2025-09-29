import pandas as pd
import re
import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu


st._config.set_option('themebase','dark')

st.set_page_config(layout='wide')

title_txt = '''<h1 style='font-size : 55px;text-align:center;color:purple;background-color:lightgrey;'>BHIMA JEWELLERY</h1>'''
st.markdown(title_txt,unsafe_allow_html=True)

st.write(" ")

st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 50px;  /* optional: same height */
    }
    </style>
""", unsafe_allow_html=True)

def update_auth(x):
    if len(str(x['Autho. No'])) < 6:
        if x['Crdit Card No'] in df1['Card Number'].values:
            return df1.loc[df1['Card Number'] == x['Crdit Card No'], 'Auth Code'].iloc[0]
        elif x['Crdit Card No'] in final_hdfc_df['CARDNBR'].values:
            return final_hdfc_df.loc[final_hdfc_df['CARDNBR'] == x['Crdit Card No'], 'APP_CODE'].iloc[0]
        else:
            return x['Autho. No']
    else:
        return x['Autho. No']
    

def update_card(x):
    if len(str(x['Crdit Card No'])) < 4:
        if x['Autho. No'] in df1['Auth Code'].values:
            return df1.loc[df1['Auth Code'] == x['Autho. No'], 'Card Number'].iloc[0]
        elif x['Autho. No'] in final_hdfc_df['APP_CODE'].values:
            return final_hdfc_df.loc[final_hdfc_df['APP_CODE'] == x['Autho. No'], 'CARDNBR'].iloc[0]
        else:
            return x['Crdit Card No']
    else:
        return x['Crdit Card No']



pdm_file = st.file_uploader("Upload Padam File",type=["csv", "xlsx"])

if st.button('Submit',type='primary'):
    

    if pdm_file !=  None:

        if "pdm_file" not in st.session_state:

            st.session_state["pdm_file"] = pdm_file

        if pdm_file.name.endswith(".csv"):

            df = pd.read_csv(pdm_file,dtype=str)

        else:

            df = pd.read_excel(pdm_file,dtype=str)

            columns_lst = ['Crdit Card No', 'Autho. No', 'Amt.Recd.On Card']

            lst = []
            for col in df.columns:
                if df[col].astype(str).str.contains('S.No|Doc',na=False).any():
                    lst.append(col)

            start_index = df[df[lst[0]].str.contains('S.No|Doc',na=False)].index.tolist()
            start_index = int(start_index[0])

            
            cols = df.loc[start_index].tolist()

            df.columns = cols

            df.columns = [str(col).strip() for col in df.columns]

            df = df.loc[start_index:]

            df.drop(index=start_index,inplace=True)

            df = df.reset_index(drop=True)

            for i in df.columns:
                if i not in lst:
                    df.rename(columns={'Card No.':'Crdit Card No','Autho.No.':'Autho. No','Amount':'Amt.Recd.On Card'},inplace=True)

            cols_lst = df.columns.drop(['Crdit Card No','Autho. No','Amt.Recd.On Card']).tolist()

            df.drop(columns=cols_lst,inplace=True)

            df.dropna(inplace=True)
            
            
            df['Discrepancy'] = df.apply(lambda x: 'Yes' if (len(str(x['Crdit Card No']))<4) or (len(str(x['Autho. No']))<6)  else 'No',axis=1)

            st.dataframe(df)
            st.info(f"{df.shape[0]} : Rows")



fed_files = st.file_uploader("Upload Federal Statement",accept_multiple_files=True,type=["csv", "xlsx"])

if st.button('submit',type='primary'):

    try:

        if fed_files != None:

            if "fed_files" not in st.session_state:

                st.session_state["fed_files"] = fed_files

            if fed_files:
                dfs=[]
                for upload in fed_files:
                    df1 = pd.read_excel(upload)
                    dfs.append(df1)

                df1 = pd.concat(dfs,ignore_index=True)

                lst1 =[]
                for col in df1.columns:
                    if df1[col].astype(str).str.contains('S.No',na=False).any():
                        lst1.append(col)

                fed_start_index = df1[df1.loc[:,'Unnamed: 0'].str.contains('S.No',na=False)].index.tolist()
                fed_start_index = int(fed_start_index[0])

                df1 = df1.loc[fed_start_index:]

                fed_cols = df1.loc[fed_start_index].values.tolist()

                df1.columns = fed_cols

                df1.drop(index=fed_start_index,inplace=True)

                df1 = df1.reset_index(drop=True)

                fed_cols_lst_1 = df1.columns.drop(['Card Number','Auth Code','Channel Type','Txn Amt']).tolist()

                df1.drop(columns = fed_cols_lst_1,inplace=True)

                df1 = df1.loc[df1['Channel Type'] == 'POS',:]

                df1.drop('Channel Type',axis=1,inplace=True)
                
                def card(x):
                    return str(x) if str(x)[0].isdigit() else None
                df1['Card Number'] = df1['Card Number'].apply(card)
                df1['Card Number'] = df1['Card Number'].apply(lambda x:x[-4:])
                df1['Txn Amt'] = df1['Txn Amt'].astype(int)
                df1['Card Number'] = df1['Card Number'].apply(lambda x:x.zfill(4) if len(x)<4 else x)
                df1['Auth Code'] = df1['Auth Code'].apply(lambda x:x.zfill(6) if len(x)<6 else x)
                st.dataframe(df1)

    except Exception as e:
        st.error("Please Upload the Correct Statement")

try:

    if st.button('Federal_Match',type='primary'):
        
        df = pd.read_excel(pdm_file,dtype=str)
        
        if "df" not in st.session_state:
            st.session_state["df"] = df
        
        columns_lst = ['Crdit Card No', 'Autho. No', 'Amt.Recd.On Card']

        lst = []
        for col in df.columns:
            if df[col].astype(str).str.contains('Doc',na=False).any():
                lst.append(col)

        start_index = df[df[lst[0]].str.contains('Doc',na=False)].index.tolist()
        start_index = int(start_index[0])

        
        cols = df.loc[start_index].tolist()

        df.columns = cols

        df.columns = [str(col).strip() for col in df.columns]

        df = df.loc[start_index:]

        df.drop(index=start_index,inplace=True)

        df = df.reset_index(drop=True)

        for i in df.columns:
            if i not in lst:
                df.rename(columns={'Card No.':'Crdit Card No','Autho.No.':'Autho. No','Amount':'Amt.Recd.On Card'},inplace=True)

        cols_lst = df.columns.drop(['Crdit Card No','Autho. No','Amt.Recd.On Card']).tolist()

        df.drop(columns=cols_lst,inplace=True)

        df.dropna(inplace=True)
                
                
        df['Discrepancy'] = df.apply(lambda x: 'Yes' if (len(str(x['Crdit Card No']))<4) or (len(str(x['Autho. No']))<6)  else 'No',axis=1)
        
        df.drop('Discrepancy',axis=1,inplace=True)
        

        dfs=[]
        for upload in fed_files:
            df1 = pd.read_excel(upload)
            dfs.append(df1)

        df1 = pd.concat(dfs,axis=0,ignore_index=True)

        lst1 =[]
        for col in df1.columns:
            if df1[col].astype(str).str.contains('S.No',na=False).any():
                lst1.append(col)

        fed_start_index = df1[df1.loc[:,'Unnamed: 0'].str.contains('S.No',na=False)].index.tolist()
        fed_start_index = int(fed_start_index[0])
        fed_start_index = df1[df1.loc[:,'Unnamed: 0'].str.contains('S.No',na=False)].index.tolist()
        fed_start_index = int(fed_start_index[0])

        df1 = df1.loc[fed_start_index:]

        fed_cols = df1.loc[fed_start_index].values.tolist()

        df1.columns = fed_cols

        df1.drop(index=fed_start_index,inplace=True)

        df1 = df1.reset_index(drop=True)

        fed_cols_lst_1 = df1.columns.drop(['Card Number','Auth Code','Channel Type','Txn Amt']).tolist()

        df1.drop(columns = fed_cols_lst_1,inplace=True)

        df1 = df1.loc[df1['Channel Type'] == 'POS',:]

        df1.drop('Channel Type',axis=1,inplace=True)            
        
        def card(x):
            return str(x) if str(x)[0].isdigit() else None
        
        df1['Card Number'] = df1['Card Number'].apply(card)
        df1['Card Number'] = df1['Card Number'].apply(lambda x:x[-4:])
        df1['Txn Amt'] = df1['Txn Amt'].astype(int)
        df1['Card Number'] = df1['Card Number'].apply(lambda x:x.zfill(4) if len(x)<4 else x)
        df1['Auth Code'] = df1['Auth Code'].apply(lambda x:x.zfill(6) if len(x)<6 else x)
        df1['card_auth'] = df1['Card Number']+df1['Auth Code']
        
        df1.columns = df1.columns.str.strip()     
        df1.columns = df1.columns.str.replace('\n','',regex=True)

        #df['Autho. No'] = df.apply(update_auth, axis=1)
        #df['Crdit Card No'] = df.apply(update_card, axis=1)

        df['card_auth'] = df['Crdit Card No']+df['Autho. No']
        df1['card_auth'] = df1['Card Number']+df1['Auth Code']

        fed_reconciled_df = pd.merge(df,df1,how='inner',on='card_auth')
        fed_reconciled_df.drop_duplicates(keep='first',inplace=True)
        st.dataframe(fed_reconciled_df)

except Exception as e:
    st.error("Please Uplaod the Padam File/Correct Statement")
            
hdfc_files = st.file_uploader("Upload HDFC Statement",accept_multiple_files=True,type=["csv", "xlsx"])

if st.button('SUBMIT',type='primary'):

    try:

        if hdfc_files != None:
            if "hdfc_files" not in st.session_state:
                st.session_state["hdfc_files"] = hdfc_files
            
            if hdfc_files:
                dfs=[]
                for upload in hdfc_files:
                    df2 = pd.read_excel(upload,dtype=str)
                    dfs.append(df2)

                final_hdfc_df = pd.concat(dfs,axis=0,ignore_index=True)
                cols_2 = final_hdfc_df.columns.drop(['CARDNBR','APP_CODE','PYMT_CHGAMNT']).tolist()
                final_hdfc_df.drop(columns=cols_2,inplace=True)
                final_hdfc_df.dropna(inplace=True)
                final_hdfc_df['PYMT_CHGAMNT'] = final_hdfc_df['PYMT_CHGAMNT'].astype(int)
                final_hdfc_df['CARDNBR'] = final_hdfc_df['CARDNBR'].apply(lambda x:x[-4:])
                final_hdfc_df['CARDNBR'] = final_hdfc_df['CARDNBR'].apply(lambda x:x.zfill(4) if len(x)<4 else x)
                final_hdfc_df['APP_CODE'] = final_hdfc_df['APP_CODE'].apply(lambda x:x.zfill(6) if len(x)<6 else x)
                st.dataframe(final_hdfc_df)
    except Exception as e:
        st.error("Please Upload the Correct Statement")
try:
    if st.button('HDFC Match',type='primary'):

        df = pd.read_excel(pdm_file,dtype=str)
        
        if "df" not in st.session_state:
            st.session_state["df"] = df

        lst = []
        for col in df.columns:
            if df[col].astype(str).str.contains("S.No|Doc",na=False).any():
                lst.append(col)

        start_index = df[df[lst[0]].str.contains("S.No|Doc",na=False)].index.tolist()
        start_index = int(start_index[0])

            
        cols = df.loc[start_index].tolist()

        df.columns = cols

        df.columns = [str(col).strip() for col in df.columns]

        df = df.loc[start_index:]

        df.drop(index=start_index,inplace=True)

        df = df.reset_index(drop=True)

        for i in df.columns:
            if i not in lst:
                df.rename(columns={'Card No.':'Crdit Card No','Autho.No.':'Autho. No','Amount':'Amt.Recd.On Card'},inplace=True)

        cols_lst = df.columns.drop(['Crdit Card No','Autho. No','Amt.Recd.On Card']).tolist()

        df.drop(columns=cols_lst,inplace=True)

        df.dropna(inplace=True)
        
            
        df['Discrepancy'] = df.apply(lambda x: 'Yes' if (len(str(x['Crdit Card No']))<4) or (len(str(x['Autho. No']))<6)  else 'No',axis=1)       
        
        df.drop('Discrepancy',axis=1,inplace=True)

        df['card_auth'] = df['Crdit Card No']+df['Autho. No']

        dfs=[]
        for upload in hdfc_files:
            df1= pd.read_excel(upload,dtype=str)
            dfs.append(df1)

        final_hdfc_df = pd.concat(dfs,axis=0,ignore_index=True)
        cols_2 = final_hdfc_df.columns.drop(['CARDNBR','APP_CODE','PYMT_CHGAMNT']).tolist()
        final_hdfc_df.drop(columns=cols_2,inplace=True)
        final_hdfc_df.dropna(inplace=True)
        final_hdfc_df['PYMT_CHGAMNT'] = final_hdfc_df['PYMT_CHGAMNT'].astype(int)
        final_hdfc_df['CARDNBR'] = final_hdfc_df['CARDNBR'].apply(lambda x:x[-4:])
        final_hdfc_df['CARDNBR'] = final_hdfc_df['CARDNBR'].apply(lambda x:x.zfill(4) if len(x)<4 else x)
        final_hdfc_df['APP_CODE'] = final_hdfc_df['APP_CODE'].apply(lambda x:x.zfill(6) if len(x)<6 else x)
        
        df.columns = df.columns.str.strip()     
        df.columns = df.columns.str.replace('\n','',regex=True)

        #df['card_auth'] = df['Crdit Card No']+df['Autho. No']
        final_hdfc_df['card_auth'] = final_hdfc_df['CARDNBR']+final_hdfc_df['APP_CODE']
        hdfc_recon_df = pd.merge(df,final_hdfc_df,how='inner',on='card_auth')
        hdfc_recon_df.drop_duplicates(keep='first',inplace=True)
        st.dataframe(hdfc_recon_df)
except Exception as e:
    st.error("Please Upload the Padm File/Correct Statement")

            
try:
    if st.button('Get',type='primary'):

        df = pd.read_excel(pdm_file,dtype=str)
        
        if "df" not in st.session_state:
            st.session_state["df"] = df
        
        lst = []
        for col in df.columns:
            if df[col].astype(str).str.contains('Doc',na=False).any():
                lst.append(col)

        start_index = df[df[lst[0]].str.contains('Doc',na=False)].index.tolist()
        start_index = int(start_index[0])

            
        cols = df.loc[start_index].tolist()

        df.columns = cols

        df.columns = [str(col).strip() for col in df.columns]

        df = df.loc[start_index:]

        df.drop(index=start_index,inplace=True)

        df = df.reset_index(drop=True)

        for i in df.columns:
            if i not in lst:
                df.rename(columns={'Card No.':'Crdit Card No','Autho.No.':'Autho. No','Amount':'Amt.Recd.On Card'},inplace=True)

        cols_lst = df.columns.drop(['Crdit Card No','Autho. No','Amt.Recd.On Card']).tolist()

        df.drop(columns=cols_lst,inplace=True)

        df.dropna(inplace=True)
        
            
        df['Discrepancy'] = df.apply(lambda x: 'Yes' if (len(str(x['Crdit Card No']))<4) or (len(str(x['Autho. No']))<6)  else 'No',axis=1)       
        
        df.drop('Discrepancy',axis=1,inplace=True)

        df['card_auth'] = df['Crdit Card No']+df['Autho. No']

        

        dfs=[]
        for upload in fed_files:
            df1 = pd.read_excel(upload)
            dfs.append(df1)

        df1 = pd.concat(dfs,axis=0,ignore_index=True)
       

        lst1 =[]
        for col in df1.columns:
            if df1[col].astype(str).str.contains('S.No',na=False).any():
                lst1.append(col)

        fed_start_index = df1[df1.loc[:,'Unnamed: 0'].str.contains('S.No',na=False)].index.tolist()
        fed_start_index = int(fed_start_index[0])

        df1 = df1.loc[fed_start_index:]

        fed_cols = df1.loc[fed_start_index].values.tolist()

        df1.columns = fed_cols

        df1.drop(index=fed_start_index,inplace=True)

        df1 = df1.reset_index(drop=True)

        fed_cols_lst_1 = df1.columns.drop(['Card Number','Auth Code','Channel Type','Txn Amt']).tolist()

        df1.drop(columns = fed_cols_lst_1,inplace=True)

        df1 = df1.loc[df1['Channel Type'] == 'POS',:]

        df1.drop('Channel Type',axis=1,inplace=True)
        
        def card(x):
            return str(x) if str(x)[0].isdigit() else None
        df1['Card Number'] = df1['Card Number'].apply(card)
        df1['Card Number'] = df1['Card Number'].apply(lambda x:x[-4:])
        df1['Txn Amt'] = df1['Txn Amt'].astype(int)
        df1['Card Number'] = df1['Card Number'].apply(lambda x:x.zfill(4) if len(x)<4 else x)
        df1['Auth Code'] = df1['Auth Code'].apply(lambda x:x.zfill(6) if len(x)<6 else x)

        dfs=[]
        for upload in hdfc_files:
            df2 = pd.read_excel(upload,dtype=str)
            dfs.append(df2)

        final_hdfc_df = pd.concat(dfs,axis=0,ignore_index=True)
        cols_2 = final_hdfc_df.columns.drop(['CARDNBR','APP_CODE','PYMT_CHGAMNT']).tolist()
        final_hdfc_df.drop(columns=cols_2,inplace=True)
        final_hdfc_df.dropna(inplace=True)
        final_hdfc_df['PYMT_CHGAMNT'] = final_hdfc_df['PYMT_CHGAMNT'].astype(int)
        final_hdfc_df['CARDNBR'] = final_hdfc_df['CARDNBR'].apply(lambda x:x[-4:])
        final_hdfc_df['CARDNBR'] = final_hdfc_df['CARDNBR'].apply(lambda x:x.zfill(4) if len(x)<4 else x)
        final_hdfc_df['APP_CODE'] = final_hdfc_df['APP_CODE'].apply(lambda x:x.zfill(6) if len(x)<6 else x)

        final_hdfc_df['card_auth'] = final_hdfc_df['CARDNBR']+final_hdfc_df['APP_CODE']

        df.columns = df.columns.str.strip()     
        df.columns = df.columns.str.replace('\n','',regex=True)

        df['Autho. No'] = df.apply(update_auth, axis=1)
        df['Crdit Card No'] = df.apply(update_card, axis=1)           


        df['card_auth'] = df['Crdit Card No']+df['Autho. No']
        df1['card_auth'] = df1['Card Number']+df1['Auth Code']
        final_hdfc_df['card_auth'] = final_hdfc_df['CARDNBR']+final_hdfc_df['APP_CODE']

        federal_matched_df = df.loc[df['card_auth'].isin(df1['card_auth'])]

        fed_lst = federal_matched_df['card_auth'].index.tolist()

        df.drop(index=fed_lst[0:],inplace=True)

        st.write(df.shape)

        hdfc_matched_df = df.loc[df['card_auth'].isin(final_hdfc_df['card_auth'])]

        hdfc_lst = hdfc_matched_df['card_auth'].index.tolist()

        df.drop(index=hdfc_lst[0:],inplace=True)

        df.drop_duplicates(keep='first',inplace=True)

        st.dataframe(df)
        st.write(df.shape)
        st.info(f"{df.shape[0]} : Rows not matched")

except Exception as e:
    st.error('Please Upload the Padm File/Correct Statement')





