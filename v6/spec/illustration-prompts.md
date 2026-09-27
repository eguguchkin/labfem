# labfem v6 — иллюстрации в стиле кватроченто (ревизия стиля, 2026-09-27)

Новый стиль всех живописных иллюстраций: раннее итальянское Возрождение / флорентийское
кватроченто (Боттичелли, Гирландайо) + влияние французских милфлёр-гобеленов («Дама
с единорогом»). Темпера на дереве, линейная тонкость рисунка, фарфоровая кожа с румянцем,
золотые плетёные причёски с жемчугом, декоративная флора на глубоком тёмном фоне.
Палитра остаётся фирменной: изумрудная глубь #0a2417, золото #c8a24a, слоновая кость
#ece3cf, приглушённая марена (розы) #7e2b26, патиновая зелень листвы.

Не перерисовываются (решение агента): портреты авторов (polina/veronika — живые люди,
сепия-дуотон), медальоны-символы 03 (sym-*), золото-орнаменты (fleuron), тайлы текстур.
Кракелюр снят из CSS; бархат затемнён на 15% (токены ×0.85 + вуаль .2→.32).

Сенсуальность: полупрозрачная сорочка/спущенный ворот, открытые плечи и ключицы,
«сексуально, но не пошло» — без явной наготы (мягче для модерации, точнее по ТЗ).

---

## Якорь стиля (STYLE — подставляется в каждый промпт)

```
early Italian Renaissance tempera on wood panel, Florentine quattrocento, Sandro
Botticelli style, elegant linear draughtsmanship, delicate porcelain skin with soft
rose blush, long elaborately braided golden hair adorned with pearls and ribbons,
decorative botanical motifs — roses, lilies, myrtle, ivy — rendered in fine gold-touched
detail, millefleur Flemish-French tapestry influence, matte mineral pigments, subtle
gold-leaf highlights, deep dark emerald-black background (#0a2417), mystical medieval
French tapestry atmosphere
```

## Негатив (NEG — подставляется в каждый промпт)

```
photograph, photorealism, 3d render, digital smooth skin, modern clothing, modern
interior, text, letters, signature, watermark, frame border, oversaturated colors,
oil painting impasto, thick brush strokes, extra fingers, missing fingers, deformed
hands, deformed face, asymmetrical eyes, lowres, jpeg artifacts
```

---

## Сюжеты по секциям

### 01 hero — «женщина, нюхающая цветы» (2048×2048, квадрат → кропы land/port)

Композиция под верстку: лицо в верхней трети (профиль/полупрофиль), нижняя треть —
спокойная тёмная зелень без ярких пятен (текст поверх), края — растяжимая листва.

```
{STYLE}. A sensual young woman in profile three-quarter view, smelling a pale rose
held to her face with slender elegant hand, eyes closed, serene expression, cascading
golden braided hair with pearls and ribbons flowing down, translucent ivory chemise
slipping from one shoulder, bare shoulders and collarbones, surrounded by lush dark
greenery with pale roses and ivy on deep emerald-black background. Face in the upper
third of the composition, lower third dissolves into calm dark foliage without bright
details, candle-warm glow on cheekbone and shoulder
```
size: 2048x2048

### 02 feminity — «чаша плодов» (1280×1600 → 800×1000)

Смысл секции: женское естество — телесность, изобилие, право на желание.

```
{STYLE}. A sensual young woman with a live inviting gaze at the viewer, offering a
shallow ceramic bowl of ripe peaches and figs, one halved fig in her other hand near
her chest, translucent ivory chemise with gold-embroidered neckline slipping from one
shoulder, bare shoulders and collarbones, golden braided hair with pearls, dark
emerald-green interior with dark foliage and a few pale roses behind her
```
size: 1280x1600

### 03 optics — «зеркальце с тёплым светом» (1280×1600 → 800×1000)

Смысл: четыре линзы, зеркало как инструмент взгляда; в стекле — свет, не лицо.

```
{STYLE}. Head and shoulders of a young woman in three-quarter turn, holding a small
oval gilded hand mirror at her chest, in the mirror glass only a warm golden glow of
light, no reflection, eyes downcast with quiet attention, golden braided hair with
pearls and ribbons, translucent chemise, bare shoulders, deep dark emerald background
with delicate dark botanical ornaments and a few ivy leaves
```
size: 1280x1600

### 04 for-whom — «крольчонок на пороге» (1280×1600 → 800×1000)

Смысл: порог, уязвимость, «ничего не нужно доказывать»; кролик из разрешённого списка
животных — трепет и доверие (гобелен «Дама с единорогом»).

```
{STYLE}. A young woman with closed eyes and a tender guarded expression, holding a
small white rabbit against her chest with both slender hands, rabbit calm and trusting,
translucent ivory chemise with open neckline, bare shoulders and collarbones, golden
braided hair with pearls, deep dark emerald background with dark leaves and a few pale
roses, quiet threshold atmosphere
```
size: 1280x1600

### 06 карточки (5 шт, 1280×1600 → 800×1000)

**1. cat-black — «кошка, которая живёт в тебе» (флагман)**

```
{STYLE}. A regal black cat with luminous amber eyes sitting in the arms of a young
woman, cat calm and dignified, woman in translucent ivory chemise with bare shoulders,
golden braided hair, a circular halo of gold leaf behind the cat, dark ivy and a
gilded branch around, deep emerald-black background, French medieval tapestry mood
```

**2. pomegranate — «granatum: зерно и кожура»**

```
{STYLE}. A young woman holding a split pomegranate in slender elegant hands, ruby
pomegranate seeds glistening like jewels, one hand opening the fruit, translucent
ivory chemise slipping from one shoulder, bare collarbones, golden braided hair with
pearls, pomegranate branches with dark red blossoms on deep emerald-black background,
Botticelli Primavera mood
```

**3. thread-spindle — «нить и веретено»**

```
{STYLE}. Close composition of a young woman's slender hands spinning golden thread
on a medieval distaff spindle, fine glowing thread winding through her fingers,
sleeves of a translucent ivory chemise slipping from shoulders, foreground millefleur
tapestry ground with small flowers and leaves, deep dark emerald background, medieval
French tapestry atmosphere
```

**4. water-dark — «тёмная вода»**

```
{STYLE}. A young woman kneeling at the edge of dark still water at night, touching
the water surface with one hand making soft circles, her faint reflection in the
water, white water lilies near the shore, a single lit candle on the bank, hair loose
and golden, translucent ivory chemise, deep emerald-black nocturne, mystical quiet
tapestry mood
```

**5. snake-skin — «змея, сброшенная кожа»**

```
{STYLE}. A slender snake coiling gently around a young woman's bare forearm, she
looks at it with calm attention, a shed snake skin lying on a stone nearby, translucent
ivory chemise off one shoulder, golden braided hair with pearls, dark emerald garden
background with ivy and dark leaves, mystical medieval tapestry mood
```

### АНТРАКТ — «звезда над ручьём» (1280×1600 → 1460×1825 кроп-ресайз)

Чистая живописная пауза без текста; элемент композиции из референса 4 — светящаяся
звезда в ладонях; «женщина у ручья» из примеров сюжетов.

```
{STYLE}. A young woman kneeling beside a dark forest stream at night, holding a small
glowing golden star cupped in her slender hands above the water, starlight reflecting
on the stream surface and on her face, long loose golden hair, translucent ivory
chemise slipping from one shoulder, bare shoulders, dark emerald forest depth around
with delicate dark leaves and a few pale flowers, mystical quiet medieval tapestry
nocturne
```

### 07 circle — «хоровод» (1280×1600 → 800×1000)

Смысл: круг, равенство, без сцены и эксперта.

```
{STYLE}. Five young women dancing in a circle holding hands in a night garden, like
Botticelli graces, joyful faces lit by candlelight, light translucent linen draperies
with bare shoulders and arms in classical measure, golden and chestnut braided hair
adorned with flowers, low stone table with lit candles and a clay bowl in the center,
dark emerald garden with ivy and roses around, medieval tapestry round dance mood
```

### 08 invite — «дверь, письмо и единорог» (1280×1600 → 800×1000)

Сюжет прежний (дверь, письмо с печатью) + единорог из разрешённого списка — гобелен
«Дама с единорогом».

```
{STYLE}. A sensual young woman opening a tall arched garden door, one hand lifting a
heavy dark emerald curtain, warm golden light from beyond the door on her shoulder and
cheek, in her other hand a folded letter with a dark red wax seal, a white unicorn with
a golden horn standing calmly beside her at the threshold, translucent ivory chemise
with open neckline, bare shoulders, golden braided hair with pearls, mystical medieval
French tapestry mood
```

---

## Постобработка (post.py, ревизия v7)

- paint/cards: resize (800,1000) LANCZOS → grain_vignette → webp q82; без inset-кропов
  (t2i-оригиналы чистые по краям).
- hero: v7-hero-1 2048² — ЗЕРКАЛИМ (в источнике лицо слева, тексту нужен правый край),
  затем кропы land (0,40,1600,940) — лицо ~70–86% ширины, макушка с полем 60px — и
  port (414,0,1566,2048) — лицо ~75% ширины.
- антракт: v7-interlude-1 1280×1600 → 1460×1825, лёгкий UnsharpMask(2.0/55) без
  контраста (t2i не мылит, в отличие от i2i).
- og-cover: кроп v7-interlude-1 1200×630.
- Имена файлов ассетов НЕ меняются — HTML/CSS не трогаем (правки только alt-тексты).

---

## Итоги генерации v7 (2026-09-27, qc-вердикты)

24 кандидата (12 сюжетов × 2) + перегенерация spindle. Отбраковки: forwhom-1
(латинская надпись «PAX IN SILENTIO» на книге), circle-2 (картуш «VIRET SEMPER» +
пропорции ребёнка), invite-2 (надпись «HORTUS CONCLUSUS» на арке + рог прошивает
щёку), spindle-1/2 v7 (лица обрезаны верхним краем — перегенерация с «head and face
fully visible in upper third»).

Победители: feminity-1, optics-2, forwhom-2, cat-2, pomegranate-1, water-2,
snake-2, interlude-1, circle-1, invite-1, spindle — v7b-spindle-2 (перегенерация:
лён на дистафе фактурный, пальцы на веретене естественные), hero — v7-hero-1
(закрытый глаз, буквально «нюхает розу»; Боттичелли-профиль).

Ручная QC-методика: зум-кропы 520px по хватаам (пальцы/кисти читаются — «варёжки»
отбраковываются), зум-кропы лиц, контроль правого края на артефакты рам.
Правило «no text»: любой отрендеренный латинский текст = отбраковка.
