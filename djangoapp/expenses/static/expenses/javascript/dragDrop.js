const pictureFrame = document.getElementById('nf-picture');

let dropFile = null;

const dragOver = (event) => {
    event.preventDefault();
};


const dragEnter = ({target}) => {
    console.log(target);
    target.classList.add("drag-drop-highlight");
};

const dragLeave = ({target}) => {
    console.log(target);
    target.classList.remove("drag-drop-highlight");
};

const drop = (event) => {
    event.preventDefault();
    const frame = event.currentTarget;
    frame.classList.remove("drag-drop-highlight");

    const file = event.dataTransfer.files[0];
    if (!file) return;

    if (file.type.startsWith("image/")) {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.maxWidth = "100%";
        img.style.maxHeight = "100%";
        frame.style.textAlign = "center"

        frame.innerHTML = "";   // limpa o quadro
        frame.appendChild(img);
    }
    
};

pictureFrame.addEventListener("dragover", dragOver);
pictureFrame.addEventListener("dragenter", dragEnter);
pictureFrame.addEventListener("dragleave", dragLeave);
pictureFrame.addEventListener("drop", drop);