$(function () {
    $('.left > iframe').attr('src', $(".left > input").val());
    responsive();
});

function responsive() {
    $(".left > iframe").css({
        "height": $(window).height() - $(".left > input").height()
    });
}

$(window).resize(function () {
   responsive();
});

$(".left > input").bind('keypress', function (e) {
    if (e.keyCode == '13') {
        $('.left > iframe').attr('src', $(this).val());
    }
});