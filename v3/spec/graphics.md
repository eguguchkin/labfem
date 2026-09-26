# Аудит графики и пакет ТЗ для генерации в растре

## 0. Что рисует графику в текущем коде (источники для замены)

| Тип | Узел кода | Комментарий |
|---|---|---|
| Живописные панели | SVG-symbols `#paint-hero`, `#paint-hands`, `#paint-persephona`, `#paint-venus`, `#paint-demeter`, `#paint-ariadne`, `#mono-pk`, `#mono-vg`, `#paint-terrace` | векторные «заглушки» темперы → заменяются растром 1:1 по узлам |
| Орнамент | `#floret` (разделители `.divider` + лепестки `.petals`), `#sprig` (определён, но не задействован), глиф `❧` в `.modal-card ul li::before` и `.event .rows i` | → растр с альфой |
| Буллиты/точки | CSS-фигуры `.list-orn li::before` (капля-зерно), `.tl li::before` + `.soon/.done` (точки таймлайна) | → растр с альфой |
| Лого/иконки | `#pom` (`.brand`, `footer .mark`), `#i-psy/#i-myth/#i-art/#i-exp` (`.lens .med`) | → растр с альфой |
| Текстуры/фоны | `body::after` (data-URI feTurbulence), CSS-градиенты секций, `.partner`, `#s8.warm` | → растровые тайлы/воши |
| Остаётся вектором/CSS | шеврон `select` (data-URI), линии `.divider::before/after`, статус-чипы, кнопки, золотые круги `.frame::before/after` | генерация не нужна |

## 1. Структура файлов и общий пайплайн

```
/img/
  paint/  hero-woman-pomegranate.webp · hands-pomegranate-peach.webp · cycle-persephona.webp ·
          cycle-venus.webp · cycle-demeter.webp · cycle-ariadne.webp · monogram-polina.webp ·
          monogram-veronika.webp · terrace-panorama.webp
  orn/    floret-gold.png · floret-peach.png · floret-pomegranate.png · fleuron-gold.png ·
          bullet-seed.png · dot-seed-pomegranate.png · dot-seed-peach.png · dot-seed-emerald.png ·
          sprig-gold.png · watermark-wreath.png
  icon/   icon-psy.png · icon-myth.png · icon-art.png · icon-exp.png
  logo/   logo-pom.png · logo-pom-peach.png · favicon-32.png · apple-touch-180.png
  tex/    paper-grain.png · tempera-crackle.png · goldleaf-on-black.png · peach-wash.png
  meta/   og-cover.png
```

Правила пайплайна (применимы ко всем пунктам):
- Генерировать в **2× от целевого размера**, затем даунскейл до целевого (Lanczos), экспорт: живописные панели и воши — **WebP q82**; орнамент, иконки, лого, буллиты, точки — **PNG 8-bit с альфой**; текстуры — **PNG 24-bit seamless**.
- Альфа: qwen-image-3 не умеет прозрачность → все «изолированные» элементы генерируются **на чисто-белом фоне**, затем вырезка: `magick in.png -fuzz 8% -transparent white +dither out.png` (для тонких линий дополнительно `-channel A -blur 0x0.4 +channel`).
- Бесшовность текстур проверять монтажом 2×2; швы править offset-тестом (`magick t.png -page +256+256 -virtual-pixel Tile -flatten`).
- Все `<img>` получают явные `width/height`; ниже первого экрана — `loading="lazy" decoding="async"`; герой — `fetchpriority="high"`.
- Арочные кропы (герой, карточки) делает CSS (`.ph{border-radius:999px 999px 10px 10px;overflow:hidden}`), поэтому растр прямоугольный, но **композиция учитывает safe-area** (указано в промптах).
- После полной замены удалить из `<defs>` все symbols и gradients (они больше не нужны), кроме удалённого блока — ничего не оставлять.

**Общее стилевое ядро STYLE CORE** (вшивается в каждый промпт живописи дословно):
`Italian Quattrocento tempera panel in the manner of Sandro Botticelli and Simone Martini: fine graceful linear contours, soft matte egg-tempera surface, delicate gold-leaf line work and punched gold dots, serene idealized forms, elongated elegant proportions. Strict palette: emerald green #17564A and deep emerald #0D3B32, deep ultramarine blue #1F3164 and #15224A, golden sand #F1E7D2 and #E8DBBC, warm paper ivory #FBF5E8, blush peach #E58F6E, pomegranate red #A6403A, antique gold #B98A2E, pale gold #E7D3A4. Luminous warm ivory-gold ambient light, airy and light, never dark or muddy. Flat decorative perspective, ornamental detailing. No text, no letters, no watermark, no signature, no frame, no modern objects.`

---

## A. Живописные панели (9)

### A1. Герой: «Женщина с гранатом на террасе»
- **Узел сейчас:** `#s1 figure#heroFig .ph > svg > use#paint-hero`
- **Файл:** `/img/paint/hero-woman-pomegranate.webp`, целевой размер **840×1120 (3:4)**, генерировать 1024×1365+
- **Промпт:** `STYLE CORE Vertical composition, aspect ratio 3:4. A serene young woman with long wind-blown wavy golden hair (#D8A452 highlights, #C08A3E shadows) standing on a sunlit Mediterranean villa terrace; behind her a white-gold stone balustrade, slender dark cypresses #0D3B32 and olive trees, a horizontal band of deep ultramarine sea #1F3164 with thin gold wave lines, hazy blue-grey mountains on the horizon; soft peach-gold ivory sky with a pale gold sun disc #F3DFAE upper right. She wears an emerald green gown #17564A with two thin antique-gold trim arcs and a deep ultramarine drapery #15224A over one shoulder; in her lowered hand a pomegranate branch with one ripe split pomegranate #A6403A showing ivory-ruby seeds and two emerald leaves. Thin gold vine ornament with tiny four-petal blossoms curls into both upper corners; scattered gold-leaf specks in the sky. Arched-top crop safe area: face and head fully inside central 60% of width and below top 18% of height; upper corners contain only sky, sun and ornament; lower edge may cut the gown. Frontal three-quarter pose, calm downward-soft gaze, blush peach on cheeks and lips #C4574E.`
- **Размещение:** заменить `<svg>…</svg>` внутри `.ph` на `<img src="/img/paint/hero-woman-pomegranate.webp" width="840" height="1120" fetchpriority="high" alt="Женщина с ветвью граната на средиземноморской террасе, темпера в манере Боттичелли">`; добавить один раз глобально CSS: `.ph img,.terrace img,.oval img{width:100%;height:auto;display:block;object-fit:cover}`. Арку и двойную золотую кайму оставляет существующий `.frame/.ph`.

### A2. Деталь: «Руки с гранатом и персиком»
- **Узел:** `#s2 figure.frame .ph > svg > use#paint-hands`
- **Файл:** `/img/paint/hands-pomegranate-peach.webp`, **800×800 (1:1)**
- **Промпт:** `STYLE CORE Square composition 1:1. A tempera still-life detail: two graceful feminine hands with pale warm skin #F7E3CE entering from lower-left and lower-right, cupped together at the exact center, holding a split pomegranate #A6403A with glossy ruby seeds and one blush peach #E58F6E with a single emerald leaf; sleeve hints of deep emerald #0D3B32 and ultramarine #15224A fabric in the two bottom corners. A thin antique-gold #B98A2E vine ornament with pale-gold #E7D3A4 leaves and tiny blossoms curls around the fruit across a warm golden-sand background #F1E7D2; scattered punched gold dots. Centered symmetric composition, plain sand margins of at least 8% on all edges, no vignette.`
- **Размещение:** `<img src="…" width="800" height="800" loading="lazy" alt="Руки, держащие гранат и персик, темперная деталь">` внутри того же `.ph`.

### A3–A6. Панели циклов (4 штуки, единый формат)
- **Узлы:** `#s6 .tcard .ph > svg > use#paint-persephona / #paint-venus / #paint-demeter / #paint-ariadne` (порядок карточек слева направо)
- **Файлы:** `cycle-persephona.webp`, `cycle-venus.webp`, `cycle-demeter.webp`, `cycle-ariadne.webp`, **600×760 (≈3:3.8)**, генерировать 768×960+
- **Общее в каждом промпте:** `…Arched-top crop safe area: main emblem fully inside central 70% of width and below top 20% of height; upper corners only sky/ornament. No human figures.`

**A3 Персефона:** `STYLE CORE Vertical composition, aspect ratio 4:5. Emblem of Persephone: an ancient doorway arch in deep ultramarine shadow #15224A at the left edge, four wide sand-stone steps #E8DBBC with fine joint lines descending from the doorway toward lower right into a blooming spring garden; a single ripe pomegranate #A6403A with gold crown lying on the second step; slender emerald shoots #1E6B5C with young leaves and small peach-pink anemone flowers #E58F6E rising on the right; left third of the panel subtly cooler and shadowed, right two thirds warm luminous ivory-gold light; thin gold vine ornament in the upper right corner; scattered gold specks. No human figures. Arched-top crop safe area as above.`
**A4 Венера:** `STYLE CORE Vertical composition, aspect ratio 4:5. Emblem of Venus Anadyomene: a large golden scallop shell #EFDDB4 with fine radiating ribs floating on a band of deep ultramarine sea #1F3164 with thin gold wave lines occupying the lower third; a single luminous ivory pearl resting in the shell; three blush-peach roses #E58F6E with pale centers flying through the warm ivory sky on thin gold wind swirls; a pale gold sun halo #F3DFAE above; scattered gold specks. No human figures. Arched-top crop safe area as above.`
**A5 Деметра:** `STYLE CORE Vertical composition, aspect ratio 4:5. Emblem of Demeter: an upright golden wheat sheaf #E9C078 with detailed ears, tied by a pomegranate-red #A6403A ribbon bow, standing in a shallow woven sand-stone basket #E8DBBC; inside the basket two blush peaches #E58F6E and one pomegranate #A6403A; olive-green branches #5E7264 with narrow leaves at both lower sides; a thin detached gold ring halo #D8B878 floating behind the wheat tips against warm ivory sky; scattered gold specks. No human figures. Arched-top crop safe area as above.`
**A6 Ариадна:** `STYLE CORE Vertical composition, aspect ratio 4:5. Emblem of Ariadne: a circular green hedge labyrinth #5E7264 drawn as three concentric rings with small gaps, seen frontally on warm sand ground #E4D5B2; a shining antique-gold thread #D8B878 winding from a small gold thread ball at lower left through the labyrinth gaps to a blush-peach heart-shaped blossom #E58F6E at the labyrinth center; a band of deep ultramarine sea #1F3164 with hazy mountains high on the horizon; thin gold vine ornament upper left; scattered gold specks. No human figures. Arched-top crop safe area as above.`
- **Размещение (каждая):** `<img src="/img/paint/cycle-venus.webp" width="600" height="760" loading="lazy" decoding="async" alt="Эмблема цикла „Венера": раковина, жемчужина и розы на море">` (alt по смыслу панели) внутрь соответствующего `.tcard .ph`.

### A7–A8. Медальоны команды (фон под типографскую монограмму)
- **Узлы:** `#s5 .person .oval > svg > use#mono-pk / #mono-vg`
- **Файлы:** `monogram-polina.webp`, `monogram-veronika.webp`, **320×380 (4:4.75)**
- **Промпт A7:** `STYLE CORE Vertical composition 4:5. An ornamental medallion background: warm ivory-gold field #FBF3E0; the exact center left completely empty as a smooth clean ivory oval area reserved for future typography; from both lower corners rise thin antique-gold #B98A2E vine sprigs with pale-gold #E7D3A4 leaves; at the bottom edge a small laurel branch and a tiny open book silhouette in deep emerald #0D3B32 line work; a single pomegranate-red dot #A6403A under the empty center; scattered gold specks; plain even margins, no vignette. No letters, no text anywhere.`
- **Промпт A8:** то же, но атрибуты внизу: `a thin paintbrush crossed with a small round hand mirror in deep ultramarine #15224A line work`, точка под центром — `blush-peach dot #E58F6E`.
- **Размещение:** монограмму-буквы больше не генерируем и не рисуем SVG — накладываем типографикой:
```html
<div class="oval"><img src="/img/paint/monogram-polina.webp" width="320" height="380" loading="lazy" alt="Орнаментальный медальон Полины Кронер"><b class="mono-letter">ПК</b></div>
```
```css
.person .oval{position:relative;overflow:hidden}
.mono-letter{position:absolute;inset:0;display:grid;place-items:center;font-family:'Cormorant',serif;
  font-style:italic;font-weight:600;font-size:clamp(44px,4vw,60px);color:var(--emerald-deep);padding-bottom:10px}
.person+.person .mono-letter{color:var(--blue-deep)}
```

### A9. Панорама террасы
- **Узел:** `#s8 .terrace > svg > use#paint-terrace`
- **Файл:** `/img/paint/terrace-panorama.webp`, **2400×840 (20:7)**, генерировать широкоформатно
- **Промпт:** `STYLE CORE Wide horizontal panorama, aspect ratio 20:7. An empty Mediterranean terrace in late summer golden light: foreground warm sand-stone floor #E4D5B2 with faint joint lines; at center a round wooden table #C9A25C with a deep-blue ceramic jug #1F3164 and a shallow bowl of blush peaches #E58F6E and pomegranates #A6403A; six empty dark-emerald #0D3B32 chairs standing in a loose circle around the table; behind, a white-gold stone balustrade with two urns; beyond it a band of deep ultramarine sea #1F3164 with thin gold wave lines, hazy blue-grey mountains, slender cypresses and olive trees bearing pomegranate fruits at both sides; warm ivory-peach sky with a pale gold sun glow upper right; scattered gold specks. Absolutely no people, no animals, no text. Horizon at upper third; keep table and chairs inside central 60% of width.`
- **Размещение:** `<img src="/img/paint/terrace-panorama.webp" width="2400" height="840" loading="lazy" alt="Пустая средиземноморская терраса с кругом стульев, морем и горами">` внутрь `.terrace` (скругление 20px уже есть).

---

## B. Орнамент, разделители, буллиты (7 позиций / 11 файлов)

Стилевое ядро орнамента ORN CORE (вшивать дословно): `Flat decorative ornament in Italian Quattrocento grotesque style, thin elegant uniform strokes with graceful curls, vector-like flat illustration, perfectly centered, isolated on solid pure white background, no shadow, no gradient, no texture, no text, no border, crisp clean edges.`

### B1. Розетка-флорет, 3 колорита
- **Узлы:** `.divider svg use#floret` (2 разделителя) и `.petals span svg use#floret` (6 лепестков: 3 золотых, 2 персиковых, 1 гранатовый)
- **Файлы:** `orn/floret-gold.png`, `orn/floret-peach.png`, `orn/floret-pomegranate.png`, **64×64**, альфа
- **Промпт (gold):** `ORN CORE A small symmetric four-petal rosette fleuron: four almond-shaped petals arranged as a cross around one round center dot, single flat color antique gold #B98A2E, square 1:1.` (peach: `single flat color blush peach #E58F6E`; pomegranate: `single flat color pomegranate red #A6403A`)
- **Размещение:** разделители: `<div class="divider" aria-hidden="true"><img src="/img/orn/floret-gold.png" alt="" width="26" height="26"></div>` + CSS `.divider img{width:26px;height:26px}`; лепестки: внутри каждого `.petals span` заменить svg на `<img src="/img/orn/floret-gold.png" alt="" width="16" height="16">` (span 2,6 → peach, span 4 → pomegranate) + CSS `.petals img{width:16px;height:16px}`.

### B2. Флерон-лист (буллит модалки и карточки события)
- **Узлы:** `.modal-card ul li::before{content:"❧"}`, `.event .rows i` (текст «❧»)
- **Файл:** `orn/fleuron-gold.png`, **48×48**, альфа
- **Промпт:** `ORN CORE A single curled acanthus-leaf fleuron (foliate hand) tilted to upper-right: one main spiral curl with three small leaflets and a tiny bud tip, single flat color antique gold #B98A2E, square 1:1.`
- **Размещение:**
```css
.modal-card ul li::before{content:"";position:absolute;left:2px;top:.28em;width:15px;height:15px;
  background:url('/img/orn/fleuron-gold.png') center/contain no-repeat}
.event .rows i{display:inline-block;width:15px;height:15px;vertical-align:-2px;margin-right:8px;
  background:url('/img/orn/fleuron-gold.png') center/contain no-repeat}
```
и в HTML `.event .rows` заменить `<i>❧</i>` на пустой `<i></i>`.

### B3. Буллит-зерно списков
- **Узел:** `.list-orn li::before` (сейчас CSS-капля с radial-gradient)
- **Файл:** `orn/bullet-seed.png`, **48×48**, альфа
- **Промпт:** `ORN CORE but softly colored: a single pomegranate-seed teardrop bud, rounded drop with a pointed tip tilted 45 degrees to upper-left, filled with a soft radial blend from blush peach #E58F6E at the highlight to pomegranate red #A6403A at the base, outlined by a hairline antique-gold #B98A2E contour, one tiny ivory highlight dot; isolated on pure white, square 1:1.`
- **Размещение:**
```css
.list-orn li::before{content:"";position:absolute;left:1px;top:.42em;width:15px;height:15px;
  background:url('/img/orn/bullet-seed.png') center/contain no-repeat;border-radius:0;transform:none}
```

### B4. Точки таймлайна, 3 колорита
- **Узлы:** `.tl li::before`, `.tl li.soon::before`, `.tl li.done::before`
- **Файлы:** `orn/dot-seed-pomegranate.png`, `orn/dot-seed-peach.png`, `orn/dot-seed-emerald.png`, **32×32**, альфа
- **Промпт:** `ORN CORE A small round berry dot filled flat with pomegranate red #A6403A, surrounded by one thin detached antique-gold ring #D8B878 with a clean 4-pixel gap between dot and ring, square 1:1.` (варианты: заливка `blush peach #E58F6E` / `emerald green #17564A`)
- **Размещение:**
```css
.tl li::before{content:"";position:absolute;left:-40px;top:.42em;width:13px;height:13px;border-radius:0;box-shadow:none;
  background:url('/img/orn/dot-seed-pomegranate.png') center/contain no-repeat}
.tl li.soon::before{background-image:url('/img/orn/dot-seed-peach.png')}
.tl li.done::before{background-image:url('/img/orn/dot-seed-emerald.png')}
```

### B5. Ветвь-маргиналия (выводим `#sprig` из резерва в живой декор)
- **Узел сейчас:** symbol определён, не используется → добавляем новые узлы
- **Файл:** `orn/sprig-gold.png`, **280×280**, альфа
- **Промпт:** `ORN CORE A flowing diagonal vine sprig rising from lower-left to upper-right: one long S-curved stem with three stylized almond leaves (flat pale-gold #E7D3A4 fill, gold #B98A2E contour) and three tiny four-petal blossoms (flat gold dots with petals), airy and sparse, square 1:1.`
- **Размещение:** в `#s1`, `#s2`, `#s8` добавить `<i class="marginalia m-right" aria-hidden="true"></i>` (в s2 — `m-left`):
```css
.marginalia{position:absolute;width:190px;height:190px;opacity:.5;pointer-events:none;
  background:url('/img/orn/sprig-gold.png') center/contain no-repeat}
.m-left{left:-34px;bottom:6%}.m-right{right:-24px;top:9%;transform:scaleX(-1)}
```

### B6. Венок-водяной знак фонов секций
- **Узел:** новый фоновый слой `.sec.alt`, `.sec.warm`
- **Файл:** `orn/watermark-wreath.png`, **900×900**, альфа
- **Промпт:** `ORN CORE A large circular laurel-and-vine wreath ring open at the top: two symmetric branches with slender leaves and tiny blossoms meeting at the bottom in a small bow, thin single-color antique gold #B98A2E lines, airy, square 1:1.`
- **Размещение:**
```css
.sec.alt::before,.sec.warm::before{content:"";position:absolute;right:-90px;top:-70px;width:680px;height:680px;
  background:url('/img/orn/watermark-wreath.png') center/contain no-repeat;opacity:.07;pointer-events:none}
.sec>.wrap{position:relative}
```

---

## C. Лого и иконки (5 позиций / 6 файлов + производные)

### C1. Лого-гранат, 2 колорита + favicon
- **Узлы:** `.brand svg use#pom` (30px), `footer .mark svg use#pom` (34px)
- **Файлы:** `logo/logo-pom.png` (128×128), `logo/logo-pom-peach.png` (128×128); производные без генерации: `favicon-32.png`, `apple-touch-180.png` (ресайз logo-pom)
- **Промпт (основной):** `ORN CORE but two-color: a heraldic pomegranate emblem: rounded fruit filled flat pomegranate red #A6403A with a three-pointed crown calyx on top, a split opening showing three ivory seeds #F1E7D2, two small symmetric leaves at the sides outlined antique gold #B98A2E, hairline gold contour around the fruit, square 1:1.` (peach-вариант: fruit `blush peach #E58F6E`, seeds `deep ultramarine #15224A`, leaves/contour gold)
- **Размещение:** `.brand`: `<img src="/img/logo/logo-pom.png" width="30" height="30" alt="">`; футер: `<img src="/img/logo/logo-pom-peach.png" width="34" height="34" alt="">`; в `<head>`: `<link rel="icon" type="image/png" sizes="32x32" href="/img/logo/favicon-32.png"><link rel="apple-touch-icon" href="/img/logo/apple-touch-180.png">`.

### C2. Иконки четырёх оптик (4 файла)
- **Узлы:** `.lens .med svg use#i-psy / #i-myth / #i-art / #i-exp`
- **Файлы:** `icon/icon-psy.png`, `icon-myth.png`, `icon-art.png`, `icon-exp.png`, **96×96**, альфа
- **Промпт-ядро ICON CORE:** `Minimal linear icon in Quattrocento elegance, single flat antique gold #B98A2E stroke of uniform thickness with rounded caps, no fills except tiny dots, centered, isolated on pure white, no shadow, no text, square 1:1.`
  - psy: `subject: the Greek letter psi as a symbol of depth psychology — one vertical line crossed by a U-shaped curve opening upward, standing on a short horizontal base line.`
  - myth: `subject: a diagonal laurel branch with five slender leaves and two berries, symbol of myth and story.`
  - art: `subject: a painter's palette outline with three small paint dots and one thin brush lying across it.`
  - exp: `subject: a winding thread wave line ending in a small round hand mirror, symbol of personal experience.`
- **Размещение:** `<span class="med"><img src="/img/icon/icon-psy.png" width="38" height="38" alt=""></span>` + CSS `.lens .med img{width:38px;height:38px}`.

---

## D. Текстуры и фоновые слои (4)

### D1. Зерно бумаги (весь сайт)
- **Узел:** `body::after` (сейчас data-URI feTurbulence)
- **Файл:** `tex/paper-grain.png`, **512×512 seamless**, без альфы
- **Промпт:** `Seamless tileable fine grain texture of handmade Italian Renaissance paper: warm ivory base #F1E7D2 with extremely subtle darker fibers, tiny flecks and faint laid lines, uniform very low contrast, edge-to-edge flat scan look, no vignette, no border, no objects, no text, tileable pattern.`
- **Размещение:** `body::after{background-image:url('/img/tex/paper-grain.png');background-size:512px 512px;background-repeat:repeat;opacity:.06}` (data-URI убрать, blend multiply и fixed оставить).

### D2. Краkelюр темперы (поверх живописи)
- **Узел:** новый оверлей `.frame .ph`, `.tcard .ph`, `.terrace`
- **Файл:** `tex/tempera-crackle.png`, **512×512 seamless**
- **Промпт:** `Seamless tileable overlay texture of aged egg-tempera paint: pure white base with very light warm-grey hairline craquelure and faint linen canvas weave, extremely low contrast, uniform density, edge-to-edge, no vignette, no objects, tileable pattern.`
- **Размещение:**
```css
.frame .ph,.tcard .ph,.terrace{position:relative}
.frame .ph::after,.tcard .ph::after,.terrace::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:url('/img/tex/tempera-crackle.png') repeat;background-size:380px;mix-blend-mode:multiply;opacity:.14;border-radius:inherit}
```

### D3. Золотая пыль (футер)
- **Файл:** `tex/goldleaf-on-black.png`, **512×512 seamless**
- **Промпт:** `Seamless tileable sparse gold-leaf flecks texture: solid pure black background with irregular metallic gold flakes and tiny gold dots #D8B878, very low density about six percent coverage, varied flake sizes, edge-to-edge, no vignette, no text, tileable pattern.`
- **Размещение:** `footer{position:relative} footer::before{content:"";position:absolute;inset:0;background:url('/img/tex/goldleaf-on-black.png') repeat;background-size:420px;mix-blend-mode:screen;opacity:.5;pointer-events:none} footer .wrap{position:relative}`.

### D4. Акварельная вошь (тёплые зоны)
- **Узлы:** фон `.partner` и секции `#s8.warm`
- **Файл:** `tex/peach-wash.png`, **1200×800 (3:2)**, без альфы
- **Промпт:** `Soft luminous watercolor wash background: very light blush peach #F6E0CE and pale gold #E7D3A4 clouds gently bleeding into warm ivory #FBF5E8, airy translucent layers, no hard edges, no objects, no figures, no text, subtle handmade paper grain, horizontal aspect 3:2, evenly light across the whole frame.`
- **Размещение:** `.partner{background-image:url('/img/tex/peach-wash.png');background-size:cover;background-blend-mode:soft-light}`; `#s8.warm{background:url('/img/tex/peach-wash.png') right top/980px no-repeat, linear-gradient(180deg,rgba(246,224,206,0),rgba(246,224,206,.65) 30%,rgba(246,224,206,.35))}`.

---

## E. Мета-графика (1)

### E1. OG-обложка соцсетей
- **Узел:** новый `<meta property="og:image">` в `<head>`
- **Файл:** `img/meta/og-cover.png`, **1200×630**
- **Промпт:** `STYLE CORE Horizontal social cover, aspect ratio 1200:630. Left 45 percent: an arched-top tempera painting of a serene woman with wind-blown golden hair holding a split pomegranate, cropped at chest, on emerald gown; right 55 percent: completely plain golden sand field #F1E7D2 with one thin antique-gold vine sprig in the lower right corner and generous empty space in the right center reserved for future typography; soft even light, no text, no letters, no logo, no watermark.`
- **Размещение:** файл положить как есть; типографику поверх правого поля добавить вручную в Figma/Photoshop (не генерировать!): заголовок «Лаборатория феминности» — Cormorant 600, 76px, #15224A; подстрочник «психология × миф × искусство» — Manrope 500, 26px, #6A6252; отступ справа 80px, базовая линия по центру поля. В `<head>`: `<meta property="og:image" content="https://DOMAIN/img/meta/og-cover.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">`.

---

## F. Итоговый чек-лист внедрения (порядок работ)

1. Сгенерировать и вырезать альфу: B1–B5, C1–C2 (11 прогонов + 6 колорит-дублей). 2. Текстуры D1–D4 с проверкой швов. 3. Живопись A1–A9 (9 прогонов), даунскейл, WebP. 4. OG-обложка + ручная типографика. 5. Замена узлов сверху вниз по странице (hero → s2 → s5 → s6 → s8), добавление CSS-снипетов из пунктов размещения. 6. Производные favicon/apple-touch из logo-pom.png. 7. Удалить из `<defs>` все symbols/gradients и data-URI feTurbulence; проверить Lighthouse (CLS=0 за счёт width/height), прогнать alt-тексты. 8. Контроль стиля: ни один растр не выходит за палитру (#17564A, #0D3B32, #1F3164, #15224A, #F1E7D2, #E8DBBC, #FBF5E8, #E58F6E, #A6403A, #B98A2E, #D8B878, #E7D3A4); фон всех живописных панелей остаётся светлым («светлый, но не блёклый»), лицо/эмблема — в safe-area арочного кропа.