// 强制对齐到15分钟粒度
document.querySelector('input[type="datetime-local"]').addEventListener('input', function(e) {
    const date = new Date(e.target.value);
    const minutes = date.getMinutes();
    date.setMinutes(Math.round(minutes / 15) * 15);  // [^4]
    e.target.value = date.toISOString().slice(0,16);
});
