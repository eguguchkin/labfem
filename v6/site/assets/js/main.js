/* Лаборатория Феминности — v6, этап 2 (ревизия по правкам пользователя).
   Статическая версия + навигация-«оглавление». Плавный скролл по якорям — CSS
   (html{scroll-behavior:smooth}).

   Навигация: появляется после прокрутки ниже 60% hero, активный пункт —
   секция под верхней кромкой вьюпорта (IntersectionObserver). */
(function () {
  var nav = document.getElementById('nav');
  if (!nav) return;
  var links = Array.prototype.slice.call(nav.querySelectorAll('a'));
  var secs = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });

  function onScroll() {
    var show = window.scrollY > window.innerHeight * 0.6;
    nav.classList.toggle('on', show);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a, i) {
          a.classList.toggle('active', secs[i] === e.target);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    secs.forEach(function (s) { if (s) io.observe(s); });
  }
})();

/* План этапа 4 (анимации и эффекты):
   1. reveal-on-scroll: IntersectionObserver, класс .rv → opacity/translateY,
      задержки каскадом для медальонов и карточек; гасить при reduced-motion.
   2. параллакс полотен: translateY по scrollY с коэффициентом .06–.1 для
      .pair-canvas и .hero-canvas (transform, без layout-трэш).
   3. «дыхание света»: медленная пульсация box-shadow у .medallion-ring
      (keyframes 8s, только при reduced-motion: no-preference).
   4. форма подписки: перехват submit, строка «письмо дойдёт… спасибо» italic
      вместо отправки (action="#" остаётся fallback без JS).
   5. лёгкий ken-burns для hero-canvas (scale 1→1.04 за 24s, alternate).
*/
