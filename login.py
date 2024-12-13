import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests

# Khởi tạo Firebase chỉ một lần, sử dụng đường dẫn tương đối
firebase_json_path = "hotel-43f3e-f759d5da9de7.json"  # File JSON phải nằm trong cùng thư mục với mã nguồn
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_json_path)
    firebase_admin.initialize_app(cred)

def main():  
    st.title(":key: :blue[Login / Sign up]")

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
        
    def sign_up_with_email_and_password(email, password, username=None):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            if username:
                payload["displayName"] = username 
            
            r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, json=payload)
            response = r.json()
            if r.status_code == 200:
                return response.get('email', 'Unknown email')
            else:
                st.warning(f"Signup failed: {response.get('error', {}).get('message', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error during sign-up: {e}")

    def sign_in_with_email_and_password(email, password):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, json=payload)
            response = r.json()
            if r.status_code == 200:
                return {
                    'email': response['email'],
                    'username': response.get('displayName', 'Unknown username')
                }
            else:
                st.warning(f"Signin failed: {response.get('error', {}).get('message', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error during sign-in: {e}")

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, json=payload)
            response = r.json()
            if r.status_code == 200:
                return True, "Password reset email sent successfully."
            else:
                error_message = response.get('error', {}).get('message', 'Unknown error')
                return False, f"Password reset failed: {error_message}"
        except Exception as e:
            return False, f"Error during password reset: {e}"

    def handle_login():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.signedout = True
            st.session_state.signout = True    
        except Exception as e: 
            st.warning(f"Login failed: {e}")

    def handle_logout():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    def handle_reset_password():
        email = st.text_input('Enter your email for password reset:')
        if st.button('Send Reset Link'):
            success, message = reset_password(email)
            if success:
                st.success(message)
            else:
                st.warning(message)

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                if user:
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()
        else:
            st.button('Login', on_click=handle_login)
            handle_reset_password()

    if st.session_state.signout:
        st.text('Name: ' + st.session_state.username)
        st.text('Email: ' + st.session_state.useremail)
        st.button('Sign out', on_click=handle_logout)
