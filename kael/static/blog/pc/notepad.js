$(function () {
    $('.left > iframe').attr('src', $(".left > input").val());
    responsive();
});

function responsive() {
    $(".left > iframe").css({
        "height": $(window).height() - $(".left > input").height() - $('.title').height(),
    });

    $(".right > .r_top").css({
        "height": $(window).height() / 2 - $(".title").height(),
        "width": "100%"
    });

    $(".right > .r_bottom").css({
        "height": $(window).height() / 2 - $(".title").height() - 2,
        "width": "100%"
    })
}

$(window).resize(function () {
   responsive();
});

$(".left > input").bind('keypress', function (e) {
    if (e.keyCode == '13') {
        $('.left > iframe').attr('src', $(this).val());
    }
});