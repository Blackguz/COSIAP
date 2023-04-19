document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("solicitudesPorNivelEstudios").getContext("2d");

  const data = {
    labels: niveles_estudios,
    datasets: [
      {
        label: "Solicitudes por nivel de estudios",
        data: solicitudes_por_nivel,
        backgroundColor: [
          "rgba(75, 192, 192, 0.5)",
          "rgba(255, 206, 86, 0.5)",
          "rgba(255, 99, 132, 0.5)"
        ],
        borderColor: [
          "rgba(75, 192, 192, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(255, 99, 132, 1)"
        ],
        borderWidth: 1
      }
    ]
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  const solicitudesPorNivelEstudiosChart = new Chart(ctx, {
    type: "bar",
    data: data,
    options: options
  });


  function graficoGeneros(data) {
    const ctx = document.getElementById("solicitudesPorGenero").getContext("2d");
    const chart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Masculino", "Femenino"],
        datasets: [
          {
            label: "Género",
            data: data,
            backgroundColor: ["rgba(75, 192, 192, 0.2)", "rgba(255, 99, 132, 0.2)"],
            borderColor: ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)"],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
  graficoGeneros(generos);
});
