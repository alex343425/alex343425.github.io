# 發布劇情 WIKI 到 GitHub Pages

網站已產生在 [`docs/`](docs/)，首頁是 [`docs/index.html`](docs/index.html)。它是純靜態網站，不需要資料庫、伺服器程式或額外套件。網站網址使用相對路徑，放在 `帳號.github.io/儲存庫名稱/` 也能正常連結。

## 最省事的發布方式：自動部署

1. 在 GitHub 建立儲存庫，將**這個資料夾的全部內容**放到儲存庫根目錄，並推送到 `main` 分支。`wiki/`、`術語表.md`、15 份原文 `.txt`、`build_site.py`、`site_assets/` 與 `.github/workflows/pages.yml` 都要一起上傳。
2. 在儲存庫的 **Settings → Pages → Build and deployment**，將 **Source** 設為 **GitHub Actions**。
3. 到 **Actions** 頁查看「發布劇情 WIKI」流程。首次部署完成後，網站網址會出現在 Pages 設定頁，也會出現在部署流程結果中。

日後只需修改 `wiki/` 內的 Markdown 或 `術語表.md` 並推送到 `main`；流程會重新核對來源、產生網站並部署。工作流程也可在 Actions 頁手動執行。若儲存庫使用 `main`、`master` 以外的分支，請修改 `.github/workflows/pages.yml` 的 `branches`。

新增篇章、人物或組織條目時，請在標題及條目名稱並列中文與日文原文，例如「匹爾蒂（ピュルテ）」。既有術語可先查 `術語表.md`；執行 `python bilingual_labels.py --preview` 可檢視尚待補註的標題，再執行 `python bilingual_labels.py` 補入。日中名稱相同時只列一次；編者自行撰寫的劇情小標不需回譯。

## 不使用自動部署

也可以在 GitHub Pages 設定選 **Deploy from a branch → main → /docs**，直接發布已產生的 `docs/`。採用這種方式時，Markdown 更新後要先在電腦執行：

```powershell
python build_site.py
python verify_site.py
```

然後把更新後的 `docs/` 一起推送。請不要手動編輯 `docs/` 裡的 HTML；它會在下一次產生網站時重建。

## 在電腦預覽

```powershell
python build_site.py
python -m http.server 8000 --directory docs
```

在瀏覽器開啟 `http://localhost:8000/`。搜尋功能需要透過這個本機網址或 GitHub Pages 網址開啟；直接雙擊 HTML 檔時，瀏覽器可能禁止讀取搜尋索引。

## 手機閱讀

直接在手機檔案檢視器開啟單一 HTML 頁面時，頁面的手機版樣式與導覽按鈕已包含在 HTML 內，可閱讀該頁。若要切換其他篇章、開啟原文或使用站內搜尋，請在手機瀏覽器開啟 GitHub Pages 網址；離線切換篇章則需保留整個 `docs/` 資料夾的目錄結構。部分手機檔案檢視器會限制 JavaScript，此時請改用瀏覽器開啟。

網站目前收錄 9 篇主線、6 篇番外、角色與設定等資料頁、術語表及章節索引。原文放在 `docs/原文/`，從分篇頁面的「原文」連結可開啟。所有頁面都含完整劇透。
