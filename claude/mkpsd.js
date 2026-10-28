// Skriver en PSD med lager (redigerbar text) från spec.json + PNG-lager. Körs: node mkpsd.js <mapp>
const fs = require('fs'), path = require('path');
const { PNG } = require('pngjs');
const agPsd = require('ag-psd');
const dir = process.argv[2];
const spec = JSON.parse(fs.readFileSync(path.join(dir, 'spec.json'), 'utf8'));
const img = f => { const p = PNG.sync.read(fs.readFileSync(path.join(dir, f))); return { width: p.width, height: p.height, data: new Uint8ClampedArray(p.data) }; };
const children = spec.lager.map(l => {
  const o = { name: l.namn, imageData: img(l.fil), opacity: l.opacity ?? 1 };
  if (l.text) o.text = {
    text: l.text.rader.join('\r'), transform: [1, 0, 0, 1, l.text.x, l.text.y], antiAlias: 'smooth',
    style: { font: { name: l.text.font }, fontSize: l.text.storlek, fillColor: { r: l.text.farg[0], g: l.text.farg[1], b: l.text.farg[2] },
      autoLeading: false, leading: l.text.radavstand, tracking: l.text.spärr || 0 },
    paragraphStyle: { justification: l.text.just || 'center' },
  };
  return o;
});
const psd = { width: spec.bredd, height: spec.hojd, imageData: img(spec.platt), children };
fs.writeFileSync(spec.ut, Buffer.from(agPsd.writePsd(psd, { invalidateTextLayers: true, generateThumbnail: false })));
console.log('PSD', spec.ut);
