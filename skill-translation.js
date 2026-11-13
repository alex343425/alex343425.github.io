const skillTranslationUrl = 'https://raw.githubusercontent.com/alex343425/otogitranslate/refs/heads/main/Skills/skills.json';

// 沿用 otogitranslate 的完整句子／數字模板比對，不改動原始資料與搜尋 TAG。
function createSkillTranslator(dictionary) {
    const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
    const placeholders = text => [...text.matchAll(/\{(\d+)\}/g)]
        .map(match => Number(match[1])).sort((a, b) => a - b).join(',');
    const normalizeNewlines = (text, separator) =>
        text.replace(/(?:\r\n|\r|\n|\\r\\n|\\r|\\n)+/g, separator);
    const aliases = { exact: new Map(), templates: new Map() };

    if (!dictionary || dictionary.schemaVersion !== 1 || dictionary.locale !== 'zh-TW') {
        throw new Error('技能翻譯字典格式或語系不符');
    }
    for (const field of ['exact', 'templates']) {
        const entries = dictionary[field];
        if (!entries || typeof entries !== 'object' || Array.isArray(entries)) {
            throw new Error(`技能翻譯字典缺少 ${field}`);
        }
        for (const [source, target] of Object.entries(entries)) {
            if (!source || typeof target !== 'string' || !target.trim() ||
                (field === 'templates' && placeholders(source) !== placeholders(target)) ||
                (field === 'exact' && /\{\d+\}/.test(target))) {
                throw new Error('技能翻譯字典含有無效譯文或數字佔位符');
            }
            // 遊戲描述的實際／字面換行，在網頁資料中可能已改成「、」或刪除。
            // 只將這些格式差異建立為完整句子的別名，保留原始精確匹配的優先權。
            for (const separator of ['、', '']) {
                const normalized = normalizeNewlines(source, separator);
                if (normalized !== source && !own(entries, normalized)) {
                    aliases[field].set(normalized, target);
                }
            }
        }
    }

    function describe(source) {
        const exact = own(dictionary.exact, source) ? dictionary.exact[source] : aliases.exact.get(source);
        if (exact !== undefined) return exact;
        if (/\{\d+\}/.test(source)) return null;
        const values = [];
        const key = source.replace(/[0-9０-９]+(?:[.．][0-9０-９]+)?/g,
            value => `{${values.push(value) - 1}}`);
        const template = own(dictionary.templates, key) ? dictionary.templates[key] : aliases.templates.get(key);
        if (template === undefined) return null;
        return template.replace(/\{(\d+)\}/g, (_, index) => values[Number(index)]);
    }

    const caches = { skill: new Map(), leader: new Map() };
    return function translateDescription(source, leader = false) {
        if (typeof source !== 'string') return source;
        const cache = leader ? caches.leader : caches.skill;
        if (cache.has(source)) return cache.get(source);

        // 網頁自行附加的中文搜尋備註不屬於遊戲描述，須分開比對後接回。
        const noteIndex = source.search(/<br\s*\/?\s*>(?=降(?:抗搜尋|血技能)：)/i);
        const body = noteIndex < 0 ? source : source.slice(0, noteIndex);
        const notes = noteIndex < 0 ? '' : source.slice(noteIndex);
        const candidates = [body];
        if (leader) {
            // 隊長技能的分隔逗號在匯出時已變成 <br>，先還原再比對完整模板。
            const breaks = /<br\s*\/?\s*>|&br;|\r\n|\r|\n|\\r\\n|\\r|\\n/gi;
            candidates.push(body.replace(breaks, '、'), body.replace(breaks, ''));
        }
        let translated = null;
        for (const candidate of candidates) {
            translated = describe(candidate);
            if (translated !== null) break;
        }
        let result = source;
        if (translated !== null) {
            translated = normalizeNewlines(translated, '、');
            // 只有隊長技能沿用逗號換行；固有技、專武、飾品保留譯文標點。
            if (leader) translated = translated.replace(/、|&br;|\r\n|\r|\n|\\r\\n|\\r|\\n/g, '<br>');
            result = translated + notes;
        }
        cache.set(source, result);
        return result;
    };
}

// 各頁僅提供描述與重新渲染函式；字典只在第一次切換中文時下載。
function createSkillLanguageControl({ container, getDescriptions = () => [], onChange,
    label = '切換技能描述的日文／繁體中文' }) {
    let language = 'ja';
    let translator = null;
    let busy = false;
    let ready = false;
    const button = document.getElementById('skillLanguageToggle') || document.createElement('button');
    button.id = 'skillLanguageToggle';
    button.type = 'button';
    button.innerHTML = '<span class="language-ja">日文</span> / <span class="language-zh">中文</span>';
    button.setAttribute('aria-label', label);
    if (container) container.prepend(button);

    let overlay = document.getElementById('translationOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'translationOverlay';
        overlay.className = 'translation-overlay';
        overlay.hidden = true;
        overlay.innerHTML = '<div class="translation-progress" role="status" aria-live="polite" aria-atomic="true"><div class="translation-spinner" aria-hidden="true"></div><p id="translationMessage"></p></div>';
        document.body.append(overlay);
    }
    const message = document.getElementById('translationMessage');
    const yieldForPaint = () => new Promise(resolve => setTimeout(resolve, 20));
    function updateButton() {
        button.disabled = !ready || busy;
        button.setAttribute('aria-pressed', String(language === 'zh-TW'));
        button.title = language === 'zh-TW'
            ? '目前為繁體中文，按下切換為日文' : '目前為日文，按下切換為繁體中文';
    }
    updateButton();

    button.addEventListener('click', async () => {
        if (busy || !ready) return;
        busy = true;
        updateButton();
        const nextLanguage = language === 'ja' ? 'zh-TW' : 'ja';
        message.textContent = nextLanguage === 'zh-TW' && !translator
            ? '正在抓取中文文本…' : '正在切換技能描述…';
        overlay.hidden = false;
        document.body.setAttribute('aria-busy', 'true');
        try {
            await yieldForPaint();
            if (nextLanguage === 'zh-TW' && !translator) {
                const controller = new AbortController();
                const timeout = setTimeout(() => controller.abort(), 45000);
                let jsonText;
                try {
                    const response = await fetch(skillTranslationUrl, { signal: controller.signal });
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    jsonText = await response.text();
                } finally {
                    clearTimeout(timeout);
                }
                message.textContent = '正在處理翻譯…';
                await yieldForPaint();
                const translate = createSkillTranslator(JSON.parse(jsonText.replace(/^\uFEFF/, '')));
                const descriptions = getDescriptions();
                for (let start = 0; start < descriptions.length; start += 200) {
                    descriptions.slice(start, start + 200).forEach(entry => {
                        if (typeof entry === 'string') translate(entry);
                        else translate(entry.source, entry.leader);
                    });
                    message.textContent = `正在處理翻譯… ${Math.min(start + 200, descriptions.length)} / ${descriptions.length}`;
                    await yieldForPaint();
                }
                translator = translate;
            }
            language = nextLanguage;
            onChange();
        } catch (error) {
            console.error('技能翻譯載入失敗：', error);
            alert('中文文本載入或處理失敗，請稍後再試。');
        } finally {
            busy = false;
            updateButton();
            overlay.hidden = true;
            document.body.removeAttribute('aria-busy');
            button.focus({ preventScroll: true });
        }
    });

    function display(source, leader = false) {
        return language === 'zh-TW' && translator ? translator(source, leader) : source;
    }
    return {
        button,
        display,
        text: (source, leader = false) => String(display(source, leader) || '').replace(/<br\s*\/?\s*>/gi, '\n'),
        searchTexts: (source, leader = false) => [...new Set([display(source, leader), source])]
            .map(text => String(text || '').replace(/<br\s*\/?\s*>/gi, '、')),
        setReady(value = true) { ready = value; updateButton(); }
    };
}

