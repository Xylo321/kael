function SYX() {
    var key_word = $(".key_word").val().trim();

    if(key_word.length > 255) {
        infor("话多非君子所为", function () {
        });
        return;
    }

    $(".article > .human > .opera > .pn > li > .current_page").html("1");
    $(".article > .robot > .opera > .pn > li > .current_page").html("1");
    $(".image > .human > .opera > .pn > li > .current_page").html("1");
    $(".image > .robot > .opera > .pn > li > .current_page").html("1");
    $(".video > .human > .opera > .pn > li > .current_page").html("1");
    $(".video > .robot > .opera > .pn > li > .current_page").html("1");

    // 搜索人类文章
    search_article(key_word, 1, 1);
    // 搜索机器文章
    search_article(key_word, 1, 0);

    // 获取人类文章搜索总页数
    get_article_total_page(key_word, 1);
    // 获取机器文章搜索总页数
    get_article_total_page(key_word, 0);

    // 搜索人类图片
    search_image(key_word, 1, 1);
    // 搜索机器图片
    search_image(key_word, 1, 0);

    // 获取人类图片搜索总页数
    get_image_total_page(key_word, 1);
    // 获取机器图片搜索总页数
    get_image_total_page(key_word, 0);

    // 搜索人类视频
    search_video(key_word, 1, 1);
    // 搜索机器视频
    search_video(key_word, 1, 0);

    // 获取人类视频搜索总页数
    get_video_total_page(key_word, 1);
    // 获取机器视频搜索总页数
    get_video_total_page(key_word, 0);
}

/* 点击搜索 */
$(".send_search").click(function() {
    SYX();
});

/* 解决窗口变小时导航换行的问题 */
$(window).resize(function() {
    responsive();
});

function responsive() {
    // var fw = $(".top > .nav").width() + $(".top > .account").width();
    // if($(window).width() > fw)
    //     $(".top").css({
    //         "width": $(window).width()
    //     })
    // else
    //     $(".top").css({
    //         "width": fw
    //     })
}

/* 退出登陆 */
$("#logout").click(function() {
    $.ajax({
        url: "/account/logout",
        type: 'GET',
        cache: false,
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                infor("退出成功", function () {
                    location.href = "/search/";
                }, false);
            } else {
                infor("退出失败", function () {
                });
            }
        },
        error: function (err) {
            infor("网络错误", function () {
            });
        },
        async: false
    });
});

/* 文章跳转 */
function go_article_page(href) {
    window.open(href);
}

/* 搜索文章 */
function search_article(key_word, page, type) {
    $.ajax({
        url: "/search/search_article",
        data: {
            "key_word": key_word,
            "page": page,
            "type": type
        },
        type: 'POST',
        cache: false,
        dataType: "json",
        success: function(data) {
            if (data.status == 1) {
                // 渲染dom
                var content_html = "";
                for(var i = 0; i < data.data.length; i++) {
                    var article_id = data.data[i].id;
                    var article_title = data.data[i].title;
                    var article_title_param = encodeURIComponent(data.data[i].title).valueOf();
                    var category_name = data.data[i].category_name;
                    var content = data.data[i].content.replace(/[<>&"']/g, "");
                    var href = '/search/go_article_page?article_id=' + article_id + '&article_title=' + article_title_param + '&type=' + type;
                    content_html += "<div><a target=_blank href=" + href + " title='" + content + "'>" + article_title + "</a>" +
                        "<span>" + category_name + "</span></div>";
                }
                switch(type) {
                    case 1:
                        $(".article > .human > fieldset > .content").html(content_html);
                        break;
                    case 0:
                        $(".article > .robot > fieldset > .content").html(content_html);
                        break;
                    default:
                        break;
                }
            } else {
                var content_html = "";
                switch(type) {
                    case 1:
                        $(".article > .human > fieldset > .content").html(content_html);
                        break;
                    case 0:
                        $(".article > .robot > fieldset > .content").html(content_html);
                        break;
                    default:
                        break;
                }
            }
        },
        error: function (err) {
            infor("网络错误", function() {
            });
        },
        async: true
    });
}

/* 获取文章总页数 */
function get_article_total_page(key_word, type) {
    $.ajax({
        url: "/search/search_article_total_page",
        data: {
            "key_word": key_word,
            "type": type
        },
        type: 'POST',
        cache: false,
        dataType: "json",
        success: function(data) {
            if (data.status == 1) {
                // 渲染dom
                var total_page = data.data[0].total_page;
                switch(type) {
                    case 1:
                        $(".article > .human > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    case 0:
                        $(".article > .robot > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    default:
                        break;
                }
            } else {
                var total_page = 0;
                switch(type) {
                    case 1:
                        $(".article > .human > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    case 0:
                        $(".article > .robot > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    default:
                        break;
                }
            }
        },
        error: function (err) {
            infor("网络错误", function() {
            });
        },
        async: true
    });
}

/* 点击下一页：文章，人类 */
$(".article > .human > .opera > .pn > li > .next_page").click(function() {
    var total_page = $(".article > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".article > .human > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page < total_page) {
        current_page += 1;
        $(".article > .human > .opera > .pn > li > .current_page").html(current_page);
        search_article(key_word, current_page, 1);
    }
});

/* 点击上一页：文章，人类 */
$(".article > .human > .opera > .pn > li > .pre_page").click(function() {
    var total_page = $(".article > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);


    var current_page = $(".article > .human > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page > 1) {
        current_page -= 1;
        $(".article > .human > .opera > .pn > li > .current_page").html(current_page);
        search_article(key_word, current_page, 1);
    }
});

/* 点击下一页：文章，机器 */
$(".article > .robot > .opera > .pn > li > .next_page").click(function() {
    var total_page = $(".article > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".article > .robot > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page < total_page) {
        current_page += 1;
        $(".article > .robot > .opera > .pn > li > .current_page").html(current_page);
        search_article(key_word, current_page, 0);
    }
});

/* 点击上一页：文章，机器 */
$(".article > .robot > .opera > .pn > li > .pre_page").click(function() {
    var total_page = $(".article > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".article > .robot > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page > 1) {
        current_page -= 1;
        $(".article > .robot > .opera > .pn > li > .current_page").html(current_page);
        search_article(key_word, current_page, 0);
    }
});

/* 点击跳转：文章，人类 */
$(".article > .human > .opera > .pn > li > .article_page_go").click(function() {
    var key_word = $(".key_word").val().trim();

    var total_page = $(".article > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var go = $(".article > .human > .opera > .pn > li > .we_go_page").val().trim();
    try {
        go = parseInt(go);

        if(go >= 1 && go <= total_page && !isNaN(go)) {
            search_article(key_word, go, 1);
            $(".article > .human > .opera > .pn > li > .current_page").html(go);
        }
        else infor("跳转页数输入有误", function() {
            $(".article > .human > .opera > .pn > li > .we_go_page").val("");
            $(".article > .human > .opera > .pn > li > .we_go_page").focus();
        });
    } catch (e) {
        infor("跳转页数输入有误", function() {});
    }
});

/* 点击跳转：文章，机器 */
$(".article > .robot > .opera > .pn > li > .article_page_go").click(function() {
    var key_word = $(".key_word").val().trim();

    var total_page = $(".article > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var go = $(".article > .robot > .opera > .pn > li > .we_go_page").val().trim();
    try {
        go = parseInt(go);
        if(go >= 1 && go <= total_page && !isNaN(go)) {
            search_article(key_word, go, 0);
            $(".article > .robot > .opera > .pn > li > .current_page").html(go);
        } else
            infor("跳转页数输入有误", function() {
                $(".article > .robot > .opera > .pn > li > .we_go_page").val("");
                $(".article > .robot > .opera > .pn > li > .we_go_page").focus();
            });
    } catch (e) {
        infor("跳转页数输入有误", function() {});
    }
});


/******************************************************************************************************************/

/* 点击图片跳转：人类 */
$(".human > fieldset > .content").on("click", ".my_img_img", function () {
    var photo_id = $(this).attr("photo_id");
    var photo_title = $(this).attr("title");
    var type = $(this).attr('type');
    var url = '/search/go_image_page?photo_id=' + photo_id + '&photo_title=' +  photo_title + '&type=' + type;
    window.open(url, "_blank");
});

/* 点击图片跳转：机器 */
$(".robot > fieldset > .content").on("click", ".my_img_img", function () {
    var photo_id = $(this).attr("photo_id");
    var photo_title = $(this).attr("title");
    var type = $(this).attr('type');
    var url = '/search/go_image_page?photo_id=' + photo_id + '&photo_title=' +  photo_title + '&type=' + type;
    window.open(url, "_blank");
});

/* 搜索图片 */
function search_image(key_word, page, type) {
    $.ajax({
        url: "/search/search_image",
        data: {
            "key_word": key_word,
            "page": page,
            "type": type
        },
        type: 'POST',
        cache: false,
        dataType: "json",
        success: function(data) {
            if (data.status == 1) {
                // 渲染dom
                var content_html = "";
                for(var i = 0; i < data.data.length; i++) {
                    var photo_id = data.data[i].id;
                    var photo_title = data.data[i].title;
                    var url = data.data[i].url;

                    content_html += "<img class='my_img_img' type='" + type + "' src='" + url + "' photo_id='" + photo_id + "' title='" + photo_title + "' alt='抱歉图片可能自己飞了！'>";
                }
                switch(type) {
                    case 1:
                        $(".image > .human > fieldset > .content").html(content_html);
                        break;
                    case 0:
                        $(".image > .robot > fieldset > .content").html(content_html);
                        break;
                    default:
                        break;
                }
            } else {
                var content_html = "";
                switch(type) {
                    case 1:
                        $(".image > .human > fieldset > .content").html(content_html);
                        break;
                    case 0:
                        $(".image > .robot > fieldset > .content").html(content_html);
                        break;
                    default:
                        break;
                }
            }
        },
        error: function (err) {
            infor("网络错误", function() {
            });
        },
        async: true
    });
}

/* 获取图片总页数 */
function get_image_total_page(key_word, type) {
    $.ajax({
        url: "/search/search_image_total_page",
        data: {
            "key_word": key_word,
            "type": type
        },
        type: 'POST',
        cache: false,
        dataType: "json",
        success: function(data) {
            if (data.status == 1) {
                // 渲染dom
                var total_page = data.data[0].total_page;
                switch(type) {
                    case 1:
                        $(".image > .human > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    case 0:
                        $(".image > .robot > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    default:
                        break;
                }
            } else {
                var total_page = 0;
                switch(type) {
                    case 1:
                        $(".image > .human > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    case 0:
                        $(".image > .robot > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    default:
                        break;
                }
            }
        },
        error: function (err) {
            infor("网络错误", function() {
            });
        },
        async: true
    });
}

/* 点击下一页：图片，人类 */
$(".image > .human > .opera > .pn > li > .next_page").click(function() {
    var total_page = $(".image > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".image > .human > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page < total_page) {
        current_page += 1;
        $(".image > .human > .opera > .pn > li > .current_page").html(current_page);
        search_image(key_word, current_page, 1);
    }
});

/* 点击上一页：图片，人类 */
$(".image > .human > .opera > .pn > li > .pre_page").click(function() {
    var total_page = $(".image > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);


    var current_page = $(".image > .human > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page > 1) {
        current_page -= 1;
        $(".image > .human > .opera > .pn > li > .current_page").html(current_page);
        search_image(key_word, current_page, 1);
    }
});

/* 点击下一页：图片，机器 */
$(".image > .robot > .opera > .pn > li > .next_page").click(function() {
    var total_page = $(".image > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".image > .robot > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page < total_page) {
        current_page += 1;
        $(".image > .robot > .opera > .pn > li > .current_page").html(current_page);
        search_image(key_word, current_page, 0);
    }
});

/* 点击上一页：图片，机器 */
$(".image > .robot > .opera > .pn > li > .pre_page").click(function() {
    var total_page = $(".image > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".image > .robot > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page > 1) {
        current_page -= 1;
        $(".image > .robot > .opera > .pn > li > .current_page").html(current_page);
        search_image(key_word, current_page, 0);
    }
});

/* 点击跳转：图片，人类 */
$(".image > .human > .opera > .pn > li > .image_page_go").click(function() {
    var key_word = $(".key_word").val().trim();

    var total_page = $(".image > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var go = $(".image > .human > .opera > .pn > li > .we_go_page").val().trim();
    try {
        go = parseInt(go);
        if(go >= 1 && go <= total_page && !isNaN(go)) {
            search_image(key_word, go, 1);
            $(".image > .human > .opera > .pn > li > .current_page").html(go);
        }
        else infor("跳转页数输入有误", function() {
            $(".image > .human > .opera > .pn > li > .we_go_page").val("");
            $(".image > .human > .opera > .pn > li > .we_go_page").focus();
        });
    } catch (e) {
        infor("跳转页数输入有误", function() {});
    }
});

/* 点击跳转：图片，机器 */
$(".image > .robot > .opera > .pn > li > .image_page_go").click(function() {
    var key_word = $(".key_word").val().trim();

    var total_page = $(".image > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var go = $(".image > .robot > .opera > .pn > li > .we_go_page").val().trim();
    try {
        go = parseInt(go);
        if(go >= 1 && go <= total_page && !isNaN(go)) {
            search_image(key_word, go, 0);
            $(".image > .robot > .opera > .pn > li > .current_page").html(go);
        } else
            infor("跳转页数输入有误", function() {
                $(".image > .robot > .opera > .pn > li > .we_go_page").val("");
                $(".image > .robot > .opera > .pn > li > .we_go_page").focus();
            });
    } catch (e) {
        infor("跳转页数输入有误", function() {});
    }
});

/********************************************************************************************************************/

/* 点击下一页：视频，人类 */
$(".video > .human > .opera > .pn > li > .next_page").click(function() {
    var total_page = $(".video > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".video > .human > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page < total_page) {
        current_page += 1;
        $(".video > .human > .opera > .pn > li > .current_page").html(current_page);
        search_video(key_word, current_page, 1);
    }
});

/* 点击上一页：视频，人类 */
$(".video > .human > .opera > .pn > li > .pre_page").click(function() {
    var total_page = $(".video > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);


    var current_page = $(".video > .human > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page > 1) {
        current_page -= 1;
        $(".video > .human > .opera > .pn > li > .current_page").html(current_page);
        search_video(key_word, current_page, 1);
    }
});

/* 点击下一页：视频，机器 */
$(".video > .robot > .opera > .pn > li > .next_page").click(function() {
    var total_page = $(".video > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".video > .robot > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page < total_page) {
        current_page += 1;
        $(".video > .robot > .opera > .pn > li > .current_page").html(current_page);
        search_video(key_word, current_page, 0);
    }
});

/* 点击上一页：视频，机器 */
$(".video > .robot > .opera > .pn > li > .pre_page").click(function() {
    var total_page = $(".video > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var current_page = $(".video > .robot > .opera > .pn > li > .current_page").html().trim();
    if(current_page != "") {
        current_page = parseInt(current_page);
    } else {
        return;
    }

    var key_word = $(".key_word").val().trim();

    if(current_page > 1) {
        current_page -= 1;
        $(".video > .robot > .opera > .pn > li > .current_page").html(current_page);
        search_video(key_word, current_page, 0);
    }
});

/* 点击跳转：视频，人类 */
$(".video > .human > .opera > .pn > li > .video_page_go").click(function() {
    var key_word = $(".key_word").val().trim();

    var total_page = $(".video > .human > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var go = $(".video > .human > .opera > .pn > li > .we_go_page").val().trim();
    try {
        go = parseInt(go);
        if(go >= 1 && go <= total_page && !isNaN(go)) {
            search_video(key_word, go, 1);
            $(".video > .human > .opera > .pn > li > .current_page").html(go);
        }
        else infor("跳转页数输入有误", function() {
            $(".video > .human > .opera > .pn > li > .we_go_page").val("");
            $(".video > .human > .opera > .pn > li > .we_go_page").focus();
        });
    } catch (e) {
        infor("跳转页数输入有误", function() {});
    }
});

/* 点击跳转：视频，机器 */
$(".video > .robot > .opera > .pn > li > .video_page_go").click(function() {
    var key_word = $(".key_word").val().trim();

    var total_page = $(".video > .robot > .opera > .pn > li > .total_page").html().trim();
    total_page = parseInt(total_page);

    var go = $(".video > .robot > .opera > .pn > li > .we_go_page").val().trim();
    try {
        go = parseInt(go);
        if(go >= 1 && go <= total_page && !isNaN(go)) {
            search_image(key_word, go, 0);
            $(".video > .robot > .opera > .pn > li > .current_page").html(go);
        } else
            infor("跳转页数输入有误", function() {
                $(".video > .robot > .opera > .pn > li > .we_go_page").val("");
                $(".video > .robot > .opera > .pn > li > .we_go_page").focus();
            });
    } catch (e) {
        infor("跳转页数输入有误", function() {});
    }
});

/* 点击视频跳转：人类 */
$(".human > fieldset > .content").on("click", ".my_video_img", function () {
    var video_id = $(this).attr("video_id");
    var video_title = $(this).attr("video_title");
    var type = $(this).attr("type");
    var url = '/search/go_video_page?video_id=' + video_id + '&video_title=' +  video_title + '&type=' + type;
    window.open(url, "_blank");
});

/* 点击视频跳转：机器 */
$(".robot > fieldset > .content").on("click", ".my_video_img", function () {
    var video_id = $(this).attr("video_id");
    var video_title = $(this).attr("video_title");
    var type = $(this).attr("type");
    var url = '/search/go_video_page?video_id=' + video_id + '&video_title=' +  video_title + '&type=' + type;
    window.open(url, "_blank");
});

/* 搜索视频 */
function search_video(key_word, page, type) {
    $.ajax({
        url: "/search/search_video",
        data: {
            "key_word": key_word,
            "page": page,
            "type": type
        },
        type: 'POST',
        cache: false,
        dataType: "json",
        success: function(data) {
            if (data.status == 1) {
                // 渲染dom
                var content_html = "";
                for(var i = 0; i < data.data.length; i++) {
                    var video_id = data.data[i].id;
                    var video_title = data.data[i].title;
                    var category_name = data.data[i].category_name;
                    var url = data.data[i].url;
                    console.log(url)

                    if(url != null && url != "") {
                        content_html += '\
                        <div>\
                            <div class="my_video">\
                                <img class="my_video_img" type="' + type + '" video_id="' + video_id + '" video_title="' + video_title + '" src="' + url + '"/>\
                            </div>\
                            <div class="title">\
                                <a class="my_video_img" type="' + type + '"video_id="' + video_id + '" video_title="' + video_title + '">' + video_title + '</a>\
                            </div>\
                        </div>\
                        ';
                    }
                }
                switch(type) {
                    case 1:
                        $(".video > .human > fieldset > .content").html(content_html);
                        break;
                    case 0:
                        $(".video > .robot > fieldset > .content").html(content_html);
                        break;
                    default:
                        break;
                }
            } else {
                var content_html = "";
                switch(type) {
                    case 1:
                        $(".video > .human > fieldset > .content").html(content_html);
                        break;
                    case 0:
                        $(".video > .robot > fieldset > .content").html(content_html);
                        break;
                    default:
                        break;
                }
            }
        },
        error: function (err) {
            infor("网络错误", function() {
            });
        },
        async: true
    });
}

/* 获取视频总页数 */
function get_video_total_page(key_word, type) {
    $.ajax({
        url: "/search/search_video_total_page",
        data: {
            "key_word": key_word,
            "type": type
        },
        type: 'POST',
        cache: false,
        dataType: "json",
        success: function(data) {
            if (data.status == 1) {
                // 渲染dom
                var total_page = data.data[0].total_page;
                switch(type) {
                    case 1:
                        $(".video > .human > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    case 0:
                        $(".video > .robot > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    default:
                        break;
                }
            } else {
                var total_page = 0;
                switch(type) {
                    case 1:
                        $(".video > .human > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    case 0:
                        $(".video > .robot > .opera > .pn > li > .total_page").html(total_page);
                        break;
                    default:
                        break;
                }
            }
        },
        error: function (err) {
            infor("网络错误", function() {
            });
        },
        async: true
    });
}


//*********************入口函数******************
$(function() {
    responsive();

    SYX();
});

function keydown_send_search(e) {
    if (e.keyCode == 13) {
        SYX();
    }
}

$(".play_or_pause").click(function () {
    var au = document.getElementById("远征MUSIC");
    var si = null;
    if($(this).text() == "➠") {
        au.play();
        $(this).text("❡");
    } else {
        au.pause();
        $(this).text("➠");
    }
});