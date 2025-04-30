const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const browseBtn = document.getElementById('browse-btn');
const uploadingFilesContainer = document.getElementById('uploading-files');
const api_url = 'http://54.226.227.106/upload'; //once it sent to me  change it
const allowedTypes = [
  'application/pdf',
  'image/jpeg',
  'image/png',
  'text/plain'
];

browseBtn.addEventListener('click', () => {
  fileInput.click();
});

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.style.backgroundColor = 'rgba(0, 0, 0, 0.3)';
});

dropZone.addEventListener('dragleave', () => {
  dropZone.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
  const files = e.dataTransfer.files;
  handleFiles(files);
});

fileInput.addEventListener('change', (e) => {
  handleFiles(e.target.files);
});

function handleFiles(files) {
  Array.from(files).forEach(file => {
    if(!allowedTypes.includes(file.type)) {
      shwToast('Invalid file type ❌');
      return;
    }

    const fileItem = document.createElement('div');
    fileItem.classList.add('file-item');

    fileItem.innerHTML = `
      <div class="file-name">${file.name}</div>
      <div class="progress-bar">
        <div class="progress" style="width: 0%;"></div>
      </div>
      <div class="file-status">Uploading...</div>
    `;

    uploadingFilesContainer.appendChild(fileItem);

    const progress = fileItem.querySelector('.progress');
    const status = fileItem.querySelector('.file-status');

    const formData = new FormData();
    formData.append('file', file);

    // Using XMLHttpRequest  to handel the progress event
    const xhr = new XMLHttpRequest();
    xhr.open ('POST', api_url, true);

    //Track progress to handel progress event
    xhr.upload.onprogress = function (e) {
        if (e.lengthComputable) {
            const precent = (e.loaded / e.total) * 100;
            progress.style.width = precent + '%';

            if(precent < 50) {
              status.textContent = `Uploading... ${Math.round(percent)}%`;
            } else if (precent < 100 && precent > 50){
              status.textContent = `Halfway there 🏃‍♂️💨 (${Math.round(percent)}%)`;
            }
        }
    };

    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            progress.style.width = '100%';
            status.innerHTML = `File uploaded successfully 🤟🏻. <a href="${response.url}" target="_blank">Download File</a>`;
            shwToast('Upload successfully ☝🏻');
        } else {
            progress.style.backgroundColor = 'red';
            status.innerHTML = 'Upload failed 🥲';
            shwToast('Upload failed 🥲');
        }
    };

    xhr.onerror = function() {
        progress.style.backgroundColor = 'red';
        status.innerHTML =  'Upload failed 🥲';
        shwToast('Upload failed 🥲');
    };
      xhr.send(formData);
  });
}

function shwToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}