import streamlit as st
from streamlit_option_menu import option_menu
import login
import recommend
import contact  # Import trang liên hệ

# Cấu hình trang
st.set_page_config(
    page_title="Hotel Recommendation",
    page_icon=":tokyo_tower:"  # Biểu tượng tòa nhà
)

# MultiApp Class để quản lý nhiều trang
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self, selected):
        for app in self.apps:
            if app['title'] == selected:
                app['function']()  # Gọi hàm của trang tương ứng

# Khởi tạo ứng dụng
if __name__ == "__main__":
    app = MultiApp()
    app.add_app("🔒 Login", login.main)  
    app.add_app("🕵️ Recommend", recommend.main)  
    app.add_app("📞 Contact", contact.main)  # Thêm trang liên hệ

    # Sidebar menu
    st.sidebar.markdown("<h2 style='font-size: 24px;'>🏨 Main Menu</h2>", unsafe_allow_html=True)
    selected = st.sidebar.selectbox("Choose a page", ["🔒 Login", "🕵️ Recommend", "📞 Contact"])
    
    # Chạy ứng dụng với trang được chọn
    app.run(selected)
