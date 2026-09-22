"""Единый манифест графических ассетов «Лаборатории феминности».

Один источник правды для gen.py (генерация) и ink.py (вырезание фона).
Промпты — из graphics.md; прозрачность не просим у модели (qwen отдаёт растр
без альфы), вместо этого требуем плоский фон #F5F0E8 и режем его в ink.py.
"""

BG = "#F5F0E8"

TAIL = (
    " Isolated subject on a perfectly flat solid warm milky paper background color "
    + BG
    + " filling the whole canvas edge to edge, background completely empty and uniform."
    " Avoid: pure white, pure black, neon or oversaturated colors, glossy 3D render,"
    " plastic texture, flat modern vector icon, harsh digital gradients, CSS-like drop"
    " shadow, heavy baroque ornaments, crowns, luxury wedding style, esoteric symbols,"
    " moons, stars, mandalas, tarot, occult, text, letters, numbers, watermark, logo,"
    " brand signs, stock photo, smiling models, aggressive marketing UI, thick cartoon"
    " contours, childish illustration, coffee stains, dirt, grunge, torn paper,"
    " vignette, frame around subject, colored backdrop."
)

V, S, W = "1024x1536", "1024x1024", "1536x1024"

# id: (size, target_width_px, prompt без хвоста[, свой хвост вместо TAIL])
ASSETS: dict[str, tuple] = {
    # --- орнаментика ---
    "b1-divider": (W, 760, "Horizontal botanical divider, one slightly uneven hairline in warm ochre #C4A265 at 50 percent opacity stretching across the full width, a small six-petal flower with two tiny leaves at the center, line tapers gracefully toward both ends, antique pen-drawn engraving, warm graphite #3A3230 and ochre, very wide low horizontal composition centered in the frame, no baroque curls, no bright colors."),
    "b2-dots": (S, 220, "Three tiny five-petal flowers in a horizontal row, separated by small delicate dots, fine antique etched line, warm graphite #3A3230, subtle stipple centers, minimal book ornament, wide low horizontal composition centered in the frame, no bright colors."),
    "b5-corner": (S, 170, "One delicate corner ornament placed in the upper left corner, a thin botanical sprig with two small leaves and a tiny bud curving along a barely visible right angle, antique pen-drawn line, warm graphite #3A3230 and soft ochre #C4A265, minimal and refined, not baroque, no full frame, no bright colors."),
    "b7-marginal": (V, 110, "Tiny marginal botanical sprig with one leaf and a small closed bud, delicate antique etched line, sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, hand-colored slightly irregular, vertical composition, no bright colors."),
    "b8-endpiece": (W, 400, "Small book end-piece, a short flowering branch with two leaves and one falling petal, horizontal composition centered in the frame, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, aged book illustration, no bright colors."),
    "b10-petal": (S, 120, "Single dried flower petal, translucent and slightly curled, delicate irregular edges, fine etched contour, sepia #6B5B4E with faint dusty-rose watercolor wash #C9A9A0 at 20 percent, hand-colored slightly beyond the contour, square composition, no bright colors."),
    "b11-favicon": (S, 128, "Minimal emblem, a simplified apple-blossom twig with one small flower and one bud, fine antique engraved line but clean and bold enough to remain legible at 16 pixels, warm graphite #3A3230, square composition, no circle frame, no bright colors, no excessive detail."),

    # --- секция 02 ---
    "d1-peon": (V, 540, "A complex peony in full bloom with one side bud and several leaves, antique botanical engraving, fine slightly uneven etched line, delicate cross-hatching and stippling, scientific accuracy with poetic softness, warm graphite #3A3230 and sepia #6B5B4E, translucent hand-colored watercolor wash dusty rose #C9A9A0 at 20-25 percent, faint lavender #B8A9C9 at 10 percent in shaded areas, wash slightly irregular and barely beyond contour, aged book illustration, vertical composition, no rose cliche, no bright colors, no gloss."),
    "d2-figure": (V, 430, "A soft faceless female figure seen from behind, gentle engraved silhouette, simple shawl, holding a peony branch, archetypal and poetic, age ambiguous, no facial features, fine antique etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and lavender #B8A9C9 washes at 15 percent, aged book illustration, vertical composition, no stock-photo realism, no bright colors."),

    # --- секция 03 ---
    "e1-braid": (W, 800, "Four thin living lines interweaving into a delicate braid-like botanical pattern, each line subtly different but visually equal, small leaves and tiny buds along the lines, composition like a quiet scientific diagram, antique engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, very faint watercolor accents dusty rose #C9A9A0, lavender #B8A9C9, sage #8B9478 and ochre #C4A265 at 10-15 percent, horizontal composition centered in the frame, no esoteric symbols, no bright colors."),
    "e2-psy": (S, 140, "Small emblem of an antique magnifying glass held over a single leaf with fine veins, scientific but poetic, antique botanical engraving, thin slightly uneven etched line, delicate stippling, warm graphite #3A3230 and sepia #6B5B4E, faint translucent sage watercolor wash #8B9478 at 15 percent, square composition, no modern icon style, no bright colors."),
    "e3-myth": (S, 140, "Small emblem of a simple antique urn with a delicate vine and one small flower curling from it, myth as an old story, antique engraving, thin slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent lavender watercolor wash #B8A9C9 at 15 percent, square composition, no classical faces, no esoteric symbols, no bright colors."),
    "e4-art": (S, 140, "Small emblem of an engraver's nib or fine pen beside a half-drawn flowering sprig, the idea of line, craft and image, antique etching style, thin slightly uneven living line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, square composition, no palette cliche, no bright colors."),
    "e5-life": (S, 140, "Small emblem of a simple teacup, an open blank notebook and a pressed petal, lived experience and quiet conversation, antique engraving, thin slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent terracotta #B07D6A and ochre #C4A265 watercolor wash at 15 percent, square composition, no legible text, no modern objects, no bright colors."),

    # --- секция 04 ---
    "f1-window": (V, 400, "A female silhouette seen from behind near a window, age ambiguous, no facial features, soft contemplative posture, one hand lightly near the frame, timeless simple clothing, antique engraving, fine slightly uneven etched line, delicate hatching suggesting warm light without glow, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, vertical composition, no interior clutter, no bright colors."),
    "f2-hands": (S, 340, "Two cupped female hands holding a single seed or dried petal, gesture of care and attention, no faces, age ambiguous, fine antique engraving, slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose watercolor wash #C9A9A0 at 15 percent, square composition, no jewelry, no bright colors."),
    "f3-touch": (W, 560, "A slender female hand reaching to touch a flowering branch, only hand and branch, no face, delicate antique etched line, fine hatching and stippling, warm graphite #3A3230 and sepia #6B5B4E, faint translucent sage #8B9478 and dusty-rose #C9A9A0 watercolor washes at 15 percent, horizontal composition centered in the frame, no bright colors."),
    "f4-shawl": (V, 400, "A seated female figure seen from behind, wrapped in a soft shawl, head slightly lowered, simple wooden chair, quiet introspection, age ambiguous, no facial features, antique engraving, fine slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent lavender watercolor wash #B8A9C9 at 15 percent, vertical composition, no dramatic shadows, no bright colors."),
    "f5-table": (W, 580, "Two faceless female silhouettes sitting across a small round table with two simple teacups, calm conversation, age ambiguous, timeless simple clothing, antique engraving, thin living line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and ochre #C4A265 watercolor washes at 15 percent, horizontal composition centered in the frame, no modern cafe details, no bright colors."),

    # --- секция 05 ---
    "g1-lavender": (V, 120, "A small lavender sprig with two or three delicate flower spikes, marginal botanical note, fine antique etched line, sepia #6B5B4E, translucent lavender watercolor wash #B8A9C9 at 20 percent, hand-colored slightly irregular, vertical composition, no bright colors."),

    # --- секция 06 ---
    "h1-diary": (W, 460, "A small open antique diary with blank aged pages, a dried leaf tucked between them and a thin ribbon bookmark, no legible text, fine antique engraving, slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent terracotta watercolor wash #B07D6A at 15 percent, horizontal composition centered in the frame, no bright colors."),

    # --- секция 07 ---
    "i1-drawing": (W, 600, "Female hands drawing in an open blank notebook with a thin pencil, a small flower resting nearby, no faces, age ambiguous, antique engraving, fine slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and ochre #C4A265 watercolor washes at 15 percent, horizontal composition centered in the frame, no legible text, no modern objects, no bright colors."),
    "i2-tea": (S, 340, "A simple ceramic teacup and saucer with one delicate curl of steam, a dried petal beside it, antique engraving, thin slightly uneven etched line, fine hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent terracotta watercolor wash #B07D6A at 15 percent, square composition, no bright colors."),
    "i3-chairs": (W, 600, "A circle of six simple wooden chairs around a small low table with a single flower in a plain vase, slightly elevated view, no people, antique engraving, fine slightly uneven etched line, delicate hatching, warm graphite #3A3230 and sepia #6B5B4E, faint translucent sage watercolor wash #8B9478 at 15 percent, horizontal composition centered in the frame, no modern furniture, no bright colors."),

    # --- секция 08 ---
    "j1-final": (W, 440, "Small closing botanical motif, a short apple-blossom branch with one open flower, one bud and one falling petal, lighter and more delicate than a title illustration, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, horizontal composition centered in the frame, no bright colors."),
    "j2-envelope": (S, 240, "A delicate envelope or guest-book page with a tiny botanical sprig tucked under its flap, no legible text, fine antique engraving, slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, faint translucent dusty-rose #C9A9A0 and ochre #C4A265 watercolor washes at 15 percent, square composition, no wax seal as central element, no bright colors."),

    # --- эмблемы карточек ---
    "k1-apple": (S, 140, "Small card emblem, one apple-blossom sprig with a single open flower and one bud, simplified composition legible at 48-64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, square composition, no bright colors."),
    "k2-peon-bud": (S, 140, "Small card emblem, a single peony bud with two leaves, simplified composition legible at 48-64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent dusty-rose watercolor wash #C9A9A0 at 20 percent, square composition, no bright colors."),
    "k3-iris": (S, 140, "Small card emblem, one iris flower with slender leaves, simplified composition legible at 48-64 pixels, antique botanical engraving, fine slightly uneven etched line, warm graphite #3A3230 and sepia #6B5B4E, translucent lavender watercolor wash #B8A9C9 at 20 percent, square composition, no bright colors."),
}

# уже сгенерировано отдельно, но держим в манифесте для пересборки
ASSETS["c1-title"] = (V, 520, "A single branch of blossoming apple tree with three open blossoms, two buds and delicate leaves, diagonal composition, antique botanical engraving and etching, fine slightly uneven living line, delicate hatching and stippling, scientific accuracy with poetic softness, warm graphite #3A3230 and sepia #6B5B4E ink, translucent hand-colored watercolor wash dusty rose #C9A9A0 at 20 percent on petals only, wash slightly irregular and barely beyond contour, aged book illustration, vertical composition, no gloss, no heavy shadow.")

# портреты авторов: гравюра с сохранением сходства с фото из raw/.
# Общий TAIL не годится (в нём "smiling models"), поэтому свой хвост четвёртым элементом.
PTAIL = (
    " Plain flat uniform warm milky paper background #F5F0E8 filling the whole canvas."
    " Avoid: photographic realism, glossy photo texture, color photograph look, neon or"
    " oversaturated colors, heavy baroque ornaments, text, letters, numbers, watermark,"
    " logo, frame around subject, vignette, pure white, pure black, thick cartoon"
    " contours, childish illustration."
)

ASSETS["p1-veronika"] = (V, 640, "Portrait of one specific real woman taken from the reference photo. Preserve her exact identity and facial likeness above all: oval face, warm open smile with visible teeth, dark brown eyes, full straight-cut fringe covering the brow, very long straight dark chestnut hair falling over the shoulders, age about thirty five. Change only the medium: render her as an antique book engraving portrait, head and shoulders, simple timeless light blouse, fine antique etching, thin slightly uneven living line, delicate hatching and stippling, warm graphite #3A3230 and sepia #6B5B4E ink, faint translucent dusty-rose watercolor wash #C9A9A0 at 12 percent, aged book illustration, vertical composition, clean plain paper background without any hatched or textured rectangle, no frame.", PTAIL, {"lossy": 88})

ASSETS["p2-polina"] = (V, 640, "Portrait of one specific real woman taken from the reference photo. Preserve her exact identity and facial likeness above all: soft round face, calm closed-lip half smile, large light grey-green eyes, straight natural brows, full lips, long wavy light-brown hair well below the shoulders with a side part, thin pendant necklace, age about thirty. Change only the medium: render her as an antique book engraving portrait, head and shoulders, simple timeless dark blouse, fine antique etching, thin slightly uneven living line, delicate hatching and stippling, warm graphite #3A3230 and sepia #6B5B4E ink, very faint evenly diffused lavender watercolor wash #B8A9C9 at 10 percent, aged book illustration, vertical composition, clean plain paper background without any hatched or textured rectangle, no frame.", PTAIL, {"lossy": 88})

# --- фактуры бумаги (режет tools/paper.py, не ink.py: лист здесь ровный целиком) ---
# Общий TAIL не годится: он запрещает coffee stains и vignette, а нам нужны
# благородные следы возраста. Хвост свой, «грязь» по-прежнему под запретом.
TTAIL = (
    " Flat even diffuse lighting without any shadow or highlight, the whole canvas filled"
    " edge to edge with a uniform warm milky paper tone " + BG + ", very high key, quiet"
    " and delicate. Avoid: objects, subjects, people, hands, text, letters, numbers,"
    " drawings, illustration, frame, border, vignette, pure white, pure black, neon or"
    " oversaturated colors, glossy 3D render, plastic, harsh digital gradients, dirt,"
    " grime, grunge, mold, dust, coffee rings, tears, burnt edges, watermark, logo,"
    " stock photo."
)

ASSETS["t1-paper"] = (S, 1024, "All-over seamless surface texture of a sheet of handmade cotton rag paper seen very close: fine chaotic plant fibers, tiny pulp flecks and a faint cloud-like unevenness of the pulp, tone variation within three percent of the base cream, no subject and no composition, the texture continues past every edge.", TTAIL, {"lossy": 82})

PAPER = ("t1-paper", "t2-bloom")  # их обрабатывает paper.py, ink.py их пропускает

ASSETS["t2-bloom"] = (V, 1024, "Very faint noble age marks on an old book page: two or three soft irregular water blooms with barely visible tide lines, a handful of tiny pale foxing speckles, gentle uneven tone near the edges of the sheet, every mark no darker than five percent of the paper tone, no subject and no composition, the marks spread loosely over the whole page.", TTAIL, {"lossy": 82})

# референсы для image-to-image (портреты авторов)
REFS = {
    "p1-veronika": "raw/veronika-art-2.png",
    "p2-polina": "raw/polina-art-2.png",
}
