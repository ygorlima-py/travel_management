export async function injectionCardValueAdmin(data) {
    const cardTotalEnterprise = document.getElementById('total-enterprise'); 
    const cardTeamRegister = document.getElementById('team-registers');
    const cardProjectionMonth = document.getElementById('projection-month');
    const teamRegisters = data.team_registers;
    const totalEnterpriseValue = data.total_enterprise;     
    const projectionMonth = data.projection_month;

    cardTotalEnterprise.textContent = `R$ ${totalEnterpriseValue.toFixed(2).replace('.', ',')}`; 
    cardTeamRegister.textContent = teamRegisters
    cardProjectionMonth.textContent = `R$ ${projectionMonth.toFixed(2).replace('.', ',')}`;
}