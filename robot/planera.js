// Planerar annonserna. Stilarna bygger på referensbilderna och går att ändra här.
const stilar = [
  { namn: 'Mork sten', beskrivning: 'resting on rough dark volcanic rock / black stone, dramatic directional side light, deep shadows, dark charcoal gradient background' },
  { namn: 'Regn och mossa', beskrivning: 'resting on a wet mossy rock outdoors, fine raindrops and water beads on the rock, overcast moody nordic light, shallow depth of field' },
  { namn: 'Fargmatchad studio', beskrivning: 'seamless studio backdrop in a smooth gradient that matches the product color, soft top light, subtle reflection on the floor, minimal and premium' },
  { namn: 'Sockel', beskrivning: 'standing on a raw concrete or stone pedestal block, minimal studio set, soft daylight from the side, gentle long shadows' },
  { namn: 'Asfalt', beskrivning: 'lying on dark grainy asphalt with tiny pebbles, low raking light, gritty urban texture, cinematic contrast' },
  { namn: 'Sprucken jord', beskrivning: 'lying on dry cracked earth / desert ground, warm golden hour light, earthy tones, strong texture' },
  { namn: 'Linne', beskrivning: 'lying on softly draped off-white linen fabric, bright natural window light, airy, calm and clean' },
  { namn: 'Morkt traa', beskrivning: 'lying on a dark walnut wood desk, warm moody evening light, a hint of a keyboard blurred in the background' },
];
const annonsstil = 'Premium, moody product photography in the style of high-end phone case brands (Nudient, Native Union, Mous): natural or color-matched textures, dramatic directional light, rich realistic shadows, minimal composition with lots of negative space.';
const set = $('Inställningar').first().json;
const filer = $('Hitta robotfiler').all().map(i => i.json);
const id = {}; for (const f of filer) id[f.name] = f.id;
const nycklar = [...new Set(filer.map(f => (f.name.match(/^A_bild_(.+)\.png$/) || [])[1]).filter(Boolean))]
  .filter(k => id[`A_mask_${k}.png`] && id[`A_topp_${k}.png`] && id[`C_bild_${k}.png`] && id[`C_mask_${k}.png`] && id[`C_topp_${k}.png`]);
const bFiler = filer.filter(f => /^B_bild_.+_(L|D)\.jpg$/.test(f.name));
const text = (typ, ton, kat) => filer.filter(f => f.name.startsWith(`R_${typ}_${ton}_${kat}_`));
const kategori = k => (k[0] === 's' ? 's' : 'p'); // s = skal, p = övriga produkter
if (!nycklar.length) throw new Error('Hittar inga robotfiler. Välj mappen Chat Robotfiler i steget Hitta robotfiler.');
const slump = a => a[Math.floor(Math.random() * a.length)];
const datum = new Date().toISOString().slice(0, 10);
const vikt = { A: Number(set.andel_A ?? 0.5), B: bFiler.length ? Number(set.andel_B ?? 0.25) : 0, C: Number(set.andel_C ?? 0.25) };
const valjTyp = () => { let r = Math.random() * (vikt.A + vikt.B + vikt.C); for (const t of ['A', 'B', 'C']) { if ((r -= vikt[t]) < 0) return t; } return 'A'; };
const ut = [];
for (let i = 0; i < set.antal; i++) {
  const typ = valjTyp();
  const nr = String(i + 1).padStart(2, '0');
  if (typ === 'B') {
    const f = slump(bFiler); const ton = f.name.match(/_(L|D)\.jpg$/)[1]; const kb = f.name.match(/^B_bild_(.+)_(L|D)\.jpg$/)[1];
    ut.push({ json: { typ, namn: `reborn-${datum}-${nr}-foto.jpg`, ids: { bild: f.id, text: slump(text('B', ton, kategori(kb))).id } } });
    continue;
  }
  const k = slump(nycklar); const stil = stilar[Math.floor(Math.random() * stilar.length)];
  const ton = Math.random() < 0.6 ? 'D' : 'L';
  const toppTon = ton === 'D' ? 'The upper 25% of the image must be calm, simple and fairly dark so a white headline is easy to read.' : 'The upper 25% of the image must be calm, simple and light so a black headline is easy to read.';
  const prompt = typ === 'A'
    ? `${annonsstil}\nThe image contains a real product photo of a premium phone accessory. Keep the product exactly as it is: do not change its shape, color, texture, logo, buttons, camera frame, position, size or angle. Only create the surroundings in the transparent areas.\nScene: the product is ${stil.beskrivning}. Match the existing camera angle and perspective so the product sits naturally in the scene with realistic contact shadows and reflections.\n${toppTon} Keep the bottom 8% calm for a small logo.\nIMPORTANT: no text, letters, numbers, logos or watermarks anywhere. Do not add other phones or products.`
    : `${annonsstil}\nThis is a real product photo placed in the middle of a tall 9:16 canvas. Extend the photo naturally into the transparent areas above and below: continue the same surface, background, lighting and colors seamlessly so it looks like one single photograph. Do not change anything inside the existing photo and do not change the product.\n${toppTon} Keep the bottom 8% calm for a small logo.\nIMPORTANT: no text, letters, numbers, logos or watermarks anywhere. Do not add other phones or products.`;
  ut.push({ json: {
    typ, namn: `reborn-${datum}-${nr}-${typ === 'A' ? stil.namn.toLowerCase().replace(/[^a-z0-9]+/g, '-') : 'story'}.png`,
    prompt, modell: set.modell, kvalitet: set.kvalitet, storlek: typ === 'A' ? '1024x1280' : '1008x1792',
    ids: { bild: id[`${typ}_bild_${k}.png`], mask: id[`${typ}_mask_${k}.png`], topp: id[`${typ}_topp_${k}.png`], text: slump(text(typ, ton, kategori(k))).id },
  }});
}
return ut;
