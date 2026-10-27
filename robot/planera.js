// Planerar dagens annonser. Stilarna nedan kan du ändra, lägga till eller ta bort.
const stilar = [
  { namn: 'Studio', beskrivning: 'clean premium studio product shot, soft gradient backdrop, soft diffused light, subtle reflection, minimal' },
  { namn: 'Livsstil', beskrivning: 'lifestyle scene, the phone held naturally in a hand in a bright modern cafe, shallow depth of field, warm natural light' },
  { namn: 'Skrivbord', beskrivning: 'on a minimal wooden desk next to a laptop and coffee, morning window light, calm and premium' },
  { namn: 'Gata', beskrivning: 'urban street at golden hour, phone in hand, blurred city background, cinematic' },
  { namn: 'Bil', beskrivning: 'phone mounted on a magnetic car mount in a modern car interior, sleek dashboard, evening light' },
  { namn: 'Natur', beskrivning: 'outdoors on a smooth rock with moss, soft overcast light, scandinavian nature, fresh' },
  { namn: 'Mork lyx', beskrivning: 'dark luxurious scene, black textured surface, dramatic rim light, high contrast, premium' },
  { namn: 'Gym', beskrivning: 'modern gym, phone resting on a bench next to a towel and dumbbell, energetic light' },
];
const set = $('Inställningar').first().json;
const bilder = $('Hitta material').all().map(i => i.json).filter(f => /^image\/(png|jpe?g|webp)$/.test(f.mimeType || ''));
if (!bilder.length) throw new Error('Inga bilder i mappen Material. Lägg in PNG- eller JPG-bilder på dina skal.');
const annonsstil = (set.annonsstil || '').trim();
const slump = a => a[Math.floor(Math.random() * a.length)];
const datum = new Date().toISOString().slice(0, 10);
const storlek = { '1x1': '1024x1024', '4x5': '1024x1280', '9x16': '1008x1792' }[set.format] || '1024x1280';
const plats = set.textplats === 'nere'
  ? 'Keep the lower 30% of the image calm and uncluttered (simple background only) so a headline can be placed there later. Place the product in the upper-middle part.'
  : 'Keep the upper 30% of the image calm and uncluttered (simple background only) so a headline can be placed there later. Place the product in the lower-middle part.';
const ut = [];
for (let i = 0; i < set.antal; i++) {
  const stil = stilar[i % stilar.length];
  const bild = slump(bilder);
  const prompt = `Create a photorealistic, high-end social media advertising photo for a premium phone accessory brand.
The attached image shows the exact product. Reproduce it exactly as shown: identical shape, material texture and weave pattern, colors, camera cutout and camera frame, buttons, edges and proportions. Do not redesign, simplify or invent details on the product. If the image shows a phone case together with an accessory, always keep them together.${annonsstil ? `\nStyle of my best performing ads (use as inspiration for mood, light and composition): ${annonsstil}` : ''}
Scene: ${stil.beskrivning}.
${plats}
Professional commercial photography, realistic lighting and shadows, sharp focus on the product, natural colors, premium feel.
IMPORTANT: Do not add any text, letters, numbers, words, logos, watermarks or brand names anywhere in the image.`;
  ut.push({ json: {
    namn: `reborn-${datum}-${String(i + 1).padStart(2, '0')}-${stil.namn.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.png`,
    stil: stil.namn, prompt, modell: set.modell, kvalitet: set.kvalitet, storlek, filId: bild.id, filnamn: bild.name,
  }});
}
return ut;
