# Задание на этап 2 — вёрстка статического сайта (desktop + mobile)

Контекст: этап 1 завершён. Готовы: work/brandbook.md (дух, ценности, ToV),
work/stylebook.md (токены, типографика, фактуры, компоненты, сетка),
work/structure-texts.md (финальные тексты 8 секций), work/prompts.md (промпты),
все изображения в site/assets/img/{tex,hero,paint,cards,orn,authors,meta}.
Работаем ТОЛЬКО в /home/pi/workspace/labfem/v6 (spec/ не трогаем, другие v<N> не читаем).

## Что сделать

1. **Шрифты.** Самохост woff2: Cormorant (400,500,600 + italic) и EB Garamond (400,500 + italic),
   подмножества cyrillic + latin, в site/assets/fonts/ + @font-face в style.css
   (font-display: swap). Скачать с Google Fonts (woff2 через UA-заголовок Chrome) или
   fonts.gstatic.com. Если сеть недоступна — fallback-стек 'Cormorant Garamond', Georgia, serif
   и пометить TODO в style.css.

2. **site/index.html** — одна страница, 8 секций по work/structure-texts.md, якоря
   #lab #feminity #optics #for-whom #about #meetings #format #invite.
   Семантика: header (hero) + section*7 + footer. Все тексты — дословно из structure-texts.md.
   Ссылки: карточка «кошка» → https://cats.jungway.ru/ (target _blank rel noopener),
   telegram-заглушка → #. Форма подписки: action="#" method="post" (JS этапа 4 перехватит).
   meta: charset, viewport, description, og:title/og:description/og:image=assets/img/meta/og-cover.webp,
   theme-color #04150d, favicon (сгенерить 32x32 из fleuron: PIL, alpha).
   Изображения: width/height атрибуты, alt по смыслу полотна, loading=lazy кроме hero.

3. **site/assets/css/style.css** — вся палитра и состояния токенами в :root (копировать
   блок токенов из stylebook.md §1 дословно). Реализовать:
   - слои фона: html{background:var(--velvet-deep)}; html::before — velvet-tile repeat
     background-size 1024px; html::after — crackle-tile repeat 640px, mix-blend soft-light,
     opacity .14, pointer-events none, z-index выше контента (учесть ловушку v5: фон body
     не ставить, текстурные слои только на html).
   - типографика по stylebook §2; лейблы/номера секций по §2.
   - арки и багеты по §4 (двойная линия: outer 1px --gold-dim, inner 1px --gold, зазор 6-8px;
     арка border-radius 50% 50% 0 0 / 30% 30% 0 0).
   - компоненты по §5: кнопка-табличка, карточка программы (арка 4:5), портрет автора
     (арка 2:3), цитата-панель, форма (поле на parchment-tile, текст --velvet-deep).
   - сетка по §6: контейнер 1160px; hero min-height 100svh; секции-простенки 60-70svh;
     парность текст/полотно с зеркалом; разделители — волосяная линия + fleuron.
   - состояния по §7 (hover/focus-visible/reduced-motion).
   - брейкпоинты: ≥1024 desktop; 641-1023 планшет (колонки 2 для оптик и карточек);
     ≤640 mobile: всё в колонку, H1 40-56px, карточки 100% ширины, медальоны 2×2.

4. **site/assets/js/main.js** — на этапе 2 МИНИМАЛЬНЫЙ: плавный скролл по якорям
   (scroll-behavior: smooth в css достаточно; js оставить пустым с комментарием-планом
   этапа 4). Никаких эффектов.

5. **Сборка/проверка локально:** открыть через python http.server 0.0.0.0:8080 из site/;
   скриншоты desktop 1440x900 и mobile 390x844: playwright-core + chrome-headless-shell
   (см. memory pibox-headless-screenshots: LD_LIBRARY_PATH=chrome-sysroot, гасить CSS-анимации;
   скрипт /tmp/shots/shoot.js из v5 можно воссоздать: сначала прокрутить всю страницу,
   затем img.loading='eager' + waitForFunction complete; fullPage >16384px не снимать —
   только вьюпорт-снимки по секциям). Скриншоты сохранять в /tmp/lab6/shots2/.

6. **Самопроверка перед сдачей:** все 8 секций присутствуют; тексты совпадают с
   structure-texts.md дословно; ни одного цвета вне палитры (grep по css: только var(--*)
   и токены в :root); все img существуют (битых ссылок нет); мобильная вёрстка без
   горизонтального скролла (document.scrollingElement.scrollWidth == innerWidth).

## Критерий готовности
Страница открывается, выглядит как «тёмный зал с восемью полотнами»: бархатный фон без
швов, золото только линиями/багетом, арки у hero/портретов/карточек, кракелюр поверх
всего едва заметен. Скриншоты desktop+mobile приложены к отчёту (по 4-5 вьюпорт-кадров:
hero, оптика, о нас, встречи, приглашение).

## Отчёт
Коротко: что сделано, список файлов, известные компромиссы, путь к скриншотам.
Далее — сформулировать задание этапа 3 (проверка текстур/цветов/шрифтов + предложения
визуальных эффектов) в work/next-stage-prompt.md, перезаписав этот файл.
