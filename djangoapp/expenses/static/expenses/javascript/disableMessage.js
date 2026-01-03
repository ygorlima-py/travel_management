

document.addEventListener('DOMContentLoaded' , () => {
    const messagesContainer = document.querySelector('.message');
    if(!messagesContainer) return;
    
    setTimeout(() => messagesContainer.remove(), 3000);
})