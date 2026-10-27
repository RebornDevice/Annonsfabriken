import json, uuid, sys
TEST = len(sys.argv) > 1
U=lambda: str(uuid.uuid4())
P="$('Planera annonser').item.json"
def mapp(label): return {"__rl":True,"mode":"list","value":"","cachedResultName":label}
def hamta(namn, falt, prop, pos):
    if TEST:
        return {"id":U(),"name":namn,"type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":pos,
          "parameters":{"url":"=http://127.0.0.1:8791/files/{{ "+P+".ids."+falt+" }}","options":{"response":{"response":{"responseFormat":"file","outputPropertyName":prop}}}}}
    return {"id":U(),"name":namn,"type":"n8n-nodes-base.googleDrive","typeVersion":3,"position":pos,
      "parameters":{"operation":"download","fileId":{"__rl":True,"mode":"id","value":"={{ "+P+".ids."+falt+" }}"},"options":{"binaryPropertyName":prop}}}
nodes=[
 {"id":U(),"name":"Varje natt","type":"n8n-nodes-base.scheduleTrigger","typeVersion":1.2,"position":[0,0],"parameters":{"rule":{"interval":[{"triggerAtHour":3}]}}},
 {"id":U(),"name":"Testa nu","type":"n8n-nodes-base.manualTrigger","typeVersion":1,"position":[0,200],"parameters":{}},
 {"id":U(),"name":"Inställningar","type":"n8n-nodes-base.set","typeVersion":3.4,"position":[220,100],
  "parameters":{"assignments":{"assignments":[
    {"id":U(),"name":"antal","value":6,"type":"number"},
    {"id":U(),"name":"andel_A","value":0.5,"type":"number"},
    {"id":U(),"name":"andel_B","value":0.25,"type":"number"},
    {"id":U(),"name":"andel_C","value":0.25,"type":"number"},
    {"id":U(),"name":"modell","value":"gpt-image-2","type":"string"},
    {"id":U(),"name":"kvalitet","value":"medium","type":"string"}]},"options":{}},
  "notes":"antal = annonser per körning\nandel_A = ny AI-miljö runt riktiga skalet\nandel_B = riktiga fotot med text\nandel_C = fotot utbyggt till story\nkvalitet = low / medium / high","notesInFlow":True},
 {"id":U(),"name":"Hitta robotfiler","type":"n8n-nodes-base.googleDrive","typeVersion":3,"position":[440,100],
  "parameters":{"resource":"fileFolder","returnAll":True,"filter":{"folderId":mapp("Välj mappen Chat Robotfiler"),"whatToSearch":"files"},"options":{"fields":["id","name"]}},
  "executeOnce":True,"notes":"Välj mappen Chat Robotfiler","notesInFlow":True},
 {"id":U(),"name":"Planera annonser","type":"n8n-nodes-base.code","typeVersion":2,"position":[660,100],"parameters":{"jsCode":open('planera.js').read()}},
 {"id":U(),"name":"Foto eller AI?","type":"n8n-nodes-base.if","typeVersion":2.2,"position":[880,100],
  "parameters":{"conditions":{"options":{"caseSensitive":True,"leftValue":"","typeValidation":"loose","version":2},
   "conditions":[{"id":U(),"leftValue":"={{ $json.typ }}","rightValue":"B","operator":{"type":"string","operation":"equals"}}],"combinator":"and"},"options":{}}},
 hamta("Hämta foto","bild","data",[1100,-120]),
 hamta("Hämta text (foto)","text","text",[1320,-120]),
 {"id":U(),"name":"Lägg på text (foto)","type":"n8n-nodes-base.editImage","typeVersion":1.1,"position":[1540,-120],
  "parameters":{"operation":"composite","dataPropertyName":"data","dataPropertyNameComposite":"text","operator":"Over","positionX":0,"positionY":0,"options":{"format":"jpeg","quality":92}}},
 hamta("Hämta bild","bild","bild",[1100,240]),
 hamta("Hämta skyddsmall","mask","mask",[1320,240]),
 {"id":U(),"name":"Skapa miljö (OpenAI)","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[1540,240],
  "parameters":{"method":"POST","url":"https://api.openai.com/v1/images/edits","authentication":"predefinedCredentialType","nodeCredentialType":"openAiApi",
   "sendBody":True,"contentType":"multipart-form-data","bodyParameters":{"parameters":[
     {"name":"model","value":"={{ $json.modell }}"},{"name":"prompt","value":"={{ $json.prompt }}"},
     {"name":"size","value":"={{ $json.storlek }}"},{"name":"quality","value":"={{ $json.kvalitet }}"},
     {"name":"n","value":"1"},{"name":"output_format","value":"png"},
     {"parameterType":"formBinaryData","name":"image","inputDataFieldName":"bild"},
     {"parameterType":"formBinaryData","name":"mask","inputDataFieldName":"mask"}]},
   "options":{"batching":{"batch":{"batchSize":2,"batchInterval":2000}},"timeout":300000}},
  "retryOnFail":True,"maxTries":2,"waitBetweenTries":5000,"onError":"continueRegularOutput"},
 {"id":U(),"name":"Till bildfil","type":"n8n-nodes-base.code","typeVersion":2,"position":[1760,240],"parameters":{"mode":"runOnceForEachItem","jsCode":open('tillbild.js').read()}},
 {"id":U(),"name":"Bara lyckade","type":"n8n-nodes-base.filter","typeVersion":2.2,"position":[1980,240],
  "parameters":{"conditions":{"options":{"caseSensitive":True,"leftValue":"","typeValidation":"loose","version":2},
   "conditions":[{"id":U(),"leftValue":"={{ $json.fel }}","rightValue":"","operator":{"type":"string","operation":"empty","singleValue":True}}],"combinator":"and"},"options":{}}},
 hamta("Hämta riktiga skalet","topp","topp",[2200,240]),
 hamta("Hämta text (AI)","text","text",[2420,240]),
 {"id":U(),"name":"Lägg på skal och text","type":"n8n-nodes-base.editImage","typeVersion":1.1,"position":[2640,240],
  "parameters":{"operation":"multiStep","dataPropertyName":"data","operations":{"operations":[
    {"operation":"composite","dataPropertyNameComposite":"topp","operator":"Over","positionX":0,"positionY":0},
    {"operation":"composite","dataPropertyNameComposite":"text","operator":"Over","positionX":0,"positionY":0}]},"options":{"format":"png"}}},
 {"id":U(),"name":"Spara i Färdiga bilder","type":"n8n-nodes-base.googleDrive","typeVersion":3,"position":[2860,60],
  "parameters":{"name":"={{ "+P+".namn }}","driveId":{"__rl":True,"mode":"list","value":"My Drive"},"folderId":mapp("Välj mappen Chat Färdiga bilder"),"inputDataFieldName":"data","options":{}},
  "notes":"Välj mappen Chat Färdiga bilder","notesInFlow":True},
]
def c(a,b,i=0): return (a,b,i)
links=[("Varje natt","Inställningar",0),("Testa nu","Inställningar",0),("Inställningar","Hitta robotfiler",0),("Hitta robotfiler","Planera annonser",0),
 ("Planera annonser","Foto eller AI?",0),("Hämta foto","Hämta text (foto)",0),("Hämta text (foto)","Lägg på text (foto)",0),("Lägg på text (foto)","Spara i Färdiga bilder",0),
 ("Hämta bild","Hämta skyddsmall",0),("Hämta skyddsmall","Skapa miljö (OpenAI)",0),("Skapa miljö (OpenAI)","Till bildfil",0),("Till bildfil","Bara lyckade",0),
 ("Bara lyckade","Hämta riktiga skalet",0),("Hämta riktiga skalet","Hämta text (AI)",0),("Hämta text (AI)","Lägg på skal och text",0),("Lägg på skal och text","Spara i Färdiga bilder",0)]
con={}
for a,b,i in links: con.setdefault(a,{"main":[[]]})["main"][0].append({"node":b,"type":"main","index":0})
con["Foto eller AI?"]={"main":[[{"node":"Hämta foto","type":"main","index":0}],[{"node":"Hämta bild","type":"main","index":0}]]}
wf={"name":"Reborn Annonsrobot","nodes":nodes,"connections":con,"settings":{"executionOrder":"v1","timezone":"Europe/Stockholm"},"pinData":{}}
if TEST:
    wf['nodes']=[n for n in nodes if n['name'] not in ('Varje natt','Spara i Färdiga bilder')]
    for n in wf['nodes']:
        if n['name']=='Hitta robotfiler':
            n.update({"type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"parameters":{"url":"http://127.0.0.1:8791/lista","options":{}}}); n.pop('executeOnce',None)
        if n['name']=='Skapa miljö (OpenAI)':
            p=n['parameters']; p['url']='http://127.0.0.1:8791/v1/images/edits'; p['authentication']='none'; p.pop('nodeCredentialType')
            p['sendHeaders']=True; p['headerParameters']={"parameters":[{"name":"Authorization","value":"Bearer test"}]}
    for k in ('Varje natt',): con.pop(k)
    con["Lägg på text (foto)"]={"main":[[]]}; con["Lägg på skal och text"]={"main":[[]]}
    wf['id']='testflow2'; wf['active']=False
    json.dump([wf],open(sys.argv[1],'w'),ensure_ascii=False)
else:
    json.dump(wf,open('Reborn-Annonsrobot.json','w'),ensure_ascii=False,indent=1)
print('ok')
