/* Hossam Video Factory dashboard */
const $ = (s, el) => (el || document).querySelector(s);
const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));

const METHOD_COLORS = {
  code: "#136052", screenshot: "#2a5a4e", hossam_image: "#437F3E",
  direct_image: "#B3CE65", image_animate: "#FF5A33", first_last_frame: "#D97A1F",
  text_to_video: "#FF3B6B",
};
const STAGES = ["ingest", "audio_clean", "transcribe", "plan", "approval",
  "generation", "assembly", "render", "done"];

let STATE = { projects: [], keys: {} };
let CURRENT = null;

function toast(msg, err) {
  const t = $("#toast");
  t.textContent = msg;
  t.className = "toast show" + (err ? " err" : "");
  setTimeout(() => t.className = "toast", 2600);
}

async function api(path, opts) {
  const r = await fetch(path, opts);
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || r.status);
  return data;
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g,
    c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

/* ------------------------------------------------ nav */
$$("nav button").forEach(b => b.onclick = () => {
  $$("nav button").forEach(x => x.classList.toggle("active", x === b));
  ["projects", "project", "config", "keys"].forEach(v =>
    $("#view-" + v).style.display = "none");
  if (b.dataset.view === "projects") { $("#view-projects").style.display = ""; loadState(); }
  if (b.dataset.view === "config") { $("#view-config").style.display = ""; loadConfig(); }
  if (b.dataset.view === "keys") { $("#view-keys").style.display = ""; renderKeys(); }
});

/* ------------------------------------------------ projects */
async function loadState() {
  STATE = await api("/api/state");
  renderProjects();
}

function stepper(stage) {
  const idx = STAGES.indexOf(stage);
  return `<div class="stepper">` + STAGES.map((s, i) =>
    `<span class="step ${i < idx ? "done" : i === idx ? "current" : ""}">${s}</span>`).join("") + `</div>`;
}

function renderProjects() {
  const el = $("#view-projects");
  if (!STATE.projects.length) {
    el.innerHTML = `<div class="empty"><div class="big">🎬</div>
      No projects yet.<br>Create one from your terminal:<br><br>
      <code>python pipeline/new_project.py my-video</code><br>
      then drop your voiceover into <code>projects/my-video/input/</code></div>`;
    return;
  }
  const keyBadges = Object.entries(STATE.keys).map(([k, v]) =>
    `<span class="badge ${v ? "ok" : "bad"}">${k}: ${v ? "set" : "missing"}</span>`).join(" ");
  el.innerHTML = `<div class="row" style="justify-content:space-between;align-items:center">
    <div>${keyBadges}</div></div><div style="height:12px"></div>
    <div class="project-grid">` + STATE.projects.map(p => `
    <div class="card">
      <h3 data-open="${p.name}">${esc(p.title)} <span class="muted">(${p.name})</span></h3>
      ${stepper(p.stage)}
      <div class="row" style="gap:8px">
        <span class="badge ${p.storyboard_status === "approved" ? "ok" : p.storyboard_status === "none" ? "bad" : "warn"}">
          storyboard: ${p.storyboard_status}</span>
        ${p.aspect ? `<span class="badge info">${p.aspect}</span>` : ""}
        ${p.duration_s ? `<span class="badge info">${p.duration_s}s</span>` : ""}
      </div>
      <div class="muted" style="margin-top:10px">
        ${p.scene_count} scenes &middot; est <span class="money">$${p.estimated_cost_usd || 0}</span>
        &middot; spent <span class="money actual">$${p.actual_cost_usd || 0}</span>
      </div>
    </div>`).join("") + `</div>`;
  $$("[data-open]", el).forEach(h => h.onclick = () => openProject(h.dataset.open));
}

/* ------------------------------------------------ project detail */
async function openProject(name) {
  CURRENT = name;
  $$("nav button").forEach(x => x.classList.remove("active"));
  ["projects", "config", "keys"].forEach(v => $("#view-" + v).style.display = "none");
  const el = $("#view-project");
  el.style.display = "";
  el.innerHTML = `<div class="card">Loading ${esc(name)}…</div>`;
  await renderProject();
}

async function renderProject() {
  const d = await api(`/api/project/${CURRENT}`);
  const sb = d.storyboard || { scenes: [], status: "none" };
  const ov = d.overview;
  const total = sb.total_duration || ov.duration_s || 1;
  const el = $("#view-project");

  el.innerHTML = `
  <div class="card">
    <div class="row" style="justify-content:space-between;align-items:flex-start">
      <div>
        <h2 style="margin:0">${esc(ov.title)}</h2>
        <div class="muted">${esc(CURRENT)} &middot; ${ov.aspect || "?"} &middot; ${ov.duration_s || "?"}s
          &middot; ${sb.scenes.length} scenes</div>
        ${stepper(ov.stage)}
      </div>
      <div class="row" style="gap:8px">
        <button class="btn ghost" onclick="openProject('${CURRENT}')">Refresh</button>
        <button class="btn ghost" onclick="loadState();document.querySelector('#view-projects').style.display='';this.closest('#view-project').style.display='none'">Back</button>
        <button class="btn danger" id="btn-reject">Reject</button>
        <button class="btn accent" id="btn-approve">Approve storyboard</button>
      </div>
    </div>
    <div id="costbar">
      <div>Estimated AI cost: <b class="money">$${sb.estimated_cost_usd || 0}</b></div>
      <div>Actual spent: <b class="money actual">$${(d.ledger && d.ledger.total_cost_usd) || 0}</b></div>
      <div>Status: <b>${esc(sb.status)}</b></div>
      <div>Hook: 0–${(sb.hook && sb.hook.end_s) || 0}s (${((sb.hook && sb.hook.scene_ids) || []).join(", ")})</div>
    </div>
    <div class="timeline">${sb.scenes.map(s => {
      const l = ((s.end - s.start) / total * 100).toFixed(3);
      const x = (s.start / total * 100).toFixed(3);
      return `<div class="tl-seg" data-scene="${s.id}" title="${s.id} ${s.start}-${s.end}s ${s.method}"
        style="left:${x}%;width:${l}%;background:${METHOD_COLORS[s.method] || "#333"}">${s.id}</div>`;
    }).join("")}</div>
    <div class="muted">Scene colors by method: code/screenshot/hossam = free greens &middot; image = yellow-green &middot; AI video = orange/red (costs credits)</div>
  </div>

  <div class="card">
    <h2 style="margin-top:0">Scenes <span class="muted">(edit inline, then Save; approve to unlock generation)</span></h2>
    <div style="overflow-x:auto"><table id="scenes-table">
      <thead><tr><th>#</th><th>Time</th><th>Beat</th><th>Style</th><th>Method</th>
      <th>Headline / Narration</th><th>Prompts &amp; assets</th><th>Cost</th></tr></thead>
      <tbody>${sb.scenes.map(sceneRow).join("")}</tbody>
    </table></div>
    <div class="row" style="margin-top:12px;gap:8px">
      <button class="btn" id="btn-save-sb">Save storyboard</button>
      <span class="muted">Saving sets status to <b>edited</b> — re-approve after saving.</span>
    </div>
  </div>

  <div class="card">
    <h2 style="margin-top:0">Pipeline log</h2>
    <pre class="log" id="plog">${esc(d.log || "(empty)")}</pre>
  </div>`;

  $("#btn-approve").onclick = async () => {
    try {
      await api(`/api/project/${CURRENT}/approve`, { method: "POST" });
      toast("Storyboard approved — generation unblocked");
      renderProject();
    } catch (e) { toast(e.message, true); }
  };
  $("#btn-reject").onclick = async () => {
    try {
      await api(`/api/project/${CURRENT}/reject`, { method: "POST" });
      toast("Rejected — back to draft");
      renderProject();
    } catch (e) { toast(e.message, true); }
  };
  $("#btn-save-sb").onclick = async () => {
    const scenes = Array.from($("#scenes-table").querySelectorAll("tbody tr")).map(tr => {
      const s = sb.scenes.find(x => x.id === tr.dataset.id);
      const g = attr => tr.querySelector(`[data-f="${attr}"]`);
      s.start = parseFloat(g("start").value) || s.start;
      s.end = parseFloat(g("end").value) || s.end;
      s.beat = g("beat").value;
      s.style = g("style").value;
      s.method = g("method").value;
      s.headline = g("headline").value;
      s.narration = g("narration").value;
      s.image_prompt = g("image_prompt").value;
      s.video_prompt = g("video_prompt").value;
      s.notes = g("notes").value;
      s.estimated_cost_usd = parseFloat(g("cost").value) || 0;
      return s;
    });
    sb.scenes = scenes.sort((a, b) => a.start - b.start);
    try {
      await api(`/api/project/${CURRENT}/storyboard`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ storyboard: sb }),
      });
      toast("Saved (status: edited)");
      renderProject();
    } catch (e) { toast(e.message, true); }
  };
}

function sceneRow(s) {
  const assets = s.assets || {};
  const assetInfo = [
    assets.video ? `🎬 ${assets.video}` : "",
    assets.first_frame ? `🖼 ${assets.first_frame}` : "",
  ].filter(Boolean).join("<br>");
  const prompts = [];
  if (s.image_prompt) prompts.push(`<div class="muted">image:</div><div class="prompt-box">${esc(s.image_prompt)}</div>`);
  if (s.video_prompt) prompts.push(`<div class="muted">video:</div><div class="prompt-box">${esc(s.video_prompt)}</div>`);
  if (assetInfo) prompts.push(`<div class="muted" style="margin-top:4px">assets:<br>${assetInfo}</div>`);
  const methods = ["code", "direct_image", "image_animate", "first_last_frame",
    "text_to_video", "screenshot", "hossam_image"];
  const styles = ["motion_graphics", "vox_animation", "whiteboard_explainer",
    "scientific_infographic", "3d_animation", "clay_animation", "stop_motion", "cinematic_broll"];
  return `<tr data-id="${s.id}">
    <td><b>${s.id}</b></td>
    <td><input data-f="start" type="number" step="0.1" value="${s.start}" style="width:74px">
        <input data-f="end" type="number" step="0.1" value="${s.end}" style="width:74px"></td>
    <td><select data-f="beat">${["hook","context","explain","example","demo","proof","quote","recap","cta"]
      .map(b => `<option ${b === s.beat ? "selected" : ""}>${b}</option>`).join("")}</select></td>
    <td><select data-f="style">${styles.map(x => `<option ${x === s.style ? "selected" : ""}>${x}</option>`).join("")}</select></td>
    <td><select data-f="method" class="${s.method.includes("video") ? "method-video" : s.method.includes("image") && s.method !== "hossam_image" && s.method !== "screenshot" ? "method-img" : "method-free"}">
      ${methods.map(m => `<option ${m === s.method ? "selected" : ""}>${m}</option>`).join("")}</select></td>
    <td><input data-f="headline" class="ar" value="${esc(s.headline || "")}" placeholder="on-screen headline">
        <textarea data-f="narration" class="ar" style="min-height:44px">${esc(s.narration || "")}</textarea></td>
    <td style="min-width:260px">${prompts.join("") || '<span class="muted">—</span>'}
        <textarea data-f="notes" style="min-height:36px" placeholder="notes">${esc(s.notes || "")}</textarea></td>
    <td><input data-f="cost" type="number" step="0.01" value="${s.estimated_cost_usd || 0}" style="width:70px"></td>
  </tr>`;
}

/* ------------------------------------------------ config */
let CONFIG = null;
async function loadConfig() {
  CONFIG = await api("/api/config");
  renderConfig();
}

function cfgInput(path, val, type = "text") {
  return `<div><label>${path}</label><input data-path="${path}" type="${type}" value="${esc(val)}"></div>`;
}

function renderConfig() {
  const c = CONFIG;
  $("#view-config").innerHTML = `
  <div class="card config-section">
    <h2 style="margin-top:0">Models &amp; providers <span class="muted">(easy upgrades: change a model name, save)</span></h2>
    <div class="row">
      <div class="grow">${cfgInput("transcription.gemini.model", c.transcription.gemini.model)}</div>
      <div class="grow">${cfgInput("transcription.provider", c.transcription.provider)}</div>
      <div class="grow">${cfgInput("planning.model", c.planning.model)}</div>
    </div>
    <div class="row">
      <div class="grow">${cfgInput("image.provider", c.image.provider)}</div>
      <div class="grow">${cfgInput("image.openai.model", c.image.openai.model)}</div>
      <div class="grow">${cfgInput("image.openai.quality", c.image.openai.quality)}</div>
    </div>
    <div class="row">
      <div class="grow">${cfgInput("video.gemini_video.model", c.video.gemini_video.model)}</div>
      <div class="grow">${cfgInput("video.gemini_video.resolution", c.video.gemini_video.resolution)}</div>
      <div class="grow">${cfgInput("video.gemini_video.max_clip_duration_s", c.video.gemini_video.max_clip_duration_s, "number")}</div>
      <div class="grow">${cfgInput("video.provider", c.video.provider)}</div>
    </div>
    <div class="row">
      <div class="grow">${cfgInput("video_defaults.aspect", c.video_defaults.aspect)}</div>
      <div class="grow">${cfgInput("video_defaults.resolution", c.video_defaults.resolution)}</div>
      <div class="grow">${cfgInput("video_defaults.fps", c.video_defaults.fps, "number")}</div>
    </div>
  </div>
  <div class="card config-section">
    <h2 style="margin-top:0">Behaviour</h2>
    <div class="row">
      <div class="grow">${cfgInput("hook.max_duration_s", c.hook.max_duration_s, "number")}</div>
      <div class="grow">${cfgInput("hook.min_cuts", c.hook.min_cuts, "number")}</div>
      <div class="grow">${cfgInput("hook.max_scene_len_s", c.hook.max_scene_len_s, "number")}</div>
      <div class="grow">${cfgInput("captions.style", c.captions.style)}</div>
      <div class="grow">${cfgInput("captions.max_words_per_chunk", c.captions.max_words_per_chunk, "number")}</div>
    </div>
  </div>
  <div class="card config-section">
    <h2 style="margin-top:0">Costs (USD estimates)</h2>
    <div class="row">
      <div class="grow">${cfgInput("costs.per_image_usd", c.costs.per_image_usd)}</div>
      <div class="grow">${cfgInput("costs.per_video_second_usd", c.costs.per_video_second_usd)}</div>
      <div class="grow">${cfgInput("costs.planning_call_usd", c.costs.planning_call_usd)}</div>
    </div>
  </div>
  <button class="btn accent" id="btn-save-config">Save configuration</button>`;

  $("#btn-save-config").onclick = async () => {
    const patch = {};
    $$('#view-config input[data-path]').forEach(inp => {
      const parts = inp.dataset.path.split(".");
      let node = patch;
      for (const p of parts.slice(0, -1)) node = node[p] = node[p] || {};
      const v = inp.value;
      node[parts[parts.length - 1]] = v === "" ? "" : (isNaN(v) || v === "true" || v === "false" ? v : Number(v));
    });
    try {
      await api("/api/config", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patch),
      });
      toast("Configuration saved");
    } catch (e) { toast(e.message, true); }
  };
}

/* ------------------------------------------------ keys */
function renderKeys() {
  const keys = STATE.keys || {};
  $("#view-keys").innerHTML = `
  <div class="card">
    <h2 style="margin-top:0">API keys</h2>
    <p class="muted">Stored locally in <code>config/api_keys.json</code> (gitignored). Values are never displayed back.
    Environment variables override these.</p>
    <div class="keys-grid">
      ${Object.keys(keys).map(k => `
      <div class="card" style="margin:0">
        <div class="row" style="justify-content:space-between;align-items:center;margin-bottom:8px">
          <b>${k}</b>
          <span class="badge ${keys[k] ? "ok" : "bad"}">${keys[k] ? "set" : "missing"}</span>
        </div>
        <div class="kv">
          <input type="password" id="key-${k}" placeholder="paste key value…">
          <button class="btn" data-key="${k}">Save</button>
        </div>
      </div>`).join("")}
    </div>
  </div>`;
  $$("#view-keys [data-key]").forEach(b => b.onclick = async () => {
    const v = $("#key-" + b.dataset.key).value.trim();
    if (!v) return toast("Empty value", true);
    try {
      const r = await api("/api/keys", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: b.dataset.key, value: v }),
      });
      Object.assign(STATE.keys, r.status);
      toast(`${b.dataset.key} saved`);
      renderKeys();
    } catch (e) { toast(e.message, true); }
  });
}

loadState().catch(e => toast(e.message, true));
setInterval(async () => {
  if ($("#view-projects").style.display === "" && !CURRENT) {
    try { await loadState(); } catch (e) {}
  }
}, 5000);
