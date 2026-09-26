#!/usr/bin/env python3
import json, base64, time, sys, os, urllib.request

SETTINGS = os.path.expanduser('~/.pi/agent/pi-image-gen/settings.json')
KEY = json.load(open(SETTINGS))['customProviders']['selectel']['apiKey']
URL = 'https://api.selectel.ru/aig/v1/images/generations'
OUT = '/tmp/lab6/raw'
os.makedirs(OUT, exist_ok=True)

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

def gen(name, size, prompt, neg):
    body = json.dumps({"model": "qwen/qwen-image-3", "prompt": prompt,
                       "negative_prompt": neg, "size": f"{size[0]}x{size[1]}"}).encode()
    for attempt in range(1, 7):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {KEY}'})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.load(r)
            b64 = data['data'][0]['b64_json']
            open(f'{OUT}/{name}.png', 'wb').write(base64.b64decode(b64))
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
