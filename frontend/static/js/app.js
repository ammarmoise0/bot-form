/**
 * FormBot - Interface simplifiee
 */

let questions = {};
let strategies = {};
let currentStrategy = null;
let previewAnswers = {};
let isSubmitting = false;
let totalSent = 0;

// ============================================================
// INIT
// ============================================================

document.addEventListener("DOMContentLoaded", async () => {
  await Promise.all([loadQuestions(), loadStrategies()]);
  renderStrategyCards();
});

async function loadQuestions() {
  questions = await (await fetch("/api/questions")).json();
}

async function loadStrategies() {
  strategies = await (await fetch("/api/strategies")).json();
}

// ============================================================
// STEP 1 : STRATEGY CARDS
// ============================================================

function renderStrategyCards() {
  const grid = document.getElementById("strategy-grid");
  grid.innerHTML = "";

  const configs = {
    satisfait: { icon: "😊", color: "#27ae60", tags: ["Notes hautes", "NPS 7-10", "Recommande"] },
    mitige: { icon: "😐", color: "#f39c12", tags: ["Notes moyennes", "NPS 4-8", "Indecis"] },
    neutre: { icon: "🤷", color: "#3498db", tags: ["Notes au milieu", "NPS 4-7", "Pas d'avis"] },
    insatisfait: { icon: "😤", color: "#e74c3c", tags: ["Notes basses", "NPS 0-5", "Ne recommande pas"] },
    mix: { icon: "🎲", color: "#9b59b6", tags: ["35% satisfaits", "30% mitiges", "15% insatisfaits", "20% neutres"] },
  };

  const order = ["satisfait", "mitige", "neutre", "insatisfait", "mix"];

  order.forEach((key) => {
    const strat = strategies[key];
    if (!strat) return;
    const cfg = configs[key] || { icon: "📋", color: "#888", tags: [] };

    const card = document.createElement("div");
    card.className = "strategy-card";
    card.id = `strat-${key}`;
    card.onclick = () => selectStrategy(key);

    card.innerHTML = `
      <div class="strategy-icon" style="background:${cfg.color}20; color:${cfg.color}">${cfg.icon}</div>
      <div class="strategy-name">${strat.name}</div>
      <div class="strategy-desc">${strat.description}</div>
      <div class="strategy-tags">
        ${cfg.tags.map((t) => `<span class="strategy-tag">${t}</span>`).join("")}
      </div>
    `;

    grid.appendChild(card);
  });
}

async function selectStrategy(key) {
  currentStrategy = key;

  // Visual selection
  document.querySelectorAll(".strategy-card").forEach((c) => c.classList.remove("selected"));
  document.getElementById(`strat-${key}`).classList.add("selected");

  // Load preview
  const data = await (await fetch(`/api/strategies/${key}/preview`)).json();
  previewAnswers = data.answers;

  // Show steps 2 and 3
  document.getElementById("step-2").style.display = "block";
  document.getElementById("step-3").style.display = "block";

  renderPreview();

  // Scroll to preview
  document.getElementById("step-2").scrollIntoView({ behavior: "smooth", block: "start" });

  showToast(`Profil "${strategies[key].name}" selectionne`, "success");
}

// ============================================================
// STEP 2 : PREVIEW
// ============================================================

function renderPreview() {
  const container = document.getElementById("preview-sections");
  container.innerHTML = "";

  const hint = document.getElementById("preview-hint");
  hint.textContent = `Voici un exemple de ce qui sera envoye avec le profil "${strategies[currentStrategy].name}". Chaque envoi generera des reponses differentes.`;

  // Group answers by section
  Object.entries(questions).forEach(([sectionName, sqs]) => {
    const sectionDiv = document.createElement("div");
    sectionDiv.className = "preview-section";
    sectionDiv.innerHTML = `<div class="preview-section-title">${sectionName}</div>`;

    let hasAnswers = false;

    sqs.forEach((q) => {
      const val = previewAnswers[q.id];
      if (val == null) return;
      hasAnswers = true;

      const display = Array.isArray(val) ? val.join(", ") : String(val);

      let answerClass = "";
      if (q.type === "rating") {
        answerClass = "rating";
      } else if (q.type === "nps") {
        const n = parseInt(val);
        answerClass = n >= 7 ? "nps-high" : n >= 5 ? "nps-mid" : "nps-low";
      }

      const item = document.createElement("div");
      item.className = "preview-item";
      item.innerHTML = `
        <span class="preview-question">${esc(q.title)}</span>
        <span class="preview-answer ${answerClass}">${esc(display)}</span>
      `;
      sectionDiv.appendChild(item);
    });

    if (hasAnswers) container.appendChild(sectionDiv);
  });
}

async function regeneratePreview() {
  if (!currentStrategy) return;

  const data = await (await fetch(`/api/strategies/${currentStrategy}/preview`)).json();
  previewAnswers = data.answers;
  renderPreview();
  showToast("Nouvel apercu genere", "info");
}

// ============================================================
// STEP 3 : SEND
// ============================================================

function changeCount(delta) {
  const input = document.getElementById("submit-count");
  let val = parseInt(input.value) || 1;
  val = Math.max(1, Math.min(100, val + delta));
  input.value = val;
}

async function sendResponses() {
  if (isSubmitting || !currentStrategy) return;
  isSubmitting = true;

  const count = parseInt(document.getElementById("submit-count").value) || 1;
  const btn = document.getElementById("send-btn");
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Envoi en cours...';

  const progressDiv = document.getElementById("send-progress");
  const progressFill = document.getElementById("progress-fill");
  const progressText = document.getElementById("progress-text");
  const resultsList = document.getElementById("results-list");

  progressDiv.style.display = "block";
  resultsList.innerHTML = "";
  progressFill.style.width = "0%";

  let okCount = 0;
  let failCount = 0;

  try {
    const response = await fetch("/api/submit/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        strategy: currentStrategy,
        answers: {},
        count: count,
        delay_min: 1.0,
        delay_max: 3.0,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = JSON.parse(line.slice(6));
        if (data.done) continue;

        if (data.success) okCount++;
        else failCount++;

        totalSent++;
        const current = okCount + failCount;
        const pct = (current / count) * 100;

        progressFill.style.width = pct + "%";
        progressText.textContent = `${current} / ${count} — ${okCount} reussi(s)${failCount > 0 ? `, ${failCount} echec(s)` : ""}`;

        const cls = data.success ? "ok" : "fail";
        const id = data.form_id ? ` — reponse #${data.form_id}` : "";
        const item = document.createElement("div");
        item.className = `result-item ${cls}`;
        item.innerHTML = `
          <span class="result-dot ${cls}"></span>
          Envoi ${data.attempt}/${data.total} — ${data.success ? "OK" : "Echec"}${id}
        `;
        resultsList.appendChild(item);
        resultsList.scrollTop = resultsList.scrollHeight;

        updateSentCounter();
      }
    }
  } catch (err) {
    showToast("Erreur de connexion", "error");
  }

  btn.disabled = false;
  btn.innerHTML = "Envoyer les reponses";
  isSubmitting = false;

  if (okCount > 0) {
    progressText.textContent = `Termine ! ${okCount}/${count} reponse(s) envoyee(s) avec succes.`;
    showToast(`${okCount} reponse(s) envoyee(s)`, "success");
  } else {
    progressText.textContent = `Echec de l'envoi.`;
    showToast("Echec de l'envoi", "error");
  }
}

function updateSentCounter() {
  document.getElementById("sent-counter").textContent = `${totalSent} reponse(s) envoyee(s)`;
}

// ============================================================
// UTILS
// ============================================================

function esc(str) {
  if (!str) return "";
  const d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}

function showToast(msg, type = "info") {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = `toast ${type} show`;
  setTimeout(() => t.classList.remove("show"), 2500);
}
