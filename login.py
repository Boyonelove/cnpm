import streamlit as st
import firebase_admin
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

    # Kiểm tra trạng thái đăng nhập và cập nhật session nếu cần
    if 'username' not in st.session_state:
        st.session_state['username'] = ''
    if 'useremail' not in st.session_state:
        st.session_state['useremail'] = ''
    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, data=payload)
            try:                                            
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    def f(): 
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.signedout = False  # Đánh dấu đã đăng nhập thành công
            st.session_state.signout = False
            st.experimental_rerun()  # Reload trang sau khi đăng nhập thành công
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = True
        st.session_state.signedout = True   
        st.session_state.username = ''
        st.experimental_rerun()  # Reload trang sau khi đăng xuất

    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}") 

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
                st.success('Account created successfully! Please Login.')
                st.balloons()
        else:
            st.button('Login', on_click=f)
            forget()

    if st.session_state.signout:
        st.text('Name: ' + st.session_state.username)
        st.text('Email: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)

