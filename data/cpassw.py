import pikepdf
from tqdm import tqdm

passwords = "C:\\Users\\caodu\\Downloads\\rockyou.txt"  # Thay bằng danh sách các mật khẩu bạn muốn thử

file_path = "C:\\Users\\caodu\\Downloads\\Đề thi N3 các năm Yuuki Bùi-20240113T234248Z-001\\Đề thi N3 các năm Yuuki Bùi\\N3 12-2010 (thiếu đề thi)\\Script Nghe N3 T12-2010.pdf"  # Thay bằng đường dẫn đến file PDF của bạn

for password in tqdm(passwords, desc="Decrypting PDF", unit="password"):
    try:
        # Thực hiện mở file PDF với mật khẩu hiện tại
        pdf = pikepdf.Pdf.open(file_path, password=password)
        # Nếu không có lỗi, in mật khẩu và kết thúc vòng lặp
        print(f"Password found: {password}")
        break
    except pikepdf.PasswordError:
        # Nếu có lỗi PasswordError, tiếp tục với mật khẩu tiếp theo
        pass
    except Exception as e:
        # In ra lỗi để kiểm tra nguyên nhân
        print(f"Error: {e}")
        pass