const icons = {
  aster: '<path d="M12 2v20M2 12h20M4.9 4.9l14.2 14.2m0-14.2L4.9 19.1"/>',
  overview: '<rect x="3" y="3" width="7" height="7" rx="1.2"/><rect x="14" y="3" width="7" height="7" rx="1.2"/><rect x="3" y="14" width="7" height="7" rx="1.2"/><rect x="14" y="14" width="7" height="7" rx="1.2"/>',
  accounts: '<path d="M20 8V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2v-2M3 8h15a2 2 0 0 1 2 2v1"/><path d="M17 10h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-4a3 3 0 0 1 0-6Z"/><path d="M17 13h.01"/>',
  activity: '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  statements: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Zm0 0v6h6M8 12h8m-8 4h8"/>',
  notifications: '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9m-8 12a2 2 0 0 0 4 0"/>',
  demo: '<path d="M9 3h6m-5 0v6l-5.5 8.8A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-3.2L14 9V3M8 15h8"/>',
  admin: '<path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z"/><path d="m9 12 2 2 4-4"/>',
  transfer: '<path d="M4 7h15m-4-4 4 4-4 4M20 17H5m4-4-4 4 4 4"/>',
  send: '<path d="M7 17 17 7M7 7h10v10"/>',
  receive: '<path d="M17 7 7 17m10 0H7V7"/>',
  deposit: '<path d="M12 4v12m-5-5 5 5 5-5M4 19v1h16v-1"/>',
  withdraw: '<path d="M12 16V4m-5 5 5-5 5 5M4 19v1h16v-1"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  chevron: '<path d="m6 9 6 6 6-6"/>',
  right: '<path d="m9 18 6-6-6-6"/>',
  arrow: '<path d="M4 12h15m-6-6 6 6-6 6"/>',
  close: '<path d="m6 6 12 12M18 6 6 18"/>',
  check: '<path d="m5 12 4 4L19 6"/>',
  lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 1 1 8 0v3m-4 5v2"/>',
  savings: '<path d="M18.4 8a6 6 0 0 0-4.1-3H11a6 6 0 0 0-5.7 4L3 10v5l2.5.5L7 19h3l1-2h3l1 2h3l1.4-3.5A5 5 0 0 0 22 12h-2.5m-5-4h-4m-3 3h.01"/><path d="M16 5c.5-1.2 1.6-2 3-2v5"/>',
  current: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h3"/>',
  fixed: '<path d="M3 10 12 4l9 6H3Zm1 10h16M6 12v5m6-5v5m6-5v5"/>',
  history: '<path d="M3 12a9 9 0 1 1 9 9 9 9 0 0 1-6.4-2.6M3 6v6h6m3-4v5l3 2"/>',
  download: '<path d="M12 3v12m-5-5 5 5 5-5M4 16v4h16v-4"/>',
  email: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
  phone: '<rect x="6" y="3" width="12" height="18" rx="2"/><path d="M11 17h2"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5m0-8h.01"/>',
  warning: '<path d="M11 4 3 19h18L13 4a1.2 1.2 0 0 0-2 0Zm1 6v4m0 2.5h.01"/>',
  user: '<circle cx="12" cy="8" r="3"/><path d="M5 20v-2a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v2"/>',
  logout: '<path d="M10 17v3H5V4h5v3m-1 5h12m-4-4 4 4-4 4"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4m10-4v4M3 10h18"/>',
  search: '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/>',
  chart: '<path d="M3 4v16h18M7 15l4-5 4 3 5-6"/>',
  menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
  more: '<path d="M5 12h.01M12 12h.01M19 12h.01" stroke-width="3"/>',
  play: '<path d="m9 5 11 7-11 7V5Z"/>',
};

const icon = (name, size = 20) => `<svg aria-hidden="true" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">${icons[name] ?? icons.info}</svg>`;
const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, part => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[part]));

const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
const shortDate = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'Asia/Karachi' });
const alertDate = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZone: 'Asia/Karachi' });
const localDate = new Intl.DateTimeFormat('en-CA', { month: '2-digit', day: '2-digit', year: 'numeric', timeZone: 'Asia/Karachi' });
const money = value => currency.format(Number(value ?? 0) / 100);
const prettyDate = (value, format = shortDate) => {
  const date = new Date(value);
  return Number.isNaN(+date) ? '—' : format.format(date);
};
const signedMoney = value => `${value < 0 ? '−' : '+'}${money(Math.abs(value))}`;
const initials = value => String(value ?? '').trim().split(/\s+/).slice(0, 2).map(part => part[0]?.toUpperCase()).join('');
const dateKey = (value = Date.now()) => {
  const date = new Date(value);
  if (Number.isNaN(+date)) return '';
  const parts = Object.fromEntries(localDate.formatToParts(date).map(({ type, value }) => [type, value]));
  return `${parts.year}-${parts.month}-${parts.day}`;
};
const monthStart = () => `${dateKey().slice(0, 7)}-01`;
const ledgerDate = tx => tx.date || dateKey(tx.at);

function readAmount(value) {
  const match = /^(\d+)(?:\.(\d{1,2}))?$/.exec(String(value).trim());
  if (!match) throw new Error('Enter an amount with up to two decimal places.');
  const amount = Number(match[1]) * 100 + Number((match[2] ?? '').padEnd(2, '0'));
  if (!Number.isSafeInteger(amount) || amount < 1) throw new Error('Enter an amount greater than zero.');
  return amount;
}

async function request(path, { method = 'GET', data } = {}) {
  let response;
  try {
    response = await fetch(path, {
      method,
      credentials: 'same-origin',
      headers: data === undefined ? undefined : { 'Content-Type': 'application/json' },
      body: data === undefined ? undefined : JSON.stringify(data),
    });
  } catch {
    throw new Error('Aster Bank is temporarily unavailable. Try again.');
  }
  const result = await response.json().catch(() => ({}));
  if (!response.ok || result.ok === false) {
    const error = new Error(result.error?.message ?? (typeof result.error === 'string' ? result.error : result.message) ?? 'The request could not be completed.');
    error.status = response.status;
    error.code = result.code ?? result.error?.code;
    throw error;
  }
  return result;
}

const post = (path, data = {}) => request(path, { method: 'POST', data });

icons.eye = '<path d="M2 12s3.7-6 10-6 10 6 10 6-3.7 6-10 6-10-6-10-6Z"/><circle cx="12" cy="12" r="2.5"/>';
icons.eyeOff = '<path d="m3 3 18 18M10.6 6.1 12 6c6.3 0 10 6 10 6a16 16 0 0 1-3 3.1M6.4 7.5A17 17 0 0 0 2 12s3.7 6 10 6a12 12 0 0 0 4.4-.8"/>';
icons.reset = '<path d="M5 5v5h5M5.5 10a7 7 0 1 1 1 7"/>';
icons.filter = '<path d="M4 7h16M7 12h10m-7 5h4"/>';
icons.clock = '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>';

const shell = document.querySelector('#app-shell');
const view = document.querySelector('#view');
const auth = document.querySelector('#auth-view');
const dialog = document.querySelector('#bank-dialog');
const toasts = document.querySelector('#toasts');

const pageNames = {
  overview: 'Overview',
  accounts: 'Accounts',
  activity: 'Activity',
  statements: 'Statements',
  notifications: 'Notifications',
  demo: 'Demo Lab',
  admin: 'Admin workspace',
};
const productNames = { savings: 'Savings', current: 'Current', fixed: 'Fixed Deposit' };
const transactionNames = {
  deposit: 'Deposit', withdraw: 'Withdrawal', transfer: 'Transfer',
  reversal: 'Reversal', interest: 'Interest', fee: 'Service fee',
};
const demoUsers = {
  customer: { name: 'Ayesha Khan', email: 'ayesha@aster.demo', credential: '123456', role: 'Customer' },
  recipient: { name: 'Omar Malik', email: 'omar@aster.demo', credential: '234567', role: 'Customer' },
  teller: { name: 'Hamza Ali', email: 'teller@aster.demo', credential: '112233', role: 'Bank Teller' },
  admin: { name: 'Sara Ahmed', email: 'admin@aster.demo', credential: '654321', role: 'Bank Admin' },
};
const sampleAccounts = { savings: '10003482', current: '10007061', recipient: '10005619' };
const state = {
  dashboard: null,
  page: 'overview',
  hideBalance: false,
  activityType: 'all',
  activitySearch: '',
  inputAccount: null,
  statement: { accountId: '', start: monthStart(), end: dateKey(), generated: false },
  readAlerts: new Set(),
  demo: { results: {}, transferId: '', running: null },
};

function remember(key, value) {
  try {
    if (value === undefined) return localStorage.getItem(key);
    localStorage.setItem(key, value);
  } catch {
    return null;
  }
}

const data = () => state.dashboard;
const user = () => data()?.user;
const accounts = () => data()?.accounts ?? [];
const accountById = id => accounts().find(account => String(account.id) === String(id));
const isAdmin = () => user()?.role === 'admin';
const isTeller = () => user()?.role === 'teller';
const permissions = () => isAdmin() ? [] : isTeller() ? ['deposit'] : ['deposit','withdraw','transfer'];
const typeLabel = type => productNames[type] ?? type;
const lastFour = id => String(id).slice(-4);
const mask = id => `•••• ${lastFour(id)}`;
const sortedTransactions = (items = data()?.transactions ?? []) => [...items].sort((a, b) => b.at.localeCompare(a.at));
const totalBalance = () => accounts().reduce((total, account) => total + (account.balance ?? 0), 0);
const ownAccountIds = () => new Set(accounts().map(account => String(account.id)));
const userRole = () => isAdmin() ? 'Bank Admin' : isTeller() ? 'Bank Teller' : 'Customer';

function applyDashboard(dashboard) {
  if (!dashboard?.user || !Array.isArray(dashboard.accounts)) throw new Error('The dashboard data could not be loaded.');
  if (user()?.id !== dashboard.user.id) {
    state.readAlerts = new Set();
    state.statement = { accountId: '', start: monthStart(), end: dateKey(), generated: false };
    state.activityType = 'all';
    state.activitySearch = '';
  }
  state.dashboard = dashboard;
}

function go(page, { focus = true } = {}) {
  if (!Object.hasOwn(pageNames, page) || (page === 'admin' && !isAdmin()) || (page === 'statements' && isTeller())) page = 'overview';
  state.page = page;
  render();
  if (focus) {
    const heading = view.querySelector('h1');
    heading?.setAttribute('tabindex', '-1');
    heading?.focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }
}

function setNavigation() {
  for (const item of shell.querySelectorAll('[data-view]')) {
    const inSidebar = item.closest('nav') && !view.contains(item);
    if (!inSidebar) continue;
    const current = item.dataset.view === state.page;
    item.classList.toggle('is-active', current);
    item.setAttribute('aria-label', pageNames[item.dataset.view]);
    if (item.dataset.view === 'statements') item.hidden = isTeller();
    if (current) item.setAttribute('aria-current', 'page');
    else item.removeAttribute('aria-current');
  }
  const profile = document.querySelector('#profile-copy');
  if (profile) {
    profile.innerHTML = `<span class="profile-avatar">${escapeHtml(initials(user().name))}</span><span class="profile-details"><strong>${escapeHtml(user().name)}</strong><small>${userRole()}</small></span>`;
  }
  const profileButton = document.querySelector('#profile-button');
  if (profileButton) profileButton.disabled = Boolean(state.demo.running);
  const admin = document.querySelector('#sidebar-admin');
  if (admin) admin.hidden = !isAdmin();
  const unread = (data().notifications ?? []).filter(alert => !state.readAlerts.has(alert.id)).length;
  const count = document.querySelector('#nav-notification-count');
  if (count) {
    count.textContent = unread;
    count.hidden = unread === 0;
  }
  const dot = document.querySelector('#header-notification-dot');
  if (dot) dot.hidden = !unread;
  const pageLabel = document.querySelector('#header-view-name');
  if (pageLabel) pageLabel.textContent = pageNames[state.page];
}

function pageHeading(title, subtitle, action = '') {
  return `<header class="view-heading"><div><h1 class="view-title">${escapeHtml(title)}</h1><p class="view-description">${escapeHtml(subtitle)}</p></div>${action}</header>`;
}

const btn = (label, attrs, iconName, style = 'secondary') =>
  `<button type="button" class="${style}-btn" ${attrs}>${iconName ? icon(iconName, 17) : ''}<span>${escapeHtml(label)}</span></button>`;
const sectionHead = (title, action = '') => `<div class="panel-head"><h2 class="panel-title">${escapeHtml(title)}</h2>${action}</div>`;
const empty = (title, detail, glyph = 'activity') => `<div class="empty-state"><span class="empty-icon">${icon(glyph, 24)}</span><strong>${escapeHtml(title)}</strong><p>${escapeHtml(detail)}</p></div>`;
const statusPill = (label, tone = 'success') => `<span class="status-pill ${tone}">${escapeHtml(label)}</span>`;
const displayBalance = amount => state.hideBalance ? '••••••' : money(amount);

function showToast(message, tone = 'success') {
  if (!toasts) return;
  const element = document.createElement('div');
  element.className = `toast ${tone}`;
  element.setAttribute('role', tone === 'error' ? 'alert' : 'status');
  element.innerHTML = `${icon(tone === 'error' ? 'warning' : 'check', 18)}<span>${escapeHtml(message)}</span><button type="button" class="icon-btn" data-close-toast aria-label="Dismiss notification">${icon('close', 16)}</button>`;
  toasts.append(element);
  window.setTimeout(() => element.remove(), 6500);
}

function balanceChart() {
  const labels = new Intl.DateTimeFormat('en-US', { weekday: 'short', timeZone: 'Asia/Karachi' });
  const days = Array.from({ length: 7 }, (_, i) => new Date(Date.now() - (6 - i) * 864e5));
  const ids = ownAccountIds();
  const changes = new Map();
  for (const tx of data().transactions ?? []) {
    const day = ledgerDate(tx);
    const net = tx.entries.reduce((sum, entry) => sum + (ids.has(String(entry.accountId)) ? entry.amount : 0), 0);
    changes.set(day, (changes.get(day) ?? 0) + net);
  }
  let balance = totalBalance();
  const values = days.map(day => dateKey(day)).reverse().map(key => {
    const close = balance;
    balance -= changes.get(key) ?? 0;
    return close;
  }).reverse();
  const low = Math.min(...values);
  const high = Math.max(...values);
  const range = Math.max(high - low, 1);
  const width = 600;
  const points = values.map((value, i) => [i * (width - 12) / 6 + 6, high === low ? 49 : 76 - (value - low) / range * 62]);
  let path = `M${points[0].join(',')}`;
  for (let i = 1; i < points.length; i++) {
    const [oldX, oldY] = points[i - 1];
    const [x, y] = points[i];
    const mid = (oldX + x) / 2;
    path += `C${mid},${oldY} ${mid},${y} ${x},${y}`;
  }
  const [endX, endY] = points.at(-1);
  const title = state.hideBalance ? 'Seven-day balance trend' : `Seven-day balance ranged from ${money(low)} to ${money(high)}`;
  return `<div class="balance-chart">
    <svg viewBox="0 0 600 88" preserveAspectRatio="none" role="img" aria-label="${escapeHtml(title)}">
      <defs><linearGradient id="balance-fill" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#a98dff" stop-opacity=".28"/><stop offset="1" stop-color="#a98dff" stop-opacity=".01"/></linearGradient></defs>
      <path class="chart-gridlines" d="M0 12H600M0 35H600M0 58H600M0 82H600" fill="none" stroke="#eae5f5" stroke-dasharray="3 4" vector-effect="non-scaling-stroke"/>
      <path d="${path}L${endX},88L6,88Z" fill="url(#balance-fill)"/>
      <path d="${path}" fill="none" stroke="#7650e9" stroke-width="2.35" vector-effect="non-scaling-stroke"/>
      <circle cx="${endX}" cy="${endY}" r="4" fill="#7650e9" stroke="white" stroke-width="1.65" vector-effect="non-scaling-stroke"/>
    </svg>
    <div class="chart-labels">${days.map((day, i) => `<span title="${escapeHtml(state.hideBalance ? dateKey(day) : money(values[i]))}">${labels.format(day)}</span>`).join('')}</div>
  </div>`;
}

function accountCard(account) {
  const fullId = escapeHtml(account.id);
  return `<button type="button" class="account-card ${escapeHtml(account.type)}" data-account-detail="${fullId}" aria-label="View ${escapeHtml(account.name || typeLabel(account.type))}, ending in ${lastFour(account.id)}">
    <span class="account-icon ${escapeHtml(account.type)}">${icon(account.type, 20)}</span>
    <span class="account-meta"><strong class="account-name">${escapeHtml(account.name || typeLabel(account.type))}</strong><small>${escapeHtml(mask(account.id))}</small></span>
    ${account.balance === undefined ? `<span class="account-owner">${escapeHtml(account.ownerName)}</span>` : `<span class="account-value">${escapeHtml(displayBalance(account.balance))}</span>`}
  </button>`;
}

function quickActions() {
  const options = {
    transfer: ['Transfer', 'data-operation="transfer"'],
    deposit: ['Deposit', 'data-operation="deposit"'],
    withdraw: ['Withdraw', 'data-operation="withdraw"'],
    statements: ['Statements', 'data-view="statements"'],
    admin: ['Admin tools', 'data-view="admin"'],
    accounts: ['Accounts', 'data-view="accounts"'],
    activity: ['Activity', 'data-view="activity"'],
    demo: ['Demo Lab', 'data-view="demo"'],
  };
  const actions = isAdmin() ? ['admin', 'activity', 'statements', 'demo'] : isTeller() ? ['deposit','activity','accounts','demo'] : ['transfer','deposit','withdraw','statements'];
  return `<aside class="quick-card">
    <div class="quick-heading"><h2>Quick actions</h2><p>Manage your money</p></div>
    <div class="quick-grid">${actions.map(key => {
      const [label, attrs] = options[key];
      return `<button class="quick-action" type="button" ${attrs}><span class="quick-icon">${icon(key, 21)}</span><strong>${label}</strong></button>`;
    }).join('')}</div>
  </aside>`;
}

function transactionPresentation(tx, ids) {
  const entries = tx.entries.filter(entry => ids.has(String(entry.accountId)));
  const net = entries.reduce((sum, entry) => sum + entry.amount, 0);
  const debit = entries.find(entry => entry.amount < 0);
  const credit = entries.find(entry => entry.amount > 0);
  const twoSided = net === 0 && debit && credit;
  const displayEntry = net < 0 || twoSided ? debit : credit ?? debit;
  const amount = twoSided ? debit.amount : net;
  const kind = tx.type === 'transfer' ? (amount < 0 ? 'send' : 'receive') : ({ deposit: 'deposit', withdraw: 'withdraw', reversal: 'reset', interest: 'receive', fee: 'withdraw' }[tx.type] ?? 'activity');
  const account = displayEntry ? accountById(displayEntry.accountId) : null;
  const accountLabel = account ? `${account.name || typeLabel(account.type)} · ${mask(account.id)}` : (displayEntry ? mask(displayEntry.accountId) : '—');
  return { amount, kind, accountLabel, status: tx.reversedAt ? ['Reversed', 'reversed'] : ['Completed', 'success'] };
}

function transactionsTable(records, { accountId = '', admin = false, effective = false } = {}) {
  const ids = accountId ? new Set([String(accountId)]) : ownAccountIds();
  if (!records.length) return empty('No transactions found', 'Transactions will appear here after you move money.');
  return `<div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">Transaction</th><th scope="col">Date</th><th scope="col">Account</th><th scope="col" class="numeric">Amount</th><th scope="col">Status</th>${admin ? '<th scope="col"><span class="sr-only">Actions</span></th>' : ''}</tr></thead><tbody>
  ${records.map(tx => {
    const info = transactionPresentation(tx, ids);
    const reversible = admin && ['deposit','withdraw','transfer'].includes(tx.type) && !tx.reversedAt;
    return `<tr><td><div class="transaction-cell"><span class="transaction-icon ${info.kind}">${icon(info.kind, 17)}</span><span><strong>${escapeHtml(tx.description || transactionNames[tx.type] || tx.type)}</strong><small>${escapeHtml(transactionNames[tx.type] ?? tx.type)}</small></span></div></td>
    <td class="muted nowrap">${escapeHtml(prettyDate(effective ? ledgerDate(tx) : tx.at))}</td><td class="muted">${escapeHtml(info.accountLabel)}</td>
    <td class="numeric amount ${info.amount > 0 ? 'amount-positive' : info.amount < 0 ? 'amount-negative' : 'amount-muted'}">${escapeHtml(info.amount ? signedMoney(info.amount) : money(0))}</td>
    <td>${statusPill(...info.status)}</td>${admin ? `<td>${reversible ? btn('Reverse', `data-reverse="${escapeHtml(tx.id)}"`, null, 'text') : ''}</td>` : ''}</tr>`;
  }).join('')}</tbody></table></div>`;
}

function overview() {
  const hour = Number(new Intl.DateTimeFormat('en', { hour: '2-digit', hourCycle: 'h23', timeZone: 'Asia/Karachi' }).format(new Date()));
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
  const firstName = user().name.trim().split(/\s+/)[0];
  const longDate = new Intl.DateTimeFormat('en-US', { weekday: 'long', month: 'short', day: 'numeric', timeZone: 'Asia/Karachi' }).format(new Date());
  const personal = !isAdmin() && !isTeller();
  return `${pageHeading(`${greeting}, ${firstName}!`, personal ? 'Here’s what’s happening with your accounts today.' : 'Here’s what’s happening across Aster Bank today.', `<span class="date-pill">${icon('calendar', 16)}${escapeHtml(longDate)}</span>`)}
    <div class="overview-grid">
      ${isTeller() ? `<section class="balance-card" aria-label="Teller deposits">
        <span class="balance-label">Teller deposits</span>
        <div class="balance-value">${money((data().transactions ?? []).reduce((sum, tx) => sum + tx.entries.reduce((total, entry) => total + entry.amount, 0), 0))}</div>
        <div class="balance-subtitle">Across ${(data().transactions ?? []).length} posted transactions</div>
      </section>` : `<section class="balance-card" aria-label="Total balance">
        <div class="balance-header">
          <span class="balance-label">${personal ? 'Total balance' : 'Total account balances'}</span>
          <button class="icon-btn balance-eye" type="button" data-toggle-balance aria-label="${state.hideBalance ? 'Show' : 'Hide'} balances" aria-pressed="${state.hideBalance}">${icon(state.hideBalance ? 'eyeOff' : 'eye', 19)}</button>
        </div>
        <div class="balance-value">${escapeHtml(displayBalance(totalBalance()))}</div>
        <div class="balance-caption balance-subtitle">Across ${accounts().length} ${accounts().length === 1 ? 'account' : 'accounts'}</div>
        ${balanceChart()}
      </section>`}
      ${quickActions()}
    </div>
    <section class="overview-accounts">
      <div class="section-head"><h2>${personal ? 'My accounts' : 'Accounts'}</h2>${btn('View all accounts', 'data-view="accounts"', null, 'text')}</div>
      ${accounts().length ? `<div class="accounts-grid">${accounts().slice(0, 3).map(accountCard).join('')}</div>` : empty('No accounts yet', 'Open an account to start moving money.', 'accounts')}
    </section>
    <section class="panel recent-activity">
      ${sectionHead('Recent activity', btn('View all activity', 'data-view="activity"', null, 'text'))}
      ${transactionsTable(sortedTransactions().slice(0, 5))}
    </section>`;
}

function openAccountActions(account) {
  return permissions().map(action => btn(action[0].toUpperCase() + action.slice(1), `data-operation="${action}" data-account="${escapeHtml(account.id)}"`, action)).join('');
}

function accountsView() {
  const canOpen = !isAdmin() && !isTeller();
  return `${pageHeading('Accounts', canOpen ? 'View your balances and manage your bank accounts.' : 'Review the accounts in this banking workspace.', canOpen ? btn('Open account', 'data-operation="openAccount"', 'plus', 'primary') : '')}
  ${accounts().length ? `<div class="accounts-grid all-accounts">${accounts().map(accountCard).join('')}</div>` : empty('No accounts yet', 'Open an account to start banking.', 'accounts')}
  <section class="panel product-panel">${sectionHead('Account types')}
    <div class="product-grid">
      <article class="product-card"><span class="account-icon savings">${icon('savings')}</span><h3>Savings</h3><p>Earn monthly interest. A minimum balance and a daily withdrawal limit apply.</p></article>
      <article class="product-card"><span class="account-icon current">${icon('current')}</span><h3>Current</h3><p>Make frequent payments with a higher daily withdrawal limit and a monthly service fee.</p></article>
      <article class="product-card"><span class="account-icon fixed">${icon('fixed')}</span><h3>Fixed Deposit</h3><p>Set money aside until maturity. Withdrawals become available on the maturity date.</p></article>
    </div>
  </section>`;
}

function filterTransactions({ type = 'all', search = '', accountId = '', start = '', end = '' } = {}) {
  const query = search.trim().toLowerCase();
  return sortedTransactions().filter(tx => {
    if (type !== 'all' && tx.type !== type) return false;
    if (accountId && !tx.entries.some(entry => String(entry.accountId) === String(accountId))) return false;
    const date = ledgerDate(tx);
    if ((start && date < start) || (end && date > end)) return false;
    return !query || [tx.id, tx.description, transactionNames[tx.type], ...tx.entries.map(({ accountId }) => accountById(accountId)?.name ?? accountId)]
      .some(value => String(value ?? '').toLowerCase().includes(query));
  });
}

function activityView() {
  const records = filterTransactions({ type: state.activityType, search: state.activitySearch });
  return `${pageHeading('Activity', 'Review deposits, withdrawals, transfers, and other account activity.')}
  <section class="panel">
    ${sectionHead('Transactions')}
    <form class="filter-bar filters" data-form="activity">
      <label class="field search-field"><span>Search transactions</span><div class="search-input">${icon('search', 17)}<input name="search" placeholder="Search transactions" value="${escapeHtml(state.activitySearch)}"></div></label>
      <label class="field"><span>Type</span><select name="type"><option value="all">All types</option>${Object.entries(transactionNames).map(([key,label]) => `<option value="${key}" ${state.activityType === key ? 'selected' : ''}>${label}</option>`).join('')}</select></label>
      <button type="submit" class="secondary-btn">${icon('filter', 16)}<span>Apply filters</span></button>
    </form>
    ${transactionsTable(records, { admin: isAdmin() })}
  </section>`;
}

function accountOptions(selected, { omit = '', placeholder = '' } = {}) {
  return (placeholder ? `<option value="">${escapeHtml(placeholder)}</option>` : '') + accounts().filter(account => String(account.id) !== String(omit)).map(account => {
    const displayName = account.name || typeLabel(account.type);
    return `<option value="${escapeHtml(account.id)}" ${String(account.id) === String(selected) ? 'selected' : ''}>${escapeHtml(displayName)} · ${lastFour(account.id)}${account.ownerName && (isTeller() || isAdmin()) ? ` · ${escapeHtml(account.ownerName)}` : ''}</option>`;
  }).join('');
}

function currentStatement() {
  const { accountId, start, end } = state.statement;
  const account = accountById(accountId);
  const records = filterTransactions({ accountId, start, end });
  const move = tx => tx.entries.reduce((sum, entry) => sum + (String(entry.accountId) === String(accountId) ? entry.amount : 0), 0);
  const net = records.reduce((sum, tx) => sum + move(tx), 0);
  const later = (data().transactions ?? []).filter(tx => ledgerDate(tx) > end).reduce((sum, tx) => sum + move(tx), 0);
  const closing = (account?.balance ?? 0) - later;
  return { records, account, opening: closing - net, closing, net };
}

function statementsView() {
  const { accountId, start, end, generated } = state.statement;
  const selected = accountById(accountId) ?? accounts()[0];
  if (selected && !accountById(accountId)) state.statement.accountId = selected.id;
  const report = generated && selected ? currentStatement() : null;
  const monthly = [...(data().monthlyStatements ?? [])].sort((a,b) => b.month.localeCompare(a.month));
  return `${pageHeading('Statements', 'Choose an account and date range to view or export its statement.')}
  ${selected ? `<section class="panel">
    ${sectionHead('Date range')}
    <form class="filter-bar filters statement-form" data-form="statement">
      <label class="field"><span>Account</span><select name="accountId" required>${accountOptions(selected.id)}</select></label>
      <label class="field"><span>From</span><input type="date" name="start" value="${escapeHtml(start)}" required max="${dateKey()}"></label>
      <label class="field"><span>To</span><input type="date" name="end" value="${escapeHtml(end)}" required max="${dateKey()}"></label>
      <button type="submit" class="primary-btn">${icon('statements', 16)}<span>Generate statement</span></button>
      <p class="form-error" role="alert" hidden></p>
    </form>
  </section>` : empty('No bank accounts', 'An account is required to generate a statement.', 'statements')}
  ${report ? `<section class="panel result-panel">
    ${sectionHead(`${report.account.name || typeLabel(report.account.type)} statement`, btn('Download CSV', 'data-download-statement', 'download'))}
    <dl class="statement-summary"><div><dt>Opening balance</dt><dd>${money(report.opening)}</dd></div><div><dt>Net movement</dt><dd>${report.net ? signedMoney(report.net) : money(0)}</dd></div><div><dt>Closing balance</dt><dd>${money(report.closing)}</dd></div></dl>
    ${transactionsTable(report.records, { accountId: report.account.id, effective: true })}
  </section>` : ''}
  <section class="panel monthly-panel">
    ${sectionHead('Monthly statements')}
    ${monthly.length ? `<div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">Month</th><th scope="col">Account</th><th scope="col" class="numeric">Opening balance</th><th scope="col" class="numeric">Interest</th><th scope="col" class="numeric">Service fee</th><th scope="col" class="numeric">Closing balance</th></tr></thead><tbody>${monthly.map(statement => `<tr>
      <td>${escapeHtml(statement.month)}</td><td>${escapeHtml(accountById(statement.accountId)?.name ?? mask(statement.accountId))}</td><td class="numeric">${money(statement.openingBalance)}</td><td class="numeric">${money(statement.interest)}</td><td class="numeric">${money(statement.fee)}</td><td class="numeric">${money(statement.closingBalance)}</td></tr>`).join('')}</tbody></table></div>` : empty('No monthly statements yet', 'Statements appear here after month-end processing.', 'statements')}
  </section>`;
}

function csvText(value) {
  let text = String(value ?? '');
  if (/^\s*[=+@-]/.test(text) || /^[\t\r\n]/.test(text)) text = `'${text}`;
  return `"${text.replace(/"/g, '""')}"`;
}

function downloadStatement() {
  const { records, account, opening, closing } = currentStatement();
  if (!account) return;
  const { start, end } = state.statement;
  const rows = [
    ['Account', 'From', 'To', 'Opening balance (USD)', 'Closing balance (USD)'].map(csvText).join(','),
    [csvText(account.id), csvText(start), csvText(end), (opening / 100).toFixed(2), (closing / 100).toFixed(2)].join(','),
    '',
    ['Date', 'Transaction ID', 'Type', 'Description', 'Amount (USD)', 'Status'].map(csvText).join(','),
    ...records.map(tx => [
      csvText(ledgerDate(tx)), csvText(tx.id), csvText(transactionNames[tx.type] ?? tx.type), csvText(tx.description),
      (tx.entries.filter(entry => String(entry.accountId) === String(account.id)).reduce((sum, entry) => sum + entry.amount, 0) / 100).toFixed(2),
      csvText(tx.reversedAt ? 'Reversed' : 'Completed'),
    ].join(',')),
  ];
  const url = URL.createObjectURL(new Blob([rows.join('\r\n') + '\r\n'], { type: 'text/csv;charset=utf-8;' }));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `aster-statement-${lastFour(account.id)}-${start}-${end}.csv`;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function notificationsView() {
  const alerts = [...(data().notifications ?? [])].sort((a,b) => b.at.localeCompare(a.at));
  const unread = alerts.filter(item => !state.readAlerts.has(item.id)).length;
  return `${pageHeading('Notifications', 'View transaction alerts and low-balance notices.')}
  <section class="panel notifications-panel">
    ${sectionHead('Alert inbox', unread ? btn('Mark all as read', 'data-mark-all', 'check') : '')}
    ${alerts.length ? `<ul class="alert-list">${alerts.map(item => {
      const warning = String(item.type).toLowerCase().includes('low');
      const read = state.readAlerts.has(item.id);
      const channel = String(item.channel ?? 'Email').toUpperCase() === 'SMS' ? 'SMS' : 'Email';
      return `<li class="alert-row ${read ? 'read' : 'unread'}">
        <span class="alert-icon ${warning ? 'warning' : ''}">${icon(warning ? 'warning' : channel === 'SMS' ? 'phone' : 'email', 19)}</span>
        <div class="alert-text"><strong>${warning ? 'Low balance' : 'Transaction alert'}</strong><p>${escapeHtml(item.message)}</p><small>${channel} · ${escapeHtml(prettyDate(item.at, alertDate))}</small></div>
        ${!read ? btn('Mark as read', `data-mark-read="${escapeHtml(item.id)}"`, null, 'text') : ''}
      </li>`;
    }).join('')}</ul>` : empty('You’re all caught up', 'New alerts will appear here when account activity occurs.', 'notifications')}
  </section>`;
}

function adminView() {
  const audit = [...(data().audit ?? [])].sort((a,b) => b.at.localeCompare(a.at));
  return `${pageHeading('Admin workspace', 'Reverse transactions, run month-end processing, and review the audit trail.', btn('Run month-end', 'data-operation="monthEnd"', 'calendar', 'primary'))}
  <section class="panel">${sectionHead('Transaction ledger')}${transactionsTable(sortedTransactions(), { admin: true })}</section>
  <section class="panel audit-panel">${sectionHead('Audit log')}
    ${audit.length ? `<div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">Action</th><th scope="col">Details</th><th scope="col">Actor</th><th scope="col">Recorded</th></tr></thead><tbody>${audit.map(entry => `<tr>
      <td><strong>${escapeHtml(String(entry.action).replaceAll('_', ' '))}</strong></td><td>${escapeHtml(entry.description)}${entry.transactionId ? `<br><small class="muted">${escapeHtml(entry.transactionId)}</small>` : ''}</td><td>${escapeHtml(entry.actorName ?? entry.actorId)}</td><td class="nowrap muted">${escapeHtml(prettyDate(entry.at, alertDate))}</td>
    </tr>`).join('')}</tbody></table></div>` : empty('Audit log is empty', 'Successful commands, reversals, and month-end runs appear here.', 'admin')}
  </section>`;
}

const demoSteps = [
  { key: 'transfer', title: 'Successful transfer', guidance: 'Send $75.00 from Ayesha’s Savings to Omar’s Savings and check that the recipient receives an alert.', glyph: 'transfer', label: 'Run transfer' },
  { key: 'limit', title: 'Daily withdrawal limit', guidance: 'Try to withdraw one cent more than today’s remaining allowance.', glyph: 'withdraw', label: 'Test daily limit' },
  { key: 'pin', title: 'Wrong PIN', guidance: 'Attempt a transfer with an incorrect PIN to exercise the protection proxy.', glyph: 'lock', label: 'Test wrong PIN' },
  { key: 'reverse', title: 'Admin reversal', guidance: 'Sign in as Bank Admin and reverse the demo transfer. This calls undo() and creates an audit entry.', glyph: 'reset', label: 'Run reversal' },
  { key: 'month', title: 'Month-end run', guidance: 'Run month-end as Bank Admin and review Savings interest and Current service fees.', glyph: 'calendar', label: 'Run month-end' },
];

function demoView() {
  const running = state.demo.running;
  return `${pageHeading('Demo Lab', 'Run the required banking scenarios against the sample accounts.')}
    <section class="panel demo-intro">
      <div class="panel-head"><div><h2 class="panel-title">Sample sign-ins</h2><p class="section-description">Scenario buttons switch to the required sample role and use simulated funds.</p></div>${statusPill(userRole(), 'neutral')}</div>
      <div class="sample-grid">${Object.entries(demoUsers).map(([key, profile]) => `<div class="sample-card"><div class="sample-identity"><span class="avatar">${initials(profile.name)}</span><div><strong>${escapeHtml(profile.name)}</strong><small>${escapeHtml(profile.role)}</small></div></div><div class="sample-detail"><span>${escapeHtml(profile.email)}</span><span>PIN <code>${profile.credential}</code></span></div>${btn(user().email === profile.email ? 'Signed in' : 'Sign in', `data-demo-login="${key}" ${running || user().email === profile.email ? 'disabled' : ''}`, null)}</div>`).join('')}</div>
    </section>
    <section class="demo-scenarios">
      ${sectionHead('Banking scenarios')}
      <div class="demo-grid">${demoSteps.map(step => {
        const result = state.demo.results[step.key];
        return `<article class="panel demo-card">
          <span class="demo-icon">${icon(step.glyph, 21)}</span>
          <h3>${step.title}</h3><p>${step.guidance}</p>
          ${result ? `<div role="status" class="demo-result ${result.ok ? 'success' : 'error'}">${icon(result.ok ? 'check' : 'warning', 16)}<span>${escapeHtml(result.message)}</span></div>` : ''}
          ${btn(running === step.key ? 'Running…' : step.label, `data-demo-run="${step.key}" ${running ? 'disabled' : ''}`, 'play')}
        </article>`;
      }).join('')}</div>
    </section>
    <section class="panel documents-panel">${sectionHead('Project files')}
      <div class="document-links">
        <a class="secondary-btn" href="/docs/use-case.svg" target="_blank" rel="noopener">${icon('statements', 18)}<span>Hand-drawn use case diagram</span></a>
        <a class="secondary-btn" href="/docs/transfer-sequence.svg" target="_blank" rel="noopener">${icon('statements', 18)}<span>Transfer sequence diagram</span></a>
        <a class="secondary-btn" href="/docs/project-guide.md" target="_blank" rel="noopener">${icon('statements', 18)}<span>Project guide</span></a>
        <a class="secondary-btn" href="/downloads/aster-bank.zip" download>${icon('download', 18)}<span>Source code</span></a>
      </div>
    </section>`;
}

function render() {
  if (!user()) return;
  const views = { overview, accounts: accountsView, activity: activityView, statements: statementsView, notifications: notificationsView, demo: demoView, admin: adminView };
  if (state.page === 'admin' && !isAdmin()) state.page = 'overview';
  view.innerHTML = `<div class="page-view ${state.page}-view">${views[state.page]()}</div>`;
  auth.hidden = true;
  shell.hidden = false;
  setNavigation();
}

function dialogBase(title, introduction, body) {
  dialog.innerHTML = `<header class="dialog-header"><div><h2 id="dialog-title">${escapeHtml(title)}</h2>${introduction ? `<p>${escapeHtml(introduction)}</p>` : ''}</div>
    <button class="icon-btn dialog-close" type="button" data-close-dialog aria-label="Close dialog">${icon('close', 20)}</button></header><div class="dialog-body">${body}</div>`;
  if (!dialog.open) dialog.showModal();
}

const pinField = () => `<label class="field"><span>Transaction PIN</span><input name="pin" type="password" inputmode="numeric" pattern="[0-9]{6}" maxlength="6" autocomplete="off" placeholder="Enter your 6-digit PIN" required></label>`;
const defaultActions = label => `<div class="form-actions">${btn('Cancel', 'data-close-dialog')}<button type="submit" class="primary-btn"><span>${escapeHtml(label)}</span></button></div>`;
const formError = '<p class="form-error" role="alert" hidden></p>';

function accountDetail(account) {
  if (!account) return;
  const name = account.name || typeLabel(account.type);
  dialogBase(name, typeLabel(account.type), `<dl class="detail-list">
    <div><dt>Account number</dt><dd class="account-number">${escapeHtml(account.id)}</dd></div>
    ${account.ownerName && (isAdmin() || isTeller()) ? `<div><dt>Account holder</dt><dd>${escapeHtml(account.ownerName)}</dd></div>` : ''}
    ${account.balance !== undefined ? `<div><dt>Balance</dt><dd>${displayBalance(account.balance)}</dd></div>` : ''}
    ${account.minBalance !== undefined ? `<div><dt>Minimum balance</dt><dd>${money(account.minBalance)}</dd></div>` : ''}
    ${account.dailyLimit != null ? `<div><dt>Daily withdrawal limit</dt><dd>${money(account.dailyLimit)}</dd></div>` : ''}
    ${account.dailyRemaining != null ? `<div><dt>Remaining today</dt><dd>${money(account.dailyRemaining)}</dd></div>` : ''}
    ${account.maturesOn ? `<div><dt>Maturity date</dt><dd>${escapeHtml(prettyDate(account.maturesOn))}</dd></div>` : ''}
    ${account.monthlyRate ? `<div><dt>Monthly interest</dt><dd>${new Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: 3 }).format(account.monthlyRate)}</dd></div>` : ''}
    ${account.monthlyFee ? `<div><dt>Monthly fee</dt><dd>${money(account.monthlyFee)}</dd></div>` : ''}
    </dl><div class="form-actions account-actions">${openAccountActions(account)}${isTeller() ? '' : btn('View statement', `data-account-statement="${escapeHtml(account.id)}"`, 'statements')}</div>`);
}

function operationDialog(action, accountId) {
  if (action === 'monthEnd' && isAdmin()) {
    dialogBase('Run month-end', 'Review account interest, fees, and generated statements.', `<form class="form-grid" data-form="operation" data-action="monthEnd">
      <label class="field"><span>Processing month</span><input type="month" name="month" max="${dateKey().slice(0, 7)}" value="${dateKey().slice(0, 7)}" required></label>
      ${pinField()}${formError}${defaultActions('Process month')}</form>`);
    return;
  }
  if (action === 'openAccount' && !isAdmin() && !isTeller()) {
    dialogBase('Open account', 'Choose an account type and give it a name.', `<form class="form-grid" data-form="operation" data-action="openAccount">
      <label class="field"><span>Account name</span><input name="name" placeholder="e.g. Rainy Day Savings" maxlength="70" required></label>
      <label class="field"><span>Account type</span><select name="type">${Object.entries(productNames).map(([type,name]) => `<option value="${type}">${name}</option>`).join('')}</select></label>
      ${pinField()}${formError}${defaultActions('Open account')}</form>`);
    return;
  }
  if (!permissions().includes(action)) return;
  const available = accounts();
  if (!available.length) {
    dialogBase('No bank accounts', 'Open an account before moving money.', `<div class="form-actions">${btn('Open account', 'data-operation="openAccount"', 'plus', 'primary')}</div>`);
    return;
  }
  const from = accountById(accountId) ?? available[0];
  const transfer = action === 'transfer';
  const names = { transfer: ['Transfer funds', 'Move money between Aster Bank accounts.', 'Confirm transfer'], deposit: ['Deposit money', 'Add money to an account.', 'Confirm deposit'], withdraw: ['Withdraw money', 'Withdraw available money from an account.', 'Confirm withdrawal'] };
  const [title, caption, submit] = names[action];
  const useOwn = transfer && available.length > 1;
  dialogBase(title, caption, `<form class="form-grid" data-form="operation" data-action="${action}">
    <label class="field"><span>${transfer ? 'From account' : 'Account'}</span><select name="accountId" required>${accountOptions(from.id)}</select></label>
    ${transfer ? `<label class="field"><span>Recipient</span><select name="recipientKind">${useOwn ? '<option value="own">My Aster account</option>' : ''}<option value="external">Another customer</option></select></label>
      <label class="field" data-own-recipient ${useOwn ? '' : 'hidden'}><span>To account</span><select name="ownRecipient" ${useOwn ? 'required' : 'disabled'}>${accountOptions('', { omit: from.id, placeholder: 'Select an account' })}</select></label>
      <label class="field" data-external-recipient ${useOwn ? 'hidden' : ''}><span>Recipient account number</span><input name="externalRecipient" inputmode="numeric" maxlength="16" placeholder="Enter account number" ${useOwn ? 'disabled' : 'required'}></label>` : ''}
    <label class="field"><span>Amount (USD)</span><input name="amount" type="number" min="0.01" step="0.01" placeholder="0.00" required></label>
    ${pinField()}${formError}${defaultActions(submit)}</form>`);
}

function reversalDialog(id) {
  if (!isAdmin()) return;
  const original = (data().transactions ?? []).find(tx => String(tx.id) === String(id));
  if (!original) return;
  dialogBase('Reverse transaction', 'Confirm the transaction and enter the admin PIN.', `<form class="form-grid" data-form="operation" data-action="reverse">
    <input type="hidden" name="transactionId" value="${escapeHtml(original.id)}">
    <div class="reversal-summary"><strong>${escapeHtml(original.description || transactionNames[original.type])}</strong><span>${escapeHtml(original.id)}</span></div>
    ${pinField()}${formError}${defaultActions('Confirm reversal')}</form>`);
}

function profileDialog() {
  dialogBase('Your profile', '', `<div class="profile-summary"><span class="avatar">${escapeHtml(initials(user().name))}</span><div><strong>${escapeHtml(user().name)}</strong><span>${escapeHtml(user().email)}</span></div>${statusPill(userRole(), 'neutral')}</div>
  <div class="form-actions">${btn('Demo Lab', 'data-view="demo"', 'demo')}${btn('Sign out', 'data-sign-out', 'logout', 'primary')}</div>`);
}

function authView(mode = 'login', message = '') {
  state.dashboard = null;
  shell.hidden = true;
  auth.hidden = false;
  const register = mode === 'register';
  auth.innerHTML = `<section class="auth-card">
    <div class="auth-brand"><span class="brand-icon"><svg viewBox="0 0 32 32" aria-hidden="true"><use href="#aster"/></svg></span><span class="brand-wordmark">aster<span>.</span><small> BANK</small></span></div>
    <h1>${register ? 'Create an account' : 'Sign in to Aster Bank'}</h1>
    <p class="auth-intro">${register ? 'Register as a customer to open and manage bank accounts.' : 'Enter your email and PIN or password to continue.'}</p>
    <form class="form-grid" data-form="auth" data-mode="${mode}">
      ${register ? '<label class="field"><span>Full name</span><input name="name" autocomplete="name" maxlength="90" required></label>' : ''}
      <label class="field"><span>Email</span><input name="email" type="email" autocomplete="username" required></label>
      ${register ? '<label class="field"><span>Password</span><input name="password" type="password" autocomplete="new-password" minlength="8" required><small>Use at least 8 characters.</small></label><label class="field"><span>Six-digit PIN</span><input name="pin" type="password" inputmode="numeric" pattern="[0-9]{6}" maxlength="6" autocomplete="off" required></label>' : '<label class="field"><span>PIN or password</span><input name="credential" type="password" autocomplete="current-password" required></label>'}
      <p class="form-error" role="alert" ${message ? '' : 'hidden'}>${escapeHtml(message)}</p>
      <button class="primary-btn" type="submit"><span>${register ? 'Register' : 'Sign in'}</span></button>
    </form>
    <div class="auth-switch">${register ? 'Already registered?' : 'New to Aster Bank?'} ${btn(register ? 'Sign in' : 'Register', `data-auth-mode="${register ? 'login' : 'register'}"`, null, 'text')}</div>
    ${register ? '' : `<div class="auth-demo">${btn('Open customer demo', 'data-demo-login="customer"', 'demo')}</div>`}
    <p class="auth-note">${icon('lock', 16)} Banking sandbox · Simulated funds</p>
  </section>`;
}

function showFormError(form, message) {
  const element = form.querySelector('.form-error');
  if (!element) return;
  element.textContent = message;
  element.hidden = !message;
}

function setBusy(form, busy) {
  form.toggleAttribute('aria-busy', busy);
  for (const button of form.querySelectorAll('button')) button.disabled = busy;
  if (form.closest('dialog')) dialog.dataset.busy = busy ? 'true' : 'false';
}

function closeDialog(force = false) {
  if (dialog.open && (force || dialog.dataset.busy !== 'true')) dialog.close();
}

async function signInDemo(key, page = 'demo') {
  const profile = demoUsers[key];
  if (!profile) return;
  if (user()?.email === profile.email) return;
  const dashboard = await post('/api/login', { email: profile.email, credential: profile.credential });
  applyDashboard(dashboard);
  closeDialog(true);
  go(page, { focus: false });
}

async function demoTransfer() {
  await signInDemo('recipient');
  const previousAlerts = new Set(data().notifications.map(alert => alert.id));
  await signInDemo('customer');
  const source = accountById(sampleAccounts.savings);
  const result = await post('/api/action', {
    action: 'transfer', accountId: sampleAccounts.savings, toAccountId: sampleAccounts.recipient,
    amount: 7500, pin: demoUsers.customer.credential,
  });
  applyDashboard(result.dashboard);
  const id = result.transaction?.id;
  if (!id || accountById(source.id).balance !== source.balance - 7500) throw new Error('The outgoing transfer could not be confirmed.');
  state.demo.transferId = id;
  await signInDemo('recipient');
  const received = data().notifications.some(alert => alert.transactionId === id && !previousAlerts.has(alert.id));
  const credit = data().transactions.find(tx => tx.id === id)?.entries.some(entry => entry.accountId === sampleAccounts.recipient && entry.amount === 7500);
  await signInDemo('customer');
  if (!received || !credit) throw new Error('The recipient credit or alert could not be confirmed.');
  return `Transfer ${id} sent $75.00. The recipient received the credit and an alert.`;
}

async function runDemo(key) {
  if (state.demo.running) return;
  state.demo.running = key;
  delete state.demo.results[key];
  render();
  try {
    let message;
    if (key === 'transfer') {
      message = await demoTransfer();
    }
    if (key === 'limit' || key === 'pin') {
      await signInDemo('customer');
      const savings = accountById(sampleAccounts.savings);
      const inLimit = key === 'limit';
      const expected = inLimit ? 'DAILY_LIMIT' : 'INVALID_PIN';
      const initialTransactions = data().transactions.length;
      const initialBalance = savings.balance;
      try {
        await post('/api/action', inLimit
          ? { action: 'withdraw', accountId: savings.id, amount: savings.dailyRemaining + 1, pin: demoUsers.customer.credential }
          : { action: 'transfer', accountId: savings.id, toAccountId: sampleAccounts.recipient, amount: 100, pin: '000000' });
        throw new Error('The operation unexpectedly succeeded.');
      } catch (error) {
        if (error.code !== expected) throw error;
        applyDashboard(await request('/api/dashboard'));
        if (accountById(savings.id).balance !== initialBalance || data().transactions.length !== initialTransactions) {
          throw new Error('The account changed during this check. Retry the scenario.');
        }
        message = `${error.message} Balance and ledger verified.`;
      }
    }
    if (key === 'reverse') {
      if (!state.demo.transferId) await demoTransfer();
      await signInDemo('admin');
      const original = data().transactions.find(tx => tx.id === state.demo.transferId && !tx.reversedAt);
      if (!original) throw new Error('Run a successful transfer to create a new transaction to reverse.');
      const id = original.id;
      const result = await post('/api/action', { action: 'reverse', transactionId: id, pin: demoUsers.admin.credential });
      applyDashboard(result.dashboard);
      state.demo.transferId = '';
      const reversal = result.transaction;
      const audited = data().audit.some(item => item.action === 'reversal' && item.transactionId === reversal?.id);
      if (reversal?.reversalOf !== id || !audited) throw new Error('The reversal or audit entry could not be confirmed.');
      message = `${id} reversed by ${reversal.id}. The reversal is in the audit log.`;
    }
    if (key === 'month') {
      await signInDemo('admin');
      const month = dateKey().slice(0, 7);
      let statements = (data().monthlyStatements ?? []).filter(item => item.month === month);
      const already = statements.length > 0;
      if (!already) {
        const result = await post('/api/action', { action: 'monthEnd', month, pin: demoUsers.admin.credential });
        applyDashboard(result.dashboard);
        statements = result.statements;
      }
      const savings = statements.find(item => item.accountId === sampleAccounts.savings);
      const current = statements.find(item => item.accountId === sampleAccounts.current);
      if (!savings || !current) throw new Error('The Savings and Current statements could not be confirmed.');
      message = `${month} ${already ? 'was processed earlier' : 'processed'}. Savings interest: ${money(savings.interest)}. Current fee: ${money(current.fee)}.`;
    }
    if (message) state.demo.results[key] = { ok: true, message };
  } catch (error) {
    state.demo.results[key] = { ok: false, message: error.message };
  } finally {
    state.demo.running = null;
    render();
    if (state.page === 'demo') view.querySelector(`[data-demo-run="${key}"]`)?.focus({ preventScroll: true });
  }
}

async function switchDemo(key, button) {
  if (state.demo.running) return;
  if (button) button.disabled = true;
  try {
    await signInDemo(key, user() ? 'demo' : 'overview');
    showToast(`Signed in as ${demoUsers[key].name}.`);
  } catch (error) {
    showToast(error.message, 'error');
    if (button) button.disabled = false;
  }
}

async function signOut(button) {
  button.disabled = true;
  try {
    await post('/api/logout');
    remember('aster-signed-out', '1');
    closeDialog(true);
    state.demo = { results: {}, transferId: '', running: null };
    authView();
  } catch (error) {
    showToast(error.message, 'error');
    button.disabled = false;
  }
}

async function submitOperation(form, fields) {
  const action = form.dataset.action;
  const payload = { action, ...fields };
  if (Object.hasOwn(fields, 'amount')) payload.amount = readAmount(fields.amount);
  if (action === 'transfer') {
    payload.toAccountId = fields.recipientKind === 'own' ? fields.ownRecipient : fields.externalRecipient?.trim();
    delete payload.recipientKind;
    delete payload.ownRecipient;
    delete payload.externalRecipient;
  }
  const result = await post('/api/action', payload);
  applyDashboard(result.dashboard);
  closeDialog(true);
  render();
  showToast(result.message || 'Operation completed.');
}

function updateTransfer(form) {
  const kind = form.elements.recipientKind.value;
  const own = form.querySelector('[data-own-recipient]');
  const external = form.querySelector('[data-external-recipient]');
  own.hidden = kind !== 'own';
  external.hidden = kind !== 'external';
  const to = form.elements.ownRecipient;
  const toId = to.value;
  to.innerHTML = accountOptions(toId, { omit: form.elements.accountId.value, placeholder: 'Select an account' });
  to.required = kind === 'own';
  to.disabled = kind !== 'own';
  form.elements.externalRecipient.required = kind === 'external';
  form.elements.externalRecipient.disabled = kind !== 'external';
}

document.addEventListener('change', event => {
  const field = event.target;
  if (field.form?.dataset.action === 'transfer' && ['recipientKind','accountId'].includes(field.name)) updateTransfer(field.form);
});

document.addEventListener('submit', async event => {
  const form = event.target;
  const type = form.dataset.form;
  if (!type) return;
  event.preventDefault();
  if (form.hasAttribute('aria-busy')) return;
  const fields = Object.fromEntries(new FormData(form));
  if (type === 'activity') {
    state.activityType = fields.type;
    state.activitySearch = fields.search;
    render();
    view.querySelector('[data-form="activity"] button').focus({ preventScroll: true });
    return;
  }
  if (type === 'statement') {
    if (fields.start > fields.end) {
      showFormError(form, 'The start date must be on or before the end date.');
      return;
    }
    state.statement = { ...fields, generated: true };
    render();
    view.querySelector('[data-download-statement]')?.focus({ preventScroll: true });
    return;
  }
  setBusy(form, true);
  showFormError(form, '');
  try {
    if (type === 'auth') {
      const dashboard = await post(`/api/${form.dataset.mode}`, fields);
      applyDashboard(dashboard);
      go(isAdmin() ? 'admin' : 'overview');
    }
    if (type === 'operation') await submitOperation(form, fields);
  } catch (error) {
    if (error.status === 401 && error.code === 'UNAUTHENTICATED' && type === 'operation') {
      closeDialog(true);
      authView('login', 'Your session expired. Sign in to continue.');
    } else {
      showFormError(form, error.message);
    }
  } finally {
    setBusy(form, false);
  }
});

document.addEventListener('click', event => {
  const target = event.target.closest('button');
  if (!target) return;
  const d = target.dataset;
  if (target.id === 'profile-button') return profileDialog();
  if (target.id === 'header-bell') return go('notifications');
  if (Object.hasOwn(d, 'closeDialog')) return closeDialog();
  if (Object.hasOwn(d, 'closeToast')) return target.closest('.toast')?.remove();
  if (Object.hasOwn(d, 'retryStartup')) return startup();
  if (d.authMode) return authView(d.authMode);
  if (Object.hasOwn(d, 'signOut')) return signOut(target);
  if (d.demoLogin) return switchDemo(d.demoLogin, target);
  if (!user()) return;
  if (d.demoRun) return runDemo(d.demoRun);
  if (d.view) {
    closeDialog();
    return go(d.view);
  }
  if (Object.hasOwn(d, 'toggleBalance')) {
    state.hideBalance = !state.hideBalance;
    render();
    return view.querySelector('[data-toggle-balance]')?.focus({ preventScroll: true });
  }
  if (d.accountDetail) return accountDetail(accountById(d.accountDetail));
  if (d.operation) return state.demo.running ? undefined : operationDialog(d.operation, d.account);
  if (d.reverse) return state.demo.running ? undefined : reversalDialog(d.reverse);
  if (d.accountStatement) {
    state.statement.accountId = d.accountStatement;
    state.statement.generated = false;
    closeDialog();
    return go('statements');
  }
  if (Object.hasOwn(d, 'downloadStatement')) return downloadStatement();
  if (Object.hasOwn(d, 'markAll')) {
    (data().notifications ?? []).forEach(alert => state.readAlerts.add(alert.id));
    return render();
  }
  if (d.markRead) {
    state.readAlerts.add(d.markRead);
    return render();
  }
});

dialog.addEventListener('cancel', event => {
  if (dialog.dataset.busy === 'true') event.preventDefault();
});

async function startup() {
  try {
    let dashboard;
    try {
      dashboard = await request('/api/dashboard');
    } catch (error) {
      if (error.status !== 401) throw error;
      if (!remember('aster-signed-out')) {
        try {
          dashboard = await post('/api/bootstrap');
        } catch (bootstrapError) {
          if (bootstrapError.status !== 401) throw bootstrapError;
        }
      }
    }
    if (!dashboard) return authView();
    applyDashboard(dashboard);
    go(isAdmin() ? 'admin' : 'overview', { focus: false });
  } catch (error) {
    auth.innerHTML = `<section class="auth-card"><h1>Aster Bank</h1><p role="alert">${escapeHtml(error.message)}</p>${btn('Try again', 'data-retry-startup', 'reset', 'primary')}</section>`;
  }
}

startup();
