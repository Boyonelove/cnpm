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
    st.title(":key: Đăng nhập, Đăng ký ")

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
            r = requests.post(url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, json=payload)
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
            r = requests.post(url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, json=payload)
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

    # Hàm đặt lại mật khẩu
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
                st.success("Email đặt lại mật khẩu đã được gửi!")
            else:
                error_message = response.get('error', {}).get('message', 'Không rõ lỗi')
                st.warning(f"Lỗi đặt lại mật khẩu: {error_message}")
        except Exception as e:
            st.error(f"Lỗi đặt lại mật khẩu: {e}")

    # Giao diện
    if not st.session_state.signed_in:
        choice = st.radio( ["Đăng nhập", "Đăng ký", "Quên mật khẩu"])
        email = st.text_input("Email")
        password = ""

        if choice == "Đăng ký":
            username = st.text_input("Tên người dùng (tuỳ chọn)")
            password = st.text_input("Mật khẩu", type="password")
            if st.button("Đăng ký"):
                sign_up(email, password, username)

        elif choice == "Đăng nhập":
            password = st.text_input("Mật khẩu", type="password")
            if st.button("Đăng nhập"):
                sign_in(email, password)

        elif choice == "Quên mật khẩu":
            if st.button("Đặt lại mật khẩu"):
                reset_password(email)

    else:
        st.success(f"Đã đăng nhập với email: {st.session_state.useremail}")
        if st.button("Đăng xuất"):
            st.session_state.signed_in = False
            st.session_state.username = ''
            st.session_state.useremail = ''
            st.info("Đã đăng xuất thành công!")

if __name__ == "__main__":
    main()
