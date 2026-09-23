/* Лаборатория феминности · site_v2
   Мягкое проявление при входе в кадр, оглавление, номера глав, форма-гостевая.
   Никаких всплывающих окон и резких анимаций — книга листается тихо. */
(() => {
  "use strict";

  /* JS есть — можно прятать блоки до проявления */
  document.documentElement.classList.remove("no-js");

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const canObserve = "IntersectionObserver" in window;

  /* ── проявление блоков при первом входе в кадр ────── */
  const faders = document.querySelectorAll(".fade-in");
  if (reduced || !canObserve) {
    for (const el of faders) el.classList.add("visible");
  } else {
    const shown = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
          shown.unobserve(e.target);
        }
      }
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    for (const el of faders) shown.observe(el);
  }

  /* ── оглавление: активная глава + точки сбоку ─────── */
  const chapters = document.querySelectorAll("main section[id]");
  const tocLinks = document.querySelectorAll(".nav-contents a");
  const dots = document.querySelectorAll(".page-dot");

  const markActive = (id) => {
    const target = `#${id}`;
    for (const a of tocLinks) a.classList.toggle("active", a.getAttribute("href") === target);
    for (const d of dots) d.classList.toggle("active", d.getAttribute("href") === target);
  };

  if (canObserve) {
    const spy = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) markActive(e.target.id);
    }, { threshold: 0.25, rootMargin: "-10% 0px -55% 0px" });
    for (const s of chapters) spy.observe(s);
  }

  /* ── оглавление на мобильных ──────────────────────── */
  const nav = document.getElementById("mainNav");
  const hint = document.querySelector(".title-scroll-hint");
  const toggle = document.getElementById("navToggle");
  const menu = document.getElementById("mobileMenu");
  let menuOpen = false;

  const setMenu = (open) => {
    if (!toggle || !menu) return;
    menuOpen = open;
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
    if (open) {
      menu.querySelector("a")?.focus();
    } else {
      toggle.focus();
    }
    nav?.classList.remove("dimmed");
  };

  if (toggle && menu) {
    toggle.addEventListener("click", () => setMenu(!menuOpen));
    menu.addEventListener("click", (ev) => {
      if (ev.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && menuOpen) setMenu(false);
    });
  }

  /* ── оглавление прячется при листании вниз ────────── */
  let last = window.scrollY;
  let ticking = false;

  const onScrollFrame = () => {
    const y = window.scrollY;
    const goingDown = y > last && y > window.innerHeight * 0.8;
    nav?.classList.toggle("dimmed", goingDown && !menuOpen);
    if (hint && y > 80) hint.classList.add("gone");
    last = y;
    ticking = false;
  };

  window.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(onScrollFrame);
  }, { passive: true });

  /* ── форма-гостевая: мягкое подтверждение ─────────── */
  const form = document.getElementById("guestbook");
  form?.addEventListener("submit", (ev) => {
    ev.preventDefault();
    const note = form.querySelector(".form-note");
    const input = form.querySelector("input");
    const btn = form.querySelector(".subscribe-btn");
    note.hidden = false;
    input.value = "";
    btn.disabled = true;
    btn.textContent = "спасибо…";
    window.setTimeout(() => {
      btn.disabled = false;
      btn.textContent = "оставить";
    }, 4000);
  });
})();
