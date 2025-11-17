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


// In this function, a bar chart is created
async function createChart(id, type, url) {

    const data = await fetchChartData(url)

    const ctx = document.getElementById(id);

    if (type == 'bar' || type == 'pie' || type == 'doughnut') {
        const config = {
            type: type,
            data: {
                labels: data.xValues,
                datasets: [{
                    backgroundColor: data.barColors,
                    data: data.yValues
                }]
            },
            options: {
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: data.chartName,
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
                            // drawBorder: false
                        }
                    }
                }
            }
        }
        new Chart(ctx, config);
    }

    else if (type == "scatter") {
        const config = {
            type: type,
            data: {
                datasets: [{
                    pointRadius: 4,
                    pointBackgroundColor: "rgba(255, 0, 0, 1)",
                    backgroundColor: "rgba(0, 8, 255, 1)",
                    data: data
                }]
            },
            options: {
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "House Prices vs. Size",
                        font: { size: 16 }
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
                labels: data.xValues,
                datasets: [{
                    fill: false,
                    lineTension: 0,
                    backgroundColor: "rgba(0,0,255,1.0)",
                    borderColor: "rgba(0,0,255,0.1)",
                    data: data.yValues
                }]
            },
            options: {
                
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "House Prices vs. Size",
                        font: { size: 16 }
                    }
                }
            }
        }
        new Chart(ctx, config);
    }


}



document.addEventListener('DOMContentLoaded', async () => {
    await createChart('chart-bars', 'bar', '/api/expenses/')
    await createChart('chart-pie', 'pie', '/api/expenses/')
})