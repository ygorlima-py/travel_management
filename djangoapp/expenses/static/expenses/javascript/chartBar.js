import { currency_status } from './utils.js'

export async function createChartBar(id, data, ticks_status) {

    const config = {
            type: 'bar',
            data: data,
            options: {
                scales: {
                    y: {
                        
                        beginAtZero: true,
                        ticks: currency_status(ticks_status)
                    },
                    x: {
                        grid: {
                            display: false,
                        }
                    }
                }
            },
        };

        const ctx = document.getElementById(id);
        new Chart(ctx, config);
}