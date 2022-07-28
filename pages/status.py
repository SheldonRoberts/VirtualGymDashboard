import streamlit as st
import requests

st.set_page_config(
    page_title="Server Status",
    page_icon="💻",
)

def get_status_symbol(up):
    if up:
        return '✅'
    return '❌'

st.write("# Server Status")

try:
    x = dict(requests.get('http://129.128.184.214:8100').json())
    works = x['msg'] == 'Hello World'
except:
    works = False

st.subheader('Websocket API: ' + get_status_symbol(works))
st.code('sudo docker restart apis')

x = requests.get('http://localhost:9021').status_code
st.subheader('Kafka Dashboard: ' + get_status_symbol( x == 200))
st.code('sudo docker restart control-center && sudo docker restart broker && sudo docker restart zookeeper')

x = requests.get('http://localhost:8006').status_code
st.subheader('Jupyter Server: ' + get_status_symbol( x == 200))
st.code('sudo docker restart jupyterlab')

x = requests.get('http://129.128.184.214:4200').status_code
st.subheader('CrateDB: ' + get_status_symbol( x == 200))
st.code('sudo docker restart cratedb')
