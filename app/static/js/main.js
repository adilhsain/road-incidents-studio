document.addEventListener("DOMContentLoaded", () => {
  loadPersonas();
  loadTeamMembers();
});

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

