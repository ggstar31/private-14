/**
 * ui.js — DOM rendering helpers
 */

import { formatDistance } from './geo.js';

export function renderCafeList(cafes, container) {
  container.innerHTML = '';

  if (cafes.length === 0) {
    container.innerHTML = '<div class="empty-state">No cafes found nearby.</div>';
    return;
  }

  cafes.forEach(cafe => {
    const card = createCard(cafe);
    container.appendChild(card);
  });
}

function createCard(cafe) {
  const card = document.createElement('div');
  card.className = 'cafe-card';
  card.dataset.id = cafe.id;

  const open = isOpenNow(cafe.open_time, cafe.close_time);

  card.innerHTML = `
    <div class="cafe-card-top">
      <div>
        <div class="cafe-name">${escape(cafe.name)}</div>
        <div class="cafe-hours">${cafe.open_time} – ${cafe.close_time}</div>
      </div>
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:0.3rem">
        ${cafe.distance != null ? `<div class="cafe-distance">${formatDistance(cafe.distance)}</div>` : ''}
        <span class="open-badge ${open ? 'open' : 'closed'}">${open ? 'Open' : 'Closed'}</span>
      </div>
    </div>
    <div class="cafe-tags">
      ${renderTags(cafe.tags)}
    </div>
  `;

  return card;
}

export function renderDetail(cafe, container) {
  const open = isOpenNow(cafe.open_time, cafe.close_time);

  container.innerHTML = `
    <div class="sheet-name">${escape(cafe.name)}</div>
    <span class="open-badge ${open ? 'open' : 'closed'}" style="display:inline-block;margin-bottom:0.5rem">
      ${open ? 'Open now' : 'Closed'}
    </span>
    <div class="sheet-row">&#128337; <span>${cafe.open_time} – ${cafe.close_time}</span></div>
    ${cafe.distance != null ? `<div class="sheet-row">&#128205; <span>${formatDistance(cafe.distance)}</span></div>` : ''}
    <div class="sheet-tags">${renderTags(cafe.tags)}</div>
    ${cafe.phone ? `<a class="sheet-phone" href="tel:${cafe.phone}">&#128222; Call ${escape(cafe.phone)}</a>` : ''}
  `;
}

function renderTags(tags) {
  if (!tags || tags.length === 0) return '';
  return tags.map(t => `<span class="tag ${t.replace(/\s+/g, '-')}">${escape(t)}</span>`).join('');
}

export function isOpenNow(openTime, closeTime) {
  const now = new Date();
  const [oh, om] = openTime.split(':').map(Number);
  const [ch, cm] = closeTime.split(':').map(Number);
  const cur = now.getHours() * 60 + now.getMinutes();
  const open = oh * 60 + om;
  const close = ch * 60 + cm;
  if (close < open) return cur >= open || cur < close; // overnight
  return cur >= open && cur < close;
}

function escape(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
