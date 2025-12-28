document.addEventListener("DOMContentLoaded", function () {
  // Cargar datos asíncronamente después de que la página ya se haya renderizado.
  fetch("/api/estadisticas")
    .then(resp => {
      if (!resp.ok) throw new Error("Error al obtener estadísticas");
      return resp.json();
    })
    .then(data => {
      renderLineChart(data.by_day);
      renderPieChart(data.by_type);
      renderColumnChart(data.by_month);
    })
    .catch(err => {
      console.error("No se pudieron cargar las estadísticas:", err);
      // Mostrar mensajes mínimos en los contenedores
      document.getElementById("chart-line").innerText = "No se pudieron cargar los datos.";
      document.getElementById("chart-pie").innerText = "No se pudieron cargar los datos.";
      document.getElementById("chart-column").innerText = "No se pudieron cargar los datos.";
    });
});

function renderLineChart(by_day) {
  // by_day = [{date: "2025-10-01", count: N}, ...]
  const categories = by_day.map(x => x.date);
  const data = by_day.map(x => x.count);

  Highcharts.chart('chart-line', {
    chart: { type: 'line' },
    title: { text: 'Avisos de adopción agregados por día' },
    xAxis: {
      categories: categories,
      title: { text: 'Día' },
      labels: { rotation: -45 }
    },
    yAxis: {
      title: { text: 'Cantidad de avisos' },
      allowDecimals: false
    },
    series: [{
      name: 'Avisos',
      data: data
      
    }],
    credits: { enabled: false },
    legend: { enabled: false },
    responsive: {
      rules: [{
        condition: { maxWidth: 500 },
        chartOptions: { legend: { enabled: false } }
      }]
    }
  });
}

function renderPieChart(by_type) {
  const gato = by_type.gato || 0;
  const perro = by_type.perro || 0;
  Highcharts.chart('chart-pie', {
    chart: { type: 'pie' },
    title: { text: 'Proporción de avisos por tipo de mascota' },
    series: [{
      name: 'Avisos',
      colorByPoint: true,
      data: [
        { name: 'Gato', y: gato },
        { name: 'Perro', y: perro }
      ]
    }],
    credits: { enabled: false }
  });
}

function renderColumnChart(by_month) {
  // by_month = { months: ['2025-01','2025-02',...], gatos: [...], perros: [...] }
  const months = by_month.months || [];
  const gatos = by_month.gatos || [];
  const perros = by_month.perros || [];

  Highcharts.chart('chart-column', {
    chart: { type: 'column' },
    title: { text: 'Avisos por mes (gatos vs perros)' },
    xAxis: {
      categories: months,
      title: { text: 'Mes' }
    },
    yAxis: {
      min: 0,
      title: { text: 'Cantidad de avisos' },
      allowDecimals: false
    },
    plotOptions: {
      column: { grouping: true, shadow: false, borderWidth: 0 }
    },
    series: [
      { name: 'Gatos', data: gatos },
      { name: 'Perros', data: perros }
    ],
    credits: { enabled: false }
  });
}
