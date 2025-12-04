let currentPage = 1;
const pageSize = 300;
let currentFilteredData = [];
document.addEventListener("DOMContentLoaded", function () {
    let searchMode = 'original'; // 這是默認的搜索模式
    let enemyDmgUpFilterValue = 'noFilter'; // 這是新的篩選條件
	let elementDmgUpFilterValue = 0; // 新增這行
	
    function loadData() {
        fetch('data.json')
        .then(response => response.json())
		.then(data => {
			currentFilteredData = data;    // ★ 重要：首次載入建立預設資料
			renderTable(data);
			currentPage = 1; 
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
            let regex = new RegExp(keyword, "gi");
            text = text.replace(regex, `<span class="highlight${index + 1}">$&</span>`);
        });
        return text;
    }

function renderTable(data, page = 1) {
    let tableBody = document.getElementById('tableBody');
    let img_showValue = document.getElementById('img_show').checked ? 1 : 0;
    tableBody.innerHTML = '';

    // 分頁處理
    let start = (page - 1) * pageSize;
    let end = start + pageSize;
    let pageData = data.slice(start, end);

    for (let item of pageData) {
        let tr = document.createElement('tr');
        let additionalInfo = item.sp_sort ? `<br>${item.sp_sort}` : '';
        let img_show_data = img_showValue ? `<a href="https://otogi.wikiru.jp/index.php?${item.skill_char}" target="_blank">
                <img src="img/${item.img_name}" alt="${item.skill_char}" height="70" onerror="this.src='img/0.png';">
            </a><br>` : '';
        let imgCellContent;
        if (item.img_name) {
            imgCellContent = `
            ${img_show_data}
            <a href="https://otogi.wikiru.jp/index.php?${item.skill_char}" target="_blank">${item.skill_char}</a>
            ${additionalInfo}`;
        } else {
            imgCellContent = '--';
        }

		tr.innerHTML = `
			<td>${item.skill_name}</td>
			<td>${item.skill_type}</td>
			<td>${item.skill_state}</td>
			<td>${imgCellContent}</td>
			<td>${item.char_em}</td>
			<td>${item.char_wep}</td>
			<td class="description-column">${item.description}</td>  `;
        tableBody.appendChild(tr);
    }

    renderPagination(data.length, page);
}
function renderPagination(totalItems, currentPage) {
    const paginationTop = document.getElementById('paginationTop');
    const paginationBottom = document.getElementById('pagination');
    
    paginationTop.innerHTML = '';
    paginationBottom.innerHTML = '';

    if (totalItems <= pageSize) {
        return; // 小於200不顯示
    }

    const totalPages = Math.ceil(totalItems / pageSize);

    function createPaginationButtons(container) {
        // 上一頁
        if (currentPage > 1) {
            const prevBtn = document.createElement('button');
            prevBtn.textContent = '上一頁';
            prevBtn.onclick = () => pageChange(currentPage - 1);
            container.appendChild(prevBtn);
        }

        // 頁碼
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

        // 下一頁
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
        let keywords = descriptionKeyword.split(' ');
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
            switch (searchMode) {
                case 'original':
                    matchesDescription = keywords.every(keyword =>
                        item.description.includes(keyword) || item.skill_name.includes(keyword));
                    break;
                case 'sequential':
                    let combinedKeywords = keywords.join('.*');
                    let regex = new RegExp(combinedKeywords);
                    matchesDescription = regex.test(item.description);
                    break;
                case 'strictSequential':
                    let combinedKeywords2 = keywords.join('[^、。・]*');
                    let regex2 = new RegExp(combinedKeywords2);
                    matchesDescription = regex2.test(item.description);
                    break;
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
        document.querySelectorAll('.description-column').forEach((cell, index) => {
            let highlightedText = highlightKeywords(filteredData[index].description, keywords);
            cell.innerHTML = highlightedText;
        });
    }

    loadData();
});
