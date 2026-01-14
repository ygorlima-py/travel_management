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
        const cardTotalRecusedTeamValue = document.getElementById('recused-expenses-value'); 
        const cardTotalApprovedMonth = document.getElementById('total-approved-month');
        const cardAwaitingApproval = document.getElementById('awaiting-approval');
        const cardTeamMembers = document.getElementById('team-members');
        const TotalRecusedTeamValue = data.total_recused_team;
        const TotalApprovedMonth = data.total_approved_month;     
        const AwaitingApproval = data.awaiting_approval;
        const teamMembers = data.team_members;

        cardTotalRecusedTeamValue.textContent = `R$ ${TotalRecusedTeamValue.toFixed(2).replace('.', ',')}`; 
        cardTotalApprovedMonth.textContent = `R$ ${TotalApprovedMonth.toFixed(2).replace('.', ',')}`;
        cardAwaitingApproval.textContent = AwaitingApproval;
        cardTeamMembers.textContent = teamMembers;

        }
    else if (data.role == "OPERATOR") {
        const cardTotalRecusedValue = document.getElementById('recused-expenses-value'); 
        const cardTotalApprovedMonth = document.getElementById('total-approved-month');
        const cardAwaitingApproval = document.getElementById('awaiting-approval');
        const cardCurrentCicle = document.getElementById('current-cicle')

        const TotalRecusedValue = data.total_recused;
        const TotalApprovedMonth = data.total_approved_month;     
        const AwaitingApproval = data.awaiting_approval;
        const currentCicle = data.current_cicle.name;

        cardTotalRecusedValue.textContent = `R$ ${TotalRecusedValue.toFixed(2).replace('.', ',')}`; 
        cardTotalApprovedMonth.textContent = `R$ ${TotalApprovedMonth.toFixed(2).replace('.', ',')}`;
        cardAwaitingApproval.textContent = AwaitingApproval;
        cardCurrentCicle.textContent = currentCicle;

    }
    }
