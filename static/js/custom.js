document.addEventListener( 'DOMContentLoaded', ()=>{ // Ожидание готовности документа
    let div = document.querySelector('.form-group');

    window.scrollTo({
        top: $('#js-scroll').offset().top, // Здесь вычисление позиции может быть сложнее
        behavior: 'smooth', // Плавность прокрутки, убрать если не нужно
    });
});




function processImage(e) {
    var img = $(this);
    var maxWidth = 250; // Max width for the image
    var maxHeight = 250;    // Max height for the image
    var ratio = 0;  // Used for aspect ratio
    var width = img.width();    // Current image width
    var height = img.height();  // Current image height

    // Check if the current width is larger than the max
    if(width > maxWidth){
        ratio = maxWidth / width;   // get ratio for scaling image
        img.css("width", maxWidth); // Set new width
        img.css("height", height * ratio);  // Scale height based on ratio
        height = height * ratio;    // Reset height to match scaled image
        width = width * ratio;    // Reset width to match scaled image
    }

    // Check if current height is larger than max
    if(height > maxHeight){
        ratio = maxHeight / height; // get ratio for scaling image
        img.css("height", maxHeight);   // Set new height
        img.css("width", width * ratio);    // Scale width based on ratio
        width = width * ratio;    // Reset width to match scaled image
        height = height * ratio;    // Reset height to match scaled image
    }
}

// функция проверяющая статус картинки, загружена или нужно ли ждать
function IsImageOk(img) {
    // During the onload event, IE correctly identifies any images that
    // weren’t downloaded as not complete. Others should too. Gecko-based
    // browsers act like NS4 in that they report this incorrectly.
    if (!img.complete) {
        return false;
    }

    // However, they do have two very useful properties: naturalWidth and
    // naturalHeight. These give the true size of the image. If it failed
    // to load, either of these should be zero.

    if (typeof img.naturalWidth !== "undefined" && img.naturalWidth === 0) {
        return false;
    }

    // No other way of checking: assume it’s ok.
    return true;
}

$('img[data-resize]').each(function(){
    // проверяем, может картинка уже загружена?
    if (IsImageOk(this)) {
         processImage.call(this);
    } else {
        $(this).on('load', processImage);
    }
});