# ГРАФИЧЕСКИЙ ИНВЕНТАРЬ САЙТА «ЛАБОРАТОРИЯ ФЕМИННОСТИ»
### Полный список ассетов + промпты для qwen-image-3

Ниже — **45 позиций**, сгруппированных по блокам страницы. Для каждой указаны: место в вёрстке (хук в коде), имя файла, размер/пропорции, полный промпт, негативный промпт и технические примечания (прозрачность, режим наложения, постобработка).

---

## 0. БАЗОВЫЙ СТИЛЕВОЙ МОДУЛЬ (Master Style Block)

**Этот блок дописывается в КОНЕЦ каждого промпта** (кроме чисто технических текстур, где он частично избыточен — для них отмечено отдельно).

```text
MASTER STYLE — "Лаборатория феминности" brand:
Editorial fine-art direction for a quiet-luxury depth-psychology brand. Italian villa garden
in midsummer; Renaissance and antiquity references; intellectual sensuality.
Strict palette only: ivory #FDFBF7, sandstone #F2EBE1, deep pine emerald #1A3C34,
Tyrrhenian deep blue #2C4B6E, antique gold ochre #D4AF37, blush peach #FFCBA4,
ripe pomegranate #C84B31. Warm limestone light, chiaroscuro, soft enveloping diffused
Mediterranean daylight, long gentle shadows. Surface: handmade cotton-rag paper grain,
matte honed finish, no gloss, subtle 35mm analogue film grain, fine hairline linework
where line art is requested. Museum-catalogue / private-gallery-in-Florence aesthetic.
Calm, expensive, restrained, thoughtful. High detail, professional colour grading.
```

**MASTER NEGATIVE (единый негативный промпт):**

```text
text, letters, words, numbers, captions, titles, labels, watermark, signature, logo, ui elements,
business stock photo, woman in white suit, yoga pose, meditation silhouette, candles, feathers,
crystals, esoteric clichés, mandala, lotus, neon colours, oversaturation, HDR, glossy plastic,
3d render, cgi, cartoon, anime, clipart, children illustration, jpeg artifacts, noise blobs,
distorted hands, extra fingers, deformed anatomy, duplicate objects, modern objects, plastic,
chrome, glass reflections of camera, vignette burn, heavy blur
```

**Технические соглашения по всему проекту**

| Параметр | Требование |
|---|---|
| Формат мастера | PNG-24 (для прозрачности) / TIFF → экспорт в **WebP** + fallback JPG q82 |
| Плотность | генерировать в **2×** от отображаемого размера (retina), `loading="lazy"`, `decoding="async"` |
| Прозрачность | qwen-image не всегда отдаёт альфу → просить «**isolated on solid pure white #FFFFFF background**» и вырезать (Photoshop / remove.bg / `magick -fuzz 6% -transparent white`) |
| Текстуры | требовать `seamless tileable`, проверять стык 2×2 |
| Именование | `/img/{блок}/{id}-{назначение}@2x.webp` — напр. `/img/meetings/m-03-labyrinth@2x.webp` |
| Архитектурная арка | все фото-«экспонаты» обрезаются маской `clip-path:url(#archClip)` — поэтому **композицию строить с расчётом на срезку верхних углов** (важный объект — по центру, отступ сверху ≥ 12 %) |

---

# ГРУППА A · ТЕКСТУРЫ И ФОНОВЫЕ ПОДЛОЖКИ

### A-01 · Зерно плёнки (`.grain`)
* **Где:** фиксированный оверлей всего сайта, `mix-blend-mode: multiply`, opacity .055, анимация сдвига
* **Файл:** `/img/texture/t-01-grain.png` · **1024×1024, seamless** · PNG grayscale

```text
Seamless tileable high-resolution film grain texture, fine 35mm silver-halide grain structure,
pure monochrome greyscale, mid-grey 50% luminance, perfectly uniform random density,
microscopic organic grain clumps, absolutely flat, no patterns, no scratches, no dust,
no hairs, no vignette, no gradient bands, no shapes, no lighting direction,
technical texture asset intended for multiply-blend overlay. Neutral, invisible structure.
```
**Negative:** `pattern, stripes, dots grid, scratches, dust, hair, vignette, gradient, shapes, objects, colour, warm tone, blur`
**Примечание:** единственный ассет, к которому Master Style **не** добавляется.

---

### A-02 · Льняная бумага / «старая бумага» (фон body, секции 02, 06)
* **Файл:** `/img/texture/t-02-paper-ivory.png` · **2048×2048, seamless**

```text
Seamless tileable texture of handmade cotton-rag paper in warm ivory #FDFBF7,
visible laid lines and chain lines, soft irregular fibre flecks, faint deckle roughness,
extremely subtle warm beige mottling and a whisper of sandstone #F2EBE1 clouding,
flat top-down scan, perfectly even diffuse light, no shadows, no creases, no folds,
no stains, no text, matte, luxury stationery paper, high resolution macro detail.
```

---

### A-03 · Мраморные прожилки (подложки карточек `.card-art`, портретов)
* **Файл:** `/img/texture/t-03-marble.png` · **2048×2048, seamless**

```text
Seamless tileable surface of pale Carrara marble, warm ivory base #FDFBF7,
very fine hairline veining in soft grey-beige and barely visible antique gold #D4AF37,
veins delicate and sparse, honed matte finish, no gloss, no polish reflection,
flat top-down scan, even diffuse lighting, no cracks, no chips, no text,
subtle, quiet, expensive stone texture.
```

---

### A-04 · Персиково-охристая акварельная подложка (секция 04 «ДЛЯ КОГО»)
* **Где:** фон `.aud` (сейчас — CSS-градиенты)
* **Файл:** `/img/texture/t-04-peach-wash.jpg` · **2560×1440 (16:9)**

```text
Seamless abstract watercolour wash background: soft wet-on-wet gradient bleeding from
blush peach #FFCBA4 in the upper-left through warm sandstone #F2EBE1 to faint antique
gold ochre #D4AF37 in the lower-right, delicate pigment granulation, cold-press paper
grain visible, extremely light and airy high-key tone, no shapes, no objects, no brush
strokes, no border, luminous, warm, calm. Watercolour on cotton paper, photographed flat.
```
**Примечание:** накладывать поверх A-02 с прозрачностью 60–70 %, чтобы читалась фактура бумаги.

---

### A-05 · Тёмный изумрудный лён (секции 03 «ОПТИКА», 08 «ПРИГЛАШЕНИЕ», футер)
* **Файл:** `/img/texture/t-05-emerald-linen.png` · **2048×2048, seamless**

```text
Seamless dark background texture: deep pine emerald #1A3C34 dyed linen fabric with a fine
plain weave, subtle fibre irregularities, faint antique gold #D4AF37 thread glints barely
visible, extremely low contrast, perfectly even tone, no vignette, no folds, no shadows,
matte, luxury packaging material, photographic macro scan, no text.
```

---

### A-06 · Пятна света сквозь листву (оверлей hero и секции 07)
* **Где:** `.dapple`-элементы hero, опционально поверх A-04
* **Файл:** `/img/texture/t-06-dappled-light.png` · **2048×2048, seamless** · режим `screen`, opacity .35

```text
Seamless texture of soft dappled sunlight filtering through olive and laurel leaves,
falling on a warm ivory lime-plaster wall: organic rounded bokeh-like light spots in
cream #FFF3DC and pale gold #FFE7BE over sandstone #F2EBE1 base, gentle shadows no denser
than 12%, dreamy Mediterranean midday atmosphere, no visible leaves, no branches, only
pure light and shadow play, high key, luminous, no text, no objects.
```

---

### A-07 · Гербарный лист (фон карточек тренингов `.card`)
* **Где:** блок 06, подложка каждой карточки-«экспоната»
* **Файл:** `/img/meetings/herbarium-sheet.png` · **1400×1750 (4:5)**

```text
An empty herbarium specimen sheet, flat top-down scan: aged ivory cotton paper #FDFBF7 with
faint sandstone #F2EBE1 mottling and the lightest foxing, a thin antique gold #A8862A
hairline double-rule border inset from the edges, a small blank rectangular label with two
empty hairline rules in the lower-right corner, tiny registration cross-marks in the corners,
completely empty centre reserved for artwork, soft even diffuse light, matte, archival
museum mounting paper, no text, no lettering, no numbers, no plants, no specimens.
```
**Примечание:** в коде — `background-image` у `.card` + `background-blend-mode: multiply`.

---

### A-08 · Штукатурка в персиковом свете (альтернативный фон блока 04)
* **Файл:** `/img/texture/t-08-plaster.jpg` · **2560×1600**

```text
A sunlit old Italian lime-plaster wall in warm ivory #FDFBF7 and pale blush #FFCBA4 light,
hand-troweled uneven surface with hairline cracks and gentle undulations, raking afternoon
sunlight from the left creating very soft relief, a faint cool emerald #1A3C34 shadow in the
lower-left corner, quiet, minimal, empty, no objects, no foliage, no text, matte,
analogue medium-format photograph aesthetic, subtle film grain.
```

---

# ГРУППА B · ЛОГОТИП, ИКОНКИ, РАЗДЕЛИТЕЛИ, БУЛЛИТЫ

> ⚠️ Пункты B-01…B-09 — **мелкая векторная графика**. Генератор даст растр с артефактами на 1 px линиях; рекомендую оставить текущие inline-SVG, а промпты использовать, если нужен «живой» рисованный характер. Кириллические буквы模型 рисует нестабильно → для B-01/B-02 предусмотрен запасной вариант **без литер** (только арка + круг).

### B-01 · Монограмма «ЛФ» в арке (шапка + футер `.brand-mon`)
* **Файл:** `/img/ui/l-01-monogram.png` · **512×640**, прозрачный (или на чистом белом под вырезку)

```text
Minimal heritage emblem mark: a thin gold hairline arch outline — semicircular top, straight
vertical sides, open bottom — containing a slim perfect circle in its upper half; inside the
circle the Cyrillic monogram letters "ЛФ" set in an elegant high-contrast Garamond-style
serif with thin hairline strokes. Single uniform line weight, antique gold #A8862A stroke,
no fill, no gradients, no shadows, no bevel, perfectly centred, isolated on solid pure white
#FFFFFF background for easy extraction. Luxury old-money brand crest, engraved precision,
crisp vector-like edges, no other text, no ornaments.
```
**Запасной вариант (без литер):** заменить `the Cyrillic monogram letters "ЛФ"` → `a small stylised pomegranate sprig with three leaves drawn in hairline gold`.

---

### B-02 · Фавикон (упрощённая монограмма)
* **Файл:** `/img/ui/l-02-favicon.png` · **512×512** → 16/32/48/180 px, ICO + apple-touch

```text
App icon style emblem: a deep pine emerald #1A3C34 rounded-square tile with a very subtle
linen texture, centred thin antique gold #D4AF37 hairline arch outline with a small circle
inside it, generous negative space, flat design, crisp edges, no gradients, no shadows,
no text, no letters, minimal luxury monogram mark, perfectly symmetrical, isolated subject.
```

---

### B-03 · OG-изображение / превью для соцсетей
* **Файл:** `/img/ui/l-03-og-cover.jpg` · **2400×1260 (1.91:1)**

```text
Elegant editorial cover image, wide horizontal composition: on the right two thirds a
cinematic view from the stone terrace of an old Italian villa — weathered limestone
balustrade, tall dark cypresses, deep blue Tyrrhenian sea at the horizon, dappled leaf
shadows on warm plaster; on the left third a large calm area of ivory lime-plaster wall
with soft peach light reserved as negative space (no objects there). Overlaid only by a
thin antique gold #D4AF37 hairline arch line drawing on the wall. Palette: ivory #FDFBF7,
sandstone #F2EBE1, deep emerald #1A3C34, Tyrrhenian blue #2C4B6E, gold #D4AF37.
Analogue medium-format photograph, subtle film grain, matte, quiet luxury, no people,
no text, no lettering, no logo.
```
**Примечание:** текст заголовка добавляется поверх в графическом редакторе (Cormorant Garamond), не в генерации.

---

### B-04 · Курсор-перо (`#cursor svg`)
* **Где:** кастомный курсор, состояние `.is-hot`
* **Файл:** `/img/ui/c-01-quill.png` · **256×256**, прозрачный

```text
A single elegant goose-quill pen drawn as minimal hairline line art, one continuous contour,
diagonal orientation from lower-left to upper-right, delicate barbs suggested by three thin
strokes, nib accent in pomegranate red #C84B31, shaft in antique gold #A8862A, uniform
2-pixel-equivalent stroke, no fill, no shadow, no gradient, crisp vector-like, isolated on
solid pure white #FFFFFF background, tiny refined icon, no text.
```

---

### B-05 · Буллит-ромб (золотой бриллиант)
* **Где:** `.ticker-track span::after`, `.optics-panel li::before`, `.card-meta i::before`, `.hero-meta`, `.letter-foot span::before`
* **Файл:** `/img/ui/c-02-diamond-bullet.png` · **64×64**, прозрачный

```text
A single tiny decorative diamond ornament: one perfect square rotated 45 degrees, solid flat
antique gold #D4AF37, razor-sharp crisp edges, no outline, no gradient, no shadow, no bevel,
centred, isolated on solid pure white #FFFFFF background, minimal typographic bullet marker,
vector-like, no text.
```
**Вариант-контур:** `hollow outline only, 1px antique gold stroke, transparent centre`.

---

### B-06 · Стрелка ссылки карточки (`.card-link svg`)
* **Файл:** `/img/ui/c-03-arrow.png` · **256×96**, прозрачный

```text
A minimal hairline arrow pointing right: one thin straight horizontal line with a small open
chevron arrowhead at the right end, single uniform stroke in antique gold #A8862A, no fill,
no shadow, no decoration, crisp vector-like precision, horizontally centred, isolated on
solid pure white #FFFFFF background, no text.
```

---

### B-07 · Разделитель «Арка» (`.divider svg`)
* **Где:** между секциями 02 → 03
* **Файл:** `/img/ui/c-04-divider-arch.png` · **256×340**, прозрачный

```text
A delicate vertical architectural ornament drawn in hairline line art: a tall thin round arch
(semicircular top, open bottom) with a second smaller concentric arch nested inside it, a
short vertical stem rising from the apex crossed by a tiny horizontal bar, and a small hollow
diamond at the very top. Single uniform thin stroke in antique gold #A8862A, no fill, no
shading, Renaissance measured-drawing precision, perfectly symmetrical, isolated on solid
pure white #FFFFFF background, no text.
```

---

### B-08 · Лепной карниз-разделитель (UI-разделитель «лепнина»)
* **Где:** альтернатива `.divider` между крупными блоками; горизонтальная полоса
* **Файл:** `/img/ui/c-05-molding-strip.png` · **2400×200**, seamless по горизонтали

```text
A horizontal band of classical neoclassical stucco moulding photographed straight-on:
carved plaster bead-and-reel relief with a small egg-and-dart course, warm ivory #FDFBF7
plaster with soft sandstone #E7DCC9 shadow in the recesses, faint antique gold #D4AF37
gilt traces in the deepest grooves, even diffuse lighting, no perspective, seamless and
tileable from left to right, matte carved plaster texture, museum interior detail,
no text, no cracks, no people.
```

---

### B-09 · Маргинальная звёздочка `✽` (`.herb-note::before`)
* **Файл:** `/img/ui/c-06-asterisk.png` · **128×128**, прозрачный

```text
A tiny hand-drawn marginalia asterisk floret: six slender tapering petals radiating from a
small centre dot, ink line art in pomegranate red #C84B31 with slightly uneven hand-drawn
line weight, delicate and small, no fill, no shadow, isolated on solid pure white #FFFFFF
background, antique book annotation mark, no text.
```

---

### B-10 · Угловой орнамент приглашения (`.letter::before/::after`)
* **Файл:** `/img/ui/c-07-corner-ornament.png` · **512×512**, прозрачный, 4 поворота

```text
A thin gold corner filigree ornament for a formal invitation card, L-shaped right-angle
composition: a double hairline rule following the corner, terminated by a small acanthus
curl and a tiny hollow diamond at the vertex, engraved line style in antique gold #A8862A,
absolutely no fill, no shading, no gradient, refined and sparse, isolated on solid pure
white #FFFFFF background, no text.
```

---

# ГРУППА C · HERO (блок 01)

### C-01 · Главная пластина hero — вид с террасы
* **Где:** `.hero-scene` (заменяет весь многослойный SVG)
* **Файл:** `/img/hero/h-01-terrace-plate.jpg` · **3840×1800 (≈21:9)** · WebP q85
* **Постобработка:** медленный Ken Burns (`scale 1.02 → 1.11`) уже реализован в CSS

```text
Cinematic wide establishing view from the stone terrace of an old Italian villa at the height
of summer, eye-level camera on a tripod. Foreground: a weathered warm limestone balustrade
with hand-turned balusters running across the lower third of the frame, and a terrace floor
of pale sandstone slabs with fine joints. Middle ground: a row of tall slender dark cypress
trees and a low silver-green olive grove on a retaining wall. Horizon: the deep blue
Tyrrhenian sea as a calm horizontal band, beyond it faint hazy blue-grey hills dissolving
into atmospheric haze. Light: a low golden sun on the right casting long warm light and
soft dappled leaf shadows moving across the plaster wall and stone floor; chiaroscuro;
gentle backlight bloom. Upper corners framed by a few large olive and laurel leaves slightly
out of focus. Palette strictly ivory #FDFBF7, sandstone #F2EBE1, deep pine emerald #1A3C34,
Tyrrhenian blue #2C4B6E, gold ochre #D4AF37, a whisper of blush peach #FFCBA4 in the sky.
Analogue medium-format photograph, 50mm, f/8, subtle 35mm film grain, matte finish, no HDR.
COMPOSITION: the left third of the frame is quiet and light — an empty sunlit plaster wall
and open sky with generous negative space reserved for typography; all visual weight on the
right and bottom. No people, no animals, no boats, no text, no modern objects.
```
**Negative:** добавить к мастеру: `people, person, silhouette, boat, car, power lines, modern furniture, glass railing, swimming pool, sunset orange oversaturated, drone view`

---

### C-02 · Передний план: ветви для параллакса (2 шт. — левая и правая)
* **Где:** `.branch-a`, `.branch-b` (отдельные слои, двигаются быстрее фона)
* **Файл:** `/img/hero/h-02-branch-left.png` · **1600×900**, прозрачный · `h-02-branch-right.png` — зеркально
* **Примечание:** в коде слой получает CSS-анимацию покачивания `swayA/swayB` → ветвь должна входить в кадр **из угла**, с запасом за обрез

```text
A large botanical foreground element: a heavy olive and laurel branch with dense elongated
dark leaves and a few small unripe olives, entering the frame from the top-left corner and
reaching toward the centre, the cut end hidden beyond the edge. Leaves in deep pine emerald
#1A3C34 shading to near-black green #0F2A23, slightly translucent backlit edges with a warm
gold rim #D4AF37, soft natural surface detail, matte. Painterly-photographic hybrid, shallow
focus on the outermost leaves, subtle film grain. Completely isolated on a solid pure white
#FFFFFF background for clean alpha extraction, no sky, no wall, no other objects, no text.
```
Для правой ветви: `entering the frame from the top-right corner and reaching toward the left`.

---

### C-03 · Золотая арка-обмер (декор hero справа)
* **Где:** `.hero-arch-line` (параллакс `data-par="-0.06"`)
* **Файл:** `/img/hero/h-03-arch-lineart.png` · **900×1260**, прозрачный

```text
A precise architectural measured drawing of a single tall round arch rendered as thin gold
line art: two concentric arch outlines (outer and inner) with straight vertical jambs open
at the bottom, a short vertical stem with a small crossbar at the apex, and one faint
horizontal baseline near the lower third. Uniform hairline stroke in antique gold #A8862A,
absolutely no fill, no shading, no perspective, Renaissance survey-drawing elegance,
perfectly symmetrical, isolated on solid pure white #FFFFFF background, no text, no
dimension marks, no numbers.
```

---

# ГРУППА D · СЕКЦИЯ 02 «ФЕМИННОСТЬ»

### D-01 · Ботаническая таблица I — «Punica granatum»
* **Где:** `.plate-frame svg.art` (правая колонка, параллакс `data-par="0.05"`)
* **Файл:** `/img/feminity/b-01-pomegranate-plate.png` · **1600×2000 (4:5)**
* **Важно:** верх композиции — под арочную обрезку `archClip`

```text
An antique botanical illustration plate in the style of a 19th-century scientific herbarium
print, vertical composition. Subject: a pomegranate branch (Punica granatum) arranged as a
specimen — glossy deep green leaves in pairs along a woody stem, two vivid orange-red
flowers with crêpe-paper petals and prominent stamens, one whole ripe pomegranate with its
calyx crown intact, and one fruit cut cleanly in half revealing densely packed translucent
crimson arils separated by pale cream membranes. A short fig-branch accent with one split
fig in the lower left. Technique: fine hairline ink contour in deep pine emerald #1A3C34,
delicate stippled and hatched shading, transparent watercolour washes, muted and restrained
colouring with antique gold #D4AF37 accents and pomegranate red #C84B31 as the dominant
warm note. Background: warm ivory aged paper #FDFBF7 with faint sandstone #F2EBE1 mottling,
a hairline gold rule framing the sheet, generous empty margins, plate-like centred
composition with the top of the branch reaching into a rounded arch of empty space.
Matte fine-art print quality, subtle paper grain, no text, no lettering, no labels, no
numbers, no signature, no Latin captions, no insects.
```
**Negative:** дополнительно `text, latin names, labels, numbers, plate number, signature, insects, butterflies, white background pure`

---

### D-02 · Опционально: вторая таблица «Ficus carica» (для чередования/лендингов тренингов)
* **Файл:** `/img/feminity/b-02-fig-plate.png` · **1600×2000 (4:5)**

```text
Antique botanical illustration plate, scientific herbarium style, vertical composition:
a fig branch (Ficus carica) with three large rough lobed dark-green leaves, one whole ripe
purple-brown fig with a drooping neck, and one fig sliced open vertically exposing the
pink-red seedy flesh with a pale rim; fine hairline ink contour in deep pine emerald #1A3C34,
stippled shading, transparent watercolour washes, antique gold #D4AF37 and pomegranate #C84B31
accents, warm ivory aged paper #FDFBF7 background with faint sandstone mottling and a hairline
gold rule frame, generous margins, matte fine-art print, no text, no labels, no numbers,
no insects, no signature.
```

---

# ГРУППА E · СЕКЦИЯ 03 «НАША ОПТИКА»

### E-01 · План итальянского сада в стиле кодексов Леонардо (подложка схемы)
* **Где:** `.optics::before` (сейчас — SVG-паттерн), opacity .14
* **Файл:** `/img/optics/o-01-garden-plan-light.png` · **2000×2000**, прозрачный, линии светло-золотые

```text
A Renaissance notebook page drawing, top-down geometric scheme of an Italian formal garden:
several concentric circles and intersecting arcs, a central octagonal fountain, four radial
cypress alleys, square and circular parterres filled with fine diagonal hatching, a villa
block at one edge, compass prick marks, construction lines and guide circles left visible,
plus a faint mirrored proportion study of a human figure reduced to pure geometry in the
centre. Executed as extremely light hairline ink in warm antique gold #D4AF37 and pale
ochre, low contrast and airy, Leonardo da Vinci codex aesthetic, no shading, no colour
fills, completely isolated on solid pure white #FFFFFF background for alpha extraction,
no legible text, no writing, no mirror writing, no numbers, no figures with faces.
```
**Вариант E-01b (для тёмного фона):** заменить `antique gold #D4AF37 ... pure white background` → `pale ivory #FDFBF7 lines at 40% opacity, isolated on solid deep pine emerald #1A3C34 background, seamless tileable`.

---

### E-02 · Пергаментная версия плана (если нужен светлый фон секции)
* **Файл:** `/img/optics/o-01b-garden-plan-parchment.jpg` · **2000×2000**

```text
A Renaissance manuscript sheet of aged parchment #F2EBE1 with warm foxing and soft creases,
bearing a top-down geometric drawing of an Italian formal garden: concentric circles,
intersecting arcs, a central fountain, radial cypress alleys, hatched square parterres,
compass prick marks and visible construction lines; fine sepia and antique gold #A8862A ink,
Leonardo da Vinci codex aesthetic, very light and delicate, low contrast, matte, flat scan,
no legible text, no handwriting, no numbers, no human figures.
```

---

### E-03 · Статичная версия диаграммы четырёх сфер (опционально, для печати/соцсетей)
* **Файл:** `/img/optics/o-02-four-spheres.png` · **1600×1400**
* **Примечание:** интерактив на сайте остаётся SVG-ом; растр — только для презентаций и OG

```text
An elegant conceptual diagram in the style of a Renaissance scientific plate: four thin
outlined circles of identical size overlapping in a perfectly symmetrical four-petal
arrangement around a single central point. Each circle is a translucent watercolour wash in
a different hue — Tyrrhenian deep blue #2C4B6E, deep pine emerald #1A3C34, antique gold
ochre #D4AF37, ripe pomegranate #C84B31 — with hairline gold contours #D4AF37, fine tick
marks along the outer circumferences, faint compass construction lines radiating from the
centre, and a small hollow gold diamond exactly at the intersection point. Background:
deep emerald #1A3C34 with an extremely faint garden-plan underdrawing visible at low
opacity. Matte, subtle paper grain, no text, no labels, no numbers, no lettering, no faces.
```

---

### E-04 · Центральный ромб-орнамент диаграммы
* **Файл:** `/img/optics/o-03-core-diamond.png` · **128×128**, прозрачный

```text
A tiny hollow diamond ornament with a small solid dot in its centre, drawn as a single thin
hairline stroke in blush peach #FFCBA4, no fill, no shadow, crisp vector-like, perfectly
centred, isolated on solid pure white #FFFFFF background, minimal decorative marker, no text.
```

---

# ГРУППА F · СЕКЦИЯ 05 «О НАС» — ПОРТРЕТЫ ОСНОВАТЕЛЕЙ

> Формат: **камео-профиль** в арочной нише. Оба портрета должны читаться как **пара**: один ракурс, одна техника, зеркально развёрнутые, разные акценты.

### F-01 · Полина — профиль с лавровым венком
* **Где:** первая `.portrait svg`
* **Файл:** `/img/about/p-01-polina.png` · **1200×1600 (3:4)**

```text
A fine-art editorial portrait rendered as a Renaissance cameo / engraved profile study,
vertical composition with a rounded arch of empty space above the head. Subject: a serene
thoughtful woman of about 45, classical balanced features, three-quarter profile facing
RIGHT, calm knowing downward-soft gaze, hair loosely gathered in a low bun at the nape with
a few free strands, a simple natural linen blouse with soft folds, visible collarbone and
neck, shoulders cropped by the bottom edge. Technique: delicate continuous hairline contour
drawing in dark ink #26332E over a warm marble-toned wash (ivory #F6EEE0 blending into
sandstone #DDCDB4), fine parallel hatching for the shadow side, soft enveloping window light
from the left, faint marble veining and paper grain in the background, a thin antique gold
#A8862A hairline arch framing the composition. Colour: predominantly monochrome warm sepia
with exactly TWO restrained colour accents — a small laurel wreath of dark green leaves
#1A3C34 resting in her hair, and a single tiny pomegranate-red #C84B31 stud earring.
Subtle 35mm film grain, museum-catalogue aesthetic, quiet, intellectual, dignified.
No text, no signature, no lettering, no other people, no jewellery besides the single stud,
no makeup emphasis, no smile, no direct eye contact with camera.
```

---

### F-02 · Вероника — профиль с оливковой ветвью
* **Где:** вторая `.portrait svg`
* **Файл:** `/img/about/p-02-veronika.png` · **1200×1600 (3:4)**

```text
A fine-art editorial portrait rendered as a Renaissance cameo / engraved profile study,
vertical composition with a rounded arch of empty space above the head, MIRROR-OPPOSITE of
its companion piece. Subject: a composed woman of about 38, classical profile facing LEFT,
soft intelligent expression, hair braided and coiled into a woven chignon with visible plait
texture, a loose linen shirt with an open neckline, neck and collarbone, shoulders cropped by
the bottom edge. Technique: delicate continuous hairline contour drawing in dark ink #26332E
over a lighter warm marble wash (ivory #F4EDE1 to sandstone #D9CDB8), fine hatching on the
shadow side, soft enveloping light from the RIGHT, faint marble veining and paper grain,
a thin antique gold #A8862A hairline arch framing the composition. Colour: predominantly
monochrome warm sepia with exactly TWO restrained accents — a fresh olive branch with
green-gold leaves #6B8C4A and one dark olive fruit held near the chignon, and a single tiny
pomegranate-red #C84B31 dot earring. Subtle 35mm film grain, museum-catalogue aesthetic,
calm, thoughtful, artistic. No text, no signature, no other people, no modern objects,
no smile, no eye contact with camera.
```

---

### F-03 · Опционально: «рабочий» портрет-дубль (для лендингов тренингов)
* **Файл:** `/img/about/p-03-founders-interior.jpg` · **1800×1200 (3:2)**

```text
Editorial interior photograph of two women in their late thirties and forties seated at a
long wooden table in an old villa library, seen from a distance and slightly from behind,
faces not sharply visible: shelves of leather-bound books, tall shuttered windows with soft
daylight, a linen tablecloth, open antique books, a glass of red wine, a small clay vessel,
scattered olive leaves. Muted warm sepia palette — ivory #FDFBF7, sandstone #F2EBE1, deep
pine emerald #1A3C34 — with a single colour accent of pomegranate red #C84B31 in a book
ribbon. Chiaroscuro, enveloping diffused light, 35mm, shallow depth of field, subtle film
grain, matte, quiet luxury documentary aesthetic, no text, no logos, no posed smiles, no
looking at camera.
```

---

# ГРУППА G · СЕКЦИЯ 06 «ВСТРЕЧИ» — 6 КАРТОЧЕК-ЭКСПОНАТОВ

> Единые требования ко всем шести: **4:5 (1400×1750)**, композиция рассчитана на арочную обрезку сверху (главный объект — по вертикальному центру), матовая поверхность, лёгкое зерно, **никакого текста и нумерации** (No. и теги рисуются HTML-ом). Все шесть должны читаться как одна серия.

### G-01 · No. 01 «Психея и Эрос: миф о доверии» (`.card` №1)
* **Файл:** `/img/meetings/m-01-psyche.png` · **1400×1750**

```text
Symbolist allegorical illustration in the manner of a Renaissance emblem book, vertical 4:5
composition with a rounded arch of negative space at the top. Subject: a large delicate
moth-butterfly (the soul, Psyche) with softly patterned wings hovering above a single small
candle flame; beneath them two slender silk ribbons intertwine and fall in loose curves,
ending in a tiny knot. Wings in translucent blush peach #FFCBA4 with antique gold #D4AF37
veining, flame in pomegranate red #C84B31 with a warm ochre core, ribbons in pale ivory.
A single thin gold circle frames the whole composition. Background: warm gradient from
#F6E9DC to #E7D2C2 with faint paper grain. Technique: fine hairline contour drawing with
delicate watercolour washes, soft chiaroscuro, matte, subtle film grain. Mood: tenderness,
fragility, trust. No text, no lettering, no numbers, no people, no human faces, no hands,
no cupids, no literal figures.
```

---

### G-02 · No. 02 «Инжир и гранат: зрелость тела» (`.card` №2)
* **Файл:** `/img/meetings/m-02-vanitas.png` · **1400×1750**

```text
An oil-painting still life in the manner of a Mediterranean vanitas, vertical 4:5
composition. Subject: split ripe figs showing glistening pink-crimson flesh, one pomegranate
halved to reveal densely packed arils, a small bunch of dark blue-black grapes, two peaches
with a soft blush, and a single vine leaf — all arranged on a sun-warmed rough limestone
parapet with a folded natural linen cloth beneath. Lighting: warm afternoon sidelight from
the right, deep pine emerald #1A3C34 shadows, ivory #FDFBF7 and ochre #D4AF37 highlights,
soft elongated cast shadows on the stone. Technique: visible brushwork and canvas weave,
warm aged varnish tone, classical Italian-Flemish still-life painting, subtle film grain,
matte. Mood: ripeness, juiciness, maturity without moralising. No text, no lettering, no
insects, no flies, no skulls, no hourglass, no candles, no people, no modern objects.
```

---

### G-03 · No. 03 «Нить Ариадны: выход из лабиринта» (`.card` №3)
* **Файл:** `/img/meetings/m-03-labyrinth.png` · **1400×1750**

```text
A conceptual illustration in Renaissance diagram style, vertical 4:5 composition with a
rounded arch of empty space at the top. Subject: a fine concentric circular labyrinth drawn
in hairline deep pine emerald #1A3C34 on a pale sage-ivory ground #EDF0EC, with faint
compass construction marks and radial guide lines; a single continuous vivid pomegranate-red
#C84B31 silk thread spirals from the outer edge inward to the exact centre, where it ends in
a small neat knot. Below the labyrinth lies an antique wooden thread bobbin / spindle with
worn gold #D4AF37 detailing and a few loose windings of the same red thread. Technique:
precise hairline linework, flat matte rendering, delicate paper grain, subtle film grain,
no shading gradients. Mood: patience, orientation, the way out that is also the way in.
No text, no lettering, no numbers, no people, no hands, no minotaur, no shadows heavier
than 10%.
```

---

### G-04 · No. 04 «Зеркало Флоры: взгляд без суда» (`.card` №4)
* **Файл:** `/img/meetings/m-04-mirror.png` · **1400×1750**

```text
A quiet allegorical still life, vertical 4:5 composition. Subject: a round antique hand
mirror with a slender gold #D4AF37 frame and a turned handle, leaning against a warm ivory
lime-plaster wall; its glass shows only soft empty reflected light and a pale sky gradient —
absolutely no face, no figure, no reflection of anything recognisable. A laurel wreath of
dark green leaves #1A3C34 is draped over the upper edge of the frame; a strand of cream
pearls is coiled at the base; a scattering of tiny white and blush-peach #FFCBA4 petals lies
on the ledge. Background gradient #F7EDE6 to #EAD9CF with paper grain. Lighting: gentle
diffused daylight from the left, soft shadows, chiaroscuro. Technique: delicate hairline
contours with muted watercolour washes, matte, subtle film grain. Mood: self-regard without
judgement. No text, no lettering, no faces, no human reflection, no flowers in full bloom,
no cosmetics, no modern objects.
```

---

### G-05 · No. 05 «Персефона: спуск и возвращение» (`.card` №5)
* **Файл:** `/img/meetings/m-05-descent.png` · **1400×1750**

```text
A symbolic architectural illustration, vertical 4:5 composition. Subject: a dark round-arched
doorway set into a pale sunlit limestone wall; inside the arch a descending flight of stone
steps leads down into deep darkness graduating from Tyrrhenian blue #2C4B6E to near-black
emerald #122923. A thin antique gold #A8862A hairline archivolt traces the arch, with a
small keystone mark at the apex. A trail of glossy pomegranate-red #C84B31 seeds is
scattered along the steps, gradually smaller and sparser as they descend into the dark.
One whole pomegranate with its calyx crown rests on the threshold in the light. Surrounding
wall in warm ivory stone #E9E4DA with fine plaster texture and hairline cracks. Lighting:
soft raking light from the left, strong but quiet chiaroscuro, no glow effects. Technique:
matte painterly rendering, subtle grain, restrained palette. Mood: initiation, descent,
cyclic return. No text, no lettering, no figures, no people, no gates, no monsters, no
fire, no candles.
```

---

### G-06 · No. 06 «Глиняные сны: лепка бессознательного» (`.card` №6)
* **Файл:** `/img/meetings/m-06-clay.png` · **1400×1750**

```text
An editorial craft still life with hands, vertical 4:5 composition. Subject: a woman's hands
(anatomically correct, five fingers each, natural short nails, no rings, no polish) shaping
a wet clay vessel on a rustic wooden table; the vessel is a rounded terracotta amphora form
in warm brown #B08968 with visible throwing rings and slip moisture; a natural linen sleeve
enters the frame at the wrists; small droplets of water and clay slip on the table; above
the vessel a single thin arc of pomegranate-red #C84B31 thread curves like a thought, with
one tiny red dot at its apex. Background: warm ivory plaster #F2EAE0 with a soft gradient
and paper grain. Lighting: soft window daylight from the left, gentle chiaroscuro, muted
palette, shallow depth of field. Technique: photographic-illustration hybrid, matte, 35mm
film grain. Mood: making, patience, form emerging. No text, no lettering, no faces, no
jewellery, no pottery wheel machinery, no modern tools, no glossy highlights.
```
**Negative (дополнительно):** `deformed hands, extra fingers, missing fingers, fused fingers, long nails, nail polish, rings, bracelets, watch, distorted anatomy`

---

### G-07 · Дополнительная карточка-заглушка «Скоро» (для пустой ячейки каталога)
* **Файл:** `/img/meetings/m-07-empty-plate.png` · **1400×1750**

```text
A minimal placeholder plate in herbarium style, vertical 4:5: an empty warm ivory sheet
#FDFBF7 with a faint sandstone #F2EBE1 mottling, a thin antique gold #A8862A hairline
double-rule border, in the centre a single delicate pressed olive sprig with three small
leaves rendered in faint hairline line art at 30% opacity, and two tiny hairline mounting
strips crossing the sprig as if it were a specimen. Generous empty space, soft diffuse
light, matte, subtle paper grain. No text, no lettering, no numbers, no labels, no flowers.
```

---

# ГРУППA H · СЕКЦИЯ 07 «КАК ЭТО ПРОИСХОДИТ» — КОЛЛАЖ ДЕТАЛЕЙ

### H-01 · Вертикальная плитка: руки и глина
* **Где:** `.tile.t-tall`
* **Файл:** `/img/format/f-01-clay-hands.png` · **1200×2080 (≈3:5)**

```text
Intimate vertical detail photograph: a woman's hands (anatomically correct, five fingers,
no rings, no polish) cupping and lifting a soft lump of wet grey-brown clay above a rustic
wooden worktable; clay slip and water droplets on the fingers, a natural linen apron edge
in the lower frame, terracotta dust; warm ivory plaster wall behind, out of focus. Soft
window daylight from the upper left, gentle chiaroscuro, muted palette of ivory #FDFBF7,
sandstone #F2EBE1, terracotta #B08968 and a tiny pomegranate-red #C84B31 accent (a single
red thread lying on the table). 50mm, f/2.8, shallow depth of field, 35mm film grain, matte,
documentary craft aesthetic. No text, no faces, no tools, no pottery wheel, no jewellery.
```
**Negative (доп.):** `deformed hands, extra fingers, fused fingers, long nails, nail polish, watch, bracelet`

---

### H-02 · Широкая плитка: стол (книга, вино, карты, оливковая ветвь)
* **Где:** `.tile.t-wide`
* **Файл:** `/img/format/f-02-table-flatlay.jpg` · **2560×1100 (≈21:9)**

```text
Overhead flat-lay editorial photograph on a softly crumpled natural linen tablecloth in warm
ivory #FDFBF7. Arrangement across a wide panoramic frame: on the left an open antique book
with woodcut-style pages that are completely blank or reduced to abstract hairline marks —
no legible text anywhere; in the centre a stemmed glass of red wine, half full, catching a
single highlight, deep garnet #8E2F1B liquid; to the right three tarot-sized cards lying
face up showing ONLY abstract allegorical engravings with thin gold #D4AF37 borders — a
radiant sun with wavy rays, a crescent moon with a small star, and an eight-pointed star —
no letters, no numbers, no figures, no faces; a dried olive branch with silver-green leaves
crossing the composition; a small wooden spool of pomegranate-red #C84B31 silk thread;
a few scattered olive leaves. Lighting: soft afternoon sunlight from the upper right with
delicate leaf shadows falling across the whole surface, gentle chiaroscuro. Palette ivory,
sandstone #F2EBE1, Tyrrhenian blue #2C4B6E accents, gold, pomegranate red. 35mm film grain,
matte, shallow vignette-free, quiet luxury editorial. No text, no lettering, no numbers on
cards, no hands, no faces, no modern objects, no phone, no candles.
```

---

### H-03 · Плитка: макросъёмка листьев
* **Где:** `.tile` (квадрат)
* **Файл:** `/img/format/f-03-leaf-macro.jpg` · **1400×1400 (1:1)**

```text
Extreme macro photograph of overlapping olive and laurel leaves against a pale sage-ivory
ground, backlit so the translucent vein structure is visible, deep emerald #25503F and olive
green #6B8C4A tones, two small glossy pomegranate-red #C84B31 berries in the lower right,
very shallow depth of field with creamy bokeh at the edges, soft diffused Mediterranean
daylight, fine surface detail, muted restrained palette, matte finish, subtle 35mm film
grain, square 1:1 composition. No text, no insects, no water drops larger than a pinhead,
no hands, no flowers.
```

---

### H-04 · Плитка: нить и узел
* **Где:** `.tile` (квадрат)
* **Файл:** `/img/format/f-04-thread-knot.jpg` · **1400×1400 (1:1)**

```text
A minimal still life, square 1:1 composition: a loose elegant knot of vivid pomegranate-red
#C84B31 silk thread lying on warm ivory paper #F1E4DA with a fine grain; beneath it an
antique wooden thread bobbin with worn antique gold #D4AF37 detailing and a few remaining
windings; two faint concentric gold circles printed as a graphic accent behind the thread,
barely visible. Soft raking light from the left producing one delicate elongated shadow,
hairline detail, matte, subtle film grain, museum-object photography aesthetic.
No text, no lettering, no hands, no needle, no scissors, no other objects.
```

---

### H-05 · Опциональная плитка: пометки на полях
* **Где:** 5-я плитка коллажа / иллюстрация к блоку «Интеграция»
* **Файл:** `/img/format/f-05-marginalia.jpg` · **1400×1400 (1:1)**

```text
Close-up detail photograph: a woman's hand (anatomically correct, no rings except one thin
gold band, no polish) writing marginal notes in the wide margin of an open antique book using
a goose quill; the handwriting is completely illegible — abstract flowing ink marks only, no
recognisable letters or words; warm ivory page #FDFBF7 with faint foxing, a linen cuff at
the wrist, soft window light from the left, muted sepia palette with antique gold #D4AF37
and a single pomegranate-red #C84B31 ribbon marking the page. 50mm, f/2.4, shallow depth of
field, 35mm film grain, matte, quiet intellectual atmosphere. No legible text, no printed
type, no faces, no modern objects.
```

---

# ГРУППA I · СЕКЦИЯ 08 «ПРИГЛАШЕНИЕ» И ФУТЕР

### I-01 · Сургучная печать с ботаническим знаком
* **Где:** `.seal` (на пригласительном письме, поворот −11°)
* **Файл:** `/img/invite/i-01-wax-seal.png` · **1200×1200 (1:1)**, прозрачный

```text
Macro photograph-illustration of a hand-pressed deep red wax seal, perfectly round with
irregular slightly uneven edges and fine cracks, wax colour graduating from #DE6A4C in the
highlight to #9E3320 in the shadow, soft satin sheen on the ridges only. Embossed in relief
inside the seal: a delicate botanical sprig with three slender leaves and a single tiny
pomegranate bud — absolutely no letters, no monogram, no numbers. Encircled by one thin
impressed ring. Beneath the seal, thick ivory cotton-rag paper #FDFBF7 with visible fibre
and a soft deckle edge; two short cream ribbon tails emerging from under the left side.
Soft directional light from the upper left with one gentle elongated drop shadow, extremely
fine detail, muted warm background, matte overall finish, subtle 35mm film grain, square
1:1 composition, isolated subject. No text, no lettering, no monogram, no coat of arms,
no skull, no roses.
```
**Версия с альфой:** `isolated on solid pure white #FFFFFF background, no paper, no shadow` → для наложения на любой фон.

---

### I-02 · Бумага приглашения (фон «письма»)
* **Где:** фон `.letter`
* **Файл:** `/img/invite/i-02-letter-paper.png` · **1800×1400**

```text
Background asset: a single sheet of handmade cotton-rag paper photographed flat from above,
soft irregular deckled edges on all four sides, warm ivory #FDFBF7 with faint laid lines and
a whisper of sandstone #F2EBE1 mottling, the lightest foxing near the corners, a thin
antique gold #A8862A hairline rule inset near the edges, completely empty centre reserved
for typography, even diffuse lighting with no shadows, matte, luxury stationery, high
resolution. No text, no lettering, no seal, no ornaments, no monogram, no flowers, no
watermark visible.
```

---

### I-03 · Золотая виноградная/лавровая кайма (разделитель футера)
* **Где:** над `.foot-bottom`
* **Файл:** `/img/footer/i-03-vine-border.png` · **2400×200**, прозрачный, seamless по горизонтали

```text
A long horizontal hairline ornament, seamless and tileable from left to right: a slender
olive and laurel vine with small elongated leaves and a few tiny antique gold #D4AF37
diamonds spaced along it, drawn as one continuous thin engraved line with muted deep pine
emerald #1A3C34 leaf accents at very low opacity, Renaissance printed-border style,
absolutely no fill, no shading, no flowers in full bloom, no fruit, sparse and refined,
isolated on solid pure white #FFFFFF background, no text.
```

---

### I-04 · Силуэт кипарисовой аллеи (низ футера / финальный аккорд)
* **Где:** декоративная полоса в футере или под блоком 08
* **Файл:** `/img/footer/i-04-cypress-row.png` · **2400×320**, прозрачный

```text
A horizontal row of tall slender cypress tree silhouettes of varying heights, rendered as
flat single-colour shapes in deep pine emerald #1A3C34 at 55% opacity with a faint antique
gold #D4AF37 rim on the right edge of each tree, minimal and graphic like a woodcut frieze,
a thin horizontal baseline under them, seamless and tileable from left to right, generous
empty space above, absolutely no texture inside the shapes, no background, isolated on
solid pure white #FFFFFF background, no text, no people, no buildings.
```

---

# СВОДНАЯ ТАБЛИЦА РАЗМЕЩЕНИЯ (что куда вставлять в коде)

| ID | Ассет | Файл | Хук в вёрстке | Как подключать |
|---|---|---|---|---|
| A-01 | Зерно плёнки | `t-01-grain.png` | `.grain` | `background-image`, `mix-blend-mode:multiply`, opacity .055 |
| A-02 | Льняная бумага | `t-02-paper-ivory.png` | `body`, `#feminity`, `#meetings` | `background-image`, `repeat`, opacity .5 |
| A-03 | Мрамор | `t-03-marble.png` | `.card-art`, `.portrait>div` | фон под иллюстрацией, `background-blend-mode:multiply` |
| A-04 | Персиковая акварель | `t-04-peach-wash.jpg` | `.aud` | `background: url() center/cover` |
| A-05 | Изумрудный лён | `t-05-emerald-linen.png` | `.optics`, `.invite`, `footer` | `background-image` + `background-color:#1A3C34` |
| A-06 | Пятна света | `t-06-dappled-light.png` | `.hero-scrim`, `.format` | `mix-blend-mode:screen`, opacity .35 |
| A-07 | Гербарный лист | `herbarium-sheet.png` | `.card` | `background-image` + `multiply` |
| A-08 | Штукатурка | `t-08-plaster.jpg` | `.aud` (альт.) | `background: cover` |
| B-01 | Монограмма | `l-01-monogram.png` | `.brand-mon` | `<img>` вместо inline-SVG, высота 46 px |
| B-02 | Фавикон | `l-02-favicon.png` | `<head>` | ICO/PNG 16–180 px |
| B-03 | OG-обложка | `l-03-og-cover.jpg` | `<meta property="og:image">` | 1200×630 (кроп) |
| B-04 | Курсор-перо | `c-01-quill.png` | `#cursor svg` | 30×30 px в `.is-hot` |
| B-05 | Буллит-ромб | `c-02-diamond-bullet.png` | `.ticker span::after`, `.optics-panel li::before`, `.card-meta i::before` | 6–9 px, PNG |
| B-06 | Стрелка | `c-03-arrow.png` | `.card-link svg` | 22×9 px |
| B-07 | Разделитель-арка | `c-04-divider-arch.png` | `.divider svg` | 26×34 px |
| B-08 | Лепной карниз | `c-05-molding-strip.png` | между `#feminity` и `#optics` | `<img>` width:100%, height:auto |
| B-09 | Звёздочка | `c-06-asterisk.png` | `.herb-note::before` | 14 px |
| B-10 | Угловой орнамент | `c-07-corner-ornament.png` | `.letter::before/::after` | 34 px, 4 поворота |
| C-01 | Hero-пластина | `h-01-terrace-plate.jpg` | `.hero-scene` | `<img>` `object-fit:cover` + Ken Burns |
| C-02 | Ветви (2 шт.) | `h-02-branch-left/right.png` | `.branch-a`, `.branch-b` | отдельные `<img>` с `data-par` |
| C-03 | Арка-обмер | `h-03-arch-lineart.png` | `.hero-arch-line` | width:min(34vw,420px) |
| D-01 | Гранатовая таблица | `b-01-pomegranate-plate.png` | `.plate-frame svg.art` | `<img>` 4:5 под `archClip` |
| D-02 | Инжирная таблица | `b-02-fig-plate.png` | резерв / лендинги | — |
| E-01 | План сада (светлый) | `o-01-garden-plan-light.png` | `.optics::before` | opacity .14, `background-size:300px` |
| E-02 | План сада (пергамент) | `o-01b-garden-plan-parchment.jpg` | светлая версия секции 03 | `background:cover` |
| E-03 | 4 сферы (статика) | `o-02-four-spheres.png` | презентации/OG | интерактив остаётся SVG |
| E-04 | Ромб ядра | `o-03-core-diamond.png` | центр диаграммы | 28 px |
| F-01 | Полина | `p-01-polina.png` | первая `.portrait` | 3:4 под `archClip` |
| F-02 | Вероника | `p-02-veronika.png` | вторая `.portrait` | 3:4 под `archClip` |
| F-03 | Основатели в интерьере | `p-03-founders-interior.jpg` | лендинг «О нас» | 3:2 |
| G-01…06 | 6 artworks карточек | `m-01…m-06-*.png` | `.card-art svg` | 4:5 под `archClip`, hover-zoom 1.06 |
| G-07 | Плейсхолдер | `m-07-empty-plate.png` | пустая ячейка каталога | 4:5 |
| H-01 | Руки и глина | `f-01-clay-hands.png` | `.tile.t-tall` | 3:5, `object-fit:cover` |
| H-02 | Стол-флэтлей | `f-02-table-flatlay.jpg` | `.tile.t-wide` | 21:9 |
| H-03 | Макро листьев | `f-03-leaf-macro.jpg` | `.tile` | 1:1 |
| H-04 | Нить и узел | `f-04-thread-knot.jpg` | `.tile` | 1:1 |
| H-05 | Пометки на полях | `f-05-marginalia.jpg` | 5-я плитка | 1:1 |
| I-01 | Сургучная печать | `i-01-wax-seal.png` | `.seal` | 124 px, `rotate(-11deg)` |
| I-02 | Бумага письма | `i-02-letter-paper.png` | `.letter` | `background:url(); background-size:100% 100%` |
| I-03 | Кайма-лоза | `i-03-vine-border.png` | над `.foot-bottom` | height:auto, `repeat-x` |
| I-04 | Кипарисы | `i-04-cypress-row.png` | низ футера | `background:bottom/100% auto repeat-x` |

---

# ЧТО СОЗНАТЕЛЬНО **НЕ** ГЕНЕРИРУЕТСЯ (остаётся SVG/CSS)

| Элемент | Причина |
|---|---|
| Диаграмма 4 сфер (`#diagram`) | нужна интерактивность: hover/focus/клик, `aria-pressed`, затемнение неактивных — растр этого не даст |
| Фильтры, кнопки, подчёркивания, прогресс-бар | состояния `:hover`, `aria-pressed`, транзишены |
| Маска-арка `#archClip` | единая геометрическая маска для всех изображений |
| Буквица (drop cap), нумерация I–V, `.sec-num` | типографика, не графика |
| Бегущая строка | текст + CSS-анимация |

---

# ЧЕК-ЛИСТ ПЕРЕД ВЕРСТКОЙ РАСТРОВ

1. **Единая серия.** Все 6 карточек (G-01…G-06) генерировать одним заходом с одинаковым Master Style — иначе серия «распадётся». При расхождении — постобработка: общий LUT (тёплые света, приглушённые тени), зерно A-01 поверх, opacity 8 %.
2. **Арочная обрезка.** Проверить каждый 4:5 и 3:4 ассет, применив маску `archClip` — верхушка главного объекта не должна срезаться.
3. **Прозрачность.** Все PNG с альфой проверить на белой и на тёмной подложке (B-04, C-02, C-03, E-01, I-01, I-03, I-04).
4. **Вес.** Hero C-01 ≤ 420 КБ WebP; плитки коллажа ≤ 180 КБ; карточки ≤ 140 КБ; текстуры ≤ 200 КБ и `repeat`.
5. **Lazy-load.** Всё, кроме C-01, — `loading="lazy"`; для hero — `fetchpriority="high"` + `<link rel="preload">`.
6. **Текст в кадре.** Ни на одном изображении не должно быть букв: названия, номера (`No. 01`), теги и подписи (`Tabula I`) рисуются HTML/CSS — это требование брендбука (SEO и читаемость).
7. **Доступность.** У каждого растра — осмысленный `alt` на русском (уже прописан в текущих `aria-label` у SVG — перенести их один в один).
8. **Кириллица в генерации.** B-01/B-02: если qwen-image-3 исказит «ЛФ» — использовать запасной вариант (арка + круг + гранатовая ветвь), а литеры наложить в редакторе шрифтом Cormorant Garamond 600.