$('p .fa-chevron-down').click(function () {
    $(this).closest("h2").next("p").slideToggle();
})