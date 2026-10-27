// Planerar dagens annonser utifrån inställningarna
const set = $('Inställningar').first().json;
const cfg = $('Hämta bibliotek').first().json;
const bas = set.bibliotek_url.replace(/[^/]*$/, '');
const skal = cfg.produkter.filter(p => p.typ === 'Skal');
const kombo = cfg.produkter.filter(p => p.typ === 'Kombo');
const stilar = cfg.stilar;
const annonsstil = (cfg.annonsstil || '').trim();
if (!skal.length) throw new Error('Inga skalbilder i biblioteket');
if (!stilar.length) throw new Error('Inga stilar i biblioteket');
const slump = a => a[Math.floor(Math.random() * a.length)];
const datum = new Date().toISOString().slice(0, 10);
const storlek = { '1x1': '1024x1024', '4x5': '1024x1280', '9x16': '1008x1792' }[set.format] || '1024x1280';
const plats = set.textplats === 'nere'
  ? 'Keep the lower 30% of the image calm and uncluttered (simple background only) so a headline can be placed there later. Place the product in the upper-middle part.'
  : 'Keep the upper 30% of the image calm and uncluttered (simple background only) so a headline can be placed there later. Place the product in the lower-middle part.';
const scen = (stil) => `Create a photorealistic, high-end EMPTY scene that will be used as the background of a product advertisement for a premium phone case brand.
Scene: ${stil.beskrivning}.${annonsstil ? `\nStyle of my best performing ads (use as inspiration for mood, light and composition): ${annonsstil}` : ''}
There must be NO phone, NO phone case, NO product and NO hands holding anything in the image. Leave a clear, simple spot ${set.textplats === 'nere' ? 'in the upper-middle' : 'in the lower-middle'} of the image where a phone will be placed later, shot straight-on at eye level with soft, even light so a product can be added naturally.
Keep the ${set.textplats === 'nere' ? 'lower' : 'upper'} 30% of the image calm and uncluttered so a headline can be placed there.
Professional commercial photography, realistic, natural colors, premium feel.
IMPORTANT: Do not add any text, letters, numbers, words, logos, watermarks or brand names anywhere in the image.`;
const andel = Math.max(0, Math.min(1, Number(set.andel_exakt ?? 0.5)));
const ut = [];
for (let i = 0; i < set.antal; i++) {
  const stil = stilar[i % stilar.length];
  const exakt = Math.random() < andel; // exakt: AI gör bara miljön, appen lägger din rendering ovanpå
  // Kombibilder (skal + tillbehör i samma bild) har typ "Kombo". Tillbehör visas aldrig ensamma.
  const prod = (kombo.length && set.ibland_tillbehor && Math.random() < 0.25) ? slump(kombo) : slump(skal);
  const prompt = `Create a photorealistic, high-end social media advertising photo for a premium phone accessory brand.
The attached image shows the exact product${prod.typ === 'Kombo' ? 's (phone case with matching accessory, always shown together)' : ''}. Reproduce it exactly as shown: identical shape, material texture and weave pattern, colors, camera cutout and camera frame, buttons, edges and proportions. Do not redesign, simplify or invent details on the product.${annonsstil ? `\nStyle of my best performing ads (use as inspiration for mood, light and composition): ${annonsstil}` : ''}
Scene: ${stil.beskrivning}.
${plats}
Professional commercial photography, realistic lighting and shadows, sharp focus on the product, natural colors, premium feel.
IMPORTANT: Do not add any text, letters, numbers, words, logos, watermarks or brand names anywhere in the image.`;
  ut.push({ json: {
    exakt,
    namn: `${exakt ? 'bakgrund' : 'reborn'}-${datum}-${String(i + 1).padStart(2, '0')}-${stil.namn.toLowerCase().replace(/[^a-z0-9åäö]+/g, '-')}.png`,
    stil: stil.namn, prompt: exakt ? scen(stil) : prompt, modell: set.modell, kvalitet: set.kvalitet, storlek,
    produktbild: bas + prod.fil
  }});
}
return ut;
