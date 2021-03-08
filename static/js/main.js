(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {

        setHeight();
        window.addEventListener("resize", setHeight);

        var title = document.title;

        var progressbar = $('#progressbar');
        var one = $('#one');
        var two = $('#two');
        var three = $('#three')


        switch (title) {
            case "Subir Archivo · RS Report":

                var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))

                var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
                    return new bootstrap.Popover(popoverTriggerEl)
                })

                progressbar.prop('style', 'width: 0%;');

                two.removeClass('btn-primary');
                two.addClass('btn-secondary');

                three.removeClass('btn-primary');
                three.addClass('btn-secondary');

                break;

            case "Características del Archivo · RS Report":

                progressbar.prop('style', 'width: 50%;');

                two.removeClass('btn-secondary');
                two.addClass('btn-primary');

                three.removeClass('btn-primary');
                three.addClass('btn-secondary');

                break;

            case "Creación del Reporte · RS Report":

                progressbar.prop('style', 'width: 100%;');

                two.removeClass('btn-secondary');
                two.addClass('btn-primary');

                three.removeClass('btn-secondary');
                three.addClass('btn-primary');

                CKEDITOR.replace('placedescription');
                break;

            case "Dashboard · RS Report":

                var map = L.map('mapid').setView([5.567541725282831, -73.33807725929755], 17);

                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map);

                L.marker([5.567541725282831, -73.33807725929755]).addTo(map)
                    .bindPopup('Tooltip de Prueba')
                    .openPopup()

                break;

            default:
                break;
        }

    });


})();


function setHeight() {
    var hWindow = window.innerHeight;
    var hHeader = document.getElementById('header').clientHeight;
    var hFooter = document.getElementById('footer').clientHeight;

    var body = document.getElementById('body');

    body.setAttribute('style', `min-height: calc(${hWindow}px - ${hHeader}px - ${hFooter}px);`);
}