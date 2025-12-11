import { createChartPie } from './chartPie.js'
import { createChartBar } from './chartBar.js'
import { createChartLine } from './chartLine.js'
import { createChartHorizontalBar } from './chartHorizontalBar.js'
import { injectionCardValueAdmin } from './cardValue.js'

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

    const chart_by_team = {
        'data': data.chart_per_team,
        'id': "chart-team"
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

    const chart_average_cost_fuel_per_team = {
        'data': data.chart_average_cost_fuel_per_team,
        'id': "chart-avg-cost-fuel-per-team",
    }

    const chart_average_cost_km = {
        'data': data.chart_average_cost_km,
        'id': "chart-avg-cost-km",
    }

    function dashbordAdmin(){
        createChartPie(chart_by_category.id, chart_by_category.data);
        createChartHorizontalBar(chart_by_team.id, chart_by_team.data, false);
        createChartLine(chart_by_month.id, chart_by_month.data, true);
        createChartBar(chart_average_by_day.id, chart_average_by_day.data, true);
        createChartHorizontalBar(chart_average_fuel.id, chart_average_fuel.data, false);
        createChartHorizontalBar(chart_average_cost_fuel_per_team.id, chart_average_cost_fuel_per_team.data, true);
        createChartHorizontalBar(chart_average_cost_km.id, chart_average_cost_km.data, true);
        injectionCardValueAdmin(data);
    }

    if (data.role == "COMPANY_ADMIN") {
        dashbordAdmin()
    } 
})