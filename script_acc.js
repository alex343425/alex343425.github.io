document.addEventListener("DOMContentLoaded", function () {
    let originalData = []; // 儲存原始資料
    let currentSort = { key: null, order: null }; // 當前排序狀態
    let filterPass = "all"; // 預設顯示全部
    let selectedAccSources = new Set(); // 存儲選中的 acc_source 篩選值

    function loadData() {
        fetch('data_acc.json')
            .then(response => response.json())
            .then(data => {
                originalData = data; // 儲存原始資料
                renderTable(data); // 初次渲染表格
                addSortingListeners(); // 綁定排序功能
                addFilterListeners(); // 綁定過濾功能
            })
            .catch(error => console.error('載入資料時發生錯誤:', error));
    }

    function renderTable(data) {
        const tableBody = document.getElementById('tableBody');
        tableBody.innerHTML = ''; // 清空表格內容

        data.forEach(item => {
            // 🔹 過濾 pass
            if (filterPass === "0" && item.pass !== 0) return;
            if (filterPass === "1" && item.pass !== 1) return;

            // 🔹 過濾 acc_source（如果有勾選任何選項）
            if (selectedAccSources.size > 0 && !selectedAccSources.has(String(item.acc_source))) return;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <img src="./acc_icon/${item.id}.png" alt="${item.n}" width="40" height="40" 
                         onerror="this.onerror=null; this.src='./acc_icon/default.png';"
                         onload="this.onerror=function() { this.src='./acc_icon_0.png'; }">
                    ${item.n}
                </td>
                <td>${item.s.Hp}</td>
                <td>${item.s.Offence}</td>
                <td>${item.s.Defence}</td>
                <td>${item.s.Magic}</td>
                <td>${item.s.Heal}</td>
                <td>${item.s.Speed}</td>
                <td>${item.d}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    function addSortingListeners() {
        const headers = document.querySelectorAll('th.sortable');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const key = header.dataset.key;

                // 若重複點擊相同的列，改變排序順序；否則初始化為降序
                if (currentSort.key === key) {
                    currentSort.order = currentSort.order === 'desc' ? 'asc' : 
                                        currentSort.order === 'asc' ? null : 'desc';
                } else {
                    currentSort.key = key;
                    currentSort.order = 'desc';
                }

                // 更新表格資料
                sortTable(key, currentSort.order);

                // 更新標題文字
                updateHeaders(header);
            });
        });
    }

    function sortTable(key, order) {
        if (!order) {
            // 若無排序順序，恢復原始資料
            renderTable(originalData);
            return;
        }

        const sortedData = [...originalData].sort((a, b) => {
            const valA = a.s[key];
            const valB = b.s[key];

            if (valA === valB) return originalData.indexOf(a) - originalData.indexOf(b); // 同值時依原順序
            return order === 'desc' ? valB - valA : valA - valB;
        });

        renderTable(sortedData);
    }

    function updateHeaders(activeHeader) {
        // 重置所有標題
        document.querySelectorAll('th.sortable').forEach(header => {
            header.textContent = header.textContent.replace(/(↓|↑)$/, '');
        });

        // 增加箭頭指示
        if (currentSort.order === 'desc') {
            activeHeader.textContent += '↓';
        } else if (currentSort.order === 'asc') {
            activeHeader.textContent += '↑';
        }
    }

    function addFilterListeners() {
        // 🔹 `pass` 過濾
        document.querySelectorAll('input[name="passFilter"]').forEach(radio => {
            radio.addEventListener('change', function () {
                filterPass = this.value; // 取得篩選條件
                renderTable(originalData); // 重新渲染表格
            });
        });

        // 🔹 `acc_source` 過濾
        document.querySelectorAll('.accSourceFilter').forEach(checkbox => {
            checkbox.addEventListener('change', function () {
                if (this.checked) {
                    selectedAccSources.add(this.value);
                } else {
                    selectedAccSources.delete(this.value);
                }
                renderTable(originalData); // 重新渲染表格
            });
        });
    }

    loadData();
});
