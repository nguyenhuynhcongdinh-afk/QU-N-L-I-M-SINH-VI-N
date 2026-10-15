import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Tiêu đề ứng dụng
st.title("Ứng dụng Quản lý và Thống kê Điểm Sinh viên")
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

# Yêu cầu 1: Hiển thị bảng dữ liệu ban đầu
st.subheader("1. Bảng dữ liệu điểm sinh viên")
st.dataframe(df, use_container_width=True)

# Yêu cầu 2: Tính điểm tổng kết
df["Tong_ket"] = (
    0.2 * df["Điểm chuyên cần"] +
    0.3 * df["Điểm giữa kỳ"] +
    0.5 * df["Điểm cuối kỳ"]
)

st.subheader("2. Bảng dữ liệu sau khi tính Điểm tổng kết")
st.dataframe(df, use_container_width=True)

# Yêu cầu 3: Xếp loại sinh viên
conditions = [
    (df["Tong_ket"] >= 8.0),
    (df["Tong_ket"] >= 6.5) & (df["Tong_ket"] < 8.0),
    (df["Tong_ket"] >= 5.0) & (df["Tong_ket"] < 6.5)
]
labels = ["Giỏi", "Khá", "Trung bình"]

df["Xep_loai"] = np.select(conditions, labels, default="Yếu")

st.subheader("3. Bảng dữ liệu sau khi Xếp loại")
st.dataframe(df, use_container_width=True)

# Yêu cầu 4: Thống kê
st.subheader("4. Thống kê kết quả học tập")

diem_tb = df["Tong_ket"].mean()
sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5).sum()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm tổng kết trung bình lớp", value=f"{diem_tb:.2f}")
    st.metric(label="Số sinh viên đạt (≥ 5)", value=int(so_sv_dat))

with col2:
    st.markdown(f"**Sinh viên điểm cao nhất:** {sv_cao_nhat['Họ và tên']} ({sv_cao_nhat['Tong_ket']})")
    st.markdown(f"**Sinh viên điểm thấp nhất:** {sv_thap_nhat['Họ and tên'] if 'Họ and tên' in sv_thap_nhat else sv_thap_nhat['Họ và tên']} ({sv_thap_nhat['Tong_ket']})")

# Yêu cầu 5: Trực quan hóa biểu đồ cột ngang
st.subheader("5. Trực quan hóa điểm tổng kết")

df_10 = df.head(10)
ten_sv = df_10["Họ và tên"]
diem = df_10["Tong_ket"]

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(ten_sv, diem)
ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Tên sinh viên")
ax.invert_yaxis()  # Đảo thứ tự để sinh viên đầu tiên nằm trên
ax.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()

# Hiển thị biểu đồ trong Streamlit
st.pyplot(fig)