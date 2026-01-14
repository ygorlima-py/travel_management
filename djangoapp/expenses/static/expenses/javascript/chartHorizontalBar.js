import { currency_status } from './utils.js'

export async function createChartHorizontalBar(id, data, ticks_status) {
    console.log(data)
    
    const config = {
        type: 'bar',
        data,
        options: {
            indexAxis: 'y',
            scales: {
                    x: {
                        
                    beginAtZero: true,
                    ticks: currency_status(ticks_status)
                }
            }   
        }
    };

        const ctx = document.getElementById(id);
        new Chart(ctx, config);
}