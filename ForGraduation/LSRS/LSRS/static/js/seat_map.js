// 颜色状态映射
const STATUS_COLORS = {
  available: '#4CAF50',
  occupied: '#F44336',
  maintenance: '#9E9E9E',
  partial: '#FFEB3B'
};

// 实时刷新机制[^2]
let refreshInterval = {{ refresh_interval|default:60 }} * 1000;

setInterval(() => {
  fetch('/api/seats/status')
    .then(res => res.json())
    .then(updateSeatColors);
}, refreshInterval);

function updateSeatColors(data) {
  document.querySelectorAll('.seat').forEach(seat => {
    const status = data[seat.dataset.seatid];
    seat.style.fill = STATUS_COLORS[status];
  });
}
