/* ============================================================
   Expense Categorizer — Dashboard Logic
   ============================================================ */

const API = window.location.origin;

// ---------- State ----------
let monthlyData = [];
let monthChart, donutChart, barChart;

// ---------- Sidebar navigation ----------
document.querySelectorAll('.nav-item').forEach((item) => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        switchView(item.dataset.view);
    });
});

function switchView(view) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));

    document.querySelector(`.nav-item[data-view="${view}"]`)?.classList.add('active');
    document.getElementById(`view-${view}`)?.classList.add('active');

    const titles = {
        dashboard: 'Dashboard',
        transactions: 'Transactions',
        upload: 'Upload',
        reports: 'Reports',
        notes: 'Notes',
        settings: 'Settings',
    };
    document.getElementById('page-title').textContent = titles[view] || 'Dashboard';

    if (view === 'dashboard') loadDashboard();
    if (view === 'transactions') loadTransactions();
    if (view === 'notes') loadNotes();
}

document.getElementById('btn-upload').addEventListener('click', () => switchView('upload'));
document.getElementById('btn-view-all').addEventListener('click', () => switchView('transactions'));

// ---------- Year selector ----------
const yearSelect = document.getElementById('year-select');
yearSelect.addEventListener('change', () => {
    ['kpi-year', 'kpi-year-2', 'dist-year', 'cmp-year', 'recent-year'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = yearSelect.value;
    });
    const sub = document.getElementById('dashboard-sub');
    if (sub) sub.textContent = `Spending for ${yearSelect.value}, built from your monthly reports.`;
    loadDashboard();
});

// ---------- Upload form ----------
const dropzone    = document.getElementById('dropzone');
const fileInput   = document.getElementById('file-input');
const fileLabel   = document.getElementById('file-label');
const uploadForm  = document.getElementById('upload-form');
const uploadBtn   = document.getElementById('upload-btn');
const uploadStatus= document.getElementById('upload-status');

let selectedFile = null;

dropzone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) { selectedFile = e.target.files[0]; updateDropzone(); }
});
['dragover', 'dragenter'].forEach(ev => dropzone.addEventListener(ev, (e) => {
    e.preventDefault(); dropzone.classList.add('dragover');
}));
['dragleave', 'drop'].forEach(ev => dropzone.addEventListener(ev, () => dropzone.classList.remove('dragover')));
dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
        selectedFile = e.dataTransfer.files[0];
        fileInput.files = e.dataTransfer.files;
        updateDropzone();
    }
});

function updateDropzone() {
    if (selectedFile) {
        fileLabel.textContent = `✓ ${selectedFile.name}`;
        dropzone.classList.add('has-file');
    }
}

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!selectedFile) return setStatus(uploadStatus, 'Please select a CSV first.', 'error');

    const fd = new FormData();
    fd.append('file', selectedFile);

    uploadBtn.disabled = true;
    setStatus(uploadStatus, 'Uploading and processing…', 'loading');

    try {
        const res = await fetch(`${API}/upload_csv`, { method: 'POST', body: fd });
        const data = await res.json();
        if (res.ok) {
            setStatus(uploadStatus, ` ${data.message} (${data.records_inserted} records)`, 'success');
            loadDashboard();
        } else {
            setStatus(uploadStatus, ` ${data.error || 'Upload failed'}`, 'error');
        }
    } catch (err) {
        setStatus(uploadStatus, `❌ Network error: ${err.message}`, 'error');
    } finally {
        uploadBtn.disabled = false;
    }
});

// ---------- Dashboard load ----------
async function loadDashboard() {
    const year = parseInt(yearSelect.value, 10);
    monthlyData = [];

    const requests = [];
    for (let m = 1; m <= 12; m++) {
        requests.push(
            fetch(`${API}/monthly_report/${m}/${year}`)
                .then(r => r.ok ? r.json() : [])
                .then(data => {
                    const total = data.reduce((s, r) => s + parseFloat(r.total || 0), 0);
                    monthlyData.push({ month: m, total, categories: data });
                })
                .catch(() => monthlyData.push({ month: m, total: 0, categories: [] }))
        );
    }
    await Promise.all(requests);
    monthlyData.sort((a, b) => a.month - b.month);

    renderKPIs();
    renderCharts();
    renderRecent();
}

function renderKPIs() {
    const total = monthlyData.reduce((s, m) => s + m.total, 0);
    document.getElementById('kpi-total').textContent = formatINR(total);
    document.getElementById('donut-total').textContent = formatINR(total);

    const withData = monthlyData.filter(m => m.total > 0);
    const latest = withData[withData.length - 1];
    document.getElementById('kpi-latest-total').textContent = latest ? formatINR(latest.total) : '—';
    document.getElementById('kpi-latest-month').textContent = latest
        ? `${monthName(latest.month)} ${yearSelect.value}` : 'No data yet';

    const catTotals = {};
    monthlyData.forEach(m => m.categories.forEach(c => {
        catTotals[c.category] = (catTotals[c.category] || 0) + parseFloat(c.total || 0);
    }));
    const top = Object.entries(catTotals).sort((a, b) => b[1] - a[1])[0];
    if (top) {
        const pct = total ? Math.round((top[1] / total) * 100) : 0;
        document.getElementById('kpi-top-cat').textContent = top[0];
        document.getElementById('kpi-top-cat-sub').textContent = `${formatINR(top[1])} · ${pct}% of spend`;
    } else {
        document.getElementById('kpi-top-cat').textContent = '—';
        document.getElementById('kpi-top-cat-sub').textContent = 'No data yet';
    }

    fetch(`${API}/transactions?year=${yearSelect.value}`)
        .then(r => r.ok ? r.json() : Promise.reject())
        .then(rows => {
            document.getElementById('kpi-count').textContent = rows.length;
            document.getElementById('kpi-count-note').textContent = `${yearSelect.value}`;
            const avg = rows.length ? rows.reduce((s, r) => s + parseFloat(r.amount || 0), 0) / rows.length : 0;
            document.getElementById('kpi-avg').textContent = formatINR(avg);
            document.getElementById('kpi-avg-note').textContent = `${yearSelect.value}`;
        })
        .catch(() => {
            document.getElementById('kpi-count').textContent = '—';
            document.getElementById('kpi-count-note').textContent = 'Needs GET /transactions';
            document.getElementById('kpi-avg').textContent = '—';
            document.getElementById('kpi-avg-note').textContent = 'Needs GET /transactions';
        });
}

function renderCharts() {
    // ---------- Monthly bar chart ----------
    const ctx1 = document.getElementById('chart-months').getContext('2d');
    monthChart?.destroy();
    monthChart = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            datasets: [{
                data: monthlyData.map(m => m.total),
                backgroundColor: '#1e293b',
                borderRadius: 4,
                maxBarThickness: 26,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1e293b',
                    padding: 10,
                    callbacks: {
                        label: (ctx) => `Spent: ${formatINR(ctx.parsed.y)}`
                    }
                }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#9ca3af', font: { size: 11 } } },
                y: {
                    grid: { color: '#f1f5f9' },
                    ticks: {
                        color: '#9ca3af', font: { size: 11 },
                        callback: (v) => '₹' + (v >= 1000 ? (v/1000) + 'k' : v)
                    }
                }
            }
        }
    });

    // ---------- Donut ----------
    const catTotals = {};
    monthlyData.forEach(m => m.categories.forEach(c => {
        catTotals[c.category] = (catTotals[c.category] || 0) + parseFloat(c.total || 0);
    }));
    const catLabels = Object.keys(catTotals);
    const catValues = Object.values(catTotals);
    const colors = ['#8b5cf6', '#f97316', '#3b82f6', '#10b981', '#ef4444'];
    const total = catValues.reduce((a, b) => a + b, 0);

    const ctx2 = document.getElementById('chart-donut').getContext('2d');
    donutChart?.destroy();
    donutChart = new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: catLabels,
            datasets: [{
                data: catValues,
                backgroundColor: colors.slice(0, catLabels.length),
                borderWidth: 0,
                cutout: '70%',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: { label: (ctx) => `${ctx.label}: ${formatINR(ctx.parsed)}` }
                }
            }
        }
    });

    const legend = document.getElementById('donut-legend');
    legend.innerHTML = '';
    catLabels.forEach((label, i) => {
        const pct = total ? Math.round((catValues[i] / total) * 100) : 0;
        const item = document.createElement('div');
        item.className = 'legend-item';
        item.innerHTML = `
            <span class="swatch" style="background:${colors[i]}"></span>
            <span class="name">${label}</span>
            <span class="pct">${pct}%</span>
            <span class="val">${formatINR(catValues[i])}</span>
        `;
        legend.appendChild(item);
    });

    // ---------- Horizontal bars ----------
    const ctx3 = document.getElementById('chart-bars').getContext('2d');
    barChart?.destroy();
    barChart = new Chart(ctx3, {
        type: 'bar',
        data: {
            labels: catLabels,
            datasets: [{
                data: catValues,
                backgroundColor: colors.slice(0, catLabels.length),
                borderRadius: 6,
                maxBarThickness: 22,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    grid: { color: '#f1f5f9' },
                    ticks: {
                        color: '#9ca3af', font: { size: 11 },
                        callback: (v) => '₹' + (v >= 1000 ? (v/1000) + 'k' : v)
                    }
                },
                y: { grid: { display: false }, ticks: { color: '#374151', font: { size: 12, weight: '600' } } }
            }
        }
    });
}

// ---------- Recent transactions (unique merchants first) ----------
async function renderRecent() {
    const list = document.getElementById('recent-list');
    try {
        const res = await fetch(`${API}/transactions?year=${yearSelect.value}`);
        if (!res.ok) throw new Error();
        const rows = await res.json();

        if (!rows.length) {
            list.innerHTML = `
                <div class="empty-state">
                    <div class="empty-title">No transactions yet</div>
                    <div class="empty-sub">Upload a CSV to see your recent activity here.</div>
                </div>`;
            return;
        }

        // Prefer 5 distinct merchants; fall back to most recent
        const seen = new Set();
        const unique = [];
        for (const r of rows.slice().reverse()) {
            if (!seen.has(r.merchant)) {
                seen.add(r.merchant);
                unique.push(r);
            }
            if (unique.length === 5) break;
        }
        const toShow = unique.length < 5
            ? rows.slice().reverse().slice(0, 5)
            : unique;

        list.innerHTML = toShow.map(r => `
            <div class="txn-row">
                <div class="txn-icon">${(r.merchant || '?').charAt(0).toUpperCase()}</div>
                <div>
                    <div class="txn-merchant">${r.merchant}</div>
                    <div class="txn-meta">${r.date} · ${r.payment_method || '—'}</div>
                </div>
                <span class="badge ${r.category}">${r.category}</span>
                <span class="txn-amount">${formatINR(r.amount)}</span>
            </div>
        `).join('');
    } catch {
        list.innerHTML = `
            <div class="empty-state">
                <div class="empty-title">Backend endpoint required</div>
                <div class="empty-sub">Add <code>GET /transactions</code> to your Flask backend to see live data here.</div>
            </div>`;
    }
}

// ---------- Transactions view ----------
async function loadTransactions() {
    const tbody = document.getElementById('txn-tbody');
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:24px">Loading…</td></tr>`;
    try {
        const res = await fetch(`${API}/transactions?year=${yearSelect.value}`);
        if (!res.ok) throw new Error('Endpoint not available');
        const rows = await res.json();
        if (!rows.length) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:24px">No transactions</td></tr>`;
            return;
        }
        tbody.innerHTML = rows.map(r => `
            <tr>
                <td>${r.id}</td>
                <td>${r.date}</td>
                <td>${r.merchant}</td>
                <td><span class="badge ${r.category}">${r.category}</span></td>
                <td>${r.payment_method || '—'}</td>
                <td style="text-align:right;font-weight:600">${formatINR(r.amount)}</td>
            </tr>
        `).join('');
    } catch {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:24px;color:#ef4444">
            Add <code>GET /transactions</code> to your Flask backend to enable this view.
        </td></tr>`;
    }
}

// ---------- Notes view ----------
async function loadNotes() {
    const list = document.getElementById('notes-list');
    try {
        const res = await fetch(`${API}/notes`);
        if (!res.ok) throw new Error();
        const notes = await res.json();
        if (!notes.length) throw new Error();
        list.innerHTML = notes.map(n => `
            <div class="txn-row">
                <div class="txn-icon">${(n.merchant || '?').charAt(0)}</div>
                <div>
                    <div class="txn-merchant">${n.merchant}</div>
                    <div class="txn-meta">${n.notes || '(no note)'}</div>
                </div>
                <span class="badge ${n.category}">${n.category}</span>
                <span class="txn-amount">${formatINR(n.amount)}</span>
            </div>
        `).join('');
    } catch {
        list.innerHTML = `
            <div class="empty-state">
                <div class="empty-title">Notes endpoint required</div>
                <div class="empty-sub">Add <code>GET /notes</code> to your Flask backend to enable this view.</div>
            </div>`;
    }
}

// ---------- Reports view ----------
document.getElementById('report-btn').addEventListener('click', async () => {
    const month = document.getElementById('month-select').value;
    const year  = document.getElementById('report-year').value;
    const status= document.getElementById('report-status');
    const cards = document.getElementById('report-cards');

    cards.innerHTML = '';
    setStatus(status, 'Loading…', 'loading');

    try {
        const res = await fetch(`${API}/monthly_report/${month}/${year}`);
        const data = await res.json();
        if (!res.ok) return setStatus(status, `❌ ${data.error}`, 'error');
        if (!data.length) return setStatus(status, 'No expenses for this month.', 'error');

        setStatus(status, `✅ ${data.length} categories`, 'success');
        cards.innerHTML = data.map(d => `
            <div class="report-item">
                <div class="category">${d.category}</div>
                <div class="total">${formatINR(d.total)}</div>
            </div>
        `).join('');
    } catch (err) {
        setStatus(status, `❌ ${err.message}`, 'error');
    }
});

// ---------- Server status ----------
async function pingServer() {
    const pill = document.getElementById('server-status');
    const text = document.getElementById('server-status-text');
    try {
        const res = await fetch(`${API}/`, { method: 'HEAD' });
        pill.classList.toggle('offline', !res.ok);
        text.textContent = res.ok ? 'Server reachable' : 'Server offline';
    } catch {
        pill.classList.add('offline');
        text.textContent = 'Server offline';
    }
}

// ---------- Helpers ----------
function formatINR(n) {
    const num = parseFloat(n) || 0;
    return '₹' + num.toLocaleString('en-IN', { maximumFractionDigits: 2 });
}

function monthName(m) {
    return ['January','February','March','April','May','June','July','August','September','October','November','December'][m-1];
}

function setStatus(el, msg, type) {
    el.textContent = msg;
    el.className = `status ${type || ''}`;
}

// ---------- Initial load ----------
pingServer();
loadDashboard();
setInterval(pingServer, 15000);