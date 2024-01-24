import pandas as pd
import re
import tkinter as tk
import pandas as pd
import time
import openpyxl
from openpyxl import load_workbook

# Đo thời gian bắt đầu
start_time = time.time()

file_path = "D:\\0. data\\2023data.csv"


def read_csv(file_path):
    """CSVファイルを読み込んでDataFrameを返す。"""
    df = pd.read_csv(file_path, usecols=[0, 1, 2, 3, 4, 5, 6, 7])
    if df.index.name is not None:
        df = df.reset_index(drop=True)
    df.columns = ['inandoutid', 'inlocation', 'intime', 'outlocation', 'outtime', 'carinfo', 'parkingtime', 'parkingfee']

    df['intime'] = pd.to_datetime(df['intime'])
    df['outtime'] = pd.to_datetime(df['outtime'])
    df['parkingfee'] = df['parkingfee'].replace('[\¥,]', '', regex=True)
    df['parkingfee'] = pd.to_numeric(df['parkingfee'], errors='coerce')
    df = df.dropna(subset=['parkingfee'])
    df['parkingfee'] = df['parkingfee'].astype(int)

    # Add 'weekday' and 'hour' columns
    df['weekday'] = df['intime'].dt.day_name()
    df['hour'] = df['intime'].dt.hour


    return df
# Đọc dữ liệu từ file CSV
df = pd.read_csv(file_path)

# Chuyển cột 'intime' và 'outtime' sang định dạng datetime
df['intime'] = pd.to_datetime(df['intime'])
df['outtime'] = pd.to_datetime(df['outtime'])

# Lọc dữ liệu theo năm 2023 và 2024
df_2023 = df[df['intime'].dt.year == 2023]
df_2024 = df[df['intime'].dt.year == 2024]

#df_2024 = df[(df['intime'] >= '2024-01-01') & (df['intime'] < '2024-01-31')]

# Tính tổng số lượng khách và doanh thu cho mỗi năm
total_customers_2023 = df_2023.shape[0]
total_customers_2024 = df_2024.shape[0]

total_revenue_2023 = df_2023['parkingfee'].sum()
total_revenue_2024 = df_2024['parkingfee'].sum()

# Tạo dataframe mới
result_df = pd.DataFrame({
    'Year': [2023, 2024],
    'Total Customers': [total_customers_2023, total_customers_2024],
    'Total Revenue': [total_revenue_2023, total_revenue_2024]
})


# Tạo hàm để tính tổng số lượng khách và tổng doanh thu theo tháng
def calculate_monthly_totals(df):
    # Tạo một bản sao của DataFrame để tránh lỗi SettingWithCopyWarning
    df = df.copy()
    
    # Thêm cột 'Month' vào DataFrame mới
    df['datetime'] = df['intime'].dt.to_period('M')
    
    # Tính tổng số lượng khách và tổng doanh thu theo tháng
    monthly_totals = df.groupby('datetime').agg({'intime': 'count', 'parkingfee': 'sum'}).reset_index()
    
    # Đổi tên cột
    monthly_totals.columns = ['datetime', 'Total Customers', 'Total Revenue']
    
    # Bổ sung: Sắp xếp lại theo thời gian
    monthly_totals = monthly_totals.sort_values(by='datetime').reset_index(drop=True)
    # Bổ sung: In định dạng ngày tháng năm
    print("Định dạng ngày tháng năm của dữ liệu năm 2024:")
    print(df[df['intime'].dt.year == 2024]['intime'])
    return monthly_totals

# Tính tổng số lượng khách và tổng doanh thu theo tháng cho năm 2023 và 2024
monthly_totals_2023 = calculate_monthly_totals(df_2023)
monthly_totals_2024 = calculate_monthly_totals(df_2024)


# Hàm để tách thành phố từ biển số xe
def extract_city(license_plate):
    match = re.search(r'([一-龯]+)(\d+)', license_plate)
    if match:
        city = match.group(1)
        return city
    else:
        return None

# Tạo bảng dữ liệu cho Bảng 1
table1_data = {'datetime': [], 'City': [], 'Total Cars': []}

# Tạo bảng dữ liệu cho Bảng 2
table2_data = {'datetime': [], 'City': [], 'Total Cars': []}

# Lặp qua từng dòng dữ liệu
for index, row in df.iterrows():
    license_plate = row['carinfo']
    city = extract_city(license_plate)

    if city:
        # Bảng 1: Thêm vào dữ liệu
        year = row['intime'].year
        table1_data['datetime'].append(pd.to_datetime(str(year), format='%Y'))
        table1_data['City'].append(city)
        table1_data['Total Cars'].append(1)

        # Bảng 2: Thêm vào dữ liệu
        year_month = f"{row['intime'].year}/{row['intime'].month:02d}"
        table2_data['datetime'].append(pd.to_datetime(year_month, format='%Y/%m'))
        table2_data['City'].append(city)
        table2_data['Total Cars'].append(1)

# Tạo DataFrame cho Bảng 1
table1 = pd.DataFrame(table1_data)

# Tạo DataFrame cho Bảng 2
table2 = pd.DataFrame(table2_data)

# Tính tổng số xe cho mỗi thành phố trong Bảng 1
table1 = table1.groupby(['datetime', 'City']).sum().reset_index()

# Tính tổng số xe cho mỗi thành phố trong Bảng 2
table2 = table2.groupby(['datetime', 'City']).sum().reset_index()

# Đọc CSV và in DataFrame
data_frame = read_csv(file_path)
print(data_frame.head(10))

# In ra kết quả
print(result_df)
print("2023:")
print(monthly_totals_2023)
print("\n2024:")
print(monthly_totals_2024)
print("Bảng 1:")
print(table1)

print("\nBảng 2:")
print(table2)

# Đo thời gian kết thúc
end_time = time.time()
execution_time = end_time - start_time
print(f"Thời gian thực thi: {execution_time:.2f} giây")