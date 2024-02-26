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

function previewImg(event) {
    var files = event.target.files;
    var previewContainer = event.target.getAttribute('data-preview')
    var imgPreviewContainer = document.getElementById(previewContainer);
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

document.addEventListener("DOMContentLoaded", function() {
    var addModal = document.getElementById('addWeedModal')

    addModal.addEventListener('hidden.bs.modal', function() {
        var form = addModal.querySelector('form');
        form.reset();

        var primaryImgPreview = addModal.querySelector('[id^=primary-image-preview]')
        var moreImgPreview = addModal.querySelector('[id^=more-image-preview]')
        if (primaryImgPreview) {
            primaryImgPreview.innerHTML = '';
        }
        if (moreImgPreview) {
            moreImgPreview.innerHTML = '';
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var updateModal = document.querySelectorAll('[id^=updateWeedModal]')

    updateModal.forEach(function(modal) {
        modal.addEventListener('hidden.bs.modal', function() {
            var form = modal.querySelector('form');
            form.reset();

            var moreImgPreview = modal.querySelector('[id^=update-more-image-preview]')
            if (moreImgPreview) {
                moreImgPreview.innerHTML = '';
            }
        });
    });
});

function markForDeletion(imageName, parentIndex, index) {
    var currentImage = document.getElementById('images_to_delete' + parentIndex);
    if (currentImage.value) {
        currentImage.value += ',' + imageName;
    } else {
        currentImage.value = imageName;
    }
    console.log(currentImage)
    console.log(currentImage.value)

    var imgDiv = document.getElementById('imgDiv' + parentIndex + '_' + index);
    imgDiv.style.display = 'none';
}