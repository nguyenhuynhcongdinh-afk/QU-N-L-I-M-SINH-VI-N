import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# 1. Tạo dữ liệu sinh viên và DataFrame
data = {
    "Họ và tên": [
        "Nguyễn Văn An", "Trần Thị Bình", "Lê Hoàng Cường", "Phạm Minh Dũng", "Hoàng Thị Hà",
        "Vũ Quốc Huy", "Đặng Thu Lan", "Bùi Đức Long", "Đỗ Ngọc Mai", "Ngô Thành Nam"
    ],
    "Điểm chuyên cần": [9, 8, 10, 7, 9, 8, 10, 6, 9, 7],
    "Điểm giữa kỳ": [8, 7, 9, 6, 8, 7, 9, 5, 8, 6],
    "Điểm cuối kỳ": [9, 8, 8, 7, 9, 8, 10, 6, 9, 7]
}

df = pd.DataFrame(data)

# Tính điểm tổng kết
df["Tong_ket"] = (
    0.2 * df["Điểm chuyên cần"] +
    0.3 * df["Điểm giữa kỳ"] +
    0.5 * df["Điểm cuối kỳ"]
)

# Xếp loại sinh viên
conditions = [
    (df["Tong_ket"] >= 8.0),
    (df["Tong_ket"] >= 6.5) & (df["Tong_ket"] < 8.0),
    (df["Tong_ket"] >= 5.0) & (df["Tong_ket"] < 6.5)
]
labels = ["Giỏi", "Khá", "Trung bình"]
df["Xep_loai"] = np.select(conditions, labels, default="Yếu")

# Đổi tên cột cho đẹp mắt khi hiển thị bảng
df_hien_thi = df.rename(columns={
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

# Hiển thị bảng điểm của 10 sinh viên
st.subheader("Bảng điểm chi tiết 10 sinh viên")
st.dataframe(df_hien_thi, use_container_width=True)

st.markdown("---")

# Thống kê chung
st.subheader("Thống kê kết quả học tập")
diem_tb = df["Tong_ket"].mean()
sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5).sum()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm trung bình của lớp", value=f"{diem_tb:.2f}")
    st.metric(label="Số sinh viên đạt (≥ 5)", value=int(so_sv_dat))

with col2:
    st.markdown(f"**Sinh viên điểm tổng kết cao nhất:** {sv_cao_nhat['Họ và tên']} ({sv_cao_nhat['Tong_ket']:.2f})")
    st.markdown(f"**Sinh viên điểm tổng kết thấp nhất:** {sv_thap_nhat['Họ và tên']} ({sv_thap_nhat['Tong_ket']:.2f})")

st.markdown("---")

# Chọn sinh viên qua danh sách xổ xuống (Selectbox)
st.subheader("Tra cứu thông tin theo sinh viên")
chon_sv = st.selectbox("Chọn tên sinh viên cần xem:", df["Họ và tên"].tolist())

# Lọc thông tin sinh viên được chọn
thong_tin_sv = df[df["Họ và tên"] == chon_sv].iloc[0]

# Hiển thị chi tiết điểm của sinh viên đó
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", thong_tin_sv["Điểm chuyên cần"])
c2.metric("Giữa kỳ", thong_tin_sv["Điểm giữa kỳ"])
c3.metric("Cuối kỳ", thong_tin_sv["Điểm cuối kỳ"])
c4.metric("Tổng kết", f"{thong_tin_sv['Tong_ket']:.2f}")
c5.metric("Xếp loại", thong_tin_sv["Xep_loai"])

st.markdown("---")

# Trực quan hóa biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ cột điểm tổng kết của 10 sinh viên")

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df["Họ và tên"], df["Tong_ket"], color="skyblue")
ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Tên sinh viên")
ax.invert_yaxis()  # Đảo thứ tự để sinh viên đầu tiên nằm trên
ax.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()

st.pyplot(fig)

st.markdown("---")

# Hiển thị thông tin người tạo ở cuối trang với kích thước chữ nhỏ
st.markdown(
    "<p style='text-align: center; font-size: 13px; color: gray;'>"
    "Người thực hiện: <b>Nguyễn Huỳnh Công Định</b> - MSSV: <b>62</b>"
    "</p>", 
    unsafe_allow_html=True
)
