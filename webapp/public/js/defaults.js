function resize(elms) {
    elms.each(function (i) {
        $(this).height($(window).height() - 10 - $(this).offset().top)
    });
};

$(document).ready(function() {
    resize($('#map_canvas, #panel_right'));
    
    $(window).resize(function(event) {
        resize($('#map_canvas, #panel_right'));
    });
    
    $("#toggle_about").click(function(event) {
        $("#about").toggle();
        resize($('#panel_right'));
    });
});