__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import nest_asyncio
nest_asyncio.apply()

from crewai import Crew, Process
from tasks import comp_task, texit
from agents import comp_res, reviewer
import streamlit as st
import pandas as pd
from io import BytesIO

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Firebase service account key as a Python dictionary
firebase_config = {
  "type": st.secrets["type"],
  "project_id": st.secrets["project_id"],
  "private_key_id": st.secrets["private_key_id"],
  "private_key": st.secrets["private_key"],
  "client_email": st.secrets["client_email"],
  "client_id": st.secrets["client_id"],
  "auth_uri":  st.secrets["auth_uri"],
  "token_uri": st.secrets["token_uri"],
  "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
  "client_x509_cert_url": st.secrets["client_x509_cert_url"]
}

# Initialize firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

colab_link = 'https://colab.research.google.com/drive/1LeIfopygLuryQ8-5ofP-kVOxaux36nGE?usp=sharing'

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

st.title(":crab: Retail Research Robot :crab:")

st.write('NOTE: Please upload a ".csv" file with a single column named "url" containing the list of all the company url in that single column. Alternatively, you can execute the following script: [Colab Notebook](%s). ' % colab_link)
st.write('Please do not run more than 20 link at a time as product still in beta. If you do not get the desired output please hit "Rerun". Happy Researching!')

df_2=pd.DataFrame(columns=['ip_url', 'company_name', 'company_description', 'company_retail', 'company_payments', 'company_lp_gl', 'company_lp_eu', 'company_lp_uk', 'company_hq_c', 'company_hq_s', 'company_hq_gpc'])
df_final=pd.DataFrame(columns=['ip_url', 'company_name', 'company_description', 'company_retail', 'company_payments', 'company_lp_gl', 'company_lp_eu', 'company_lp_uk', 'company_hq_c', 'company_hq_s', 'company_hq_gpc'])

uploaded_file = st.file_uploader("Upload a CSV file containing URLs", type=["csv"])
    
if uploaded_file is not None:

    df1 = pd.read_csv(uploaded_file)
    df_final = pd.DataFrame()
    if hasattr(df1, 'url'):
        for index, url in df1['url'].items():
            doc_ref = db.collection('url_list').document(url.replace("/", "_"))
            doc_ref.set({'url':url})

        ## Forming the tech focused crew with some enhanced configuration
        crew=Crew(
        agents=[comp_res, reviewer],
        tasks=[comp_task, texit],
        process=Process.sequential)
        
        for index, url in df1['url'].items():
            with st.spinner('Researching '+url+' ...'):
                result=crew.kickoff(inputs={'url':url})
            try:
                data_json = pd.read_json("output/data.json", typ='series')
                df_final.at[index, 'ip_url']=url
                df_final.at[index, 'company_name']=data_json['company_name']
                df_final.at[index, 'company_description']=data_json['company_description']
                df_final.at[index, 'company_retail']=data_json['company_retail']
                df_final.at[index, 'company_payments']=data_json['company_payments']
                df_final.at[index, 'company_lp_gl']=data_json['company_lp_gl']
                df_final.at[index, 'company_lp_eu']=data_json['company_lp_eu']
                df_final.at[index, 'company_lp_uk']=data_json['company_lp_uk']
                df_final.at[index, 'company_hq_c']=data_json['company_hq_c']
                df_final.at[index, 'company_hq_s']=data_json['company_hq_s']
                df_final.at[index, 'company_hq_gpc']=data_json['company_hq_gpc'].split()[0]
                doc_ref = db.collection('company').document(url.replace("/", "_"))
                doc_ref.set({
                    'input_url': url,
                    'datetime': str(datetime.now()),
                    'company_retail': df_final.at[index, 'company_retail'],
                    'company_payments': df_final.at[index, 'company_payments'],
                    'company_name': df_final.at[index, 'company_name'],
                    'company_lp_uk': df_final.at[index, 'company_lp_uk'],
                    'company_lp_gl': df_final.at[index, 'company_lp_gl'],
                    'company_lp_eu': df_final.at[index, 'company_lp_eu'],
                    'company_hq_s': df_final.at[index, 'company_hq_s'],
                    'company_hq_gpc': df_final.at[index, 'company_hq_gpc'],
                    'company_hq_c': df_final.at[index, 'company_hq_c'],
                    'company_description': df_final.at[index, 'company_description'],
                })
            except:
                df_final.at[index, 'ip_url']=url
                df_final.at[index, 'company_name']=''
                df_final.at[index, 'company_description']=''
                df_final.at[index, 'company_retail']=''
                df_final.at[index, 'company_payments']=''
                df_final.at[index, 'company_lp_gl']=''
                df_final.at[index, 'company_lp_eu']=''
                df_final.at[index, 'company_lp_uk']=''
                df_final.at[index, 'company_hq_c']=''
                df_final.at[index, 'company_hq_s']=''
                df_final.at[index, 'company_hq_gpc']=''

                doc_ref = db.collection('company').document(url.replace("/", "_"))
                doc_ref.set({
                    'input_url': url,
                    'datetime': str(datetime.now()),
                    'company_retail': df_final.at[index, 'company_retail'],
                    'company_payments': df_final.at[index, 'company_payments'],
                    'company_name': df_final.at[index, 'company_name'],
                    'company_lp_uk': df_final.at[index, 'company_lp_uk'],
                    'company_lp_gl': df_final.at[index, 'company_lp_gl'],
                    'company_lp_eu': df_final.at[index, 'company_lp_eu'],
                    'company_hq_s': df_final.at[index, 'company_hq_s'],
                    'company_hq_gpc': df_final.at[index, 'company_hq_gpc'],
                    'company_hq_c': df_final.at[index, 'company_hq_c'],
                    'company_description': df_final.at[index, 'company_description'],
                })
                continue
            df_2 = pd.concat([df_2,df_final], ignore_index=True)
            df_final.drop(df_final.index, inplace=True)
        st.write("### COMPANY DATA")
        st.dataframe(df_2, column_config={"ip_url": st.column_config.LinkColumn(), "company_lp_gl": st.column_config.LinkColumn(), "company_lp_eu": st.column_config.LinkColumn(), "company_lp_uk": st.column_config.LinkColumn()})
    else:
        st.write('Incorrect file format. Please upload a ".csv" file with a single column named "url" containing the list of all the company url in that single column. Alternatively, you can execute the following script: [Colab Notebook](%s). ' % colab_link)
    st.button(label="Rerun")
