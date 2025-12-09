import { createChartPie } from './chartPie.js'
import { createChartBar } from './chartBar.js'
import { createChartLine } from './chartLine.js'
import { atualizarCard } from './cardValue.js'

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

document.addEventListener('DOMContentLoaded', async () => {
    const data = await fetchChartData('/api/expenses')

    const chart_by_category = {
        'data': data.chart_by_category,
        'id': "chart-category"
    }

    const chart_by_cycle = {
        'data': data.chart_by_cycle,
        'id': "chart-cycle"
    }

    const chart_by_month = {
        'data': data.chart_by_month,
        'id': "chart-month",
    }

    const chart_average_by_day = {
        'data': data.chart_average_by_day,
        'id': "chart-avg-day",
    }

    const chart_average_fuel = {
        'data': data.chart_average_fuel,
        'id': "chart-avg-fuel",
    }

    const chart_average_cost_fuel = {
        'data': data.chart_average_cost_fuel,
        'id': "chart-avg-cost-fuel",
    }

    const chart_average_cost_km = {
        'data': data.chart_average_cost_km,
        'id': "chart-avg-cost-km",
    }

    createChartPie(chart_by_category.id, chart_by_category.data);
    createChartBar(chart_by_cycle.id, chart_by_cycle.data, true);
    createChartLine(chart_by_month.id, chart_by_month.data, true);
    createChartBar(chart_average_by_day.id, chart_average_by_day.data, true);
    createChartBar(chart_average_fuel.id, chart_average_fuel.data, false);
    createChartBar(chart_average_cost_fuel.id, chart_average_cost_fuel.data, true);
    createChartBar(chart_average_cost_km.id, chart_average_cost_km.data, true);
    atualizarCard(data);
})