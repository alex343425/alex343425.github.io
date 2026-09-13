document.addEventListener('DOMContentLoaded', () => {
    let originalData = [];
    let currentSort = { key: null, order: null };
    let filterPass = document.querySelector('input[name="passFilter"]:checked')?.value || '1';
    let searchTimer = null;
    let isComposing = false;
    const selectedAccSources = new Set(
        [...document.querySelectorAll('.accSourceFilter:checked')].map(checkbox => checkbox.value)
    );

    const keywordInput = document.getElementById('descriptionFilter');
    const tableBody = document.getElementById('tableBody');

    function loadData() {
        fetch('data_acc.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                originalData = data.map((item, index) => ({ ...item, _origIndex: index }));
                applyFiltersAndSort();
            })
            .catch(error => {
                console.error('載入資料時發生錯誤:', error);
                renderMessage('資料載入失敗，請稍後再試。');
            });
    }

    function getFilteredData() {
        const keywords = keywordInput.value
            .trim()
            .toLocaleLowerCase()
            .split(/\s+/)
            .filter(Boolean);

        return originalData.filter(item => {
            const matchesPass = filterPass === 'all' || String(item.pass) === filterPass;
            const matchesAccSource = selectedAccSources.size === 0 || selectedAccSources.has(String(item.acc_source));
            const searchableText = `${item.n || ''}\n${item.d || ''}`.toLocaleLowerCase();
            const matchesKeyword = keywords.every(keyword => searchableText.includes(keyword));

            return matchesPass && matchesAccSource && matchesKeyword;
        });
    }

    function applyFiltersAndSort() {
        const displayData = getFilteredData();

        if (currentSort.key && currentSort.order) {
            displayData.sort((a, b) => {
                const valueA = Number(a.s?.[currentSort.key]) || 0;
                const valueB = Number(b.s?.[currentSort.key]) || 0;

                if (valueA === valueB) {
                    return a._origIndex - b._origIndex;
                }

                return currentSort.order === 'desc' ? valueB - valueA : valueA - valueB;
            });
        } else {
            displayData.sort((a, b) => a._origIndex - b._origIndex);
        }

        renderTable(displayData);
    }

    function runSearchImmediately() {
        if (searchTimer) {
            clearTimeout(searchTimer);
            searchTimer = null;
        }
        applyFiltersAndSort();
    }

    function scheduleSearch() {
        if (isComposing) return;

        if (searchTimer) {
            clearTimeout(searchTimer);
        }
        searchTimer = setTimeout(runSearchImmediately, 150);
    }

    function renderTable(data) {
        tableBody.replaceChildren();

        if (data.length === 0) {
            renderMessage('沒有符合篩選條件的飾品。');
            return;
        }

        const fragment = document.createDocumentFragment();

        data.forEach(item => {
            const row = document.createElement('tr');
            const nameCell = document.createElement('td');
            const nameWrapper = document.createElement('div');
            const image = document.createElement('img');
            const name = document.createElement('span');

            nameWrapper.className = 'accessory-name';
            image.src = `./acc_icon/${item.id}.png`;
            image.alt = `${item.n || '飾品'}圖示`;
            image.loading = 'lazy';
            image.addEventListener('error', () => {
                image.src = './acc_icon/default.png';
            }, { once: true });
            name.textContent = item.n || '--';

            nameWrapper.append(image, name);
            nameCell.appendChild(nameWrapper);
            row.appendChild(nameCell);

            ['Hp', 'Offence', 'Defence', 'Magic', 'Heal', 'Speed'].forEach(key => {
                const cell = document.createElement('td');
                cell.className = 'num-width';
                cell.textContent = item.s?.[key] ?? '--';
                row.appendChild(cell);
            });

            const descriptionCell = document.createElement('td');
            descriptionCell.className = 'description-width';
            descriptionCell.textContent = item.d || '--';
            row.appendChild(descriptionCell);

            fragment.appendChild(row);
        });

        tableBody.appendChild(fragment);
    }

    function renderMessage(message) {
        tableBody.replaceChildren();
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.className = 'empty-message';
        cell.colSpan = 8;
        cell.textContent = message;
        row.appendChild(cell);
        tableBody.appendChild(row);
    }

    function handleSort(header) {
        const key = header.dataset.key;

        if (currentSort.key === key) {
            currentSort.order = currentSort.order === 'desc'
                ? 'asc'
                : currentSort.order === 'asc'
                    ? null
                    : 'desc';
        } else {
            currentSort = { key, order: 'desc' };
        }

        updateSortIcons();
        applyFiltersAndSort();
    }

    function updateSortIcons() {
        document.querySelectorAll('th.sortable').forEach(header => {
            const icon = header.querySelector('.sort-icon');
            const isActive = header.dataset.key === currentSort.key && currentSort.order;
            icon.textContent = isActive ? (currentSort.order === 'desc' ? '▼' : '▲') : '';
            header.setAttribute('aria-sort', isActive
                ? (currentSort.order === 'desc' ? 'descending' : 'ascending')
                : 'none');
        });
    }

    document.querySelectorAll('th.sortable').forEach(header => {
        header.addEventListener('click', () => handleSort(header));
        header.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                handleSort(header);
            }
        });
    });

    document.querySelectorAll('input[name="passFilter"]').forEach(radio => {
        radio.addEventListener('change', event => {
            filterPass = event.target.value;
            applyFiltersAndSort();
        });
    });

    document.querySelectorAll('.accSourceFilter').forEach(checkbox => {
        checkbox.addEventListener('change', event => {
            if (event.target.checked) {
                selectedAccSources.add(event.target.value);
            } else {
                selectedAccSources.delete(event.target.value);
            }
            applyFiltersAndSort();
        });
    });

    keywordInput.addEventListener('compositionstart', () => {
        isComposing = true;
        if (searchTimer) {
            clearTimeout(searchTimer);
            searchTimer = null;
        }
    });
    keywordInput.addEventListener('compositionend', () => {
        isComposing = false;
        runSearchImmediately();
    });
    keywordInput.addEventListener('input', scheduleSearch);
    keywordInput.addEventListener('keydown', event => {
        if (event.key === 'Enter' && !isComposing) {
            event.preventDefault();
            runSearchImmediately();
        }
    });
    document.getElementById('searchButton').addEventListener('click', runSearchImmediately);

    document.querySelectorAll('.quick-keyword-button').forEach(button => {
        button.addEventListener('click', () => {
            const keyword = button.dataset.keyword;
            const currentKeywords = keywordInput.value.trim();

            keywordInput.value = currentKeywords ? `${currentKeywords} ${keyword}` : keyword;
            isComposing = false;
            runSearchImmediately();
            keywordInput.focus();
        });
    });

    document.getElementById('resetButton').addEventListener('click', () => {
        if (searchTimer) {
            clearTimeout(searchTimer);
            searchTimer = null;
        }
        keywordInput.value = '';
        document.querySelectorAll('.accSourceFilter').forEach(checkbox => {
            checkbox.checked = checkbox.value === '0';
        });
        document.querySelector('input[name="passFilter"][value="1"]').checked = true;

        filterPass = '1';
        selectedAccSources.clear();
        selectedAccSources.add('0');
        currentSort = { key: null, order: null };
        updateSortIcons();
        applyFiltersAndSort();
    });

    updateSortIcons();
    loadData();
});
