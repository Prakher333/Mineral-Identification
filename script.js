document.addEventListener('DOMContentLoaded', () => {
    const uploadBox = document.getElementById('upload-box');
    const fileInput = document.getElementById('file-input');
    const previewBox = document.getElementById('preview-box');
    const previewImage = document.getElementById('preview-image');
    const removeBtn = document.getElementById('remove-btn');
    const identifyBtn = document.getElementById('identify-btn');

    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadBox.addEventListener(eventName, preventDefaults);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadBox.addEventListener(eventName, () => {
            uploadBox.classList.add('highlight');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadBox.addEventListener(eventName, () => {
            uploadBox.classList.remove('highlight');
        });
    });

    // Handle file upload
    uploadBox.addEventListener('drop', handleDrop);
    uploadBox.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFiles);
    removeBtn.addEventListener('click', removeImage);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files } });
    }

    function handleFiles(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                uploadBox.style.display = 'none';
                previewBox.style.display = 'block';
                identifyBtn.disabled = false;
            }
            reader.readAsDataURL(file);
        }
    }

    function removeImage() {
        previewBox.style.display = 'none';
        uploadBox.style.display = 'block';
        fileInput.value = '';
        identifyBtn.disabled = true;
        previewImage.src = "";
        document.getElementById("result").innerHTML = "";
    }

});

// making API call for prediction
async function uploadImage() {
    let btn = document.getElementById('identify-btn');
    let input = document.getElementById("file-input").files[0];

    btn.disabled = true;
    btn.innerText = "Analyzing...";

    if (!input) {
        alert("Please select an image.");
        return;
    }

    let formData = new FormData();
    formData.append("file", input);

    try {
        let response = await fetch("https://mineral-identification.onrender.com/predict", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        document.getElementById("result").innerHTML = `<h2>Mineral : <h1>${result.mineral}</h1></h2>`;

    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }

    btn.disabled = false;
    btn.innerText = "Analyze Rock";
}
