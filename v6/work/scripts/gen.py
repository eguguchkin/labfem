#!/usr/bin/env python3
import json, base64, http.client, time, sys, os, urllib.parse

SETTINGS = os.path.expanduser('~/.pi/agent/pi-image-gen/settings.json')
try:
    with open(SETTINGS, encoding='utf-8') as fh:
        KEY = json.load(fh)['customProviders']['selectel']['apiKey']
except (OSError, KeyError, ValueError) as exc:
    raise SystemExit(f'не удалось прочитать ключ Selectel из {SETTINGS}: {exc}') from None
URL = 'https://api.selectel.ru/aig/v1/images/generations'
OUT = '/home/pi/workspace/labfem/v6/work/img-raw'
try:
    os.makedirs(OUT, exist_ok=True)
except OSError as exc:
    raise SystemExit(f'не удалось создать каталог {OUT}: {exc}') from None

STYLE = ("STYLE ANCHOR: oil painting on canvas in the manner of 19th-century academic "
         "realism and Pre-Raphaelites (Bouguereau, Waterhouse), deep chiaroscuro, "
         "candlelit warm light from one side, rich impasto brushwork visible, aged "
         "varnish, palette limited to near-black deep emerald green (#0a2417), antique "
         "gold (#c8a24a), ivory (#ece3cf), warm flesh ochre (#e3c3a3), deep madder red "
         "(#7e2b26) as rare accent; sensual but chaste, no modern objects, no text, no "
         "watermark, no frame. ")
NEG_PAINT = ("photo, 3d render, cartoon, anime, flat vector, neon, bright saturated "
             "colors, white background, modern clothing, text, letters, watermark, "
             "signature, frame, border, plastic, glossy, deformed hands, extra limbs")

TASKS = {
 "velvet-tile": (1024, 1024,
   "Seamless tileable texture of luxurious deep emerald green velvet fabric, almost "
   "black dark green (#0a2417), soft pile nap with subtle directional sheen, gentle "
   "folds and pressure marks catching faint warm candlelight, macro view, no objects, "
   "uniform lighting, photographic macro of textile, very dark, muted, elegant. "
   "Tileable, no seams, no edges, no vignette.",
   "objects, people, visible pattern repeat, seams, borders, bright light, white, glossy plastic, satin shine"),
 "crackle-tile": (1024, 1024,
   "Seamless tileable craquelure texture of an ancient oil painting varnish: fine "
   "irregular crack network like dried lake bed, thin pale ivory cracks over mid-dark "
   "warm grey-brown ground (#4a4038), cracks sparse and delicate, evenly distributed, "
   "flat scan of old varnish surface, no image content, no figures, uniform exposure. "
   "Tileable, no seams, no vignette.",
   "painting content, faces, figures, bright colors, gold, heavy contrast, borders, text"),
 "gold-tile": (1024, 1024,
   "Seamless tileable texture of antique gold leaf gilding: burnished matte gold surface "
   "(#c8a24a) with subtle darker patina patches, tiny pits and brush burns, soft uneven "
   "sheen, macro scan, no objects, uniform light, warm. Tileable, no seams.",
   "coins, jewelry, objects, bright mirror shine, yellow neon, borders, text"),
 "parchment-tile": (1024, 1024,
   "Seamless tileable texture of aged warm parchment paper: ivory-cream (#ece3cf) with "
   "faint tea stains, fiber flecks and soft mottling, matte, evenly lit scan, very "
   "subtle, no writing, no objects. Tileable, no seams, no vignette.",
   "text, letters, drawings, dark stains, borders, torn edges, bright white"),
 "hero-full": (2048, 2048,
   STYLE + "Square composition designed for both wide and tall crops. Vertical zones: "
   "top sixth - dark emerald foliage, velvet drapery and a single candle glow at the "
   "left edge; middle - a young woman half-reclining among deep green velvet folds, "
   "head and face centered around one third of the height, eyes half-lidded toward the "
   "viewer, loose auburn hair, bare shoulders and collarbone catching warm candlelight, "
   "thin ivory linen slipping from one arm, a ripe peach resting near her hand; lower "
   "third - calm near-empty deep shadow of velvet folds, almost no detail, reserved as "
   "quiet dark space; sides - extendable dark foliage and drapery, no important detail "
   "near edges. Sensual, tender, chaste, museum quality.",
   NEG_PAINT + ", full frontal nudity, explicit, bright details in lower third, cluttered edges, centered symmetrical pose"),
 "hero-canvas": (1280, 1600,
   STYLE + "Composition: a young woman seen half-turned from behind among dense dark "
   "emerald foliage and ripe fruit - peaches and figs on a low branch - her bare shoulder "
   "and the curve of her back catching warm candlelight, loose auburn hair falling over "
   "one shoulder, head tilted down in quiet thought, eyes lowered; deep shadow swallows "
   "the lower third; a thin arc of gold leaf glows along the top edge like an altarpiece "
   "arch; vertical composition with empty dark space in the upper third for a title.",
   NEG_PAINT + ", full frontal nudity, explicit, facing camera fully, smile"),
 "fruit-ripe": (1024, 1280,
   STYLE + "Still life: ripe peaches, a split fig and one broken pomegranate with ruby "
   "seeds spilling, lying on deep emerald velvet cloth in near-darkness; dew drops on "
   "fruit skin, one peach cut open showing wet flesh; single candlelight from the left, "
   "gold rim light on the fruit edges; dark background, vertical composition.",
   NEG_PAINT + ", people, hands, plate, modern objects"),
 "cat-black": (1024, 1280,
   STYLE + "A majestic black cat, black as night, with amber eyes, seated in a calm regal "
   "pose, tail curled around its paws; behind it a round halo of burnished gold leaf; "
   "below - ivy leaves and a gilded branch on dark emerald ground; vertical composition, "
   "the cat slightly below center.",
   NEG_PAINT + ", white cat, kitten, cartoon, collar"),
 "pomegranate": (1024, 1280,
   STYLE + "A pomegranate broken open in a woman's cupped hands, seeds like rubies set in "
   "gold light; juice glistening; sleeves of dark green linen at the wrists; near-black "
   "emerald background; candlelight from above; vertical composition.",
   NEG_PAINT + ", face, full body, modern manicure"),
 "snake-skin": (1024, 1280,
   STYLE + "A slender dark snake coiling around a woman's bare forearm and letting go, "
   "its shed translucent skin left on a warm living stone beside her hand; emerald "
   "darkness around, one shaft of warm light on the stone; vertical composition, no face "
   "visible, only arm and hand.",
   NEG_PAINT + ", face, fear, horror, blood, fangs"),
 "thread-spindle": (1024, 1280,
   STYLE + "Close view of a woman's hands holding a wooden spindle, winding a thin gold "
   "thread that catches the light and leaves the frame upward; linen sleeve slipped from "
   "the shoulder; dark emerald velvet background; candlelight; vertical composition, no "
   "face.",
   NEG_PAINT + ", face, modern tools, scissors, bright colors"),
 "warm-stone": (1024, 1280,
   STYLE + "Two open palms resting on a large warm river stone, clay smudges on the "
   "fingers, a fold of raw linen beneath; the stone glows faintly with inner warmth; deep "
   "emerald darkness around; candlelight low from the side; vertical composition, no face.",
   NEG_PAINT + ", face, jewelry, modern manicure, bright background"),
 "hero-canvas-2": (1280, 1600,
   STYLE + "Composition: a young woman half-reclining on deep emerald velvet drapery "
   "among dark foliage, body in a soft S-curve, one strap of her ivory linen shift "
   "slipped from her shoulder, head tilted back, eyes closed in quiet pleasure, loose "
   "auburn hair spilling over her arm; a single ripe peach resting in the hollow of her "
   "collarbone, her fingertips lightly touching it; warm candlelight raking across her "
   "shoulder and throat; deep shadow below; thin arc of gold leaf along the top edge "
   "like an altarpiece arch; vertical composition with dark empty space in the upper "
   "third for a title; sensual, tender, chaste.",
   NEG_PAINT + ", full frontal nudity, explicit, open mouth, grin"),
 "feminity-figure": (1024, 1280,
   STYLE + "Composition: a young woman seated in three-quarter view in a dim interior, "
   "dark emerald drapery behind, a shallow bowl of ripe peaches and figs on her lap; she "
   "holds one split fig open in both hands at her chest, gaze lowered to it, lips "
   "slightly parted; bare shoulders, loose dark hair over one shoulder; candlelight "
   "from the left; vertical composition.",
   NEG_PAINT + ", full frontal nudity, explicit, still life without figure"),
 "optics-figure": (1024, 1280,
   STYLE + "Composition: head and shoulders of a young woman in half-turn holding an "
   "oval gilded hand mirror at her chest, the mirror glass turned slightly away catching "
   "a warm glow instead of a face; her eyes lowered toward it, dark hair loosely braided "
   "with a gold thread; deep emerald darkness around; candlelight; vertical composition.",
   NEG_PAINT + ", face inside mirror, double face, full frontal nudity"),
 "for-whom-figure": (1024, 1280,
   STYLE + "Composition: a young woman head and shoulders, eyes closed, face calm and "
   "open, holding a pale porcelain mask lowered in one hand at her side, the mask "
   "ribbons slipping through her fingers; bare shoulder, loose hair; a single warm shaft "
   "of light on her face; deep emerald darkness; vertical composition.",
   NEG_PAINT + ", mask on face, theatre crowd, full frontal nudity"),
 "feminity-figure-2": (1024, 1280,
   STYLE + "Composition: same scene - a young woman seated in three-quarter view in a "
   "dim interior, dark emerald drapery behind, a shallow bowl of ripe peaches and figs "
   "on her lap, one split fig held loosely in one hand at her chest; but her mood is "
   "alive and sensual: head lifted, chin raised, gaze meeting the viewer through "
   "half-lidded lashes, lips parted in a faint knowing half-smile, a warm flush on her "
   "cheeks and chest, hair slightly tousled as if she just turned; the fig is an "
   "offering, not a study - juice glistening, her other hand resting open on her thigh; "
   "posture languid and open, shoulders back; candlelight from the left warmer, catching "
   "the moisture of her lips and the hollow of her throat; vertical composition.",
   NEG_PAINT + ", frown, concentration, eating, biting, staring at fruit, grimace, "
   "still life without figure, full frontal nudity, explicit"),
 "circle-figure-3": (1024, 1280,
   STYLE + "Composition: a circle of five young women seated on low stools and cushions "
   "around a low wooden table with candles and a clay bowl, viewed from the front across "
   "the table; every woman faces the viewer (en face or three-quarter front), no one seen "
   "from behind; all young (twenties to thirties) and clearly distinct from one another - "
   "loose auburn hair, a dark braid over the shoulder, short black curls, honey-blonde "
   "waves, chestnut hair loosely pinned; each wearing only light semi-transparent ivory "
   "linen drapery slipping off the shoulders, bare shoulders, collarbones and arms "
   "glowing in candlelight, the thin fabric clinging softly and leaving much skin to the "
   "warm light, tasteful and chaste in the manner of classical academic painting; mood "
   "alive, warm and excited: soft laughter, flushed glowing faces, bright eyes, leaning "
   "toward one another, one raising a hand mid-gesture, one pouring from a small jug, "
   "one resting her chin on her palm; warm candlelight from the table center on faces, "
   "shoulders and hands; deep emerald darkness behind; intimate, sensual, joyful; "
   "vertical composition.",
   NEG_PAINT + ", elderly woman, old face, gray hair, heavy clothing, fully clothed, "
   "high collar, identical faces, twins, clones, mirrored poses, back turned, nape, "
   "modern room, electric light, explicit nudity, exposed breasts, nipples"),
 "circle-figure-2": (1024, 1280,
   STYLE + "Composition: a small circle of five women seated on low stools around a low "
   "wooden table with candles and a clay bowl, viewed from the front across the table: "
   "every woman faces the viewer (en face or three-quarter front), no one seen from "
   "behind; each clearly distinct - different age, face, hair: a young woman with loose "
   "auburn hair, a woman with a dark braid over her shoulder, an older woman with "
   "grey-streaked hair pulled back, a woman with short curly black hair, a woman with a "
   "pale headscarf; varied natural poses and gestures: one leaning forward with elbows "
   "on knees, one laughing softly with hand raised, one listening with tilted head and "
   "folded hands, one pouring from a small jug, one resting her chin on her palm; warm "
   "candlelight from the table center glowing on their faces and hands; deep emerald "
   "darkness behind; intimate, quiet, alive; vertical composition.",
   NEG_PAINT + ", identical faces, twins, clones, mirrored poses, back turned, nape, "
   "modern room, electric light, full frontal nudity"),
 "circle-figure": (1024, 1280,
   STYLE + "Composition: seen over the bare shoulder and head of a young woman in the "
   "foreground, a small circle of women seated on low stools around a low wooden table "
   "with candles and a clay bowl, all in deep shadow, warm candlelight on their faces "
   "and hands; the foreground woman's loose hair and shoulder catch the light; intimate, "
   "quiet; vertical composition.",
   NEG_PAINT + ", modern room, electric light, full frontal nudity"),
 "invite-figure": (1024, 1280,
   STYLE + "Composition: a young woman at a tall arched doorway drawing aside a heavy "
   "emerald velvet curtain with one hand, warm golden light from beyond spilling over "
   "her bare shoulder and cheek, her face turned to the viewer with a faint half-smile "
   "and lowered lashes; a folded letter with a wax seal in her other hand at her waist; "
   "vertical composition.",
   NEG_PAINT + ", modern door, electric light, full frontal nudity"),
 "water-dark": (1024, 1280,
   STYLE + "Composition: a young woman kneeling at the edge of dark still water at "
   "night, her whole figure reflected beneath her, one hand touching the surface making "
   "thin rings; water lilies and a pale bud nearby; moonless warm light from a hidden "
   "candle on the bank lighting her profile and shoulder; deep emerald and black "
   "palette; vertical composition.",
   NEG_PAINT + ", daylight, blue water, modern swimwear, full frontal nudity"),
 "fleuron": (512, 512,
   "A single small ornamental fleuron motif of antique gilded bronze: symmetrical "
   "leaf-and-bud flourish, burnished gold (#c8a24a) with dark patina in recesses, centered "
   "on pure black background, flat frontal view, no shadow, no other elements.",
   "text, frame, multiple motifs, bright background, photo"),
 "sym-mirror": (512, 512,
   "A single symbolic emblem in antique burnished gold (#c8a24a) with dark patina, flat "
   "frontal view, centered on pure black background, no shadow: an oval hand mirror with "
   "a short handle. Old-master gilded relief style, delicate, small.",
   "text, frame, photo, bright background, multiple objects"),
 "sym-snake": (512, 512,
   "A single symbolic emblem in antique burnished gold (#c8a24a) with dark patina, flat "
   "frontal view, centered on pure black background, no shadow: a snake forming a loose "
   "circle, head over tail. Old-master gilded relief style, delicate, small.",
   "text, frame, photo, bright background, multiple objects"),
 "sym-brush": (512, 512,
   "A single symbolic emblem in antique burnished gold (#c8a24a) with dark patina, flat "
   "frontal view, centered on pure black background, no shadow: a painter's brush with "
   "one thick stroke of gold paint beneath it. Old-master gilded relief style, delicate, "
   "small.",
   "text, frame, photo, bright background, multiple objects"),
 "sym-thread": (512, 512,
   "A single symbolic emblem in antique burnished gold (#c8a24a) with dark patina, flat "
   "frontal view, centered on pure black background, no shadow: a wooden spindle with a "
   "winding thread. Old-master gilded relief style, delicate, small.",
   "text, frame, photo, bright background, multiple objects"),
}

def https_post_json(url, body, headers, timeout=180):
    """POST по явному HTTPS-соединению (схема гарантирована типом соединения)."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != 'https':
        raise SystemExit(f'небезопасная схема URL: {url}')
    conn = http.client.HTTPSConnection(parts.hostname, parts.port or 443, timeout=timeout)
    try:
        conn.request('POST', parts.path or '/', body=body, headers=headers)
        with conn.getresponse() as resp:
            return json.load(resp)
    finally:
        conn.close()


def gen(name, size, prompt, neg):
    body = json.dumps({"model": "qwen/qwen-image-3", "prompt": prompt,
                       "negative_prompt": neg, "size": f"{size[0]}x{size[1]}"}).encode()
    for attempt in range(1, 7):
        try:
            data = https_post_json(URL, body, {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {KEY}'})
            b64 = data['data'][0]['b64_json']
            with open(f'{OUT}/{name}.png', 'wb') as fh:
                fh.write(base64.b64decode(b64))
            print(f'OK {name}', flush=True)
            return True
        except Exception as e:
            print(f'.. {name} attempt {attempt}: {e}', flush=True)
            time.sleep(attempt * 6)
    print(f'FAIL {name}', flush=True)
    return False

if __name__ == '__main__':
    names = sys.argv[1:] or list(TASKS)
    for n in names:
        w, h, p, neg = TASKS[n]
        gen(n, (w, h), p, neg)
