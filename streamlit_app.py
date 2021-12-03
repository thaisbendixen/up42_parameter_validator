import streamlit as st
from fastapi.testclient import TestClient
import json

from main import app
from up42_parameter_validator import UP42ParamaterValidator

# to run this app $ streamlit run app.py

client = TestClient(app)

with st.form(key='my_form'):
    input_parameters = st.text_input(label='Enter your parameters')
    submit_button = st.form_submit_button(label='Submit')
    response = client.get("/")
    assert response.status_code == 200

if submit_button:
    response = client.post("/validate", json=input_parameters)
    response_json = response.json()
    import pdb; pdb.set_trace()
    st.write(response_json)
