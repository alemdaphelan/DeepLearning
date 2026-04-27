import cv2
from ultralytics import YOLO
import easyocr

# 1. TẢI BỘ NÃO AI
print("--- ĐANG TẢI YOLO ---")
model = YOLO('best.pt') 

# 2. ĐỌC ẢNH VÀ NHẬN DIỆN
print("\n--- ĐANG TÌM BIỂN SỐ ---")
img = cv2.imread('nhieubien.jpg') 

results = model(img, conf=0.1, imgsz=1280) 

# Lấy ra TOÀN BỘ danh sách các khung xanh 
danh_sach_boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

print(f" Phát hiện thấy {len(danh_sach_boxes)} biển số trong bức ảnh! ")

# Khởi tạo công cụ đọc chữ (EasyOCR)
print("\n--- ĐANG ĐỌC CHỮ (EasyOCR) ---")
reader = easyocr.Reader(['vi', 'en'])

# 3. DÙNG VÒNG LẶP XỬ LÝ TỪNG BIỂN SỐ
for thu_tu, box in enumerate(danh_sach_boxes):
    x1, y1, x2, y2 = box
    
    # Cắt biển số hiện tại
    bien_so_cat_duoc = img[y1:y2, x1:x2]
    
    # Chuyển trắng đen để EasyOCR không bị lỗi và đọc chuẩn hơn
    bien_so_gray = cv2.cvtColor(bien_so_cat_duoc, cv2.COLOR_BGR2GRAY)
    
    # Đọc chữ
    ket_qua = reader.readtext(bien_so_gray)
    
    bien_so_hoan_chinh = ""
    for (toado_chu, text, do_tin_cay) in ket_qua:
        # Lọc bỏ các ký tự rác, chỉ giữ lại chữ cái và số
        chuoi_sach = "".join(e for e in text if e.isalnum())
        bien_so_hoan_chinh += chuoi_sach + "-"
    
    bien_so_hoan_chinh = bien_so_hoan_chinh.strip('-')
    
    print(f" Biển số thứ {thu_tu + 1}: {bien_so_hoan_chinh}")
    
    # Vẽ khung xanh và viết chữ lên bức ảnh gốc
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, bien_so_hoan_chinh, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

print("\n" + "="*40)
print("Hoàn tất xử lý toàn bộ ảnh!")
print("="*40)

# 4. HIỂN THỊ KẾT QUẢ (CHỐNG TRÀN MÀN HÌNH)
ten_cua_so = "Ket qua Nhan dien - Multi-Plate"

# Bật tính năng cho phép thay đổi kích thước cửa sổ
cv2.namedWindow(ten_cua_so, cv2.WINDOW_NORMAL) 

# Ép cửa sổ mở ra ở kích thước 1280x720 cho dễ nhìn
cv2.resizeWindow(ten_cua_so, 1280, 720) 

# Hiển thị ảnh và chờ người dùng bấm phím để thoát
cv2.imshow(ten_cua_so, img)
cv2.waitKey(0)

# Dọn dẹp sạch sẽ bộ nhớ sau khi tắt ảnh
cv2.destroyAllWindows()