import csv
import os

# ==========================================
# 1. 檔案與資料夾設定
# ==========================================
input_csv = 'master_colors.csv'
output_dir = '_colors'  

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ==========================================
# 2. 開始讀取 CSV 並生成檔案
# ==========================================
print("🚀 開始讀取資料並生成色卡檔案...\n")

try:
    with open(input_csv, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        count = 0
        for row in reader:
            code = row.get('色號', '').strip()
            name_zh = row.get('中文名', '').strip()
            name_en = row.get('英文名', '').strip()
            series = row.get('系列', 'AKS COLORS').strip()
            
            if not code:
                continue

            # ------------------------------------------
            # 3. SEO 標題與描述 (修正版)
            # ------------------------------------------
            # 移除「頂級」二字
            seo_title = f"AKS {name_zh} - 改色犀牛皮 Color PPF"
            
            # 移除「頂級」與「系列名稱」
            seo_desc = f"AKS 改色犀牛皮 {name_zh} ({code})。提供 TPU 防護與極致漆面質感，獨家乾貼工法，保護原漆、無懼跳石。"
            
            img_url = f"https://cdn.jsdelivr.net/gh/AKS-PPF/color-ppf-images@main/aks_colorppf_{code}.jpg"

            # ------------------------------------------
            # 4. 構建 Markdown 內容
            # ------------------------------------------
            # 加入 show_page 狀態開關，預設為 true
            md_content = f"""---
layout: color-single
title: "{seo_title}"
description: "{seo_desc}"
title_zh: "{name_zh}"
title_en: "{name_en}"
code: "{code}"
series: "{series}"
material: "TPU"
image: "{img_url}"
image_car: ""
gallery: []
show_page: true
date: 2026-04-03
published: true
---
"""
            
            file_path = os.path.join(output_dir, f"{code}.md")
            with open(file_path, 'w', encoding='utf-8') as mdfile:
                mdfile.write(md_content)
            
            count += 1
            if count % 50 == 0:
                print(f"⏳ 已生成 {count} 個檔案...")

    print(f"\n🎉 完美成功！總共生成了 {count} 個色卡檔案。")
    print(f"請在左側瀏覽器確認 '{output_dir}' 資料夾。")

except FileNotFoundError:
    print(f"❌ 錯誤：找不到 '{input_csv}'，請確認檔案名稱正確。")
except Exception as e:
    print(f"❌ 發生未預期的錯誤：{e}")