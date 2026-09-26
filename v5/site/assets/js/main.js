/* Лаборатория феминности — v5 */
(function () {
  'use strict';

  /* появление секций */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('is-visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  /* активная точка боковой навигации */
  const dots = document.querySelectorAll('.side-dot');
  const sections = [...dots].map((d) => document.getElementById(d.dataset.section)).filter(Boolean);
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      dots.forEach((d) => d.classList.toggle('active', d.dataset.section === e.target.id));
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  sections.forEach((s) => spy.observe(s));

  /* мягкий тост */
  const toast = document.getElementById('toast');
  let toastTimer;
  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 3400);
  }

  /* ссылки на страницы циклов — пока готовятся */
  document.querySelectorAll('.cycle-link').forEach((a) => {
    a.addEventListener('click', (ev) => {
      ev.preventDefault();
      showToast('Страница цикла готовится — напишите нам, и мы расскажем подробнее.');
    });
  });

  /* подписка (без бэкенда — мягкое подтверждение) */
  const form = document.getElementById('subscribe');
  const note = document.getElementById('subscribe-note');
  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const email = form.email.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showToast('Проверьте, пожалуйста, адрес почты.');
      form.email.focus();
      return;
    }
    form.hidden = true;
    note.hidden = false;
  });
})();
