let currentPage = 1;
const pageSize = 300;
let currentFilteredData = [];

document.addEventListener("DOMContentLoaded", function () {
    let searchMode = 'original'; 
    let enemyDmgUpFilterValue = 'noFilter'; 
	let elementDmgUpFilterValue = 0; 
	
    // Modal 元素
    const modal = document.getElementById("charModal");
    const span = document.getElementsByClassName("close")[0];

    // 關閉 Modal 的事件
    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    function loadData() {
        fetch('data.json')
        .then(response => response.json())
		.then(data => {
			currentFilteredData = data;    
			renderTable(data);
			currentPage = 1; 
            // ... (其餘 Event Listeners 保持不變) ...
            document.getElementById('ctFilter').addEventListener('change', () => filterData(data));
            document.getElementById('spirit_gauge').addEventListener('change', () => filterData(data));
            document.getElementById('buff_cancel_rate').addEventListener('change', () => filterData(data));
            document.getElementById('buff_cancel_count').addEventListener('change', () => filterData(data));
            document.getElementById('markFilter').addEventListener('change', () => filterData(data));
			document.getElementById('status_condition_downFilter').addEventListener('change', () => filterData(data));
            document.getElementById('img_show').addEventListener('change', () => filterData(data));
            document.getElementById('searchButton').addEventListener('click', () => filterData(data));
            document.querySelectorAll('.char-em-filter').forEach(checkbox => {
                checkbox.addEventListener('change', () => filterData(data));
            });
            document.querySelectorAll('.char-wep-filter').forEach(checkbox => {
                checkbox.addEventListener('change', () => filterData(data));
            });
            document.querySelectorAll('.skill-type-filter').forEach(checkbox => {
                checkbox.addEventListener('change', () => filterData(data));
            });
            document.querySelectorAll('.stat_down_filter').forEach(checkbox => {
                checkbox.addEventListener('change', () => filterData(data));
            });
			document.querySelectorAll('.char_source_filter').forEach(checkbox => {
                checkbox.addEventListener('change', () => filterData(data));
            });
            document.querySelectorAll('.skill-state-filter').forEach(checkbox => {
                checkbox.addEventListener('change', () => filterData(data));
            });
            document.getElementById('modeOriginal').addEventListener('click', function () {
                searchMode = 'original';
            });
            document.getElementById('modeSequential').addEventListener('click', function () {
                searchMode = 'sequential';
            });
            document.getElementById('modeStrictSequential').addEventListener('click', function () {
                searchMode = 'strictSequential';
            });
            document.querySelector("#descriptionFilter").addEventListener("keyup", function(event) {
                if (event.keyCode === 13) {
                    event.preventDefault();
                    filterData(data);
                }
            });
            document.querySelector("#toggleKeywordButtons").addEventListener("click", function() {
                const keywordArea = document.querySelector("#keywordButtonsArea");
                if (keywordArea.style.display === "none") {
                    keywordArea.style.display = "block";
                    this.innerText = "收起常用關鍵字";
                } else {
                    keywordArea.style.display = "none";
                    this.innerText = "展開常用關鍵字";
                }
            });
            document.querySelectorAll(".keywordBtn").forEach(button => {
                button.addEventListener("click", function() {
                    const keyword = this.getAttribute("data-keyword");
                    const currentInput = document.querySelector("#descriptionFilter").value.trim();
                    if (currentInput && !currentInput.endsWith(keyword)) {
                        document.querySelector("#descriptionFilter").value = currentInput + " " + keyword;
                    } else if (!currentInput) {
                        document.querySelector("#descriptionFilter").value = keyword;
                    }
                });
            });
            document.querySelectorAll('input[name="searchMode"]').forEach(radio => {
                radio.addEventListener('change', function () {
                    searchMode = this.value;
                });
            });
            document.querySelectorAll('input[name="enemyDmgUpFilter"]').forEach(radio => {
                radio.addEventListener('change', function () {
                    enemyDmgUpFilterValue = this.value;
                    filterData(data);
                });
            });
           document.querySelectorAll('input[name="elementDmgUpFilter"]').forEach(radio => {
                radio.addEventListener('change', function () {
                    elementDmgUpFilterValue = parseInt(this.value);
                    filterData(data);
                });
            });
        })
        .catch(error => console.error('Error fetching data:', error));
    }

    // ... (resetButton 邏輯保持不變) ...
    document.getElementById('resetButton').addEventListener('click', function () {
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        document.querySelectorAll('select').forEach(select => {
            select.selectedIndex = 0;
        });
        document.getElementById('descriptionFilter').value = '';
        loadData();
    });

    function highlightKeywords(text, keywords) {
        keywords.forEach((keyword, index) => {
            if (keyword && keyword.trim() !== '') {
                let regex = new RegExp(keyword, "gi");
                text = text.replace(regex, `<span class="highlight${index + 1}">$&</span>`);
            }
        });
        return text;
    }

    // 將 openCharModal 暴露到全域，以便 onclick 調用
    window.openCharModal = function(index) {
        const item = currentFilteredData[index];
        if (!item) return;

        const modalHeader = document.getElementById("modalHeader");
        const modalBody = document.getElementById("modalBody");
        const modal = document.getElementById("charModal");

        // 1. 設置 Header
        let imgHtml = item.img_name ? `<img src="img/${item.img_name}" alt="${item.skill_char}" height="100" style="border-radius:8px;" onerror="this.src='img/0.png';">` : '';
        let wikiLink = `https://otogi.wikiru.jp/index.php?${item.skill_char}`;
        
        modalHeader.innerHTML = `
            <div class="modal-header-img">${imgHtml}</div>
            <div class="modal-header-info">
                <h2>${item.skill_char}</h2>
                <div>
                    <span class="tag">屬性: ${item.char_em}</span>
                    <span class="tag">武器: ${item.char_wep}</span>
                    <span class="tag">${item.sp_sort}</span>
                </div>
                <a href="${wikiLink}" target="_blank" class="wiki-link-btn">前往 Wiki 頁面</a>
            </div>
        `;

        // 2. 顯示 Modal 並顯示載入中
        modalBody.innerHTML = '<p>載入資料中...</p>';
        modal.style.display = "block";

        // 3. 讀取 JSON
        // 假設 img_name 是 "18291.png"，JSON 檔名為 "18291.json"
        let jsonFileName = item.img_name.split('.')[0] + '.json';
        
        fetch(`./charjson/${jsonFileName}`)
            .then(res => {
                if (!res.ok) throw new Error('Network response was not ok');
                return res.json();
            })
            .then(charData => {
                renderModalTables(charData);
            })
            .catch(err => {
                console.error("Fetch error:", err);
                modalBody.innerHTML = '<p style="color:red;">找不到該角色的詳細資料檔 (JSON)。</p>';
            });
    };

    function renderModalTables(data) {
        const modalBody = document.getElementById("modalBody");
        let html = '';

        // Helper function to create table rows
        const createTable = (items, headers, rowMapper) => {
            if (!items || items.length === 0) return '<p>無資料</p>';
            
            let thead = headers.map(h => `<th>${h}</th>`).join('');
            let tbody = items.map(rowMapper).join('');
            
            return `
                <table class="modal-table">
                    <thead><tr>${thead}</tr></thead>
                    <tbody>${tbody}</tbody>
                </table>
            `;
        };

        // 1. Skill 表格
        if (data.skill && data.skill.length > 0) {
            html += '<div class="section-title">固有技能 (Skills)</div>';
            html += createTable(
                data.skill, 
                ['技能名', '種類', '狀態', '描述'], 
                s => `<tr>
                        <td style="width:20%">${s.skill_name}</td>
                        <td style="width:10%; text-align:center;">${s.skill_type}</td>
                        <td style="width:10%; text-align:center;">${s.skill_state}</td>
                        <td>${s.description}</td>
                      </tr>`
            );
        }

        // 2. LS 表格
        if (data.ls && data.ls.length > 0) {
            html += '<div class="section-title">隊長技能 (Leader Skills)</div>';
            html += createTable(
                data.ls, 
                ['技能名', '描述'], 
                l => `<tr>
                        <td style="width:25%">${l.skill_name}</td>
                        <td>${l.description}</td>
                      </tr>`
            );
        }

        // 3. Wep 表格
        if (data.wep && data.wep.length > 0) {
            html += '<div class="section-title">專武技能 (Weapon Skills)</div>';
            html += createTable(
                data.wep, 
                ['技能名', '描述'], 
                w => `<tr>
                        <td style="width:25%">${w.skill_name}</td>
                        <td>${w.description}</td>
                      </tr>`
            );
        }

        // 4. Acc 表格
        if (data.acc && data.acc.length > 0) {
            html += '<div class="section-title">飾品 (Accessories)</div>';
            html += createTable(
                data.acc, 
                ['名稱', '描述'], 
                a => `<tr>
                        <td style="width:25%">${a.skill_name}</td>
                        <td>${a.description}</td>
                      </tr>`
            );
        }

        if (html === '') html = '<p>此檔案中沒有技能資料。</p>';
        modalBody.innerHTML = html;
    }

    function renderTable(data, page = 1) {
        let tableBody = document.getElementById('tableBody');
        let img_showValue = document.getElementById('img_show').checked ? 1 : 0;
        
        let descriptionKeyword = document.getElementById('descriptionFilter').value;
        let keywords = descriptionKeyword.split(' ').filter(k => k.trim() !== '');

        tableBody.innerHTML = '';

        let start = (page - 1) * pageSize;
        let end = start + pageSize;
        let pageData = data.slice(start, end);

        pageData.forEach((item, index) => {
            // 計算在 currentFilteredData 中的真實索引
            let globalIndex = start + index;

            let tr = document.createElement('tr');
            let additionalInfo = item.sp_sort ? `<br>${item.sp_sort}` : '';
            
            // 修改：點擊圖片觸發 Modal
            let img_show_data = img_showValue ? `
                <a href="javascript:void(0)" class="char-link" onclick="openCharModal(${globalIndex})">
                    <img src="img/${item.img_name}" alt="${item.skill_char}" height="70" onerror="this.src='img/0.png';">
                </a><br>` : '';
            
            let imgCellContent;
            if (item.img_name) {
                // 修改：點擊名稱觸發 Modal
                imgCellContent = `
                ${img_show_data}
                <a href="javascript:void(0)" class="char-link" onclick="openCharModal(${globalIndex})">${item.skill_char}</a>
                ${additionalInfo}`;
            } else {
                imgCellContent = '--';
            }

            let displayDescription = item.description;
            if (keywords.length > 0) {
                displayDescription = highlightKeywords(displayDescription, keywords);
            }

            tr.innerHTML = `
                <td>${item.skill_name}</td>
                <td>${item.skill_type}</td>
                <td>${item.skill_state}</td>
                <td>${imgCellContent}</td>
                <td>${item.char_em}</td>
                <td>${item.char_wep}</td>
                <td class="description-column">${displayDescription}</td>`;
            tableBody.appendChild(tr);
        });

        renderPagination(data.length, page);
    }

    // ... (其餘 renderPagination, pageChange, filterData 函式保持不變) ...
    function renderPagination(totalItems, currentPage) {
        const paginationTop = document.getElementById('paginationTop');
        const paginationBottom = document.getElementById('pagination');
        
        paginationTop.innerHTML = '';
        paginationBottom.innerHTML = '';
    
        if (totalItems <= pageSize) {
            return; 
        }
    
        const totalPages = Math.ceil(totalItems / pageSize);
    
        function createPaginationButtons(container) {
            if (currentPage > 1) {
                const prevBtn = document.createElement('button');
                prevBtn.textContent = '上一頁';
                prevBtn.onclick = () => pageChange(currentPage - 1);
                container.appendChild(prevBtn);
            }
    
            for (let i = 1; i <= totalPages; i++) {
                const pageBtn = document.createElement('button');
                pageBtn.textContent = i;
                if (i === currentPage) {
                    pageBtn.disabled = true;
                } else {
                    pageBtn.onclick = () => pageChange(i);
                }
                container.appendChild(pageBtn);
            }
    
            if (currentPage < totalPages) {
                const nextBtn = document.createElement('button');
                nextBtn.textContent = '下一頁';
                nextBtn.onclick = () => pageChange(currentPage + 1);
                container.appendChild(nextBtn);
            }
        }
    
        createPaginationButtons(paginationTop);
        createPaginationButtons(paginationBottom);
    }
    
    function pageChange(page) {
        currentPage = page;
        renderTable(currentFilteredData, currentPage);
    }

    function filterData(data) {
        let ctValue = parseInt(document.getElementById('ctFilter').value);
        let spirit_gaugeValue = parseInt(document.getElementById('spirit_gauge').value);
        let buff_cancel_rateValue = parseInt(document.getElementById('buff_cancel_rate').value);
        let buff_cancel_countValue = parseInt(document.getElementById('buff_cancel_count').value);
        let markFilterValue = parseInt(document.getElementById('markFilter').value);
        let status_condition_downFilterValue = parseInt(document.getElementById('status_condition_downFilter').value);
        let descriptionKeyword = document.getElementById('descriptionFilter').value;
        
        let keywords = descriptionKeyword.split(' ').filter(k => k.trim() !== '');

        let selectedCharEm = [];
        document.querySelectorAll('.char-em-filter:checked').forEach(checkbox => {
            selectedCharEm.push(checkbox.value);
        });
        let selectedCharWep = [];
        document.querySelectorAll('.char-wep-filter:checked').forEach(checkbox => {
            selectedCharWep.push(checkbox.value);
        });
        let selectedSkillType = [];
        document.querySelectorAll('.skill-type-filter:checked').forEach(checkbox => {
            selectedSkillType.push(...checkbox.value.split(','));
        });
        let selectedStatDown = [];
        document.querySelectorAll('.stat_down_filter:checked').forEach(checkbox => {
            selectedStatDown.push(parseInt(checkbox.value));
        });
        let selectedCharSource = [];
        document.querySelectorAll('.char_source_filter:checked').forEach(checkbox => {
            selectedCharSource.push(parseInt(checkbox.value));
        });
        let selectedSkillState = [];
        document.querySelectorAll('.skill-state-filter:checked').forEach(checkbox => {
            selectedSkillState.push(...checkbox.value.split(','));
        });

        let filteredData = data.filter(item => {
            let matchesCt = ctValue == 0 || item.drain_baria >= ctValue;
            let matchesspirit_gauge = spirit_gaugeValue == 0 || item.spirit_gauge >= spirit_gaugeValue;
            let matchesbuff_cancel_rate = buff_cancel_rateValue == 0 || item.buff_cancel_rate >= buff_cancel_rateValue;
            let matchesbuff_cancel_count = buff_cancel_countValue == 0 || item.buff_cancel_count >= buff_cancel_countValue;
            let matchesDescription;
            const searchText = `${item.description} ${item.skill_name} ${item.skill_char}`;

            switch (searchMode) {
                case 'original':
                    matchesDescription = keywords.every(keyword =>
                        searchText.includes(keyword)
                    );
                    break;

                case 'sequential': {
                    let combinedKeywords = keywords.join('.*');
                    let regex = new RegExp(combinedKeywords);
                    matchesDescription = regex.test(searchText);
                    break;
                }

                case 'strictSequential': {
                    let combinedKeywords2 = keywords.join('[^、。・]*');
                    let regex2 = new RegExp(combinedKeywords2);
                    matchesDescription = regex2.test(searchText);
                    break;
                }
            }
            let matchesCharEm =  item.char_em === '全' || selectedCharEm.length === 0 || selectedCharEm.includes(item.char_em);
            let matchesCharWep = selectedCharWep.length === 0 || selectedCharWep.includes(item.char_wep);
            let matchesSkillType = selectedSkillType.length === 0 || selectedSkillType.includes(item.skill_type);
            let matchesStatDown = selectedStatDown.length === 0 || (Array.isArray(item.stat_down) && selectedStatDown.some(stat => item.stat_down.includes(stat)));
            
            let matchesCharSource = selectedCharSource.length === 0 || selectedCharSource.includes(item.sp_sort_for_search);
            
            let matchesSkillState = selectedSkillState.length === 0 || selectedSkillState.includes(item.skill_state);
            let matchesmarkFilter = markFilterValue == 0 || item.mark >= markFilterValue;
            let matchesstatus_condition_downFilter = status_condition_downFilterValue == 0 || item.status_condition_down >= status_condition_downFilterValue;

            let matchesEnemyDmgUp;
            switch (enemyDmgUpFilterValue) {
                case 'noFilter':
                    matchesEnemyDmgUp = true;
                    break;
                case 'anyValue':
                    matchesEnemyDmgUp = Array.isArray(item.enemy_dmg_up) && item.enemy_dmg_up.length > 0;
                    break;
                case 'contains1':
                    matchesEnemyDmgUp = Array.isArray(item.enemy_dmg_up) && item.enemy_dmg_up.includes(1);
                    break;
                case 'contains2':
                    matchesEnemyDmgUp = Array.isArray(item.enemy_dmg_up) && item.enemy_dmg_up.includes(2);
                    break;
                case 'contains3':
                    matchesEnemyDmgUp = Array.isArray(item.enemy_dmg_up) && item.enemy_dmg_up.includes(3);
                    break;
            }
            let matchesElementDmgUp;
            if (elementDmgUpFilterValue === 0) {
                matchesElementDmgUp = true;
            } else if (item.em_resist === 6) {
                matchesElementDmgUp = true;
            } else {
                matchesElementDmgUp = item.em_resist === elementDmgUpFilterValue;
            }
            return matchesCt && matchesspirit_gauge && matchesbuff_cancel_rate && matchesbuff_cancel_count && matchesDescription && matchesCharEm && matchesCharWep && matchesSkillType && matchesStatDown && matchesSkillState && matchesmarkFilter && matchesstatus_condition_downFilter && matchesEnemyDmgUp && matchesElementDmgUp && matchesCharSource;
        });
        currentPage = 1;
        currentFilteredData = filteredData;
        renderTable(currentFilteredData, currentPage);
    }

    loadData();
});