document.addEventListener("DOMContentLoaded", () => {
  loadPersonas();
  loadTeamMembers();
  initializePeopleSummaryPage();
  initializeDeepAnalysisPage();
});

function initializePeopleSummaryPage() {
  const searchButton = document.getElementById("search-button");
  const resetButton = document.getElementById("reset-button");
  if (!searchButton || !resetButton) {
    return;
  }

  searchButton.addEventListener("click", () => {
    fetchPeopleSummary();
  });

  resetButton.addEventListener("click", () => {
    resetPeopleFilters();
    fetchPeopleSummary();
  });

  fetchPeopleSummary();
}

function initializeDeepAnalysisPage() {
  const runButton = document.getElementById("run-analysis-button");
  if (!runButton) {
    return;
  }

  runButton.addEventListener("click", () => {
    fetchDeepAnalysis();
  });

  fetchDeepAnalysis();
}

function fetchDeepAnalysis() {
  const loading = document.getElementById("deep-loading");
  const error = document.getElementById("deep-error");
  const emptyMessage = document.getElementById("deep-empty");
  const table = document.getElementById("deep-table");
  const resultCount = document.getElementById("deep-result-count");
  const insightsList = document.getElementById("insights-list");
  const queryCode = document.getElementById("deep-query");

  if (!loading || !error || !emptyMessage || !table || !resultCount || !insightsList || !queryCode) {
    return;
  }

  loading.hidden = false;
  error.hidden = true;
  emptyMessage.hidden = true;
  table.hidden = true;
  insightsList.innerHTML = "";

  const params = new URLSearchParams();
  const injuryType = document.getElementById("injury-type-select").value;
  if (injuryType && injuryType !== "All Injuries") {
    params.set("injury_type", injuryType);
  }

  fetch(`/api/deep-analysis?${params.toString()}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      loading.hidden = true;
      renderDeepAnalysis(data);
    })
    .catch((fetchError) => {
      loading.hidden = true;
      error.hidden = false;
      error.textContent = `Unable to load deep analysis data. ${fetchError.message}`;
    });
}

function renderDeepAnalysis(data) {
  const table = document.getElementById("deep-table");
  const tbody = table.querySelector("tbody");
  const resultCount = document.getElementById("deep-result-count");
  const emptyMessage = document.getElementById("deep-empty");
  const insightsList = document.getElementById("insights-list");

  if (!Array.isArray(data) || data.length === 0) {
    tbody.innerHTML = "";
    table.hidden = true;
    resultCount.textContent = "Showing 0 results";
    insightsList.innerHTML = "";
    emptyMessage.hidden = false;
    return;
  }

  const sortedData = data.slice().sort((a, b) => b.incident_count - a.incident_count).slice(0, 20);
  const averageCount = sortedData.reduce((sum, row) => sum + Number(row.incident_count || 0), 0) / sortedData.length;
  const roundedAverage = averageCount ? Number(averageCount.toFixed(1)) : 0;

  resultCount.textContent = `Showing ${sortedData.length} results`;

  tbody.innerHTML = sortedData
    .map((row, index) => {
      const count = Number(row.incident_count || 0);
      const diffPercent = averageCount ? ((count - averageCount) / averageCount) * 100 : 0;
      const diffText = `${diffPercent >= 0 ? "+" : ""}${diffPercent.toFixed(1)}% above average`;
      const medal = getMedalIcon(index + 1);
      return `
        <tr>
          <td>${medal} ${index + 1}</td>
          <td>${row.age_group || row.AGE_GROUP || "Unknown"}</td>
          <td>${row.road_user_type || row.ROAD_USER_TYPE || "Unknown"}</td>
          <td>${row.inj_level || row.INJ_LEVEL || "Unknown"}</td>
          <td>${count}</td>
          <td>${diffText}</td>
        </tr>
      `;
    })
    .join("");

  insightsList.innerHTML = generateDeepInsights(sortedData, averageCount);
  table.hidden = false;
  emptyMessage.hidden = true;
}

function getMedalIcon(rank) {
  if (rank === 1) return "🥇";
  if (rank === 2) return "🥈";
  if (rank === 3) return "🥉";
  return "";
}

function generateDeepInsights(rows, averageCount) {
  if (!Array.isArray(rows) || rows.length === 0) {
    return "<p>No insights available.</p>";
  }

  const topRows = rows.slice(0, 3);
  return topRows
    .map((row, index) => {
      const count = Number(row.incident_count || 0);
      const diffPercent = averageCount ? ((count - averageCount) / averageCount) * 100 : 0;
      return `<p><strong>Insight ${index + 1}:</strong> The highest risk group is ${row.age_group || row.AGE_GROUP || "Unknown"} ${row.road_user_type || row.ROAD_USER_TYPE || "road user"} with ${count} incidents — ${diffPercent >= 0 ? "+" : ""}${diffPercent.toFixed(1)}% above average.</p>`;
    })
    .join("");
}

function fetchPeopleSummary() {
  const loading = document.getElementById("people-loading");
  const error = document.getElementById("people-error");
  const emptyMessage = document.getElementById("people-empty");
  const table = document.getElementById("people-table");
  const resultCount = document.getElementById("result-count");
  const summaryGrid = document.getElementById("summary-grid");

  if (!loading || !error || !emptyMessage || !table || !resultCount || !summaryGrid) {
    return;
  }

  loading.hidden = false;
  error.hidden = true;
  emptyMessage.hidden = true;
  table.hidden = true;

  const params = new URLSearchParams();
  const injuryLevel = document.getElementById("injury-level-select").value;
  const ageGroup = document.getElementById("age-group-select").value;
  const roadUser = document.getElementById("road-user-select").value;

  if (injuryLevel && injuryLevel !== "All") {
    params.set("injury_level", injuryLevel);
  }
  if (ageGroup && ageGroup !== "All") {
    params.set("age_group", ageGroup);
  }
  if (roadUser && roadUser !== "All") {
    params.set("road_user_type", roadUser);
  }

  fetch(`/api/people-summary?${params.toString()}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      loading.hidden = true;
      renderPeopleSummary(data);
    })
    .catch((fetchError) => {
      loading.hidden = true;
      error.hidden = false;
      error.textContent = `Unable to load people summary. ${fetchError.message}`;
    });
}

function renderPeopleSummary(data) {
  const table = document.getElementById("people-table");
  const tbody = table.querySelector("tbody");
  const resultCount = document.getElementById("result-count");
  const emptyMessage = document.getElementById("people-empty");
  const summaryGrid = document.getElementById("summary-grid");

  if (!Array.isArray(data) || data.length === 0) {
    tbody.innerHTML = "";
    table.hidden = true;
    resultCount.textContent = "Showing 0 results";
    summaryGrid.innerHTML = "";
    emptyMessage.hidden = false;
    return;
  }

  const sortedData = data.slice().sort((a, b) => b.total_people - a.total_people);
  const totalPeople = sortedData.reduce((sum, item) => sum + Number(item.total_people || 0), 0);
  const totalHospital = sortedData.reduce((sum, item) => sum + Number(item.hospital_count || 0), 0);
  const totalRows = sortedData.length;
  const admissionRate = totalPeople ? ((totalHospital / totalPeople) * 100).toFixed(1) : "0.0";

  resultCount.textContent = `Showing ${totalRows} results`;
  summaryGrid.innerHTML = `
    <div class="summary-card">
      <span class="summary-label">Total Records</span>
      <strong>${totalRows}</strong>
    </div>
    <div class="summary-card">
      <span class="summary-label">Total People</span>
      <strong>${totalPeople}</strong>
    </div>
    <div class="summary-card">
      <span class="summary-label">Overall Hospital Admission Rate</span>
      <strong>${admissionRate}%</strong>
    </div>
  `;

  tbody.innerHTML = sortedData
    .map((row) => {
      const hospitalRate = row.total_people ? `${((row.hospital_count / row.total_people) * 100).toFixed(1)}%` : "0.0%";
      const injuryClass = getInjuryLevelClass(row.INJ_LEVEL || row.injury_level || "");
      return `
        <tr>
          <td>${row.ROAD_USER_TYPE || row.road_user_type || "Unknown"}</td>
          <td><span class="level-badge ${injuryClass}">${row.INJ_LEVEL || row.injury_level || "Unknown"}</span></td>
          <td>${row.total_people || 0}</td>
          <td>${row.hospital_count || 0}</td>
          <td>${row.ejected_count || 0}</td>
          <td>${hospitalRate}</td>
        </tr>
      `;
    })
    .join("");

  table.hidden = false;
  emptyMessage.hidden = true;
}

function getInjuryLevelClass(level) {
  const normalized = String(level).trim().toLowerCase();
  if (normalized === "fatal") {
    return "level-fatal";
  }
  if (normalized.includes("serious")) {
    return "level-serious";
  }
  if (normalized.includes("not injured") || normalized === "not injured") {
    return "level-not-injured";
  }
  return "level-other";
}

function resetPeopleFilters() {
  const injuryLevel = document.getElementById("injury-level-select");
  const ageGroup = document.getElementById("age-group-select");
  const roadUser = document.getElementById("road-user-select");

  if (injuryLevel) {
    injuryLevel.value = "All";
  }
  if (ageGroup) {
    ageGroup.value = "All";
  }
  if (roadUser) {
    roadUser.value = "All";
  }
}

function loadPersonas() {
  const container = document.getElementById("persona-grid");
  const loading = document.getElementById("persona-loading");
  const error = document.getElementById("persona-error");

  if (!container || !loading || !error) {
    return;
  }

  fetch("/api/personas")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }
      return response.json();
    })
    .then((personas) => {
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
    })
    .catch((fetchError) => {
      loading.hidden = true;
      error.hidden = false;
      error.textContent = `Unable to load personas. ${fetchError.message}`;
    });
}

function loadTeamMembers() {
  const table = document.getElementById("team-table");
  const tbody = table ? table.querySelector("tbody") : null;
  const loading = document.getElementById("team-loading");
  const error = document.getElementById("team-error");

  if (!table || !tbody || !loading || !error) {
    return;
  }

  fetch("/api/team-members")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }
      return response.json();
    })
    .then((teamMembers) => {
      loading.hidden = true;
      if (!Array.isArray(teamMembers) || teamMembers.length === 0) {
        error.hidden = false;
        error.textContent = "No team members were found.";
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
    })
    .catch((fetchError) => {
      loading.hidden = true;
      error.hidden = false;
      error.textContent = `Unable to load team members. ${fetchError.message}`;
    });
}

