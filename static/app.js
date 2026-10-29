/* Freelancer Expense Tracker — frontend.
   Vanilla JavaScript. Talks to the Flask API, renders the UI, keeps state
   in sync with the server. No framework — just fetch + DOM. */

const API_BASE = "/api/expenses";
const form = document.getElementById("expense-form");
const formError = document.getElementById("form-error");
const expenseDate = document.getElementById("expense-date");
const expensesBody = document.getElementById("expenses-body");
const tableWrap = document.getElementById("table-wrap");
const emptyState = document.getElementById("empty-state");
const expenseCount = document.getElementById("expense-count");
const summaryGrid = document.getElementById("summary-grid");

// Default the date field to today so the user can add with one less click.
expenseDate.value = new Date().toISOString().split("T")[0];

// ---------------------------------------------------------------------------
// Fetch + render
// ---------------------------------------------------------------------------

async function loadExpenses() {
  const res = await fetch(API_BASE);
  const data = await res.json();

  renderSummary(data);
  renderTable(data.expenses, data.grand_total);
}

function renderSummary(data) {
  summaryGrid.innerHTML = `
    <div class="stat-card">
      <div class="stat-label">Total expenses</div>
      <div class="stat-value">₹${data.grand_total.toFixed(2)}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Number of expenses</div>
      <div class="stat-value">${data.count}</div>
    </div>
  `;

  const categoryCards = data.categories
    .map(
      (c) => `
      <div class="stat-card">
        <div class="stat-label">${escapeHtml(c.category)}</div>
        <div class="stat-value">₹${c.total.toFixed(2)}</div>
        <div style="font-size:12px;color:#6b7280;margin-top:4px;">
          ${c.count} ${c.count === 1 ? "expense" : "expenses"}
        </div>
      </div>
    `
    )
    .join("");

  summaryGrid.innerHTML += categoryCards;
}

function renderTable(expenses) {
  expenseCount.textContent = expenses.length;

  if (expenses.length === 0) {
    tableWrap.style.display = "none";
    emptyState.style.display = "block";
    expensesBody.innerHTML = "";
    return;
  }

  tableWrap.style.display = "block";
  emptyState.style.display = "none";

  expensesBody.innerHTML = expenses
    .map(
      (e) => `
      <tr>
        <td>${formatDate(e.expense_date)}</td>
        <td>${escapeHtml(e.category)}</td>
        <td>${escapeHtml(e.description) || "—"}</td>
        <td class="numeric">₹${Number(e.amount).toFixed(2)}</td>
        <td class="numeric actions">
          <button class="btn btn-danger" onclick="deleteExpense(${e.id})" title="Delete">
            Delete
          </button>
        </td>
      </tr>
    `
    )
    .join("");
}

// ---------------------------------------------------------------------------
// Actions
// ---------------------------------------------------------------------------

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.textContent = "";

  const payload = {
    amount: form.amount.value,
    category: form.category.value,
    description: form.description.value,
    expense_date: form.expense_date.value,
  };

  try {
    const res = await fetch(API_BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      formError.textContent =
        (data.details && data.details.join(", ")) || data.error || "Failed to add expense.";
      return;
    }

    form.reset();
    expenseDate.value = new Date().toISOString().split("T")[0];
    await loadExpenses();
  } catch (err) {
    formError.textContent = "Network error. Is the server running?";
    console.error(err);
  }
});

window.deleteExpense = async function (id) {
  if (!confirm("Delete this expense?")) return;

  try {
    const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
    if (!res.ok) {
      alert("Failed to delete expense.");
      return;
    }
    await loadExpenses();
  } catch (err) {
    alert("Network error. Is the server running?");
    console.error(err);
  }
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function escapeHtml(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Initial load.
loadExpenses();
