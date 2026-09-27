# Промпты для генерации изображений — v6

Модель: Selectel AIG `qwen/qwen-image-3` (POST /aig/v1/images/generations, ключ из
~/.pi/agent/pi-image-gen/settings.json → customProviders.selectel.apiKey).
Поле ответа: data[0].b64_json. Минимум size 512x512 (256 даёт 503). Ретраи: до 6 попыток,
пауза attempt*6 сек. Конкурентность ≤ 3.

Общий стиль-якорь (добавлять в начало каждого prompt картин):
`STYLE ANCHOR: oil painting on canvas in the manner of 19th-century academic realism and
Pre-Raphaelites (Bouguereau, Waterhouse), deep chiaroscuro, candlelit warm light from one
side, rich impasto brushwork visible, aged varnish, palette limited to near-black deep
emerald green (#0a2417), antique gold (#c8a24a), ivory (#ece3cf), warm flesh ochre
(#e3c3a3), deep madder red (#7e2b26) as rare accent; sensual but chaste, no modern objects,
no text, no watermark, no frame.`

Общий negative_prompt для картин:
`photo, 3d render, cartoon, anime, flat vector, neon, bright saturated colors, white
background, modern clothing, jewelry logos, text, letters, watermark, signature, frame,
border, plastic, glossy, deformed hands, extra limbs`

Постобработка (скрипт этапа 2, python+PIL/numpy в /tmp/imgenv):
- Тайлы текстур: бесшовность зеркальной сшивкой: T = [[I, flipH(I)], [flipV(I), flipVH(I)]]
  из центральной квадратной кропки 512→ тайл 1024, затем даунскейл до 512/640 webp q82.
- Картины: даунскейл до целевого размера webp q82; лёгкое зерно (gauss σ=1.2, amp 3)
  и виньетка по краям 6%.
- Fleuron/символы: вырез альфы по порогу яркости фона, webp с альфой.

---

## T1 velvet-tile (size 1024x1024) → tex/velvet-tile.webp (тайл 512)
prompt: `Seamless tileable texture of luxurious deep emerald green velvet fabric,
almost black dark green (#0a2417), soft pile nap with subtle directional sheen, gentle
folds and pressure marks catching faint warm candlelight, macro view, no objects,
no highlights blowout, uniform lighting, photographic macro of textile, very dark,
muted, elegant. Tileable, no seams, no edges, no vignette.`
negative: `objects, people, pattern repeat visible, seams, borders, bright light, white,
glossy plastic, satin shine`

## T2 crackle-tile (size 1024x1024) → tex/crackle-tile.webp (тайл 640, overlay soft-light)
prompt: `Seamless tileable craquelure texture of an ancient oil painting varnish: fine
irregular crack network like dried lake bed, thin pale ivory cracks over mid-dark warm
grey-brown ground (#4a4038), cracks sparse and delicate, evenly distributed, flat scan
of old varnish surface, no image content, no figures, uniform exposure. Tileable,
no seams, no vignette.`
negative: `painting content, faces, figures, bright colors, gold, heavy contrast,
borders, text`

## T3 gold-tile (size 1024x1024) → tex/gold-tile.webp (тайл 256, для background-clip)
prompt: `Seamless tileable texture of antique gold leaf gilding: burnished matte gold
surface (#c8a24a) with subtle darker patina patches, tiny pits and brush burns, soft
uneven sheen, macro scan, no objects, uniform light, warm. Tileable, no seams.`
negative: `coins, jewelry, objects, bright mirror shine, yellow neon, borders, text`

## T4 parchment-tile (size 1024x1024) → tex/parchment-tile.webp (тайл 512, фон поля формы)
prompt: `Seamless tileable texture of aged warm parchment paper: ivory-cream (#ece3cf)
with faint tea stains, fiber flecks and soft mottling, matte, evenly lit scan, very
subtle, no writing, no objects. Tileable, no seams, no vignette.`
negative: `text, letters, drawings, dark stains, borders, torn edges, bright white`

## P1 hero-canvas (size 1280x1600) → hero/hero-canvas.webp (запасная v1)
prompt: `STYLE ANCHOR ... Composition: a young woman seen half-turned from behind among
dense dark emerald foliage and ripe fruit — peaches and figs on a low branch — her bare
shoulder and the curve of her back catching warm candlelight, loose auburn hair falling
over one shoulder, head tilted down in quiet thought, eyes lowered; deep shadow swallows
the lower third; a thin arc of gold leaf glows along the top edge like an altarpiece arch;
vertical composition with empty dark space in the upper third for a title.`
negative: общий + `full frontal nudity, explicit, facing camera fully, smile`

## P1c hero-full (size 2048x2048) → hero/hero-full-{land,port}.webp (полноэкранный hero)

Квадратный оригинал с «безопасным центром» под два кропа (desktop 16:9 полоса
y 420–1572, mobile 9:16 колонка x 448–1600): лицо и жест в верхней трети, нижняя
треть — спокойная тьма бархата под текст, края — растяжимая листва/драпировка.
prompt: `STYLE ANCHOR ... Square composition designed for both wide and tall crops.
Vertical zones: top sixth - dark emerald foliage, velvet drapery and a single candle
glow at the left edge; middle - a young woman half-reclining among deep green velvet
folds, head and face centered around one third of the height, eyes half-lidded toward
the viewer, loose auburn hair, bare shoulders and collarbone catching warm candlelight,
thin ivory linen slipping from one arm, a ripe peach resting near her hand; lower
third - calm near-empty deep shadow of velvet folds, almost no detail, reserved as
quiet dark space; sides - extendable dark foliage and drapery, no important detail
near edges. Sensual, tender, chaste, museum quality.`
negative: `NEG_PAINT + full frontal nudity, explicit, bright details in lower third,
cluttered edges, centered symmetrical pose`
Постобработка (post.py): два кропа одного оригинала + grain_vignette; артефакты
hero-full-land.webp (2048x1152) и hero-full-port.webp (1152x2048).

## P1b hero-canvas-2 (size 1280x1600) → hero/hero-canvas-2.webp (антракт между 06 и 07)
prompt: `STYLE ANCHOR ... Composition: a young woman half-reclining on deep emerald
velvet drapery among dark foliage, body in a soft S-curve, one strap of her ivory linen
shift slipped from her shoulder, head tilted back, eyes closed in quiet pleasure, loose
auburn hair spilling over her arm; a single ripe peach resting in the hollow of her
collarbone, her fingertips lightly touching it; warm candlelight raking across her
shoulder and throat; deep shadow below; thin arc of gold leaf along the top edge like an
altarpiece arch; vertical composition with dark empty space in the upper third for a
title; sensual, tender, chaste.`
negative: общий + `full frontal nudity, explicit, open mouth, grin`

## P2 feminity-figure (size 1024x1280) → paint/feminity-figure.webp (секция 02, запасная v1)
prompt: `STYLE ANCHOR ... Composition: a young woman seated in three-quarter view in a
dim interior, dark emerald drapery behind, a shallow bowl of ripe peaches and figs on her
lap; she holds one split fig open in both hands at her chest, gaze lowered to it, lips
slightly parted; bare shoulders, loose dark hair over one shoulder; candlelight from the
left; vertical composition.`
negative: общий + `full frontal nudity, explicit, still life without figure`

## P2b feminity-figure-2 (size 1024x1280) → paint/feminity-figure-2.webp (секция 02, основная v2)
Та же композиция, но настроение живое и чувственное: голова поднята, взгляд на зрителя
сквозь полуопущенные ресницы, полуулыбка, румянец, растрёпанные волосы; плод — подношение,
не предмет изучения; поза languid, плечи развёрнуты; свечной свет теплее, блик на губах
и ключице.
negative: общий + `frown, concentration, eating, biting, staring at fruit, grimace,
still life without figure, full frontal nudity, explicit`
(старый натюрморт fruit-ripe остаётся только как архивный ассет, на сайте не используется)

## P3 cat-black (size 1024x1280) → cards/cat-black.webp
prompt: `STYLE ANCHOR ... A majestic black cat, black as night, with amber eyes, seated
in a calm regal pose, tail curled around its paws; behind it a round halo of burnished
gold leaf; below — ivy leaves and a gilded branch on dark emerald ground; vertical
composition, the cat slightly below center.`
negative: общий + `white cat, kitten, cartoon, collar, modern`

## P4 pomegranate (size 1024x1280) → cards/pomegranate.webp
prompt: `STYLE ANCHOR ... A pomegranate broken open in a woman's cupped hands, seeds like
rubins set in gold light; juice glistening; sleeves of dark green linen at the wrists;
near-black emerald background; candlelight from above; vertical composition.`
negative: общий + `face, full body, modern hands manicure`

## P5 snake-skin (size 1024x1280) → cards/snake-skin.webp
prompt: `STYLE ANCHOR ... A slender dark snake coiling around a woman's bare forearm and
letting go, its shed translucent skin left on a warm living stone beside her hand;
emerald darkness around, one shaft of warm light on the stone; vertical composition,
no face visible, only arm and hand.`
negative: общий + `face, fear, horror, blood, fangs`

## P6 thread-spindle (size 1024x1280) → cards/thread-spindle.webp
prompt: `STYLE ANCHOR ... Close view of a woman's hands holding a wooden spindle, winding
a thin gold thread that catches the light and leaves the frame upward; linen sleeve
slipped from the shoulder; dark emerald velvet background; candlelight; vertical
composition, no face.`
negative: общий + `face, modern tools, scissors, bright colors`

## P7 water-dark (size 1024x1280) → cards/water-dark.webp (карточка 5, вместо «тёплого камня»)
prompt: `STYLE ANCHOR ... Composition: a young woman kneeling at the edge of dark still
water at night, her whole figure reflected beneath her, one hand touching the surface
making thin rings; water lilies and a pale bud nearby; moonless warm light from a hidden
candle on the bank lighting her profile and shoulder; deep emerald and black palette;
vertical composition.`
negative: общий + `daylight, blue water, modern swimwear, full frontal nudity`

## P8 optics-figure (size 1024x1280) → paint/optics-figure.webp (секция 03)
prompt: `STYLE ANCHOR ... Composition: head and shoulders of a young woman in half-turn
holding an oval gilded hand mirror at her chest, the mirror glass turned slightly away
catching a warm glow instead of a face; her eyes lowered toward it, dark hair loosely
braided with a gold thread; deep emerald darkness around; candlelight; vertical
composition.`
negative: общий + `face inside mirror, double face, full frontal nudity`
Пост: inset-кроп 4.5% — генерация даёт светлую бумажную кайму по краям.

## P9 for-whom-figure (size 1024x1280) → paint/for-whom-figure.webp (секция 04)
prompt: `STYLE ANCHOR ... Composition: a young woman head and shoulders, eyes closed,
face calm and open, holding a pale porcelain mask lowered in one hand at her side, the
mask ribbons slipping through her fingers; bare shoulder, loose hair; a single warm shaft
of light on her face; deep emerald darkness; vertical composition.`
negative: общий + `mask on face, theatre crowd, full frontal nudity`

## P10 circle-figure (size 1024x1280) → paint/circle-figure.webp (секция 07, запасная v1)
prompt: `STYLE ANCHOR ... Composition: seen over the bare shoulder and head of a young
woman in the foreground, a small circle of women seated on low stools around a low wooden
table with candles and a clay bowl, all in deep shadow, warm candlelight on their faces
and hands; the foreground woman's loose hair and shoulder catch the light; intimate,
quiet; vertical composition.`
negative: общий + `modern room, electric light, full frontal nudity`

## P10b circle-figure-2 (size 1024x1280) → paint/circle-figure-2.webp (секция 07, запасная v2)
Круг из пяти женщин вокруг низкого стола со свечами, вид спереди через стол: все в фас
или три четверти спереди, ни одной спиной; каждая явно отличается — возраст, лицо,
волосы (рыжая распущенная, тёмная коса, седые пряди, короткие кудри, светлый платок);
позы и жесты разные: наклон вперёд на локтях, тихий смех с поднятой рукой, слушает с
наклонённой головой и сложенными ладонями, наливает из кувшинчика, подбородок на ладони;
свет свечей из центра стола на лицах.
negative: общий + `identical faces, twins, clones, mirrored poses, back turned, nape,
modern room, electric light, full frontal nudity`

## P10c circle-figure-3 (size 1024x1280) → paint/circle-figure-3.webp (секция 07, основная v3)
Круг из пяти МОЛОДЫХ женщин (20–35) вокруг низкого стола со свечами, вид спереди через
стол: все в фас или три четверти спереди; каждая явно отличается волосами и лицом;
одеты только в лёгкие полупрозрачные льняные драпировки цвета слоновой кости,
соскальзывающие с плеч: открытые плечи, ключицы, руки в свечном свете, ткань мягко
облегает; нагота — в мере классической академической живописи, целомудренно;
настроение живое и возбуждённое: тихий смех, разрумяненные лица, яркие глаза, жесты
(поднятая рука, наливает из кувшинчика, подбородок на ладони); свет свечей из центра
стола на лицах, плечах и руках; изумрудная тьма позади.
negative: общий + `elderly woman, old face, gray hair, heavy clothing, fully clothed,
high collar, identical faces, twins, clones, mirrored poses, back turned, nape,
modern room, electric light, explicit nudity, exposed breasts, nipples`
Пост: inset-кроп 2% — тонкая бумажная кайма по краям генерации.

## P11 invite-figure (size 1024x1280) → paint/invite-figure.webp (секция 08)
prompt: `STYLE ANCHOR ... Composition: a young woman at a tall arched doorway drawing
aside a heavy emerald velvet curtain with one hand, warm golden light from beyond
spilling over her bare shoulder and cheek, her face turned to the viewer with a faint
half-smile and lowered lashes; a folded letter with a wax seal in her other hand at her
waist; vertical composition.`
negative: общий + `modern door, electric light, full frontal nudity`

## O1 fleuron (size 512x512) → orn/fleuron.webp (альфа)
prompt: `A single small ornamental fleuron motif of antique gilded bronze: symmetrical
leaf-and-bud flourish, burnished gold (#c8a24a) with dark patina in recesses, centered on
pure black background, flat frontal view, no shadow, no other elements.`
negative: `text, frame, multiple motifs, bright background, photo`

## O2 символы оптик (4 шт, size 512x512, альфа) → orn/sym-{mirror,snake,brush,thread}.webp
prompt-шаблон: `A single symbolic emblem in antique burnished gold (#c8a24a) with dark
patina, flat frontal view, centered on pure black background, no shadow: <SYMBOL>.
Old-master gilded relief style, delicate, small.`
- mirror: `an oval hand mirror with a short handle`
- snake: `a snake forming a loose circle, head over tail`
- brush: `a painter's brush with one thick stroke of gold paint beneath it`
- thread: `a wooden spindle with a winding thread`
negative: `text, frame, photo, bright background, multiple objects`

## M1 og-cover (не генерировать)
Кроп P1b (hero-canvas-2) по центру 1200x630 + тонировка --velvet-deep по краям; текст не накладывается.
