const pictureFrame = document.getElementById('nf-picture');
const pictureInput = document.getElementById('picture-input');

const dragOver = (event) => {
    event.preventDefault();
};


const dragEnter = (event) => {
    const target = event.target
    target.classList.add("drag-drop-highlight");
};

const dragLeave = (event) => {
    const target = event.target
    target.classList.remove("drag-drop-highlight");
};

const drop = (event) => {
    event.preventDefault();
    const frame = event.currentTarget;
    frame.classList.remove("drag-drop-highlight");

    const file = event.dataTransfer.files[0];
    if (!file) return;

    // Create DataTransfer and attribute to input
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    pictureInput.files = dataTransfer.files;

    if (file.type.startsWith("image/")) {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.maxWidth = "100%";
        img.style.maxHeight = "70%";

        frame.innerHTML = "";   // limpa o quadro
        frame.appendChild(img);
    }
    
};

pictureFrame.addEventListener("dragover", dragOver);
pictureFrame.addEventListener("dragenter", dragEnter);
pictureFrame.addEventListener("dragleave", dragLeave);
pictureFrame.addEventListener("drop", drop);
pictureFrame.addEventListener("click", () => {
    if (!pictureInput.files.length) {
        pictureInput.click();
    }

});

// It triggers when the input value changes.
pictureInput.addEventListener('change', (event)=> {
    const file = event.target.files[0];
    if (!file) return;
    
    if (file.type.startsWith("image/")) {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.maxWidth = "100%";
        img.style.maxHeight = "100vh";

        pictureFrame.innerHTML = "";   // limpa o quadro
        pictureFrame.appendChild(img);
    }

});

// Show picture recive in the drag and drop
window.addEventListener('DOMContentLoaded', function() {
    const dragDrop = document.getElementById('nf-picture');
    const img = dragDrop.querySelector('img');

    if (img) {
        dragDrop.style.padding = '0';
        pictureInput.removeAttribute('required'); // Remove the atribute required of input
    }

    const form = document.getElementById('form-expense');
    
    form.addEventListener('submit', function(e) {
        const dragDrop = document.getElementById('nf-picture');
        const img = dragDrop.querySelector('img');

        if (!img && (!pictureInput.files || pictureInput.files.length === 0)) {
            alert('Por favor, adicione uma imagem do recibo!');
            e.preventDefault();
            return false;
        }
    });
});

    
