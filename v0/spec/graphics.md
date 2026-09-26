Ниже — полный комплект графических ассетов для сайта. Там, где гайдбук даёт выбор («или»), я зафиксировал конкретный мотив, чтобы визуальная система была цельной.

Промпты даны на английском — для qwen-image-3 так стабильнее держатся стиль, линия и ограничения. Назначение, формат и состав комплекта — на русском.

---

## ОБЩИЕ ПРАВИЛА ГЕНЕРАЦИИ

### Единый negative prompt

Использовать для всех сюжетных и орнаментальных ассетов:

```text
pure white #FFFFFF, pure black #000000, neon colors, oversaturated colors, glossy 3D render, plastic texture, flat modern vector icon, harsh digital gradients, CSS-like drop shadow, heavy baroque ornaments, crowns, luxury wedding style, esoteric symbols, moons, stars, mandalas, tarot, occult, text, letters, numbers, watermark, logo, brand signs, stock photo, smiling models, aggressive marketing UI, thick cartoon contours, childish illustration, coffee stains, dirt, grunge, torn paper, solid background, colored backdrop, frame around subject
```

**Исключения:**

- `B9` — разрешена только одна кириллическая буква `Л`.
- `B6` — сам объект является лёгкой рамкой, но без барокко и тяжести.
- `A1–A5` — это фоны, поэтому требования прозрачности и отсутствия фона к ним не применяются.

### Технические замечания

- qwen-image-3 выдаёт растр. Для финального сайта тонкие линии желательно отрисовать/перевести в SVG, а акварельные подкраски оставить отдельными полупрозрачными слоями.
- Если модель не отдаёт прозрачный фон, генерируйте на плоском фоне `#F5F0E8` и аккуратно вырезайте.
- Все иллюстрации должны выглядеть как одна серия: одинаковая толщина линии, одинаковая степень «ручной» акварельной подкраски.
- Акварельный слой должен быть чуть небрежным, местами выходить за контур на 1–2 px.
- Весь текст, рукописные подписи, номера глав и стрелки ссылок должны быть живым текстом, а не картинками.

---

# ИТОГОВЫЙ СОСТАВ КОМПЛЕКТА

**51 ассет:**

- фоны и текстуры — 5
- орнаментика и системная графика — 11
- секция 01 — 1
- секция 02 — 2
- секция 03 — 5
- секция 04 — 5
- секция 05 — 1
- секция 06 — 4
- секция 07 — 4
- секция 08 — 2
- карточки — 6
- соцсети и контакты — 4
- навигация, опционально — 1

Фотографии для секции «О нас» в этот список не входят: по гайдбуку там нужны настоящие фото, а не гравюры.

---

# 1. ФОНЫ И ТЕКСТУРЫ

## A1. Молочная бумага

**Назначение:** основной фон сайта.  
**Формат:** 2048×2048, seamless, PNG.

**Prompt:**

> Seamless subtle aged paper texture, warm milky base color #F5F0E8, very fine grain, barely visible natural fibers, gentle uneven surface, low-contrast noble book-page material, flat scan, soft and calm, square composition, no objects, no text, no stains, no obvious repeating pattern, no vignette, no pure white, no pure black.

---

## A2. Кремовая страница

**Назначение:** фон секций 03, 07 и карточных блоков.  
**Формат:** 2048×2048, seamless, PNG.

**Prompt:**

> Seamless subtle aged paper texture, warm cream base color #F0E9DC, very fine grain, barely visible natural fibers, gentle uneven surface, low-contrast book-page material, flat scan, soft and calm, square composition, no objects, no text, no stains, no obvious repeating pattern, no vignette, no pure white, no pure black.

---

## A3. Светлый пергамент

**Назначение:** подложки, выделенные блоки, форма подписки.  
**Формат:** 2048×2048, seamless, PNG.

**Prompt:**

> Seamless subtle parchment paper texture, very light warm base color #FAF6EE, fine grain, delicate natural fibers, gentle uneven surface, low-contrast noble aged paper, flat scan, square composition, no objects, no text, no stains, no obvious repeating pattern, no vignette, no pure white, no pure black.

---

## A4. Молочная бумага с розовым подтоном

**Назначение:** фон секции 02 «Феминность».  
**Формат:** 2048×2048, seamless, PNG.

**Prompt:**

> Seamless subtle aged paper texture, warm milky base color #F5F0E8 with an extremely delicate dusty-rose undertone #C9A9A0 at 3–5 percent, as if warm evening light falls at a slightly different angle, very fine grain, barely visible natural fibers, gentle uneven surface, low-contrast book-page material, flat scan, no objects, no text, no stains, no obvious repeating pattern, no pure white, no pure black.

---

## A5. Кремовая бумага с лавандовым подтоном

**Назначение:** фон секции 05 «О нас».  
**Формат:** 2048×2048, seamless, PNG.

**Prompt:**

> Seamless subtle aged paper texture, warm cream base color #F0E9DC with an extremely delicate lavender undertone #B8A9C9 at 3–4 percent, very fine grain, barely visible natural fibers, gentle uneven surface, low-contrast book-page material, flat scan, no objects, no text, no stains, no obvious repeating pattern, no pure white, no pure black.

---

# 2. ОРНАМЕНТИКА И СИСТЕМНАЯ ГРАФИКА

## B1. Горизонтальный цветочный разделитель

**Назначение:** разделитель между секциями.  
**Формат:** 2048×128, прозрачный PNG.

**Prompt:**

> Horizontal botanical divider, one slightly uneven hairline in warm ochre #C4A265 at 50 percent opacity, a small six-petal flower with two tiny leaves at the center, line tapers gracefully toward both ends, antique pen-drawn engraving, warm graphite #3A3230 and ochre, isolated on transparent background, very wide composition, no frame, no text, no baroque curls, no bright colors.

---

## B2. Точечный разделитель из трёх цветков

**Назначение:** пауза в тексте, разделитель между записями.  
**Формат:** 512×128, прозрачный PNG.

**Prompt:**

> Three tiny five-petal flowers in a horizontal row, separated by small delicate dots, fine antique etched line, warm graphite #3A3230, subtle stipple centers, isolated on transparent background, minimal book ornament, no frame, no text, no bright colors.

---

## B3. Маркер списка «звёздочка-цветочек»

**Назначение:** маркер списка, мелкий акцент.  
**Формат:** 256×256, прозрачный PNG.

**Prompt:**

> Small six-pointed flower-star bullet marker, fine antique etched line, warm graphite #3A3230 or soft ochre #C4A265, minimal, clean, legible at 12–16 pixels, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## B4. Тонкая рукописная линейка

**Назначение:** разделители, подчёркивания, линии в карточках.  
**Формат:** 2048×64, прозрачный PNG.

**Prompt:**

> Single hand-drawn horizontal hairline, slightly uneven ink pressure, delicate living line, warm graphite #3A3230 at 40 percent opacity, isolated on transparent background, very wide composition, no texture, no frame, no text, no bright colors.

---

## B5. Угловой орнамент для карточек

**Назначение:** лёгкое оформление карточек, цитат, выделенных блоков.  
**Формат:** 512×512, прозрачный PNG. Генерировать один угол, затем зеркалить.

**Prompt:**

> One delicate corner ornament, a thin botanical sprig with two small leaves and a tiny bud curving along a barely visible corner angle, antique pen-drawn line, warm graphite #3A3230 and soft ochre #C4A265, isolated on transparent background, minimal and refined, not baroque, no full frame, no text, no bright colors.

---

## B6. Лёгкая орнаментальная рамка

**Назначение:** редкое оформление карточки или цитаты.  
**Формат:** 1536×1024, прозрачный PNG.

**Prompt:**

> Light rectangular ornamental frame drawn as if with a fine pen, slightly uneven single line, tiny botanical accents at the corners, open transparent center, antique engraving, warm graphite #3A3230 and soft ochre #C4A265 at low opacity, isolated on transparent background, refined and restrained, no heavy baroque ornament, no text, no bright colors.

---

## B7. Малая виньетка для полей

**Назначение:** пометка на полях рядом с рукописным текстом.  
**Формат:** 512×768, прозрачный PNG.

**Prompt:**

> Tiny marginal botanical sprig with one leaf and a small closed bud, delicate antique etched line, sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, hand-colored slightly irregular, isolated on transparent background, vertical composition, no frame, no text, no bright colors.

---

## B8. Универсальная концовка главы

**Назначение:** завершение секций, финальный декоративный мотив.  
**Формат:** 1536×576, прозрачный PNG.

**Prompt:**

> Small book end-piece, a short flowering branch with two leaves and one falling petal, horizontal composition, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, aged book illustration, isolated on transparent background, no frame, no text, no bright colors.

---

## B9. Инициал «Л»

**Назначение:** буквица для названия «Лаборатория феминности».  
**Формат:** 1024×1024, прозрачный PNG.

**Prompt:**

> Decorated Cyrillic initial letter Л, elegant early-twentieth-century book antiqua, warm graphite #3A3230 or soft ochre #C4A265, a thin apple-blossom twig subtly woven around one stroke, refined manuscript feeling, delicate antique engraving, isolated on transparent background, square composition, only the single Cyrillic letter Л, no other text, no medieval heaviness, no baroque ornament.

Если qwen-image-3 неточно передаст кириллицу, лучше сгенерировать только botanical-орнамент и совместить его с живой типографской буквой `Л`.

---

## B10. Засушенный лепесток

**Назначение:** сквозной мотив «между страницами», микродеталь, разделитель.  
**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Single dried flower petal, translucent and slightly curled, delicate irregular edges, fine etched contour, sepia #6B5B4E with faint dusty-rose watercolor wash #C9A9A0 at 20 percent, hand-colored slightly beyond the contour, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## B11. Эмблема для favicon

**Назначение:** техническая эмблема проекта.  
**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Minimal favicon emblem, a simplified apple-blossom twig with one small flower and one bud, fine antique engraved line but clean enough to remain legible at 16 pixels, warm graphite #3A3230, isolated on transparent background, square composition, no circle frame, no text, no bright colors, no excessive detail.

---

# 3. СЕКЦИЯ 01 — ТИТУЛ

## C1. Главная титульная ветвь

**Назначение:** ключевая иллюстрация первого разворота.  
**Формат:** 1024×1536, прозрачный PNG.  
**Отображение:** 200–320 px по большей стороне.

**Prompt:**

> A single branch of blossoming apple tree with three open blossoms, two buds and delicate leaves, diagonal composition, antique botanical engraving and etching, fine slightly uneven living line, delicate hatching and stippling, scientific accuracy with poetic softness, warm graphite #3A3230 and sepia #6B5B4E, translucent hand-colored watercolor wash dusty rose #C9A9A0 at 20 percent on petals only, wash slightly irregular and barely beyond contour, aged book illustration, isolated on transparent background, vertical composition, no frame, no text, no bright colors, no gloss, no heavy shadow.

---

# 4. СЕКЦИЯ 02 — ФЕМИННОСТЬ

## D1. Основной цветок секции

**Назначение:** главная иллюстрация эссе о феминности.  
**Формат:** 1024×1536, прозрачный PNG.

**Prompt:**

> A complex peony in full bloom with one side bud and several leaves, antique botanical engraving, fine slightly uneven etched line, delicate cross-hatching and stippling, scientific accuracy with poetic softness, warm graphite #3A3230 and sepia #6B5B4E, translucent hand-colored watercolor wash dusty rose #C9A9A0 at 20–25 percent, faint lavender #B8A9C9 at 10 percent in shaded areas, wash slightly irregular and barely beyond contour, aged book illustration, isolated on transparent background, vertical composition, no frame, no text, no rose cliché, no bright colors, no gloss.

---

## D2. Альтернативный женский образ

**Назначение:** вариант главной иллюстрации секции, если нужен образ, а не цветок.  
**Формат:** 1024×1536, прозрачный PNG.

**Prompt:**

> A soft faceless female figure seen from behind, gentle engraved silhouette, simple shawl, holding a peony branch, archetypal and poetic, age ambiguous, no facial features, fine antique etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and lavender #B8A9C9 washes at 15 percent, aged book illustration, isolated on transparent background, vertical composition, no frame, no text, no stock-photo realism, no bright colors.

---

# 5. СЕКЦИЯ 03 — НАША ОПТИКА

## E1. Общая метафора четырёх линий

**Назначение:** альтернативная или вводная иллюстрация к четырём источникам оптики.  
**Формат:** 1536×768, прозрачный PNG.

**Prompt:**

> Four thin living lines interweaving into a delicate braid-like botanical pattern, each line subtly different but visually equal, small leaves and tiny buds along the lines, composition like a quiet scientific diagram, antique engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, very faint watercolor accents dusty rose #C9A9A0, lavender #B8A9C9, sage #8B9478 and ochre #C4A265 at 10–15 percent, isolated on transparent background, horizontal composition, no frame, no text, no esoteric symbols, no bright colors.

---

## E2. Эмблема «Психология»

**Назначение:** первая из четырёх линз.  
**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small emblem of an antique magnifying glass held over a single leaf with fine veins, scientific but poetic, antique botanical engraving, thin slightly uneven etched line, delicate stippling, warm graphite #3A3230 and sepia #6B5B4E, faint translucent sage watercolor wash #8B9478 at 15 percent, isolated on transparent background, square composition, no frame, no text, no modern icon style, no bright colors.

---

## E3. Эмблема «Миф»

**Назначение:** вторая линза.  
**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small emblem of a simple antique urn with a delicate vine and one small flower curling from it, myth as an old story, antique engraving, thin slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent lavender watercolor wash #B8A9C9 at 15 percent, isolated on transparent background, square composition, no frame, no text, no classical faces, no esoteric symbols, no bright colors.

---

## E4. Эмблема «Искусство»

**Назначение:** третья линза.  
**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small emblem of an engraver’s nib or fine pen beside a half-drawn flowering sprig, the idea of line, craft and image, antique etching style, thin slightly uneven living line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, isolated on transparent background, square composition, no frame, no text, no palette cliché, no bright colors.

---

## E5. Эмблема «Личный опыт»

**Назначение:** четвёртая линза.  
**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small emblem of a simple teacup, an open blank notebook and a pressed petal, lived experience and quiet conversation, antique engraving, thin slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent terracotta #B07D6A and ochre #C4A265 watercolor wash at 15 percent, isolated on transparent background, square composition, no legible text, no modern objects, no bright colors.

---

# 6. СЕКЦИЯ 04 — ДЛЯ КОГО

Эти пять vignettes — пул. В финальной вёрстке использовать 3–5 в зависимости от количества текстовых зарисовок.

## F1. Силуэт у окна

**Формат:** 1024×1280, прозрачный PNG.

**Prompt:**

> A female silhouette seen from behind near a window, age ambiguous, no facial features, soft contemplative posture, one hand lightly near the frame, timeless simple clothing, antique engraving, fine slightly uneven etched line, delicate hatching suggesting warm light without glow, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, isolated on transparent background, vertical composition, no frame, no text, no interior clutter, no bright colors.

---

## F2. Руки, держащие семя или лепесток

**Формат:** 1024×1024, прозрачный PNG.

**Prompt:**

> Two cupped female hands holding a single seed or dried petal, gesture of care and attention, no faces, age ambiguous, fine antique engraving, slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, isolated on transparent background, square composition, no frame, no text, no jewelry, no bright colors.

---

## F3. Рука, прикасающаяся к ветви

**Формат:** 1280×768, прозрачный PNG.

**Prompt:**

> A slender female hand reaching to touch a flowering branch, only hand and branch, no face, delicate antique etched line, fine hatching and stippling, warm graphite #3A3230 and sepia #6B5B4E, faint translucent sage #8B9478 and dusty-rose #C9A9A0 watercolor washes at 15 percent, isolated on transparent background, horizontal composition, no frame, no text, no bright colors.

---

## F4. Свернувшаяся в кресле figura в шали

**Формат:** 1024×1536, прозрачный PNG.

**Prompt:**

> A young woman curled up sideways in a deep old armchair, knees drawn to her chest, wrapped in a soft oversized shawl, head bowed and resting on her knees, face hidden, thick long loose wavy hair falling over her shoulder and down her back with visible separate strands, a small simple ceramic cup on the floor beside the chair, mood of quiet rest and being completely at ease and unobserved, age ambiguous, antique engraving, fine slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent lavender watercolor wash #B8A9C9 at 15 percent, isolated on transparent background, vertical composition, no frame, no text, no dramatic shadows, no bright colors.

---

## F5. Две фигуры за столом

**Формат:** 1280×768, прозрачный PNG.

**Prompt:**

> Two faceless female silhouettes sitting across a small round table with two simple teacups, calm conversation, age ambiguous, timeless simple clothing, antique engraving, thin living line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and ochre #C4A265 watercolor washes at 15 percent, isolated on transparent background, horizontal composition, no frame, no text, no modern café details, no bright colors.

---

# 7. СЕКЦИЯ 05 — О НАС

## G1. Лавандовая виньетка для пометки на полях

**Назначение:** графическая часть рукописной пометки рядом с портретами.  
**Формат:** 512×768, прозрачный PNG.

**Prompt:**

> A small lavender sprig with two or three delicate flower spikes, marginal botanical note, fine antique etched line, sepia #6B5B4E, translucent lavender watercolor wash #B8A9C9 at 20 percent, hand-colored slightly irregular, isolated on transparent background, vertical composition, no frame, no text, no bright colors.

---

# 8. СЕКЦИЯ 06 — ВСТРЕЧИ

## H1. Заставка дневника встреч

**Назначение:** вводная иллюстрация секции.  
**Формат:** 1024×512, прозрачный PNG.

**Prompt:**

> A small open antique diary with blank aged pages, a dried leaf tucked between them and a thin ribbon bookmark, no legible text, fine antique engraving, slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent terracotta watercolor wash #B07D6A at 15 percent, isolated on transparent background, horizontal composition, no frame, no bright colors.

---

## H2. Маркер ближайшей встречи

**Назначение:** акцент рядом с датой ближайшего события.  
**Формат:** 256×256, прозрачный PNG.

**Prompt:**

> Tiny flower bud on a short stem, marker for an upcoming meeting, fine antique engraved line, warm graphite #3A3230, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, isolated on transparent background, square composition, clean and legible at small size, no frame, no text, no bright colors.

---

## H3. Маркер прошедшей встречи

**Назначение:** «архивная» запись.  
**Формат:** 256×256, прозрачный PNG.

**Prompt:**

> A faded pressed leaf, archive marker for a past meeting, very low contrast sepia #6B5B4E, delicate etched veins, appearance of about 60 percent opacity, isolated on transparent background, square composition, clean and legible at small size, no frame, no text, no dirt, no bright colors.

---

## H4. Маркер будущей встречи

**Назначение:** гипотетическая запись-набросок.  
**Формат:** 256×256, прозрачный PNG.

**Prompt:**

> A barely sketched sprout emerging from a small seed, future meeting marker, fine light graphite lines #3A3230, partly dotted and delicate, appearance of about 50 percent opacity, isolated on transparent background, square composition, clean and legible at small size, no frame, no text, no bright colors.

---

# 9. СЕКЦИЯ 07 — КАК ЭТО ПРОИСХОДИТ

Гайдбук предполагает 2–3 иллюстрации. Ниже три основных и одна резервная.

## I1. Руки, рисующие в тетради

**Формат:** 1280×768, прозрачный PNG.

**Prompt:**

> Female hands drawing in an open blank notebook with a thin pencil, a small flower resting nearby, no faces, age ambiguous, antique engraving, fine slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and ochre #C4A265 watercolor washes at 15 percent, isolated on transparent background, horizontal composition, no legible text, no modern objects, no bright colors.

---

## I2. Чашка чая

**Формат:** 1024×1024, прозрачный PNG.

**Prompt:**

> A simple ceramic teacup and saucer with one delicate curl of steam, a dried petal beside it, antique engraving, thin slightly uneven etched line, fine hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent terracotta watercolor wash #B07D6A at 15 percent, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## I3. Круг стульев

**Формат:** 1280×768, прозрачный PNG.

**Prompt:**

> A circle of six simple wooden chairs around a small low table with a single flower in a plain vase, slightly elevated view, no people, antique engraving, fine slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent sage watercolor wash #8B9478 at 15 percent, isolated on transparent background, horizontal composition, no frame, no text, no modern furniture, no bright colors.

---

## I4. Резервная иллюстрация: раскрытая тетрадь

**Формат:** 1024×512, прозрачный PNG.

**Prompt:**

> An open blank notebook with a pressed petal and a thin ribbon, quiet preparation for a meeting, fine antique engraving, slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent lavender watercolor wash #B8A9C9 at 15 percent, isolated on transparent background, horizontal composition, no legible text, no frame, no bright colors.

---

# 10. СЕКЦИЯ 08 — ПРИГЛАШЕНИЕ

## J1. Финальная ветвь

**Назначение:** концовка книги, симметричный ответ титульной виньетке.  
**Формат:** 1536×576, прозрачный PNG.

**Prompt:**

> Small closing botanical motif, a short apple-blossom branch with one open flower, one bud and one falling petal, lighter and smaller than a title illustration, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, isolated on transparent background, horizontal composition, no frame, no text, no bright colors.

---

## J2. Конверт / гостевая книга

**Назначение:** опциональная деталь рядом с формой подписки.  
**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> A delicate envelope or guest-book page with a tiny botanical sprig tucked under its flap, no legible text, fine antique engraving, slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and ochre #C4A265 watercolor washes at 15 percent, isolated on transparent background, square composition, no wax seal as central element, no frame, no bright colors.

---

# 11. ЭМБЛЕМЫ КАРТОЧЕК

Набор из шести ботанических эмблем. Если карточек больше, серию нужно продолжить в том же стиле.

## K1. Яблоневый цвет

**Формат:** 512×512, прозрачный PNG.  
**Отображение:** 48–64 px.

**Prompt:**

> Small card emblem, one apple-blossom sprig with a single open flower and one bud, simplified composition legible at 48–64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## K2. Пионовый бутон

**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small card emblem, a single peony bud with two leaves, simplified composition legible at 48–64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## K3. Ирис

**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small card emblem, one iris flower with slender leaves, simplified composition legible at 48–64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent lavender watercolor wash #B8A9C9 at 20 percent, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## K4. Лаванда

**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small card emblem, two delicate lavender spikes, simplified composition legible at 48–64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent lavender watercolor wash #B8A9C9 at 20 percent, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## K5. Шалфей / луговая трава

**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small card emblem, a sprig of sage or meadow herb with small leaves, simplified composition legible at 48–64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent sage watercolor wash #8B9478 at 20 percent, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

## K6. Прорастающее семя

**Формат:** 512×512, прозрачный PNG.

**Prompt:**

> Small card emblem, a tiny seedling emerging from a seed pod with two young leaves, simplified composition legible at 48–64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent sage #8B9478 and ochre #C4A265 watercolor washes at 15 percent, isolated on transparent background, square composition, no frame, no text, no bright colors.

---

# 12. ИКОНКИ СОЦСЕТЕЙ И КОНТАКТОВ

Иконки должны быть не логотипами, а тонкими виньетками-метафорами. Набор можно адаптировать под фактические платформы.

## L1. Email

**Формат:** 256×256, прозрачный PNG.  
**Отображение:** 20–24 px.

**Prompt:**

> Small contact icon, a delicate envelope with a tiny botanical sprig on it, thin antique engraved line, soft warm graphite #3A3230, isolated on transparent background, square composition, minimal, legible at 20–24 pixels, no text, no brand logo, no bright colors.

---

## L2. Telegram-метафора

**Формат:** 256×256, прозрачный PNG.

**Prompt:**

> Small icon, a stylized paper plane drawn as a light engraved vignette, not a brand logo, thin warm graphite #3A3230 line, faint translucent dusty-rose watercolor wash #C9A9A0 at 10 percent, isolated on transparent background, square composition, minimal, legible at 20–24 pixels, no text, no bright colors.

---

## L3. Instagram-метафора

**Формат:** 256×256, прозрачный PNG.

**Prompt:**

> Small icon, a softly rounded square frame with a tiny flower inside, evoking a photo album without using a standard camera logo, thin antique engraved line, soft warm graphite #3A3230, faint translucent lavender watercolor wash #B8A9C9 at 10 percent, isolated on transparent background, square composition, minimal, legible at 20–24 pixels, no text, no bright colors.

---

## L4. YouTube-метафора

**Формат:** 256×256, прозрачный PNG.

**Prompt:**

> Small icon, a delicate rounded rectangle with a simple leaf-shaped play triangle inside, evoking video without using a standard brand logo, thin antique engraved line, soft warm graphite #3A3230, faint translucent terracotta watercolor wash #B07D6A at 10 percent, isolated on transparent background, square composition, minimal, legible at 20–24 pixels, no text, no bright colors.

---

# 13. НАВИГАЦИЯ, ОПЦИОНАЛЬНО

## M1. Боковая закладка

**Назначение:** вариант навигации «закладка в книге».  
**Формат:** 128×1024, прозрачный PNG.

**Prompt:**

> Thin vertical bookmark ribbon, soft dusty rose #C9A9A0 or gentle lavender #B8A9C9, subtle paper texture, slightly irregular edge, quiet and delicate, isolated on transparent background, tall narrow composition, no text, no shadow, no bright colors, no modern glossy UI style.

---

## ЧТО НЕ НУЖНО ГЕНЕРИРОВАТЬ КАК ИЛЛЮСТРАЦИИ

- фотографии двух портретов для секции 05 — это отдельные фото-материалы;
- рукописные пометки — они должны быть набраны живым рукописным шрифтом;
- названия секций, даты, номера глав, стрелки `→`, юридические подписи;
- кнопки, поля формы, состояния наведения — это интерфейсные элементы, а не картинки.

Если нужно, следующим шагом могу подготовить отдельные промпты для двух тёплых портретов-заглушек в секцию «О нас» или начать генерацию первой серии — например, титульной ветви и орнаментальных разделителей.