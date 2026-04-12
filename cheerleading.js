document.addEventListener("DOMContentLoaded", function () {
  const dataSource = 'data_cheerleading.json';
  let dataCache = [];
  let currentFilteredData = []; // 用於保存當前過濾後的資料，給 Modal 根據 index 讀取

  // 讀取資料
  function loadData() {
    fetch(dataSource)
      .then(response => response.json())
      .then(data => {
        dataCache = data;
        filterAndRender();
        setupFilters();
        setupModal(); // 初始化 Modal 事件
      })
      .catch(error => console.error('Error fetching data:', error));
  }

  // 設定 Modal 開關事件
  function setupModal() {
    const modal = document.getElementById("charModal");
    const span = document.getElementsByClassName("close")[0];

    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
  }

  // 根據文字內容回傳對應的底色
  function getBgColor(text) {
    if (text.indexOf('橘') !== -1) return 'orange';
    if (text.indexOf('藍') !== -1) return 'lightskyblue';
    if (text.indexOf('紫') !== -1) return 'mediumpurple';
    if (text.indexOf('粉') !== -1) return 'pink';
    if (text.indexOf('綠') !== -1) return 'lightgreen';
    return '';
  }

  // 渲染表格資料
  function renderTable(data) {
    currentFilteredData = data; // 記錄當下顯示的資料
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';
    
    data.forEach((item, index) => {
      const permanentDisplay = (item.permanent_skill_up === 1) ? "✔" : "";
      
      const additionalInfo = item.sp_sort ? `<br>${item.sp_sort}` : '';
      let imgCellContent = '';
      
      if (item.img_name) {
        imgCellContent = `
            <a href="javascript:void(0)" class="char-link" onclick="openCharModal(${index})">
                <img src="img/${item.img_name}" alt="${item.skill_char}" loading="lazy" height="70" onerror="this.src='img/0.png';">
            </a><br>
            <a href="javascript:void(0)" class="char-link" onclick="openCharModal(${index})">${item.skill_char}</a>
            ${additionalInfo}
        `;
      } else {
        imgCellContent = `<a href="javascript:void(0)" class="char-link" onclick="openCharModal(${index})">${item.skill_char}</a>${additionalInfo}`;
      }
      
      // 根據內容決定底色
      const sourceSkillBg = getBgColor(item.source_skill);
      const slot1Bg = getBgColor(item.slot1);
      const slot2Bg = getBgColor(item.slot2);
      const slot3Bg = getBgColor(item.slot3);

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${imgCellContent}</td>
        <td>${item.char_em}</td>
        <td>${item.char_wep}</td>
        <td style="${sourceSkillBg ? 'background-color:' + sourceSkillBg + ';' : ''}">${item.source_skill}</td>
        <td style="${slot1Bg ? 'background-color:' + slot1Bg + ';' : ''}">${item.slot1}</td>
        <td style="${slot2Bg ? 'background-color:' + slot2Bg + ';' : ''}">${item.slot2}</td>
        <td style="${slot3Bg ? 'background-color:' + slot3Bg + ';' : ''}">${item.slot3}</td>
        <td>${permanentDisplay}</td>
      `;
      tableBody.appendChild(tr);
    });
  }

  // 暴露給全域以便 `<a>` 標籤點擊時呼叫
  window.openCharModal = function(index) {
    const item = currentFilteredData[index];
    if (!item) return;

    const modalHeader = document.getElementById("modalHeader");
    const modalBody = document.getElementById("modalBody");
    const modal = document.getElementById("charModal");

    // 1. 設置 Header
    let imgHtml = item.img_name ? `<img src="img/${item.img_name}" alt="${item.skill_char}" height="100" style="border-radius:8px;" onerror="this.src='img/0.png';">` : '';
    // 依據原始的 wiki 連結邏輯組合 (加入星數與角色名)
    let wikiLink = `https://otogi.wikiru.jp/index.php?★${item.r}/${item.skill_char}`;
    
    modalHeader.innerHTML = `
        <div class="modal-header-img">${imgHtml}</div>
        <div class="modal-header-info">
            <h2>${item.skill_char}</h2>
            <div>
                <span class="tag">屬性: ${item.char_em}</span>
                <span class="tag">武器: ${item.char_wep}</span>
                <span class="tag">${item.sp_sort || '無分類'}</span>
            </div>
            <a href="${wikiLink}" target="_blank" class="wiki-link-btn">前往 Wiki 頁面</a>
        </div>
    `;

    // 2. 顯示 Modal 並顯示載入中
    modalBody.innerHTML = '<p>載入資料中...</p>';
    modal.style.display = "block";

    if (!item.img_name) {
        modalBody.innerHTML = '<p style="color:red;">無對應圖片，無法推斷詳細資料檔 (JSON)。</p>';
        return;
    }

    // 3. 讀取 JSON
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

  // 生成 Modal 內的表格
  function renderModalTables(data) {
    const modalBody = document.getElementById("modalBody");
    let html = '';

    // Helper function
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

  // 根據所有篩選條件過濾與排序資料
  function filterAndRender() {
    const selectedCharEm = Array.from(document.querySelectorAll('.char-em-filter:checked')).map(el => el.value);
    const selectedCharWep = Array.from(document.querySelectorAll('.char-wep-filter:checked')).map(el => el.value);
    const selectedCharSource = Array.from(document.querySelectorAll('.char_source_filter:checked')).map(el => parseInt(el.value));
    
    const selectedSkillColor = Array.from(document.querySelectorAll('.skill_color_filter:checked')).map(el => el.value);
    const selectedSkillBreak = Array.from(document.querySelectorAll('.skill-break-filter:checked'));
    
    const permanentFilter = document.querySelector('input[name="permanent_filter"]:checked').value;
    const awakeFilter = document.querySelector('input[name="awake_filter"]:checked').value;
    const sortOption = document.querySelector('input[name="sort_option"]:checked').value;
    
    let filteredData = dataCache.filter(item => {
      const matchEm = item.char_em === '全' || selectedCharEm.length === 0 || selectedCharEm.includes(item.char_em);	  
      const matchWep = selectedCharWep.length === 0 || selectedCharWep.includes(item.char_wep);
      const matchRoleSource = selectedCharSource.length === 0 || selectedCharSource.includes(item.sp_sort_for_search);
      const matchSkillColor = selectedSkillColor.length === 0 || selectedSkillColor.includes(item.source_skill);
      
      let matchSkillBreak = true;
      selectedSkillBreak.forEach(checkbox => {
        const field = checkbox.getAttribute('data-field');
        const threshold = parseInt(checkbox.getAttribute('data-threshold'));
        if (!(item[field] >= threshold)) {
          matchSkillBreak = false;
        }
      });
      
	  let matchPermanent = true;
	  if (permanentFilter === "1") {
		matchPermanent = item.permanent_skill_up >= 1;
	  }

	  let matchAwake = true;
	  if (awakeFilter === "1") {
		matchAwake = item.awake !== undefined && item.awake >= 1;
	  } else if (awakeFilter === "2") {
		matchAwake = item.awake !== undefined && item.awake >= 2;
	  }

	  return matchEm && matchWep && matchRoleSource && matchSkillColor && matchSkillBreak && matchPermanent && matchAwake;
	});
    
    if (sortOption === "hp") {
      filteredData.sort((a, b) => b.hp - a.hp);
    } else if (sortOption === "def") {
      filteredData.sort((a, b) => b.def - a.def);
    }
    
    renderTable(filteredData);
  }

  // 設定所有篩選與排序事件
  function setupFilters() {
    document.querySelectorAll('.char-em-filter').forEach(checkbox => {
      checkbox.addEventListener('change', filterAndRender);
    });
    document.querySelectorAll('.char-wep-filter').forEach(checkbox => {
      checkbox.addEventListener('change', filterAndRender);
    });
    document.querySelectorAll('.char_source_filter').forEach(checkbox => {
      checkbox.addEventListener('change', filterAndRender);
    });
    document.querySelectorAll('.skill_color_filter').forEach(checkbox => {
      checkbox.addEventListener('change', filterAndRender);
    });
    document.querySelectorAll('.skill-break-filter').forEach(checkbox => {
      checkbox.addEventListener('change', filterAndRender);
    });
	document.querySelectorAll('input[name="awake_filter"]').forEach(radio => {
	  radio.addEventListener('change', filterAndRender);
	});
    document.querySelectorAll('input[name="permanent_filter"]').forEach(radio => {
      radio.addEventListener('change', filterAndRender);
    });
    document.querySelectorAll('input[name="sort_option"]').forEach(radio => {
      radio.addEventListener('change', filterAndRender);
    });
    document.getElementById('resetButton').addEventListener('click', function () {
      document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
      });
      document.querySelector('input[name="permanent_filter"][value="0"]').checked = true;
      document.querySelector('input[name="sort_option"][value="default"]').checked = true;
      renderTable(dataCache);
    });
  }

  loadData();
});