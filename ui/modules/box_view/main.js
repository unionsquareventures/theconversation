$(document).ready(function() {
    $(".post .title").ellipsis();

    $(".box_view").masonry({
        itemSelector: '.post',
        columnWidth: 270,
        gutterWidth: 30,
        isAnimated: true,
    });

});

