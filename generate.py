import csv
import os

# 1. 設定檔案名稱與產出目錄
# 確保你的 colors.csv 檔案名稱一模一樣
input_csv = 'colors.csv'
output_dir = '_colors'

# 2. 如果 _colors 資料夾不存在，就自動建立
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"已建立新資料夾：{output_dir}")

# 3. 打開 CSV 檔案開始讀取 (加上 encoding='utf-8-sig' 確保 Windows Excel 中文不亂碼)
try:
    with open(input_csv, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        count = 0
        for row in reader:
            code = row.get('編碼', '').strip()
            name_zh = row.get('繁體中文色名', '').strip()
            status = row.get('狀態', 'N').strip().upper()
            
            # 如果編碼是空的就跳過
            if not code:
                continue
                
            # 判斷是否上架 (Y 才顯示，其餘隱藏)
            published = "true" if status == 'Y' else "false"
            
            # 4. 準備要寫入 Markdown 的內容 (這是給 GitHub Pages 讀的身分證)
            md_content = f"""---
layout: color-single
title: "{code}"
title_zh: "{name_zh}"
code: "{code}"
published: {published}
---
"""
            
            # 5. 將內容存成 .md 檔案
            file_path = os.path.join(output_dir, f"{code}.md")
            with open(file_path, 'w', encoding='utf-8') as mdfile:
                mdfile.write(md_content)
            count += 1

    print(f"✅ 成功！已從 CSV 生成 {count} 個色卡檔案至 {output_dir} 資料夾。")

except FileNotFoundError:
    print(f"❌ 錯誤：找不到 {input_csv}，請確認檔案是否放在同一個資料夾。")