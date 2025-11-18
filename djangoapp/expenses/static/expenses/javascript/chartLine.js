import { currency_status } from './utils.js'

export async function createChartLine(id, data, ticks_status ) {

    const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: {
                    ticks: currency_status(ticks_status),
                    grid: {
                        display: false,
                    }
                },
                x: {
                    grid: {
                        display: false,
                    }
                }
            }
        }
    };

        const ctx = document.getElementById(id);
        new Chart(ctx, config);
}
