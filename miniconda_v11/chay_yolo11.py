import cv2
from ultralytics import YOLO
import easyocr


print("--- ĐANG TẢI YOLO11 ---")
model = YOLO('yolo11_best.pt') 


print("\n--- ĐANG TÌM BIỂN SỐ ---")
img = cv2.imread('nhieubien.jpg') 


results = model(img, conf=0.15, imgsz=1280) 

danh_sach_boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
print(f" Phát hiện thấy {len(danh_sach_boxes)} biển số trong bức ảnh! ")

print("\n--- ĐANG ĐỌC CHỮ (EasyOCR) ---")
reader = easyocr.Reader(['vi', 'en'])


for thu_tu, box in enumerate(danh_sach_boxes):
    x1, y1, x2, y2 = box
    
    bien_so_cat_duoc = img[y1:y2, x1:x2]
    bien_so_gray = cv2.cvtColor(bien_so_cat_duoc, cv2.COLOR_BGR2GRAY)
    
    ket_qua = reader.readtext(bien_so_gray)
    
    bien_so_hoan_chinh = ""
    for (toado_chu, text, do_tin_cay) in ket_qua:
        chuoi_sach = "".join(e for e in text if e.isalnum())
        bien_so_hoan_chinh += chuoi_sach + "-"
    
    bien_so_hoan_chinh = bien_so_hoan_chinh.strip('-')
    
    print(f" Biển số thứ {thu_tu + 1}: {bien_so_hoan_chinh}")
    
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, bien_so_hoan_chinh, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

print("\n" + "="*40)
print("Hoàn tất xử lý bằng YOLO11!")
print("="*40)


ten_cua_so = "Ket qua Nhan dien - YOLO11"
cv2.namedWindow(ten_cua_so, cv2.WINDOW_NORMAL) 
cv2.resizeWindow(ten_cua_so, 1280, 720) 
cv2.imshow(ten_cua_so, img)
cv2.waitKey(0)
cv2.destroyAllWindows()