document.addEventListener("DOMContentLoaded", function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 600); 
        }, 10000);
    });
});

function togglePasswordVisibility(password_id) {
    var passwordInput = document.getElementById(password_id);
    var isVisibility = passwordInput.type === 'text';
    passwordInput.type = isVisibility ? 'password' : 'text';
    var toggle_icon = passwordInput.nextElementSibling.querySelector('i');
    toggle_icon.className = isVisibility ? 'fa-regular fa-eye' : 'fa-regular fa-eye-slash';
};

function toggleManageButton() {
    var manageButton = document.querySelectorAll('.manage-buttons');
    manageButton.forEach(function(button) {
        if (button.classList.contains('d-none')) {
            button.classList.remove('d-none');
        } else {
            button.classList.add('d-none');
        }
    });
};

function previewImg(event) {
    var files = event.target.files;
    var imgPreviewContainer = document.getElementById('image-preview-container');
    imgPreviewContainer.innerHTML = '';

    for (var i = 0; i < files.length; i++) {
        if (!files[i].type.match('image.*')) {
            continue;
        }
        var reader = new FileReader();
        reader.onload = (function(theFile) {
            return function(e) {
                var imgDiv = document.createElement('div');
                imgDiv.classList.add('col-3', 'my-2');

                var img = document.createElement('img');
                img.classList.add('img-fluid', 'rounded', 'border', 'shadow-sm');
                img.src = e.target.result;
                img.alt = theFile.name;
                imgDiv.appendChild(img);
                imgPreviewContainer.appendChild(imgDiv);
            };
        })(files[i]);
        reader.readAsDataURL(files[i]);
    }
};