# Bài tập lớn python nhóm 16: Ứng dụng desktop Python scraping
## I. Chức năng:
### - Lấy dữ liệu sản phẩm từ shopee, hiển thị, sắp xếp và lưu vào file csv
### - Download ảnh từ 1 link cho trước
## II.Yêu cầu tài nguyên:
- Các thư viện sau:
    - BeautifulSoup
    - Selenium
    - tkinter
    - PIL
    - requests
    - tqdm
    - lxml
- Đối với cài đặt các thư viện trên: Các bạn vào cmd và copy paste đoạn code sau
```
    pip install -r requirements.txt
```
- Deprecated: Đối với trường hợp khi run bị lỗi, các bạn cần lên trang chủ [Download_Chromedriver](https://chromedriver.chromium.org/downloads), chọn phiên bản tương thích với chương trình Chrome ở máy và thay thế vào thư mục `data/Chromedriver`
> Bản Selenium mới nhất hiện không cần webdriver. Shopee cập nhật liên tục nên sẽ có thay đổi các bạn hãy tủy chỉnh code để phù hợp.
## III. Chạy ứng dụng
Sau khi làm theo hướng dẫn trên, các bạn run file main.py