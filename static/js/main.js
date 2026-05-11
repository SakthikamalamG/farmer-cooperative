function getToken() { return localStorage.getItem('token'); }
function getUser()  { try { return JSON.parse(localStorage.getItem('user')); } catch(e) { return null; } }

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('cart');
    window.location.href = '/';
}

function updateNavbar() {
    const user  = getUser();
    const token = getToken();
    if (user && token) {
        document.getElementById('nav-login').classList.add('d-none');
        document.getElementById('nav-register').classList.add('d-none');
        document.getElementById('nav-logout').classList.remove('d-none');
        document.getElementById('nav-notifications').classList.remove('d-none');
        document.getElementById('nav-chat').classList.remove('d-none');
        const info = document.getElementById('nav-user-info');
        if (info) { info.style.display = ''; document.getElementById('nav-username').textContent = user.full_name || user.username; }
        if (user.role === 'farmer') document.getElementById('nav-farmer').classList.remove('d-none');
        if (user.role === 'admin')  document.getElementById('nav-admin').classList.remove('d-none');
        loadNotifications();
    }
}

async function loadNotifications() {
    const token = getToken();
    if (!token) return;
    try {
        const res = await fetch('/api/notifications', { headers: { 'Authorization': 'Bearer ' + token } });
        if (!res.ok) return;
        const notifications = await res.json();
        const unread = notifications.filter(n => !n.is_read).length;
        document.getElementById('notif-count').textContent = unread || '';
        const list = document.getElementById('notification-list');
        if (!notifications.length) { list.innerHTML = '<p class="text-muted text-center p-3 mb-0">No notifications</p>'; return; }
        list.innerHTML = notifications.slice(0, 10).map(n => `
            <div class="p-2 border-bottom ${n.is_read ? 'bg-light' : ''}">
                <div class="small fw-semibold">${n.title || ''}</div>
                <div class="small text-muted">${n.message || ''}</div>
                <div class="text-muted" style="font-size:.72rem">${new Date(n.created_at).toLocaleString()}</div>
            </div>`).join('');
    } catch(e) {}
}

function toggleNotifications() {
    const panel = document.getElementById('notification-panel');
    panel.classList.toggle('d-none');
    if (!panel.classList.contains('d-none')) markAllNotificationsRead();
}

async function markAllNotificationsRead() {
    const token = getToken();
    if (!token) return;
    try {
        await fetch('/api/notifications/mark-all-read', { method: 'POST', headers: { 'Authorization': 'Bearer ' + token } });
        document.getElementById('notif-count').textContent = '';
    } catch(e) {}
}

document.addEventListener('DOMContentLoaded', updateNavbar);
