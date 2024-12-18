import streamlit as st

def main():
    # Kiểm tra trạng thái đăng nhập
    if "signed_in" in st.session_state and st.session_state.signed_in:
        st.title("Thông tin liên hệ")
        st.write("Nếu bạn cần hỗ trợ, hãy liên hệ với chúng tôi qua các thông tin dưới đây:")

        # Thông tin liên lạc
        st.subheader("Liên hệ trực tiếp:")
        st.write("📍 **Địa chỉ:** 123 Đường ABC, Quận 1, Thành phố Hồ Chí Minh")
        st.write("📧 **Email:** support@hotelfinder.com")
        st.write("📞 **Hotline:** 0909 123 456")

        # Các liên kết mạng xã hội
        st.subheader("Theo dõi chúng tôi:")
        st.markdown("[🌐 Website chính thức](https://example.com)")
        st.markdown("[📘 Facebook](https://facebook.com/example)")
        st.markdown("[📷 Instagram](https://instagram.com/example)")

        # Chính sách hỗ trợ
        st.subheader("Chính sách hỗ trợ:")
        st.write("- **Thời gian hỗ trợ:** 8:00 - 22:00 (hàng ngày)")
        st.write("- **Chính sách hoàn tiền:** [Xem chi tiết](https://example.com/policy)")
    else:
        st.warning("Vui lòng đăng nhập để xem trang này!")
        st.button("Quay lại trang đăng nhập", on_click=lambda: st.experimental_rerun())
