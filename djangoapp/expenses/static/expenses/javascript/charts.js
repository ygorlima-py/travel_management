// Here we make the request to fetch the data
async function fetchChartData(url) {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);

        }

        const data = await response.json();

        return data;
    }

    catch (error) {
        console.error('Erro to search data: ', error)

        return {
            xValues: ['erro'],
            yValues: [0],
            barColors: ['grey'],
        }
    }
}

// Tranfform unity to Real Brazilian
const currency = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
})

// In this function, a bar chart is created
async function createChart(id, type, url) {

    const data = await fetchChartData(url)

    const ctx = document.getElementById(id);

    if (type == 'bar' || type == 'pie' || type == 'doughnut') {
        const config = {
            type: type,
            data: {
                labels: data.chart_by_category.xValues,
                datasets: [{
                    backgroundColor: data.chart_by_category.barColors,
                    data: data.chart_by_category.yValues
                }]
            },

            options: {
                plugins: {
                    legend: { 
                        display: true,
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: data.chart_by_category.chartName,
                        font: { size: 16 }
                    }
                },
                scales: {
                    x: {
                        display: false,
                        grid: {
                            display: true,
                            drawBorder: false
                        }
                    },
                    y: {
                        display: false,
                        grid: {
                            display: true,
                            drawBorder: true
                        },
                        ticks: {
                        callback: (value) => currency.format(value)
                    }
                    }
                }
            }
        }
        new Chart(ctx, config);
    }

    else if (type == "line") {
    
        const config = {
            type: type,
            data: {
                labels: data.chart_by_month.xValues,
                datasets: [{
                    fill: false,
                    lineTension: 0,
                    backgroundColor: "rgba(0,0,255,1.0)",
                    borderColor: "rgba(0,0,255,0.1)",
                    data: data.chart_by_month.yValues
                }]
            },
            options: {       
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: data.chart_by_month.chartName,
                        font: { size: 16 }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    },
                    y: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            callback: (value) => currency.format(value)
                        }
                    }
                }


            }
        }
        new Chart(ctx, config);
    }


}



document.addEventListener('DOMContentLoaded', async () => {
    await createChart('chart-pie', 'pie', '/api/expenses/'),
    await createChart('custo-x-ciclo', 'bar', '/api/expenses/'),
    await createChart('chart-line', 'line', '/api/expenses/')
    await createChart('custo-dia-x-ciclo', 'bar', '/api/expenses/')
})