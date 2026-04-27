# 🚀 AKS PPF 官方網站 - 系統架構與開發者維護指南

本文件為 AKS 官方網站的「系統架構藍圖」與「核心業務邏輯說明」。
當未來需要進行交接、除錯、或是擴充新功能（如：新增改色膜系列、新增色卡）時，請務必先閱讀此文件。

---

## 🏢 1. 基礎架構與伺服器 (Infrastructure)

本網站採用輕量化但具備企業級防護的「無頭式靜態架構 (Static Site with CDN)」。

| 服務供應商 | 扮演角色 | 核心任務與設定狀態 |
| :--- | :--- | :--- |
| **GoDaddy** | 網域註冊商 | 僅負責持有 `aks-ppf.com` 網域，DNS 命名伺服器已全權移交給 Cloudflare。 |
| **Cloudflare** | CDN 與 DNS | 負責全站 HTTPS 加密 (SSL/TLS 設為 Full)、全球快取加速，以及執行舊網站的 301 批次轉址 (Bulk Redirects)。 |
| **GitHub Pages**| 網站伺服器 | 負責編譯 Jekyll 系統，存放所有 HTML/CSS/JS 代碼，並綁定 Custom Domain。 |

---

## 📂 2. 靜態資源分離架構 (Asset Separation)

為了提升網站載入速度、節省編譯時間並保持主專案整潔，我們將「網頁代碼」與「圖片資源」分拆在不同的 GitHub 倉庫 (Repositories) 中。這等同於我們擁有自己的免費圖片 CDN 伺服器。

* **主站代碼倉庫：** `aks-official-website` (對應正式網域 `www.aks-ppf.com`)
* **圖片素材倉庫：** `images`、`color-ppf-images` (保留 GitHub 原始網域 `aks-ppf.github.io`)

⚠️ **開發守則：**
在主站代碼中呼叫圖片時，**必須使用絕對路徑**指向圖片專屬倉庫，不可使用相對路徑。
* ✅ 正確寫法：`<img src="https://aks-ppf.github.io/images/ui/logo.png">`
* ❌ 錯誤寫法：`<img src="/images/ui/logo.png">`

---

## 🧠 3. 核心功能實作邏輯 (Core Features Logic)

本站底層由 **Jekyll (靜態網站產生器)** 驅動，以下為核心業務模組的運作邏輯：

### A. 400+ 線上色卡系統 (Markdown 資料庫邏輯)
我們沒有使用傳統的 MySQL 資料庫，而是利用 Jekyll 的 Markdown (MD) 檔案系統來管理龐大的色卡資料。

* **運作原理：** 每一款顏色都是一個獨立的 `.md` 檔案。
* **資料結構 (YAML Front Matter)：** 在每個 `.md` 檔的頂部，我們利用 `---` 包夾的區塊來定義該顏色的屬性（如：顏色名稱、色號、系列、預覽圖連結等）。
* **渲染方式：** 前端頁面利用 Liquid 語法（`{% for color in site.colors %}` 等迴圈），自動去讀取這些 md 檔的資料，並一次性生成 400 多個色卡網格。
* **💡 擴充 SOP：** 日後若要新增顏色，**完全不需要改寫 HTML 排版**。只需要新增一個 `.md` 檔，填好 Front Matter 屬性並上傳，系統就會自動把它加入線上色卡庫中。

### B. 前端視覺動態引擎 (Animation & Parallax Engine)
為了確保網站效能，我們沒有引入肥大的外部動畫函式庫，而是原生刻了一套基於 `IntersectionObserver` 的輕量級動態引擎。

1. **進場動畫 (`.io-reveal`)：**
   * **邏輯：** 只要在 HTML 標籤加上 `class="io-reveal"`，該元素預設會是隱藏且稍微位移的狀態。
   * **觸發：** 當使用者往下捲動，元素進入螢幕可視範圍 (Viewport) 時，JS 引擎會自動幫它加上 `.is-in` 的 class，觸發 CSS 轉場動畫（浮現並解開模糊）。
   * **順序控制：** 透過加上 `data-delay="1"` 到 `"5"`，可控制同一區塊內元素的進場先後順序，創造瀑布般的層次感。

2. **視差滾動 (`data-parallax`)：**
   * **邏輯：** 在圖片或元素加上 `data-parallax="0.12"`。JS 的 `requestAnimationFrame` 會計算元素與視窗的相對位置，在滾動時給予微小的 Y 軸偏移與縮放，創造空間立體感。
   * **效能保護：** 針對手機版 (寬度小於 900px) 自動關閉視差運算，並支援系統級的「減少動態效果 (prefers-reduced-motion)」無障礙規範。

### C. 全站 SEO 自動化大腦
* 在 `_layouts/default.html` 的 `<head>` 區塊內，我們植入了 `{% include schema.html %}`。
* 它會根據當前頁面的屬性（首頁、文章頁、產品頁），自動生成對應的 JSON-LD 結構化資料。交接與維護時，**嚴禁刪除此行代碼**。

---

## 🛠️ 4. 日後營運與維護 SOP (Maintenance Guide)

### 情況一：修改了代碼或圖片，但前台沒更新？
**原因：** Cloudflare 邊緣節點的快取 (Cache) 尚未過期。
**解法：** 1. 登入 Cloudflare 進入 `aks-ppf.com` 管理介面。
2. 左側選單：**Caching** ➡️ **Configuration**。
3. 點擊 **Purge Everything**，清空全球快取。
4. 使用瀏覽器「無痕視窗」重新檢視。

### 情況二：Jekyll 全站排版大破圖？
**原因：** `_config.yml` 網址設定錯誤。
**解法：** 確認 `_config.yml` 中的設定必須為：
```yaml
url: "[https://www.aks-ppf.com](https://www.aks-ppf.com)"
baseurl: ""  # 必須保留雙引號，不可留白或寫入子路徑
