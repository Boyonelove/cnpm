import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import json
import requests

# Khởi tạo Firebase chỉ một lần
firebase_json_path = "hotel-43f3e-f759d5da9de7.json"  
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_json_path)
    firebase_admin.initialize_app(cred)

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

def reset_to_login():
    """
    Đặt lại trạng thái đăng nhập và chuyển người dùng về trang login.
    """
    st.session_state['user_logged_in'] = False
    st.session_state['username'] = None
    st.session_state['email'] = None  # Xóa email người dùng khi đăng xuất
    st.experimental_rerun()  # Tải lại trang để chuyển hướng về trang login

def main():
    # Kiểm tra trạng thái đăng nhập
    if 'user_logged_in' not in st.session_state or not st.session_state['user_logged_in']:
        st.warning("Vui lòng đăng nhập để truy cập trang này.")
        # Tạo nút để quay lại trang đăng nhập
        if st.button("Quay lại đăng nhập"):
            reset_to_login()  # Đặt lại trạng thái đăng nhập và quay về trang login
        return  # Dừng hàm lại nếu người dùng chưa đăng nhập

    # Hiển thị tên người dùng sau khi đăng nhập
    if 'username' in st.session_state:
        st.write(f"Chào {st.session_state.username}!")

    # Đăng xuất
    if st.button("Đăng xuất"):
        reset_to_login()

if __name__ == "__main__":
    main()
