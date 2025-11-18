// Create chart type pie
export async function createChartPie(id, data) {

    // Append '4d' to the colors (alpha channel), except for the hovered index
    function handleHover(evt, item, legend) {
        legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
            colors[index] = index === item.index || color.length === 9 ? color : color + '4D';
        });
        legend.chart.update();
    }

    // Removes the alpha channel from background colors
    function handleLeave(evt, item, legend) {
        legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
            colors[index] = color.length === 9 ? color.slice(0, -2) : color;
        });
        legend.chart.update();
    }

    const ctx = document.getElementById(id);
    const config = {
        type: 'pie',
        data: data,
        options: {
            plugins: {
                legend: {
                    onHover: handleHover,
                    onLeave: handleLeave
                }
            }
        }
    };

    new Chart(ctx, config);
}