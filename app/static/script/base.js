document.addEventListener("DOMContentLoaded", function() {
    handleAlerts();
});

// Make flash messages disappear after 10 seconds
function handleAlerts() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 600); 
        }, 6000);
    });
}

// Toggle password visibility
function togglePasswordVisibility(password_id) {
    var passwordInput = document.getElementById(password_id);
    var isVisibility = passwordInput.type === 'text';
    passwordInput.type = isVisibility ? 'password' : 'text';
    var toggle_icon = passwordInput.nextElementSibling.querySelector('i');
    toggle_icon.className = isVisibility ? 'fa-regular fa-eye' : 'fa-regular fa-eye-slash';

    // Update aria-label or title for screen readers
    var actionText = isVisibility ? 'Show Password' : 'Hide Password';
    passwordInput.nextElementSibling.setAttribute('aria-label', actionText);
    passwordInput.nextElementSibling.setAttribute('title', actionText);
};

// change password input border color based on password complexity and enable/disable submit button
function validatePassword(password_id, tooltip_id) {
    var passwordInput = document.getElementById(password_id);
    var tooltip = document.getElementById(tooltip_id)
    var submitButton = passwordInput.form.querySelector('button[type=submit]')
    var pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$/;
    
    if (pattern.test(passwordInput.value)) {
        passwordInput.style.borderColor = 'green';
        tooltip.style.display = 'none';
        submitButton.disabled = false;
    } else {
        passwordInput.style.borderColor = 'red';
        tooltip.style.display = 'block';
        submitButton.disabled = true;
    }
}

// Preview image before upload
function previewImg(event) {
    var files = event.target.files;
    var previewContainer = event.target.getAttribute('data-preview')
    var imgPreviewContainer = document.getElementById(previewContainer);
    imgPreviewContainer.innerHTML = '';

    for (var i = 0; i < files.length; i++) {
        // only process image files
        if (!files[i].type.match('image.*')) {
            continue;
        }
        var reader = new FileReader();
        reader.onload = (function(theFile) {
            return function(e) {
                var imgDiv = document.createElement('div');
                imgDiv.classList.add('col-3', 'my-2');
                // create img element
                var img = document.createElement('img');
                img.classList.add('img-fluid', 'rounded', 'border', 'shadow-sm');
                img.src = e.target.result;
                img.alt = theFile.name;
                // append img to father div
                imgDiv.appendChild(img);
                imgPreviewContainer.appendChild(imgDiv);
            };
        })(files[i]);
        reader.readAsDataURL(files[i]);
    }
};

// reset form after modal is closed
function resetForm(modal_id) {
    var modal = document.getElementById(modal_id);
    var form = modal.querySelector('form')
    if (form) {
        form.reset();
    }
    // reset weed image preview
    var primaryImgPreview = modal.querySelector('[id^=primary-image-preview]')
    var moreImgPreview = modal.querySelector('[id^=more-image-preview]')
    var updateMoreImgPreview = modal.querySelectorAll('[id^=update-more-image-preview]')
    if (primaryImgPreview) {
        primaryImgPreview.innerHTML = '';
    }
    if (moreImgPreview) {
        moreImgPreview.innerHTML = '';
    }
    if (updateMoreImgPreview) {
        updateMoreImgPreview.forEach(function(preview) {
            preview.innerHTML = '';
        })
    }
}

// mark image for deletion
function markForDeletion(imageName, parentIndex, index) {
    var currentImage = document.getElementById('images_to_delete' + parentIndex);
    if (currentImage.value) {
        currentImage.value += ',' + imageName;
    } else {
        currentImage.value = imageName;
    }
    var imgDiv = document.getElementById('imgDiv' + parentIndex + '_' + index);
    imgDiv.style.display = 'none';
}