import pandas as pd
import re

# Load the data
df = pd.read_csv('sanphamin.csv', encoding='utf-8-sig')
df.columns = df.columns.str.strip()

# --- Keyword Lists (Expanded and Refined) ---
office_keywords = [
    "office", "word", "excel", "powerpoint", "outlook", "visio", "publisher", "access",
    "office 365", "o365", "microsoft 365", "project", "sharepoint", "exchgstdcal",
    "officestd", "officemacstd", "prjct",  "officestd", 'onedrive', "teams",
    "home and business", "home & business", "home and student", "home & student",
    "professional plus", "proplus", "personal",  "business premium",
    "business essentials", "plan e3", "pro plus", "business basic", "apps for enterprise",
    "365", 'exchange online', 'skype for business', "microsoft office", "ms office",
    "onenote", "publisher", "access", "office web apps", "owa", "office online",
    "exchange server",  "project server","visio viewer", "office mobile",
    "word for windows", "excel for windows", "powerpoint for windows", "outlook for windows",
    "office 365 proplus", "mail merge toolkit", 'office home', 'office professional',
      'business standard','business', 'essentials', 'microsoft family',
    'onenote for windows 10', 'onenote for mac','onenote for web',
    'visio pro', 'visio standard','project pro', 'project standard',
    'excel services','powerpoint services','word automation services',
    "microsoft word", "microsoft excel", "microsoft powerpoint", "microsoft outlook",
    'autocad lt', "project online", "visio online", 'sharepointstdcal' # Added AutoCAD LT, more specific MS apps
]

adobe_keywords = [
    "adobe", "photoshop", "illustrator", "acrobat", "indesign", "after effects",
    "premiere", "lightroom", "creative cloud", "audition", "dreamweaver",
    "photoshop elements", "premiere elements", "creative suite", "cc for teams",
    "acrobat pro", "acrobat standard", "lightroom classic", "adobe stock",
    "dimension", "xd", "animate", "bridge", "incopy", "media encoder",
     "substance", "aero", "fresco", "adobe fonts", "behance", "portfolio", "spark",
    "adobe creative cloud",  "creative cloud all apps",
    "single app", "acrobat reader", "adobe scan", "adobe sign",
     "pdf", ".pdf", ".psd", ".ai", ".indd",  "eps", "svg", "tiff", "jpeg", "png", "gif", "raw", "dng",
      "vector graphics", "image editing", "video editing","motion graphics",
     "digital publishing",  "graphic design", "illustration", "photography",
    "masking", "animation", "3d modeling",  "web development", "html", "css", "javascript",
    "user interface", "user experience", "adobe xd",
    'adobe aero', "adobe fresco", 'illustrator on the ipad', 'photoshop on the ipad',
    'adobe creative cloud express', 'adobe express',  'acrobat pro dc', 'acrobat standard dc',
     "adobe document cloud", 'pdf services api', "adobe photoshop camera",  'content-aware fill',
     'neural filters','sky replacement','object selection tool','liquify tool'
]


server_keywords = [
     "windows svr", "sql", "sqlsvr", "exchgsvr", "sharepoint", "windows server",
    "red hat", "vmware", "linux server", "database", "data center", "datactr",
    "hyper-v", "system center", "biztalk", "remote desktop", "rds", "azure", "cloud",
    'virtualization', "active directory", "dns", "dhcp", "iis",
    "exchange server", "sql server", "mysql", "oracle", "veeam", "acronis", "veritas",
     "vcenter", 'vsphere','esxi', "linux","mdaemon",
    "altova",  "splunk", "manageengine", "nagios", "opmanager", "sqlsvrstd",
    "sqlsvrent", "winsvrstd", "winsvressntls", "winsvrdatactr",
     "windows server 2019", "windows server 2016",  "windows server 2012 r2",
      'red hat enterprise linux', 'rhel', 'centos', 'ubuntu server',
    'debian', 'suse linux enterprise server', 'sles', 'oracle linux',
     'server administration', 'system administration',  'database administration',
     'clustering', 'high availability', 'disaster recovery', 'backup and recovery',
     'powershell',  'scripting', 'automation',  'server core', 'nano server',
    ".msc", ".ps1", ".bat", ".sh", ".sql", ".rdp", 'sql server management studio', 'ssms',
    'server manager', 'hyper-v manager',  'sccm', 'scom', 'scvmm',
    'veeam backup & replication', 'acronis backup',  'mdt', 'wds',
    'group policy', 'gpo',  'wsus','windows admin center',
     "windows server essentials", "sql server express", 'sql server developer',
    'sql server enterprise', 'sql server standard','sqlcal', "exchange standard cal",
     "microsoft identity manager", 'mim', 'radius manager', 'web log explorer',
    "securitygateway", "backupassist", "xyplorer", "think-cell", "teamstudio ciao!", "nxpowerlite",
        "coldfusion", "radius manager pro","primavera","ip-guard", "veeam agent", "workshare",
]


antivirus_keywords = [
    "antivirus", "kaspersky", "eset", "norton", "bitdefender", "avg", "mcafee",
    "trend micro", "bkav", "security", "av", "endpoint protection",
    "internet security", "total security", "cybersecurity",
    "malware", "virus",  "firewall", "anti-malware", "anti-spam",
    "spyware", "ransomware", "phishing", "vpn", "web protection", "email protection",
    "data loss prevention", "dlp", "encryption","utm",  'symc endpoint',
    "ksos", "kis",  "nod32","titanium maximum security",
    "security software", "endpoint protection platform", "epp",
      "malware analysis",  "heuristic analysis",  "machine learning",
      "cloud security", "network security", "data security",  "mobile security",
    "web filtering",  "content filtering", "personal firewall", "network firewall",
      "vulnerability scanning", "penetration testing",  "compliance", "gdpr", "hipaa",
      "kaspersky endpoint security",  "kaspersky total security",
      "eset endpoint antivirus", "eset internet security",
      "norton antivirus plus", "norton 360",
      "bitdefender gravityzone", "bitdefender total security",
        "avg antivirus", "avg internet security",
    "trend micro maximum security",   "bkav pro", "bkav internet security",
     "sophos endpoint protection",'webroot secureanywhere', 'malwarebytes', 'avast',
     "zero-day protection", "exploit protection", "anti-phishing", "anti-ransomware",
     ".exe", ".dll", ".sys",  'central endpoint standard', 'mfe', 'kaspersky hybrid cloud security'
]

hardware_components = [
    "cpu", "bộ xử lý", "chip", "vi xử lý", "intel", "amd", "ryzen", "xeon", "core i", "pentium"
]

hardware_storage = [
    "ổ cứng", "hdd", "ssd", "bộ nhớ", "ram",  "ổ cứng gắn ngoài",
    "western digital", "seagate", "samsung", "kingston", 'bộ nhớ trong máy tính xách tay',
      'bộ nhớ trong apacer','ổ cứng western', 'ổ cứng ssd transcend', 'ổ cứng ssd lite-on',
    "ổ cứng ssd kingston", 'ổ cứng seagate', 'thẻ nhớ', 'bộ lưu trữ'
]

hardware_peripherals = [
    "bàn phím", "chuột", "màn hình", "tai nghe", "loa", "webcam", 'bàn phím genius',
    'chuột genius', 'chuột logitech',  'màn hình dell', 'màn hình samsung',
     'màn hình lcd', 'màn hình led',  'laptop', 'chuột logitech'
]

hardware_networking = [
   "bộ định tuyến",  "thiết bị mạng", "modem", "router", "switch",
    "access point", "wifi", "bộ phát wifi", "bộ thu wifi", "cáp mạng","thiết bị chia mạng",
      "bộ chuyển mạch hp", "bộ chuyển mạch hpe",  'bộ chuyển mạch aruba','thiết bị chuyển mạch'
]

hardware_pc = [
    "máy tính", "máy tính để bàn", "máy tính xách tay","bộ máy tính",
      "máy tính dell", "máy tính hp",   "máy tính chủ", "server", 'workstation','desktop',
    'vỏ máy', 'vỏ case',   "bo mạch", "card", "cạc", 'bộ nguồn', 'nguồn máy tính',
    'bộ tản nhiệt',   "bảng mạch chính", 'bảng mạch', "pin", 'pin laptop',
]

hardware_other = [
    "máy in", "máy scan", "camera", "ups", 'bộ lưu điện', 'apc',  'emerson','máy quét',
    "thiết bị tường lửa", 'firewall',  "tủ máy chủ",'bộ thu phát',"camera quan sát",
    "bộ chia", 'cáp', 'cáp hdmi',  'cáp vga', 'cáp usb','đầu chuyển đổi', 'adapter',
     "điện thoại", "đtdđ", "iphone", "samsung", "xiaomi", "lenovo", "dell", "hp",
     'màn hình', 'bộ micro',   'máy chiếu', 'giá treo', 'màn chiếu', 'dây hdmi',
    'máy tính bảng','máy in laser',   'máy ảnh','điện thoại di động',   'bộ kit',
]

hardware_services = [
     "dịch vụ", "triển khai", "cài đặt", "hỗ trợ", "bảo hành", "bảo trì", 'hỗ trợ kỹ thuật',
    "gia hạn", "tên miền", "đăng ký", "kỹ thuật", "sửa", "chấm công", 'tư vấn', 'thiết kế',
      'vận hành','cho thuê',  'duy trì',
]



def classify_product(product_name):
    name = product_name.lower()

    if any(keyword in name for keyword in office_keywords + adobe_keywords):
        return "Phần mềm văn phòng"
    elif any(keyword in name for keyword in server_keywords):
        return "Phần mềm server"  # Corrected label
    elif any(keyword in name for keyword in antivirus_keywords):
        return "Phần mềm Bảo mật"  # Corrected label
    elif any(keyword in name for keyword in hardware_components + hardware_storage + hardware_peripherals + hardware_networking + hardware_pc + hardware_other+hardware_services):
        return "Phần cứng"  # Simplified hardware label
    else:
        return "Khác"

# --- Apply Classification and Save ---

# Apply the classification function to create the 'Nhãn' column.  MUCH better than renaming!
df['Nhãn'] = df['Sản phẩm'].apply(classify_product)

# Clean the 'Giá vốn' column, handling non-numeric values robustly.
def clean_price(x):
    x = str(x).replace(",", "").replace(".", "").strip()  # Remove commas, periods, and spaces
    if x.isdigit():
        return int(x)
    return 0  # Return 0 for non-numeric or empty values

df['Giá vốn_clean'] = df['Giá vốn'].apply(clean_price)
# Save to a new CSV file
df.to_csv('spout.csv', index=False, encoding='utf-8-sig')

print("Classification complete.  Results saved to 'spout.csv'")