// Gör om svaret från OpenAI till en bildfil
const plan = $('Planera annonser').item.json;
if ($json.error || !$json.data) {
  const fel = $json.error ? (typeof $json.error === 'string' ? $json.error : ($json.error.message || JSON.stringify($json.error))) : 'Tomt svar';
  return { json: { namn: plan.namn, fel } };
}
const bild = await this.helpers.prepareBinaryData(Buffer.from($json.data[0].b64_json, 'base64'), plan.namn, 'image/png');
return { json: { namn: plan.namn, stil: plan.stil }, binary: { data: bild } };
