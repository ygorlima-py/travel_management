export async function injectionCardValue(data) {
    if (data.role == "COMPANY_ADMIN") {
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
    else if (data.role == "MANAGER"){
        const cardTotalPendingTeamValue = document.getElementById('pending-expenses-value'); 
        const cardTotalApprovedMonth = document.getElementById('total-approved-month');
        const cardAwaitingApproval = document.getElementById('awaiting-approval');
        const cardTeamMembers = document.getElementById('team-members');
        const TotalPendingTeamValue = data.total_pending_team;
        const TotalApprovedMonth = data.total_approved_month;     
        const AwaitingApproval = data.awaiting_approval;
        const teamMembers = data.team_members;

        cardTotalPendingTeamValue.textContent = `R$ ${TotalPendingTeamValue.toFixed(2).replace('.', ',')}`; 
        cardTotalApprovedMonth.textContent = `R$ ${TotalApprovedMonth.toFixed(2).replace('.', ',')}`;
        cardAwaitingApproval.textContent = AwaitingApproval;
        cardTeamMembers.textContent = teamMembers;

        }
    }
