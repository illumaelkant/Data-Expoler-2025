import re
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import datetime

# ----------------------------
# 1. Dữ liệu và Tiền xử lý
# ----------------------------
#data = """
#Mã KH,Khách hàng
#KH-0001,CÔNG TY TNHH ĐẦU TƯ PHÁT TRIỂN CÔNG NGHỆ BÁCH KHOA
#KH-0002,Công ty CP Phát triển Kỹ thuật và Thương mại Tân Đức
#KH-0003,NGƯỜI MUA KHÔNG LẤY HÓA ĐƠN
#KH-0004,CÔNG TY TNHH PRO ACTIVE GLOBAL VIỆT NAM
#KH-0005,Công ty TNHH Công nghệ Ktech
#KH-0006,NGÂN HÀNG TMCP Á CHÂU
#KH-0007,Công ty TNHH Tích Hợp Hệ thống CMC Sài Gòn
#KH-0008,CN Cty TNHH Máy Tính Nét (TP. Hà Nội)
#KH-0009,CỬA HÀNG VI TÍNH PHÁT ĐẠT BÌNH DƯƠNG
#KH-0010,CN CTY TNHH KDDI VN TẠI TP. HCM
#"""

#df = pd.read_csv(pd.io.common.StringIO(data)) # Không cần đọc từ string nữa

def preprocess_customer_name(name):
    name = name.lower()
    name = re.sub(r'[.,"\'-]', '', name)
    name = re.sub(r'tnhh', 'trách nhiệm hữu hạn', name)
    name = re.sub(r'cp', 'cổ phần', name)
    name = re.sub(r'tmcp', 'thương mại cổ phần', name)
    name = re.sub(r'mtv', 'một thành viên', name)
    name = re.sub(r'cn', 'chi nhánh', name)
    name = re.sub(r'cty', 'công ty', name)
    name = re.sub(r'vpdd', 'văn phòng đại diện', name)
    name = re.sub(r'tp', 'thành phố', name)
    name = re.sub(r'hcm', 'hồ chí minh', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


# ----------------------------
# 2. Gán nhãn (Không cần trích xuất đặc trưng, KMeans, PCA)
# ----------------------------
def label_customer(name):
    """Gán nhãn cho khách hàng dựa trên tên."""
    name = preprocess_customer_name(name)

    keywords = {
        'Công nghệ': ['công nghệ', 'tin học', 'viễn thông', 'phần mềm', 'máy tính', 'it', 'hệ thống', 'digital', 'software', 'hardware', 'internet', 'trí tuệ nhân tạo', 'ai', 'machine learning', 'deep learning', 'big data', 'cloud', 'iot', 'blockchain', 'an ninh mạng', 'cybersecurity', 'lập trình', 'coding', 'website', 'ứng dụng', 'app', 'mạng', 'network', 'server', 'data center', 'hạ tầng', 'infrastructure', 'vi mạch', 'chip', 'điện tử', 'electronic', 'tự động hóa', 'automation', 'robotics', 'robot', '3d printing', 'in 3d', 'virtual reality', 'vr', 'augmented reality', 'ar', 'game', 'trò chơi', 'esports', 'thương mại điện tử', 'ecommerce', 'tech', 'innovation', 'startup', 'hệ điều hành', 'operating system', 'database', 'cơ sở dữ liệu'],
        'Dịch vụ': ['dịch vụ', 'tư vấn', 'hỗ trợ', 'giải pháp', 'vận tải', 'logistics', 'giao nhận', 'tiếp vận', 'du lịch', 'khách sạn', 'nhà hàng', 'giải trí', 'sự kiện', 'event', 'marketing', 'quảng cáo', 'truyền thông', 'bán hàng', 'sales', 'chăm sóc khách hàng', 'customer service', 'tài chính', 'ngân hàng', 'bảo hiểm', 'kế toán', 'kiểm toán', 'nhân sự', 'hr', 'đào tạo', 'training', 'giáo dục', 'education', 'y tế', 'healthcare', 'pháp lý', 'legal', 'bất động sản', 'real estate', 'cho thuê', 'rental', 'vệ sinh', 'cleaning', 'bảo trì', 'maintenance', 'sửa chữa', 'repair', 'thiết kế', 'design', 'in ấn', 'printing', 'quản lý', 'management', 'vận hành', 'operation', 'outsourcing'],
        'Năng lượng': ['điện', 'năng lượng', 'dầu khí', 'xăng dầu', 'pin', 'mặt trời', 'gió', 'sinh khối', 'than', 'khí đốt', 'hạt nhân', 'nuclear', 'tái tạo', 'renewable', 'máy phát điện', 'generator', 'biến tần', 'inverter', 'lưới điện', 'power grid', 'trạm biến áp', 'substation', 'tiết kiệm năng lượng', 'energy saving', 'hiệu quả năng lượng', 'energy efficiency', 'bền vững', 'sustainable', 'môi trường', 'environment', 'khí thải', 'emission', 'carbon', 'hóa dầu', 'petrochemical', 'lọc dầu', 'refinery', 'khai thác', 'exploration', 'vận chuyển', 'transportation', 'phân phối', 'distribution', 'cung cấp', 'supply', 'điện lực', 'power', 'ev', 'xe điện', 'trạm sạc', 'charging station'],
        'Sản xuất': ['sản xuất', 'chế tạo', 'công nghiệp', 'nhà máy', 'bao bì', 'may mặc', 'thực phẩm', 'đồ uống', 'gia công', 'vật liệu', 'cơ khí', 'mechanical', 'kim loại', 'metal', 'nhựa', 'plastic', 'gỗ', 'wood', 'dệt may', 'textile', 'da giày', 'footwear', 'hóa chất', 'chemical', 'nông nghiệp', 'agriculture', 'thủy sản', 'seafood', 'chăn nuôi', 'livestock', 'trồng trọt', 'cultivation', 'phân bón', 'fertilizer', 'thuốc trừ sâu', 'pesticide', 'giống cây trồng', 'seed', 'máy móc', 'machinery', 'thiết bị', 'equipment', 'dây chuyền', 'production line', 'kiểm soát chất lượng', 'quality control', 'iso', 'haccp', 'gmp', 'xuất nhập khẩu', 'import export', 'nguyên liệu', 'raw material', 'thành phẩm', 'finished goods'],
        'Xây dựng': ['xây dựng', 'kiến trúc', 'thi công', 'bất động sản', 'công trình', 'nội thất', 'ngoại thất', 'vật liệu xây dựng', 'cầu đường', 'bridge', 'hầm', 'tunnel', 'cao ốc', 'building', 'nhà ở', 'housing', 'chung cư', 'apartment', 'biệt thự', 'villa', 'khu đô thị', 'urban area', 'khu công nghiệp', 'industrial park', 'hạ tầng', 'infrastructure', 'san lấp', 'leveling', 'móng', 'foundation', 'kết cấu', 'structure', 'hoàn thiện', 'finishing', 'sơn', 'paint', 'gạch', 'brick', 'xi măng', 'cement', 'thép', 'steel', 'bê tông', 'concrete', 'cửa', 'door', 'cửa sổ', 'window', 'thiết kế', 'design', 'quy hoạch', 'planning', 'giám sát', 'supervision', 'an toàn lao động', 'work safety'],
    }

    for label, words in keywords.items():
        if any(word in name for word in words):
            return label

    return 'Khác'


# ----------------------------
# 3. Hàm chính (Đọc, Gán nhãn, Ghi file)
# ----------------------------
def main():
    """Hàm chính để đọc, xử lý và ghi dữ liệu."""
    try:
        # Đọc file CSV
        df = pd.read_csv("khachhanginput.csv")

        # Kiểm tra cột 'Khách hàng'
        if "Khách hàng" not in df.columns:
            raise ValueError("File CSV phải có cột 'Khách hàng'.")

        # Áp dụng hàm gán nhãn
        df['Nhãn'] = df['Khách hàng'].apply(label_customer)

        # Tạo tên file output dựa trên ngày giờ
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        output_filename = f"khachhangoutput_{timestamp}.csv"

          # Kiểm tra và tạo thư mục 'output_files' nếu nó không tồn tại.
        output_dir = "output_files"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Ghi ra file, đường dẫn tương đối đến thư mục.
        df.to_csv(os.path.join(output_dir, output_filename), index=False)
        print(f"Gán nhãn thành công! Kết quả đã được ghi vào file {output_filename}")

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file khachhanginput.csv")
    except ValueError as ve:
         print(f"Lỗi: {ve}")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")

if __name__ == "__main__":
    main()
