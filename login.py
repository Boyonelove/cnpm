import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
import json

# Khởi tạo Firebase (chỉ một lần)
firebase_json_path = "hotel-43f3e-f759d5da9de7.json"  # Đường dẫn tới file JSON của Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_json_path)
    firebase_admin.initialize_app(cred)


def main():
    st.title(":key: Đăng nhập hoặc Đăng ký")

    # Quản lý trạng thái
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signed_in' not in st.session_state:
        st.session_state.signed_in = False

    # Hàm đăng ký
    def sign_up(email, password, username=None):
        try:
            url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            if username:
                payload["displayName"] = username
            r = requests.post(url, params={"key": "API_KEY"}, json=payload)
            response = r.json()
            if 'error' in response:
                st.warning(f"Lỗi đăng ký: {response['error']['message']}")
            else:
                st.success("Tài khoản đã được tạo! Hãy đăng nhập.")
        except Exception as e:
            st.error(f"Lỗi đăng ký: {e}")

    # Hàm đăng nhập
    def sign_in(email, password):
        try:
            url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            r = requests.post(url, params={"key": "API_KEY"}, json=payload)
            response = r.json()
            if 'error' in response:
                st.warning(f"Lỗi đăng nhập: {response['error']['message']}")
            else:
                st.session_state.signed_in = True
                st.session_state.username = response.get('displayName', '')
                st.session_state.useremail = response['email']
                st.success(f"Chào mừng, {st.session_state.username or 'Người dùng'}!")
        except Exception as e:
            st.error(f"Lỗi đăng nhập: {e}")

    # Giao diện
    if not st.session_state.signed_in:
        choice = st.radio("Chọn hành động", ["Đăng nhập", "Đăng ký"])
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        
        if choice == "Đăng ký":
            username = st.text_input("Tên người dùng (tuỳ chọn)")
            if st.button("Đăng ký"):
                sign_up(email, password, username)
        else:
            if st.button("Đăng nhập"):
                sign_in(email, password)
    else:
        st.success(f"Đã đăng nhập với email: {st.session_state.useremail}")
        if st.button("Đăng xuất"):
            st.session_state.signed_in = False
            st.session_state.username = ''
            st.session_state.useremail = ''
            st.info("Đã đăng xuất thành công!")
