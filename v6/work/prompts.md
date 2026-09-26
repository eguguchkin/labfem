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

## P1 hero-canvas (size 1280x1600) → hero/hero-canvas.webp
prompt: `STYLE ANCHOR ... Composition: a young woman seen half-turned from behind among
dense dark emerald foliage and ripe fruit — peaches and figs on a low branch — her bare
shoulder and the curve of her back catching warm candlelight, loose auburn hair falling
over one shoulder, head tilted down in quiet thought, eyes lowered; deep shadow swallows
the lower third; a thin arc of gold leaf glows along the top edge like an altarpiece arch;
vertical composition with empty dark space in the upper third for a title.`
negative: общий + `full frontal nudity, explicit, facing camera fully, smile`

## P2 fruit-ripe (size 1024x1280) → paint/fruit-ripe.webp
prompt: `STYLE ANCHOR ... Still life: ripe peaches, a split fig and one broken pomegranate
with ruby seeds spilling, lying on deep emerald velvet cloth in near-darkness; dew drops
on fruit skin, one peach cut open showing wet flesh; single candlelight from the left,
gold rim light on the fruit edges; dark background, vertical composition.`
negative: общий + `people, hands, table setting, plate, modern objects`

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

## P7 warm-stone (size 1024x1280) → cards/warm-stone.webp
prompt: `STYLE ANCHOR ... Two open palms resting on a large warm river stone, clay smudges
on the fingers, a fold of raw linen beneath; the stone glows faintly with inner warmth;
deep emerald darkness around; candlelight low from the side; vertical composition,
no face.`
negative: общий + `face, jewelry, modern manicure, bright background`

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
Кроп P1 по центру 1200x630 + тонировка --velvet-deep по краям; текст не накладывается.
