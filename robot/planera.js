// ChatGPT-delen: gör råa AI-miljöer runt riktiga skal (ingen text). Claude designar annonserna efteråt.
const stilar = [
  { namn: 'Mork studio', beskrivning: 'standing in front of a seamless dark charcoal-to-black studio gradient backdrop, soft top light, subtle reflection on the floor' },
  { namn: 'Ljus studio', beskrivning: 'standing in front of a seamless light grey studio backdrop, soft diffused daylight, soft natural shadow' },
  { namn: 'Fargmatchad', beskrivning: 'in front of a seamless studio gradient backdrop in a deep tone that matches the product color, soft rim light from behind' },
  { namn: 'Stenblock', beskrivning: 'resting on a raw dark stone block, dark gradient background, dramatic directional side light' },
  { namn: 'Betong', beskrivning: 'resting on a light grey concrete block, minimal studio set, soft daylight from the side' },
  { namn: 'Podium', beskrivning: 'standing on a round dark glossy podium, deep plum background, dramatic soft light' },
  { namn: 'Vat sten', beskrivning: 'resting on a dark wet rock outdoors with fine water droplets, overcast moody light, shallow depth of field' },
];
const annonsstil = 'Premium product photography like high-end phone case brands: clean, calm and realistic, soft professional lighting, realistic shadows, minimal composition with lots of negative space. It must look like a real photo, not like AI.';
const set = $('Inställningar').first().json;
const filer = $('Hitta robotfiler').all().map(i => i.json);
const id = {}; for (const f of filer) id[f.name] = f.id;
// Jobbläge: exakta Blender-renderingar (X_bild/X_mask/X_topp) med egen scenbeskrivning per jobb
if (String(set.jobb || '').trim()) {
  const jobb = JSON.parse(set.jobb); const st = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, '');
  return jobb.map(j => ({ json: { typ: 'X', namn: `ai-X-${j.k}-${st}.png`,
    prompt: `${annonsstil}\nThe image contains a photorealistic phone in a phone case. Keep the phone and case exactly as they are: do not change shape, color, texture, logo, buttons, camera, position, size or angle. Only create the surroundings in the transparent areas.\nScene: ${j.scen}\nMatch the existing camera angle, lens and perspective exactly, with realistic contact shadows and reflections.\nIMPORTANT: no text, letters, numbers, logos or watermarks anywhere. Do not add other phones or products.`,
    modell: set.modell, kvalitet: j.kvalitet || set.kvalitet, storlek: j.storlek || '1008x1792',
    ids: { bild: id[`X_bild_${j.k}.png`], mask: id[`X_mask_${j.k}.png`], topp: id[`X_topp_${j.k}.png`] } } }))
    .filter(i => i.json.ids.bild && i.json.ids.mask && i.json.ids.topp);
}
const textFor = (typ, k) => filer.find(f => f.name.startsWith(`R_${typ}_${k}`));
const nycklar = [...new Set(filer.map(f => (f.name.match(/^A_bild_(s\d+)\.png$/) || [])[1]).filter(Boolean))]
  .filter(k => id[`A_mask_${k}.png`] && id[`A_topp_${k}.png`] && id[`C_bild_${k}.png`] && id[`C_mask_${k}.png`] && id[`C_topp_${k}.png`] && textFor('A', k) && textFor('C', k));
const bFiler = filer.filter(f => /^B_bild_s\d+_(L|D)\.jpg$/.test(f.name)).filter(f => id[`R_B_${f.name.split('_')[2]}.png`]);
if (!nycklar.length) throw new Error('Hittar inga robotfiler i mappen Chat Robotfiler.');
const slump = a => a[Math.floor(Math.random() * a.length)];
const nu = new Date(); const datum = nu.toISOString().slice(0, 10) + '-' + nu.toISOString().slice(11, 16).replace(':', '');
const vikt = { A: Number(set.andel_A ?? 0.5), B: bFiler.length ? Number(set.andel_B ?? 0.25) : 0, C: Number(set.andel_C ?? 0.25) };
const valjTyp = () => { let r = Math.random() * (vikt.A + vikt.B + vikt.C); for (const t of ['A', 'B', 'C']) { if ((r -= vikt[t]) < 0) return t; } return 'A'; };
const anvanda = new Set();
const ut = [];
for (let i = 0; i < set.antal; i++) {
  const typ = valjTyp();
  const nr = String(i + 1).padStart(2, '0');
  if (typ === 'B') {
    const f = slump(bFiler); const k = f.name.split('_')[2];
    ut.push({ json: { typ, namn: `reborn-${datum}-${nr}-foto.jpg`, ids: { bild: f.id, text: id[`R_B_${k}.png`] } } });
    continue;
  }
  let k = slump(nycklar); for (let t = 0; t < 10 && anvanda.has(k); t++) k = slump(nycklar); anvanda.add(k);
  const stil = slump(stilar);
  const tf = textFor(typ, k); const ton = tf.name.match(/_(L|D)\.png$/)[1];
  const toppTon = ton === 'D' ? 'The upper 25% of the image must be calm, simple and fairly dark so white text is easy to read.' : 'The upper 25% of the image must be calm, simple and light so black text is easy to read.';
  const prompt = typ === 'A'
    ? `${annonsstil}\nThe image contains a real product photo of a phone case. Keep the product exactly as it is: do not change its shape, color, texture, logo, buttons, camera frame, position, size or angle. Only create the surroundings in the transparent areas.\nScene: the product is ${stil.beskrivning}. Match the existing camera angle and perspective so the product sits naturally in the scene with realistic contact shadows and reflections. The product must clearly rest on or stand on a surface; it must never look like it is floating.\n${toppTon} Keep the bottom 8% calm for a small logo.\nIMPORTANT: no text, letters, numbers, logos or watermarks anywhere. Do not add other phones or products.`
    : `${annonsstil}\nThis is a real product photo placed in the middle of a tall 9:16 canvas. Extend the photo naturally into the transparent areas above and below: continue the same surface, background, lighting and colors seamlessly so it looks like one single photograph. Do not change anything inside the existing photo and do not change the product.\n${toppTon} Keep the bottom 8% calm for a small logo.\nIMPORTANT: no text, letters, numbers, logos or watermarks anywhere. Do not add other phones or products.`;
  ut.push({ json: {
    typ, namn: `ai-${typ}-${k}-${ton}-${datum}-${nr}-${typ === 'A' ? stil.namn.toLowerCase().replace(/[^a-z0-9]+/g, '-') : 'story'}.png`,
    prompt, modell: set.modell, kvalitet: set.kvalitet, storlek: typ === 'A' ? '1024x1280' : '1008x1792',
    ids: { bild: id[`${typ}_bild_${k}.png`], mask: id[`${typ}_mask_${k}.png`], topp: id[`${typ}_topp_${k}.png`], text: tf.id },
  }});
}
return ut;
