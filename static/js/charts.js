// Инициализация графика объемов отгрузок
function initVolumeChart(currentWeekData, nextWeekData) {
  const days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'];
  
  const ctx = document.getElementById('volumeChart').getContext('2d');
  const volumeChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: days,
      datasets: [
        {
          label: 'Текущая неделя',
          data: currentWeekData,
          backgroundColor: 'rgba(52, 152, 219, 0.7)',
          borderColor: 'rgba(52, 152, 219, 1)',
          borderWidth: 1
        },
        {
          label: 'Следующая неделя',
          data: nextWeekData,
          backgroundColor: 'rgba(46, 204, 113, 0.7)',
          borderColor: 'rgba(46, 204, 113, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Объем (тонн)'
          }
        }
      }
    }
  });
}

// Инициализация тултипов
function initTooltips() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });
}

// Инициализация всех компонентов при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
  // Тултипы инициализируются всегда
  initTooltips();
  
  // График инициализируется, если есть элемент на странице
  if (document.getElementById('volumeChart')) {
    // Данные будут переданы из шаблона
    if (typeof currentWeekVolumeData !== 'undefined' && typeof nextWeekVolumeData !== 'undefined') {
      initVolumeChart(currentWeekVolumeData, nextWeekVolumeData);
    }
  }
});
