/**
 * app.js — Main application logic
 * Loads cafe data from cafes.json — no backend required.
 */

import { getCurrentPosition, haversine } from './geo.js';
import { renderCafeList, renderDetail, isOpenNow } from './ui.js';

const CACHE_KEY = 'cafekasol_cafes';

const statusMsg    = document.getElementById('status-msg');
const cafeList     = document.getElementById('cafe-list');
const searchInput  = document.getElementById('search-input');
const filterBtns   = document.querySelectorAll('.filter-btn');
const detailSheet  = document.getElementById('detail-sheet');
const sheetContent = document.getElementById('sheet-content');
const overlay      = document.getElementById('overlay');

let allCafes = [];
let userLat = null;
let userLon = null;
let activeFilter = 'all';

// ── Boot ──────────────────────────────────────────
async function init() {
  registerServiceWorker();
  await locateUser();
  await loadCafes();
  bindEvents();
}

// ── Geolocation ───────────────────────────────────
async function locateUser() {
  try {
    const pos = await getCurrentPosition();
    userLat = pos.coords.latitude;
    userLon = pos.coords.longitude;
    statusMsg.textContent = 'Location found';
  } catch {
    statusMsg.textContent = 'Location unavailable — showing all cafes';
  }
}

// ── Data loading from cafes.json ──────────────────
async function loadCafes() {
  let cafes = null;

  try {
    const res = await fetch('/cafes.json', { signal: AbortSignal.timeout(5000) });
    if (res.ok) {
      cafes = await res.json();
      localStorage.setItem(CACHE_KEY, JSON.stringify(cafes));
    }
  } catch {
    // offline — use cached data
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      cafes = JSON.parse(cached);
      statusMsg.textContent = 'Offline — showing cached cafes';
    }
  }

  if (!cafes) {
    cafeList.innerHTML = '<div class="empty-state">Could not load cafes. Check your connection.</div>';
    return;
  }

  // Calculate distance and sort by nearest
  if (userLat != null) {
    cafes = cafes.map(c => ({
      ...c,
      distance: haversine(userLat, userLon, c.lat, c.lon),
    }));
    cafes.sort((a, b) => a.distance - b.distance);
    statusMsg.textContent = `${cafes.length} cafes nearby`;
  } else {
    statusMsg.textContent = `${cafes.length} cafes in Kasol`;
  }

  allCafes = cafes;
  renderFiltered();
}

// ── Filtering & search ────────────────────────────
function renderFiltered() {
  const query = searchInput.value.trim().toLowerCase();
  let result = allCafes;

  if (query) {
    result = result.filter(c =>
      c.name.toLowerCase().includes(query) ||
      (c.tags || []).some(t => t.toLowerCase().includes(query))
    );
  }

  if (activeFilter !== 'all') {
    result = result.filter(c => {
      if (activeFilter === 'open-now') return isOpenNow(c.open_time, c.close_time);
      return (c.tags || []).includes(activeFilter);
    });
  }

  renderCafeList(result, cafeList);
  bindCardClicks();
}

// ── Events ────────────────────────────────────────
function bindEvents() {
  searchInput.addEventListener('input', renderFiltered);

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeFilter = btn.dataset.filter;
      renderFiltered();
    });
  });

  overlay.addEventListener('click', closeSheet);
}

function bindCardClicks() {
  document.querySelectorAll('.cafe-card').forEach(card => {
    card.addEventListener('click', () => {
      const cafe = allCafes.find(c => String(c.id) === card.dataset.id);
      if (cafe) openSheet(cafe);
    });
  });
}

// ── Detail sheet ──────────────────────────────────
function openSheet(cafe) {
  renderDetail(cafe, sheetContent);
  detailSheet.classList.remove('hidden');
  overlay.classList.remove('hidden');
}

function closeSheet() {
  detailSheet.classList.add('hidden');
  overlay.classList.add('hidden');
}

// ── Service Worker ────────────────────────────────
function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }
}

init();
