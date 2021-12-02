import ast
import streamlit as st
from up42_parameter_validator import UP42ParamaterValidator

# to run this app $ streamlit run app.py
with st.form(key='my_form'):
    input_parameters = st.text_input(label='Enter your parameters')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    # import pdb; pdb.set_trace()
    input_parameters_dict = ast.literal_eval(input_parameters)
    error_dict = UP42ParamaterValidator(input_parameters=input_parameters_dict).check_parameters()
    # import pdb; pdb.set_trace()
    if len(error_dict) > 0:
        st.error(f"We found the following errors {error_dict}")