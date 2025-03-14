import re
import pandas as pd

# ----------------------------
# 1. Dữ liệu và Tiền xử lý
# ----------------------------

# Đọc dữ liệu từ file CSV
try:
    df = pd.read_csv("khachhanginput.csv")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file khachhanginput.csv")
    exit()
except pd.errors.EmptyDataError:
    print("Lỗi: File khachhanginput.csv trống.")
    exit()
except pd.errors.ParserError:
    print("Lỗi: File khachhanginput.csv có định dạng không hợp lệ.")
    exit()


def preprocess_customer_name(name):
    if not isinstance(name, str):  # Kiểm tra kiểu dữ liệu
        return ""  # Hoặc giá trị mặc định khác
    name = name.lower()
    name = re.sub(r'[.,"\'-]', "", name)
    name = re.sub(r"tnhh", "trách nhiệm hữu hạn", name)
    name = re.sub(r"cp", "cổ phần", name)
    name = re.sub(r"tmcp", "thương mại cổ phần", name)
    name = re.sub(r"mtv", "một thành viên", name)
    name = re.sub(r"cn", "chi nhánh", name)
    name = re.sub(r"cty", "công ty", name)
    name = re.sub(r"vpdd", "văn phòng đại diện", name)
    name = re.sub(r"tp", "thành phố", name)
    name = re.sub(r"hcm", "hồ chí minh", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


# Áp dụng tiền xử lý cho cột 'Khách hàng' (hoặc cột tương ứng)
try:
    df["Khách hàng"] = df["Khách hàng"].apply(preprocess_customer_name)
except KeyError:
    print("Lỗi: Không tìm thấy cột 'Khách hàng' trong file CSV.")
    exit()


# ----------------------------
# 2. Trích xuất đặc trưng (Chỉ loại hình doanh nghiệp)
# ----------------------------
def extract_features(name):
    features = {}
    features["is_tnhh"] = 1 if "trách nhiệm hữu hạn" in name else 0
    features["is_cp"] = 1 if "cổ phần" in name else 0
    features["is_dntn"] = 1 if "doanh nghiệp tư nhân" in name else 0
    features["is_cn"] = 1 if "chi nhánh" in name else 0
    features["is_vpdd"] = 1 if "văn phòng đại diện" in name else 0
    features["is_hkd"] = 1 if ("hộ kinh doanh" in name or "cửa hàng" in name) else 0
    features["is_khac"] = (
        1
        if (
            features["is_tnhh"] == 0
            and features["is_cp"] == 0
            and features["is_dntn"] == 0
            and features["is_cn"] == 0
            and features["is_vpdd"] == 0
            and features["is_hkd"] == 0
        )
        else 0
    )
    return features


feature_list = df["Khách hàng"].apply(extract_features).tolist()
feature_df = pd.DataFrame(feature_list)
df = pd.concat([df, feature_df], axis=1)

# ----------------------------
# 3. Phân loại (Gán nhãn dựa trên đặc trưng)
# ----------------------------


def classify_customer(row):
    if row["is_tnhh"]:
        return "TNHH"
    elif row["is_cp"]:
        return "Cổ phần"
    elif row["is_dntn"]:
        return "DNTN"
    elif row["is_cn"]:
        return "Chi nhánh"
    elif row["is_vpdd"]:
        return "VPĐD"
    elif row["is_hkd"]:
        return "Hộ KD/Cửa hàng"
    else:
        return "Khác"


df["Phân loại"] = df.apply(classify_customer, axis=1)


# ----------------------------
# 4. Lưu kết quả
# ----------------------------
try:
    df.to_csv("output.csv", index=False)
    print("Đã phân loại và lưu kết quả vào file output.csv")
except Exception as e:
    print(f"Lỗi khi ghi file: {e}")

# In ra màn hình
print(df.head())
