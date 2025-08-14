const inputEl  = document.getElementById("input");
const outputEl = document.getElementById("output");
const srcSel   = document.getElementById("source");
const tgtSel   = document.getElementById("target");
const realtime = document.getElementById("realtime");
const btnTranslate = document.getElementById("translateBtn");
const btnCopy = document.getElementById("copyBtn");
const btnClear = document.getElementById("clearBtn");
const btnSpeak = document.getElementById("speak");

let ws = null;
let debounceTimer = null;

function ensureWS(){
  if (ws && ws.readyState === 1) return ws;
  const proto = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(`${proto}://${location.host}/ws/translate`);
  ws.onmessage = (ev) => { outputEl.value = ev.data; };
  ws.onerror = () => { };
  return ws;
}

async function translateOnce(){
  const text = inputEl.value.trim();
  const payload = { text, source: srcSel.value, target: tgtSel.value };
  const res = await fetch("/api/translate", {
    method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify(payload)
  });
  const js = await res.json();
  outputEl.value = js.text || "";
}

function translateStream(){
  ensureWS();
  const text = inputEl.value;
  const payload = JSON.stringify({ text, source: srcSel.value, target: tgtSel.value });
  ws.send(payload);
}

function schedule(){
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(()=> realtime.checked ? translateStream() : null, 220);
}


inputEl.addEventListener("input", schedule);
btnTranslate.addEventListener("click", translateOnce);
btnCopy.addEventListener("click", async ()=>{
  if (!outputEl.value) return;
  await navigator.clipboard.writeText(outputEl.value);
  btnCopy.textContent = "Kopyalandı ✓"; setTimeout(()=> btnCopy.textContent="Kopyala", 900);
});
btnClear.addEventListener("click", ()=>{
  inputEl.value = ""; outputEl.value = "";
});
document.addEventListener("keydown", (e)=>{
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") translateOnce();
});
btnSpeak.addEventListener("click", ()=>{
  const txt = outputEl.value; if (!txt) return;
  const utter = new SpeechSynthesisUtterance(txt);

  utter.lang = tgtSel.value === "tr" ? "tr-TR" : (tgtSel.value === "de" ? "de-DE" : "en-US");
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utter);
});
