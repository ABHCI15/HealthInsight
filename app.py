import streamlit as st 
import pathlib
import textwrap
# import google.generativeai as genai
import firebase_authfunctions as auth_functions

st.set_page_config(layout="wide", page_title="Login - HealthInsight", page_icon="🩺")


st.title("HealthInsight V 0.01.0")
placeholder = st.empty()
placeholder.header("Login to access the app")

# boilerplate auth code 

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    col1,col2,col3 = st.columns([1,2,1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(label='Do you have an account?',options=('Yes','No','I forgot my password'))
    auth_form = col2.form(key='Authentication form',clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Yes','No'} else auth_form.empty()
    auth_notification = col2.empty()

    # Sign In
    if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Signing in'):
            auth_functions.sign_in(email,password)

    # Create Account
    elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Creating account'):
            auth_functions.create_account(email,password)

    # Password Reset
    elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Sending password reset link'):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # Show user information
    placeholder.header('User information:')
    uid = st.session_state.user_info['localId']
    # st.write(st.session_state.user_info) st.session_state.user_info has all user info to be used later 

    # Sign out
    st.header('Sign out:')
    st.button(label='Sign Out',on_click=auth_functions.sign_out,type='primary')

    # Delete Account
    st.header('Delete account:')
    password = st.text_input(label='Confirm your password',type='password')
    st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')
    med_switch = st.button(label='Medical Q/A chatbot')
    sleep_Switch =st.button("Sleep Analysis")
    if sleep_Switch:
        st.switch_page("pages/sleep.py")
    if med_switch:
        st.switch_page("pages/medHelp.py")


