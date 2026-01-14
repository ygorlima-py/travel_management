import { currency_status } from './utils.js'

// Create chart type pie
export async function createChartPie(id, data, ticks_status) {

    const formatter = currency_status(ticks_status);

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
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            
                            if (label) {
                                label += ': ';
                            }
                            
                            // ✅ Aplica formatação se formatter.callback existe
                            if (formatter.callback) {
                                label += formatter.callback(context.parsed);
                            } else {
                                label += context.parsed;
                            }
                            
                            return label;
                        }
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}