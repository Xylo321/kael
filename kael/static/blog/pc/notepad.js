$(function () {
    var kanban_url = $(".left > input").val();
    $(".kanban_url").attr("value", kanban_url);
    $('.kanban_iframe').attr('src', kanban_url);
    $('.kanban_iframe').show();

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
        if($('.kanban_iframe').is(":visible")) {
            $('.kanban_iframe').attr('src', $(this).val());
        }
        if($('.liulanqi_iframe').is(':visible')) {
            $('.liulanqi_iframe').attr('src', $(this).val());
        }
    }
});

$(".kanban_bt").click(function () {
    if($(".liulanqi_iframe").is(":visible")) {
        var liulanqi_url = $(".left > input").val();
        $(".liulanqi_url").attr("value", liulanqi_url);
        $(".left > input").val($(".kanban_url").attr("value"));
    }
    $(".liulanqi_iframe").hide();
    $(".kanban_iframe").show();
    $(this).css({
        "color": "yellow"
    });
    $(".liulanqi_bt").css({
        "color": "white"
    });
});

$(".liulanqi_bt").click(function () {
    if($(".kanban_iframe").is(":visible")) {
        var kanban_url = $(".left > input").val();
        $(".kanban_url").attr("value", kanban_url);
        $(".left > input").val($(".liulanqi_url").attr("value"));
    }
    $(".kanban_iframe").hide();
    $(".liulanqi_iframe").show();

    $(this).css({
        "color": "yellow"
    });
    $(".kanban_bt").css({
        "color": "white"
    });
});