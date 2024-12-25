import pandas as pd
import streamlit as st
from unidecode import unidecode

# Hàm đọc dữ liệu từ file CSV
def get_data_from_csv():
    try:
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv("processed_data.csv")
        # Đổi tên các cột để đồng nhất với mã hiện tại
        df.rename(columns={
            "hotel": "hotel",
            "url": "url_hotel",
            "image_url": "url_image",
            "price": "price",
            "address": "address_hotel",
            "beach": "beach",
            "score": "score",
            "avg review": "avg_review",
            "reviews count": "review_count",
            "property": "property"
        }, inplace=True)
        return df
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi đọc dữ liệu từ file CSV: {e}")
        return pd.DataFrame()

# Hàm lọc khách sạn
def filter_hotels(df, address, price_range, min_score, max_score, property_type, beach_filter):
    # Tạo cột tạm thời không dấu để tìm kiếm
    df['address_temp'] = df['address_hotel'].str.strip().str.lower().apply(unidecode)

    # Tách các từ khóa tìm kiếm
    keywords = [unidecode(word.strip().lower()) for word in address.split(",")]

    # Bộ lọc địa chỉ: kiểm tra nếu bất kỳ từ khóa nào có trong địa chỉ
    address_filter = df['address_temp'].apply(
        lambda x: any(keyword in x for keyword in keywords)
    )

    # Xử lý điểm đánh giá -1
    df['score'] = df['score'].apply(lambda x: 0 if x == -1 else x)

    # Bộ lọc giá
    price_filter = {
        "Mọi mức giá": pd.Series([True] * len(df)),
        "Nhỏ hơn 500.000 đ/ Đêm": df['price'] < 500000,
        "500-1tr đ/ Đêm": (df['price'] >= 500000) & (df['price'] <= 1000000),
        "Lớn hơn 1tr đ/ Đêm": df['price'] > 1000000
    }[price_range]
    
    # Bộ lọc điểm đánh giá
    score_filter = (df['score'] >= min_score) & (df['score'] <= max_score)

    # Bộ lọc loại hình khách sạn
    property_filter = df['hotel'].str.contains(property_type, case=False, na=False) if property_type else pd.Series([True] * len(df))
    
    # Bộ lọc bãi biển
    if beach_filter.lower() == "có":
        beach_filter = df['beach'].str.contains("giáp biển|cách bãi biển", case=False, na=False)
    elif beach_filter.lower() == "không":
        beach_filter = df['beach'].isna() | (df['beach'].str.strip() == "")
    else:  # Nếu không quan tâm, áp dụng tất cả
        beach_filter = pd.Series([True] * len(df))

    # Kết hợp bộ lọc
    filtered_df = df[address_filter & price_filter & score_filter & property_filter & beach_filter]
     
    # Loại bỏ cột tạm thời trước khi trả về
    filtered_df = filtered_df.drop(columns=['address_temp'])

    # Loại bỏ các khách sạn trùng nhau dựa vào tên khách sạn
    filtered_df = filtered_df.drop_duplicates(subset=['hotel'], keep='first')

    # Sắp xếp theo điểm đánh giá và giá tiền từ cao xuống thấp
    return filtered_df.sort_values(by=['score', 'price'], ascending=[False, False])


# Hiển thị thông tin khách sạn
def display_hotel_card(row):
    formatted_price = f"{row['price']:,}".replace(",", ".")
    image_url = row['url_image'] if pd.notna(row['url_image']) else 'https://png.pngtree.com/png-vector/20190521/ourlarge/pngtree-hotel-icon-for-personal-and-commercial-use-png-image_1044892.jpg'
    hotel_link = row['url_hotel'] if pd.notna(row['url_hotel']) else "#"
    
    # Kiểm tra đánh giá
    if row['review_count'] == 0 or row['review_count'] == -1:
        avg_review_display = "Chưa có đánh giá"
    else:
        avg_review_display = f"{row['avg_review']} ({row['review_count']} bài đánh giá)"

    # Điểm đánh giá
    score_display = "Chưa có đánh giá" if row['score'] == 0 else f"{row['score']} / 10"

    st.markdown(f"""
    <div style='background-color: rgba(230, 245, 255, 0.9); border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; display: flex; flex-direction: column; width: 100%; max-width: 800px;'>
        <h3 style='color: #1E3A8A; font-size: 24px; text-align: center; margin-bottom: 10px;'>
            <a href='{hotel_link}' target='_blank' style='text-decoration: none; color: inherit;'>{row['hotel']}</a>
        </h3>
        <div style='display: flex; flex-direction: row; justify-content: space-between; align-items: center;'>
            <!-- Hình ảnh bên trái -->
            <div style='flex: 1; margin-left: 30px;margin-top: 0px; display: flex; justify-content: center; align-items: center;'>
                <img src='{image_url}' style='width: 107%; max-width: 500px; height: auto; border-radius: 10px;' alt='Hotel Image'>
            </div>
            <!-- Thông tin bên phải -->
            <div style='flex: 2;margin-left: 30px; display: flex; flex-direction: column; justify-content: flex-start;'>
                <p style='color: #1E3A8A; font-size: 17px; margin-bottom: 15px;'><b>⭐ Điểm đánh giá:</b> {score_display}</p>
                <p style='color: #1E3A8A; font-size: 17px; margin-bottom: 15px;'><b>🗺️ Địa chỉ:</b> {row['address_hotel']}</p>
                <p style='color: #1E3A8A; font-size: 17px; margin-bottom: 15px;'><b>💵 Giá:</b> {formatted_price} VND / đêm</p>
                <p style='color: #1E3A8A; font-size: 17px; margin-bottom: 15px;'><b>📝 Đánh giá trung bình:</b> {avg_review_display}</p>
                <p style='color: #1E3A8A; font-size: 17px; margin-bottom: 15px;'><b>🏖️ Gần bãi biển:</b> {row['beach'] if pd.notna(row['beach']) else "Không"}</p>
            </div>
        </div>
        <!-- Nút đặt phòng ở dưới -->
        <div style='display: flex;margin-right: 80px; justify-content: center; align-items: center; margin-top: 20px;'>
            <a href="{hotel_link}" style="color: white; text-decoration: none;">
                <button style="background-color: #007BFF; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; font-size: 16px;">
                    Đặt phòng ngay
                </button>
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

def main():
    # Kiểm tra trạng thái đăng nhập
    if 'signed_in' not in st.session_state or not st.session_state.signed_in:
        st.warning("Bạn cần đăng nhập trước khi truy cập hệ thống!")
        st.stop()  # Dừng việc xử lý nếu chưa đăng nhập

    st.title("Hệ thống gợi ý khách sạn")
    st.write("Tìm kiếm khách sạn phù hợp với các tiêu chí của bạn.")

    # Kiểm tra xem đã có kết quả tìm kiếm trước đó trong session_state chưa
    if "search_results" not in st.session_state:
        st.session_state.search_results = pd.DataFrame()  # Khởi tạo nếu chưa có

    # Sidebar filters
    st.sidebar.header("Bộ lọc tìm kiếm")
    with st.sidebar.form(key='search_form'):
        address = st.text_input("Nhập địa điểm:", "")
        price_range = st.selectbox("Chọn mức giá:", ["Mọi mức giá", "Nhỏ hơn 500.000 đ/ Đêm", "500-1tr đ/ Đêm", "Lớn hơn 1tr đ/ Đêm"])

        # Chọn khoảng điểm đánh giá
        min_score, max_score = st.slider("Chọn khoảng điểm đánh giá:",  min_value=0, max_value=10, value=(7, 8), step=1)

        # Cập nhật loại khách sạn thành selectbox với danh sách cố định
        property_type = st.selectbox("Chọn loại khách sạn:", ["Tuỳ chọn", "Hotel", "Motel", "Hostel", "Homestay", "Resort"])
        
        # Nếu chọn "Tuỳ chọn", không áp dụng bộ lọc
        property_type = None if property_type == "Tuỳ chọn" else property_type

        beach_filter = st.selectbox("Gần bãi biển:", ["Không quan tâm", "Có", "Không"])
        submit_button = st.form_submit_button("Tìm kiếm")

    # Reset kết quả tìm kiếm nếu bộ lọc thay đổi
    if submit_button:
        st.session_state.current_page = 1
        # Lấy dữ liệu từ database nếu chưa có hoặc đã có thay đổi trong bộ lọc
        df = get_data_from_csv()
        if df.empty:
            st.warning("Không có dữ liệu từ database.")
            return

        result_df = filter_hotels(df, address, price_range, min_score, max_score, property_type, beach_filter)
        
        if not result_df.empty:
            st.session_state.search_results = result_df  # Lưu kết quả tìm kiếm vào session_state
            
            # Phân trang
            page_size = 5  # Số lượng khách sạn trên mỗi trang
            total_pages = len(result_df) // page_size + (1 if len(result_df) % page_size > 0 else 0)

            # Lưu số trang hiện tại trong session_state
            if "current_page" not in st.session_state:
                st.session_state.current_page = 1  # Khởi tạo trang đầu tiên

            current_page = st.session_state.current_page

            # Lấy dữ liệu trang hiện tại
            start_idx = (current_page - 1) * page_size
            end_idx = start_idx + page_size
            current_page_data = result_df.iloc[start_idx:end_idx]

            # Hiển thị các khách sạn trên trang hiện tại
            for _, row in current_page_data.iterrows():
                display_hotel_card(row)

            # Thanh chọn trang
            st.markdown("---")
            cols = st.columns(5)  # Tạo 5 cột cho các nút

            with cols[0]:
                if st.button("<< Trang đầu"):
                    st.session_state.current_page = 1
                    st.rerun()  # Làm mới dữ liệu sau khi thay đổi trang
            with cols[1]:
                if st.button("< Trước"):
                    if current_page > 1:
                        st.session_state.current_page = current_page - 1
                        st.rerun()  # Làm mới dữ liệu sau khi thay đổi trang
            with cols[2]:
                st.write(f"Trang {current_page}/{total_pages}")
            with cols[3]:
                if st.button("Tiếp >"):
                    if current_page < total_pages:
                        st.session_state.current_page = current_page + 1
                        st.rerun()  # Làm mới dữ liệu sau khi thay đổi trang
            with cols[4]:
                if st.button("Trang cuối >>"):
                    st.session_state.current_page = total_pages
                    st.rerun()  # Làm mới dữ liệu sau khi thay đổi trang
        else:
            st.write("Không tìm thấy khách sạn phù hợp.")
    else:
        if "search_results" in st.session_state and not st.session_state.search_results.empty:
            # Hiển thị kết quả phân trang nếu đã có kết quả tìm kiếm
            result_df = st.session_state.search_results
            page_size = 5  # Số lượng khách sạn trên mỗi trang
            total_pages = len(result_df) // page_size + (1 if len(result_df) % page_size > 0 else 0)

            current_page = st.session_state.current_page

            start_idx = (current_page - 1) * page_size
            end_idx = start_idx + page_size
            current_page_data = result_df.iloc[start_idx:end_idx]

            # Hiển thị các khách sạn trên trang hiện tại
            for _, row in current_page_data.iterrows():
                display_hotel_card(row)

            # Thanh chọn trang
            st.markdown("---")
            cols = st.columns(5)

            with cols[0]:
                if st.button("<< Trang đầu"):
                    st.session_state.current_page = 1
                    st.rerun()
            with cols[1]:
                if st.button("< Trước"):
                    if current_page > 1:
                        st.session_state.current_page = current_page - 1
                        st.rerun()
            with cols[2]:
                st.write(f"Trang {current_page}/{total_pages}")
            with cols[3]:
                if st.button("Tiếp >"):
                    if current_page < total_pages:
                        st.session_state.current_page = current_page + 1
                        st.rerun()
            with cols[4]:
                if st.button("Trang cuối >>"):
                    st.session_state.current_page = total_pages
                    st.rerun()
        else:
            st.write("Vui lòng sử dụng bộ lọc để tìm kiếm khách sạn.")
        
# Nút Logout
    st.markdown("---")
    if st.button("Log out"):
        st.session_state.signed_in = False  # Gỡ trạng thái đăng nhập
        st.warning("Bạn đã đăng xuất. Vui lòng đăng nhập lại để tiếp tục.")
        st.rerun()
if __name__ == "__main__":
    main()
