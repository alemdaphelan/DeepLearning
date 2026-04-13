# Báo cáo Tiến độ Tuần 2: Huấn luyện Mô hình YOLOv8
Công việc đã thực hiện:

-Thu thập và chuẩn hóa bộ dữ liệu 8.400 ảnh biển số xe Việt Nam (nguồn: Roboflow).
-Viết script huấn luyện trên Google Colab (sử dụng GPU T4).
-Hoàn tất quá trình training với kiến trúc YOLOv8n

Kết quả đạt được (Artifacts):

-File trọng số tốt nhất được lưu tại: /training_module/best.pt
-Đính kèm các biểu đồ đánh giá (Loss curve, mAP50) trong thư mục /results

Kế hoạch Tuần tiếp theo:

-Xây dựng script Python sử dụng OpenCV cắt ảnh biển số từ Bounding Box của YOLO.
-Tích hợp module OCR để đọc ký tự.
