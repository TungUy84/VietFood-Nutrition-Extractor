# VietFood Nutrition Extractor (Trích xuất dữ liệu dinh dưỡng thực phẩm Việt Nam)

Dự án này là một công cụ Python giúp trích xuất dữ liệu từ file PDF "Bảng thành phần dinh dưỡng thực phẩm Việt Nam" và chuyển đổi sang định dạng CSV có cấu trúc để dễ dàng sử dụng trong các ứng dụng phân tích hoặc cơ sở dữ liệu.

Tên gợi ý cho repository: **`VietFood-Nutrition-Extractor`** hoặc **`VN-Food-Composition-Parser`**.

## 🚀 Tính năng

*   **Trích xuất bảng**: Tự động nhận diện và trích xuất bảng dữ liệu dinh dưỡng từ các trang PDF.
*   **Xử lý Font TCVN3**: Tích hợp bảng mã chuyển đổi tùy chỉnh để xử lý lỗi font (TCVN3/ABC) thường gặp trong các tài liệu cũ của Việt Nam (sửa lỗi hiển thị như "Thịt gà" thay vì "ThÞt gμ").
*   **Chuẩn hóa dữ liệu**:
    *   Mapping các cột dinh dưỡng quan trọng (Energy, Protein, Fat, Carb, Vitamin...).
    *   Tự động sửa các lỗi chính tả phổ biến trong tên thực phẩm (ví dụ: "Bánh mì", "Sữa chua", "Rau dền"...).
*   **Output chuẩn**: Xuất ra file `.csv` encoding UTF-8, sẵn sàng import vào Excel hoặc SQL.

## 📋 Yêu cầu hệ thống

*   Python 3.x
*   Các thư viện Python:
    *   `pdfplumber`
    *   `pandas`

## 🛠 Cài đặt

1.  Clone project này về máy:
    ```bash
    git clone https://github.com/username/VietFood-Nutrition-Extractor.git
    cd VietFood-Nutrition-Extractor
    ```

2.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```

3.  Đảm bảo file PDF nguồn (ví dụ `bản thành phần dinh dưỡng.pdf`) nằm trong cùng thư mục.

## ▶️ Sử dụng

Chạy script chính để thực hiện chuyển đổi:

```bash
python pdf_to_csv.py
```

Sau khi chạy xong, file kết quả `raw_food.csv` sẽ được tạo ra với các cột:
*   `Code`: Mã số thực phẩm
*   `Name`: Tên thực phẩm (Tiếng Việt)
*   `Unit`: Đơn vị tính (thường là 100g)
*   `Energy_Kcal`: Năng lượng (Kcal)
*   `Protein_g`: Đạm (g)
*   `Fat_g`: Béo (g)
*   `Carb_g`: Bột đường (g)
*   ... và các vi chất khác (Canxi, Sắt, Vitamin A, C, B1, B2).

## 🐛 Xử lý lỗi Font (Encoding)

Dự án này chứa một module xử lý font TCVN3 đặc biệt trong file `pdf_to_csv.py`. Do file PDF gốc sử dụng encoding cũ và không đồng nhất, script sử dụng một từ điển `tcvn3_map` được xây dựng thủ công để map lại các byte ký tự sang Unicode tiếng Việt chính xác.

## 🤝 Đóng góp

Nếu bạn phát hiện thêm lỗi chính tả hoặc lỗi hiển thị tên thực phẩm, hãy tạo Issue hoặc Pull Request để cập nhật thêm vào từ điển mapping.

## License

MIT License
