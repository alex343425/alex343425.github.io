(() => {
  "use strict";

  const menu = document.querySelector(".menu-button");
  const navScrim = document.querySelector(".nav-scrim");
  const sidebar = document.querySelector(".sidebar");
  const backdrop = document.querySelector(".search-backdrop");
  const searchOpen = document.querySelector(".search-open");
  const searchClose = document.querySelector(".search-close");
  const input = document.querySelector("#search-input");
  const results = document.querySelector(".search-results");
  const searchUrl = new URL(document.body.dataset.searchUrl, location.href);
  const siteRoot = new URL("../", searchUrl);
  let searchData;
  let previousFocus;

  function setMenu(open) {
    document.body.classList.toggle("nav-open", open);
    navScrim.hidden = !open;
    menu.setAttribute("aria-expanded", String(open));
    menu.setAttribute("aria-label", open ? "關閉導覽" : "開啟導覽");
  }

  menu.addEventListener("click", () => setMenu(!document.body.classList.contains("nav-open")));
  navScrim.addEventListener("click", () => setMenu(false));
  document.querySelector(".main").addEventListener("click", () => setMenu(false));
  sidebar.querySelectorAll("a").forEach(link => link.addEventListener("click", () => setMenu(false)));

  async function loadSearch() {
    if (!searchData) {
      const response = await fetch(searchUrl);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      searchData = await response.json();
    }
    return searchData;
  }

  function showMessage(message) {
    results.replaceChildren();
    const paragraph = document.createElement("p");
    paragraph.className = "search-hint";
    paragraph.textContent = message;
    results.append(paragraph);
  }

  function snippet(text, query) {
    const compact = text.replace(/\s+/g, " ").trim();
    const position = compact.toLocaleLowerCase().indexOf(query);
    if (position < 0) return compact.slice(0, 115);
    const start = Math.max(0, position - 45);
    return `${start ? "…" : ""}${compact.slice(start, start + 130)}${compact.length > start + 130 ? "…" : ""}`;
  }

  async function search() {
    const query = input.value.trim().toLocaleLowerCase();
    if (!query) {
      showMessage("輸入關鍵字，搜尋所有 WIKI 頁面。");
      return;
    }
    try {
      const pages = await loadSearch();
      if (query !== input.value.trim().toLocaleLowerCase()) return;
      const found = pages.map(page => {
        const title = page.title.toLocaleLowerCase();
        const headings = page.headings.join(" ").toLocaleLowerCase();
        const content = page.text.toLocaleLowerCase();
        const titleMatch = title.includes(query);
        const headingMatch = headings.includes(query);
        const count = content.split(query).length - 1;
        return { page, score: (titleMatch ? 100 : 0) + (headingMatch ? 40 : 0) + Math.min(count, 12), count };
      }).filter(item => item.score > 0).sort((a, b) => b.score - a.score).slice(0, 15);
      results.replaceChildren();
      if (!found.length) {
        showMessage("沒有找到符合的頁面，試試人物別名或較短的詞。");
        return;
      }
      for (const { page } of found) {
        const anchor = document.createElement("a");
        anchor.className = "search-item";
        anchor.href = new URL(page.url, siteRoot).href;
        const category = document.createElement("span");
        category.textContent = page.category;
        const title = document.createElement("strong");
        title.textContent = page.title;
        const preview = document.createElement("small");
        preview.textContent = snippet(page.text, query);
        anchor.append(category, title, preview);
        results.append(anchor);
      }
    } catch {
      showMessage("搜尋索引無法載入。請從網站網址開啟頁面，或稍後重試。");
    }
  }

  async function openSearch() {
    previousFocus = document.activeElement;
    backdrop.hidden = false;
    document.body.style.overflow = "hidden";
    input.focus();
    if (input.value) await search();
  }

  function closeSearch() {
    backdrop.hidden = true;
    document.body.style.overflow = "";
    previousFocus?.focus();
  }

  searchOpen.addEventListener("click", openSearch);
  searchClose.addEventListener("click", closeSearch);
  backdrop.addEventListener("click", event => {
    if (event.target === backdrop) closeSearch();
  });
  input.addEventListener("input", search);
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      if (!backdrop.hidden) closeSearch();
      else setMenu(false);
    }
    if (event.key === "/" && backdrop.hidden && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) {
      event.preventDefault();
      openSearch();
    }
  });

  const tocLinks = [...document.querySelectorAll(".toc a")];
  if (tocLinks.length && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        tocLinks.forEach(link => link.classList.toggle("current", link.hash === `#${entry.target.id}`));
      }
    }, { rootMargin: "-90px 0px -75% 0px" });
    tocLinks.forEach(link => {
      const heading = document.querySelector(link.hash);
      if (heading) observer.observe(heading);
    });
  }
})();
