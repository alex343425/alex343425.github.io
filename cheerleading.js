document.addEventListener("DOMContentLoaded", function () {
  const dataSource = 'data_cheerleading.json';
  let dataCache = [];

  // 讀取資料
  function loadData() {
    fetch(dataSource)
      .then(response => response.json())
      .then(data => {
        dataCache = data;
        filterAndRender();
        setupFilters();
      })
      .catch(error => console.error('Error fetching data:', error));
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
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';
    data.forEach(item => {
      const permanentDisplay = (item.permanent_skill_up === 1) ? "✔" : "";
      
      // 角色名欄位內容：圖片、超連結與 sp_sort
      const additionalInfo = item.sp_sort ? `<br>${item.sp_sort}` : '';
      let imgCellContent = '';
      if (item.img_name) {
        imgCellContent = `<a href="https://otogi.wikiru.jp/index.php?★${item.r}/${item.skill_char}" target="_blank">
                            <img src="img/${item.img_name}" alt="${item.skill_char}" height="70" onerror="this.src='img/0.png';"><br>							
							<a href="https://otogi.wikiru.jp/index.php?★${item.r}/${item.skill_char}" target="_blank">${item.skill_char}</a>
							
							
							
							${additionalInfo}`;
      } else {
        imgCellContent = `${item.skill_char}${additionalInfo}`;
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
        <td>${item.hp}</td>
        <td>${item.def}</td>
        <td style="${sourceSkillBg ? 'background-color:' + sourceSkillBg + ';' : ''}">${item.source_skill}</td>
        <td style="${slot1Bg ? 'background-color:' + slot1Bg + ';' : ''}">${item.slot1}</td>
        <td style="${slot2Bg ? 'background-color:' + slot2Bg + ';' : ''}">${item.slot2}</td>
        <td style="${slot3Bg ? 'background-color:' + slot3Bg + ';' : ''}">${item.slot3}</td>
        <td>${permanentDisplay}</td>
      `;
      tableBody.appendChild(tr);
    });
  }

  // 根據所有篩選條件過濾與排序資料
  function filterAndRender() {
    // 原有篩選：屬性、武器、角色分類
    const selectedCharEm = Array.from(document.querySelectorAll('.char-em-filter:checked')).map(el => el.value);
    const selectedCharWep = Array.from(document.querySelectorAll('.char-wep-filter:checked')).map(el => el.value);
    const selectedCharSource = Array.from(document.querySelectorAll('.char_source_filter:checked')).map(el => parseInt(el.value));
    
    // 新增篩選：固有顏色 (source_skill)
    const selectedSkillColor = Array.from(document.querySelectorAll('.skill_color_filter:checked')).map(el => el.value);
    
    // 新增篩選：拆技格子
    const selectedSkillBreak = Array.from(document.querySelectorAll('.skill-break-filter:checked'));
    
    // 新增篩選：永續昇華
    const permanentFilter = document.querySelector('input[name="permanent_filter"]:checked').value;
    // 新增篩選：隊長技昇華
    const awakeFilter = document.querySelector('input[name="awake_filter"]:checked').value;
    // 新增排序：排序條件
    const sortOption = document.querySelector('input[name="sort_option"]:checked').value;
    
    let filteredData = dataCache.filter(item => {
      const matchEm =   item.char_em === '全' || selectedCharEm.length === 0 || selectedCharEm.includes(item.char_em);	  
      const matchWep = selectedCharWep.length === 0 || selectedCharWep.includes(item.char_wep);
      const matchRoleSource = selectedCharSource.length === 0 || selectedCharSource.includes(item.sp_sort_for_search);
      const matchSkillColor = selectedSkillColor.length === 0 || selectedSkillColor.includes(item.source_skill);
      
      // 拆技格子篩選：所有勾選的條件皆必須滿足
      let matchSkillBreak = true;
      selectedSkillBreak.forEach(checkbox => {
        const field = checkbox.getAttribute('data-field');
        const threshold = parseInt(checkbox.getAttribute('data-threshold'));
        if (!(item[field] >= threshold)) {
          matchSkillBreak = false;
        }
      });
      
			// 永續昇華篩選
	  let matchPermanent = true;
	  if (permanentFilter === "1") {
		matchPermanent = item.permanent_skill_up >= 1;
	  }

	  // 隊長技昇華篩選
	  let matchAwake = true;
	  if (awakeFilter === "1") {
		matchAwake = item.awake !== undefined && item.awake >= 1;
	  } else if (awakeFilter === "2") {
		matchAwake = item.awake !== undefined && item.awake >= 2;
	  }

	  return matchEm && matchWep && matchRoleSource && matchSkillColor && matchSkillBreak && matchPermanent && matchAwake;
	});
    
    // 排序：根據所選條件進行排序
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
      // 清空所有 checkbox 與 radio (將 radio 重設為預設值)
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
