// Gör om svaret från OpenAI till en bild
const plan = $('Planera annonser').item.json;
if ($json.error || !$json.data) {
  const fel = $json.error ? (typeof $json.error === 'string' ? $json.error : ($json.error.message || JSON.stringify($json.error))) : 'Tomt svar';
  return { json: { ...plan, fel } };
}
const bild = await this.helpers.prepareBinaryData(Buffer.from($json.data[0].b64_json, 'base64'), plan.namn, 'image/png');
return { json: plan, binary: { data: bild } };
