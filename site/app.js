/* Мягкое проявление при первом входе в кадр + оглавление на мобильных. */
(function () {
  "use strict";

  var shown = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        shown.unobserve(e.target);
      }
    });
  }, { threshold: 0.18 });

  document.querySelectorAll(".reveal").forEach(function (el) { shown.observe(el); });

  var toc = document.querySelector(".toc");
  var burger = document.querySelector(".burger");
  burger.addEventListener("click", function () {
    var open = toc.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  toc.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () { toc.classList.remove("open"); });
  });

  var form = document.querySelector(".guestbook");
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    form.querySelector(".form-note").hidden = false;
    form.querySelector("input").value = "";
  });
})();
