// 1. Give every avatar its own color (based on the username)
// 1. Give every avatar its own color (based on the username)
document.querySelectorAll('.avatar').forEach(function (el) {
  var name = el.dataset.name || '';
  var sum = 0;
  for (var i = 0; i < name.length; i++) {
    sum += name.charCodeAt(i) * (i + 1);
  }
  el.style.background = 'hsl(' + ((sum * 37) % 360) + ', 70%, 50%)';
});

// 2. Ask before deleting a post
document.querySelectorAll('.delete-form').forEach(function (form) {
  form.addEventListener('submit', function (e) {
    if (!confirm('Delete this post?')) {
      e.preventDefault();
    }
  });
});

// 3. Show / hide the comments of a post
document.querySelectorAll('.toggle-comments').forEach(function (btn) {
  btn.addEventListener('click', function () {
    btn.closest('.post').querySelector('.comments-box').classList.toggle('hidden');
  });
});

// 4. Character counter (turns red near the limit)
var box = document.getElementById('post-content');
var counter = document.getElementById('char-count');
if (box) {
  box.addEventListener('input', function () {
    counter.textContent = box.value.length + '/280';
    counter.classList.toggle('warn', box.value.length > 250);
  });
}

// 5. Theme switcher (remembers your choice)
var themeSelect = document.getElementById('theme-select');
if (themeSelect) {
  themeSelect.value = localStorage.getItem('theme') || 'sunset';
  themeSelect.addEventListener('change', function () {
    document.documentElement.setAttribute('data-theme', themeSelect.value);
    localStorage.setItem('theme', themeSelect.value);
  });
}