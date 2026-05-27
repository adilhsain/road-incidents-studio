document.addEventListener("DOMContentLoaded", () => {
  loadPersonas();
  loadTeamMembers();
});

async function fetchData(url, params = {}) {
  const query = new URLSearchParams(params).toString();
  const finalUrl = query ? `${url}?${query}` : url;

  const response = await fetch(finalUrl);
  if (!response.ok) {
    throw new Error(`API returned status ${response.status}`);
  }

  const payload = await response.json();
  if (payload.error) {
    throw new Error(payload.error);
  }

  return payload.data || [];
}

function showLoading(elementId) {
  const element = document.getElementById(elementId);
  if (!element) return;
  element.innerHTML = '<div class="loading-spinner" aria-label="Loading"></div>';
  element.hidden = false;
}

function showError(elementId, message) {
  const element = document.getElementById(elementId);
  if (!element) return;
  element.textContent = message;
  element.hidden = false;
}

function formatPercent(value, total) {
  const numerator = Number(value) || 0;
  const denominator = Number(total) || 0;
  if (denominator === 0) {
    return "0.0%";
  }
  return `${((numerator / denominator) * 100).toFixed(1)}%`;
}

function colorCodeInjuryLevel(level) {
  switch ((level || "").trim()) {
    case "Fatal":
      return "injury-fatal";
    case "Serious Injury":
      return "injury-serious";
    case "Other Injury":
      return "injury-other";
    case "Not Injured":
      return "injury-none";
    default:
      return "injury-unknown";
  }
}

async function loadPersonas() {
  const container = document.getElementById("persona-grid");
  const loading = document.getElementById("persona-loading");
  const error = document.getElementById("persona-error");

  if (!container || !loading || !error) {
    return;
  }

  showLoading("persona-loading");
  error.hidden = true;

  try {
    const personas = await fetchData("/api/personas");
    loading.hidden = true;

    if (!Array.isArray(personas) || personas.length === 0) {
      container.innerHTML = "<p>No persona data available.</p>";
      return;
    }

    container.innerHTML = personas
      .map(
        (persona) => `
          <article class="card persona-card">
            <img src="https://via.placeholder.com/150" alt="Portrait of ${persona.name}" class="persona-image">
            <div class="persona-body">
              <h3>${persona.name}</h3>
              <p class="persona-meta"><strong>Age:</strong> ${persona.age} &bull; <strong>Occupation:</strong> ${persona.occupation}</p>
              <p><strong>Background:</strong> ${persona.background}</p>
              <p><strong>Goals:</strong> ${persona.goals}</p>
              <p><strong>Pain points:</strong> ${persona.pain_points}</p>
            </div>
          </article>
        `
      )
      .join("");
  } catch (fetchError) {
    loading.hidden = true;
    showError("persona-error", `Unable to load personas. ${fetchError.message}`);
  }
}

async function loadTeamMembers() {
  const table = document.getElementById("team-table");
  const tbody = table ? table.querySelector("tbody") : null;
  const loading = document.getElementById("team-loading");
  const error = document.getElementById("team-error");

  if (!table || !tbody || !loading || !error) {
    return;
  }

  showLoading("team-loading");
  error.hidden = true;

  try {
    const teamMembers = await fetchData("/api/team-members");
    loading.hidden = true;

    if (!Array.isArray(teamMembers) || teamMembers.length === 0) {
      showError("team-error", "No team members were found.");
      return;
    }

    tbody.innerHTML = teamMembers
      .map(
        (member) => `
          <tr>
            <td>${member.full_name}</td>
            <td>${member.student_number}</td>
            <td>${member.role}</td>
          </tr>
        `
      )
      .join("");

    table.hidden = false;
  } catch (fetchError) {
    showError("team-error", `Unable to load team members. ${fetchError.message}`);
  }
}

