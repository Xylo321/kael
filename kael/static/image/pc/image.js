$(window).resize(function () {
    responsive();
    set_photo_center()
});

$(function() {
    responsive();
    refresh_categories(".nav");
    if ($(".photo_title").length == 0) {
        pag_photo(1, null);

        load_first_img();
     } else {
        var photo_title = $(".photo_title").attr("value");
        get_photo(photo_title);

        pag_photo(1, null);
     }
});

function set_photo_center() {
    $('.center > .content > .photo').css({
        "width": $(".center > .content").width(),
        "height": $(window).height() - $(".center > .opera").height() - $(".center > .content > h1").height(),
        "background-repeat": "no-repeat",
        "background-size": "contain",
        "margin-top": 20,
        "background-position": "center center",
        "-webkit-background-size": "contain",
        "-moz-background-size": "contain"
    });
}

function set_photo(title, src, category_name, date) {
    var content_html = "<h1>" + title + "</h1><div class='photo'></div>";
    $(".center > .content").html(content_html);

    $('.center > .content > .photo').css({
        "background": "url('" + src + "')",
    });

    $(".base > .category_name").html(category_name);
    $(".base > .date").html(date);
    set_photo_center();

    $(".opera").show();
}

function load_first_img() {
    var si = setInterval(function () {
        if ($(".photo_list > img").length > 0) {

            var title = $(".photo_list > img").attr("title");
            var src = $(".photo_list > img").attr('src');
            var category_name = $(".photo_list > img").attr('category_name');
            var date = $(".photo_list > img").attr('date');

            set_photo(title, src, category_name, date);
            $('.content').show();
            clearInterval(si);
        }
    }, 100);
}

function responsive() {
    $(".right > .photo_list").css({
        "height": $(".right").height() - $(".right > .pagnation").height() - 24
    });

    var width = $(window).width();
    var height = $(window).height();

    if (width < 960) {
        $(".left").hide();
        $(".right").hide();
        $(".left_control").show();
        $(".right_control").show();

        $('.center').css({
            "width": width,
            "margin-left": "0",
            "margin-right": "0",
        });
        $(".left_control").css({
            "left": "0"
        });
        $(".right_control").css({
            "right": "0"
        });
    } else if (width < 1366) {
        $(".right").hide();
        $(".left").show();
        $(".left_control").hide();
        $(".right_control").show();

        $('.center').css({
            "width": width - 200,
            "margin-left": "200px",
            "margin-right": "0",
        });

        $(".right_control").css({
            "right": "0"
        });
    } else if(width < 1616){
        $(".left").show();
        $(".right").show();
        $(".left_control").hide();
        $(".right_control").hide();

        $('.center').css({
            "width": width - 400,
            "margin-left": "200px",
            "margin-right": "200px"
        });
    } else {
        $(".left").hide();
        $(".right").hide();
        $(".left_control").show();
        $(".right_control").show();

        $('.center').css({
            "width": width,
            "margin-left": 0,
            "margin-right": 0
        });

        $(".left_control").css({
            "left": 0,
        });
        $(".right_control").css({
            "right": 0,
        });
    }

    $(".content").css({
        "width": "100%"
    })
}

/* ?????????????????? */
$(".left_control").click(function () {
    if ($(".left").is(":visible")) {
        $(".left").hide();
        $(".left_control").css({
            "left": "0"
        });
    } else {
        $(".left").show();
        $(".left_control").css({
            "left": "200px"
        });
    }
});

/* ???????????????????????? */
$(".right_control").click(function () {
    if ($(".right").is(":visible")) {
        $(".right").hide();
        $(".right_control").css({
            "right": "0"
        });
    } else {
        $(".right").show();
        $(".right_control").css({
            "right": "200px"
        });
    }
});

/* ?????? */
$(".opera > a.back_home").click(function () {
    location.href = "/image/home";
});

/* ???????????? */
$("a.exit").click(function () {
    $.ajax({
        url: "/account/logout",
        type: 'GET',
        cache: false,
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                infor("????????????", function () {
                    location.href = "/account/login";
                }, true);
            } else {
                infor("????????????", function () {
                });
            }
        },
        error: function (err) {
            infor("????????????", function () {
            });
        },
        async: false
    });
});

function refresh_categories(selector) {
    var url = "/image/get_categories";
    var type = 'POST';

    var look_dom = $(".look");
    if ($(look_dom).length != 0) {
        url += "?look=" + $(look_dom).attr("value");
        type = 'GET';
    }

    $.ajax({
        url: url,
        type: type,
        cache: false,
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                switch (selector) {
                    case '.nav':
                        // ????????????????????????????????? dom
                        var nav_html = "";
                        for (var i = 0; i < data.data.length; i++) {
                            if ($(look_dom).length == 0) {
                                nav_html += '<li><a class="cat" title="' +data.data[i].name +'">' + data.data[i].name + '</a><a  class="del" title="????????????????????????????????????">&sup1;</a><a  class="rename" title="??????????????????">&sup2;</a></li>';
                            } else {
                                nav_html += '<li><a class="cat" title="' + data.data[i].name + '">' + data.data[i].name + '</a></li>';
                            }
                        }

                        if ($(look_dom).length == 0)
                            nav_html += "<li><a  class='add' title='????????????'>+</a></li>";

                        $(selector).html(nav_html);
                        break;
                    case "#upload_file > .layout > .categories":
                        if (data.data.length == 0) {
                            infor("??????????????????", function () {
                            });
                            return;
                        }
                        var nav_html = "";

                        for (var i = 0; i < data.data.length; i++) {
                            nav_html += "<option value='" + data.data[i].name + "'>" + data.data[i].name + "</option>";
                        }
                        $(selector).html(nav_html);

                        break;
                    default:
                        break;
                }
            } else {
                location.href = '/account/login';
            }
        },
        error: function (err) {
            infor("????????????", function () {
            });
        },
        async: true
    });
}

/* ???????????? */
$(".nav").on('click', 'li > .add', function () {
    shuru($(this), "?????????????????????", "right", function () {
        var name = $("#shuru > .layout > input").val().trim();
        if (name == "") {
            infor("????????????????????????", function () {
            });
            return;
        }

        $.ajax({
            url: "/image/add_category",
            type: 'POST',
            cache: false,
            data: {
                name: name,
            },
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("??????????????????", function () {
                        refresh_categories(".nav");
                    });
                } else {
                    infor("??????????????????", function () {
                    });
                }
            },
            error: function (err) {
                infor("????????????", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* ???????????? */
$(".nav").on('click', 'li > .del', function () {
    var cat_dom = $(this).siblings(".cat");
    var name = $(cat_dom).text().trim();

    shuru($(this), "???????????????????????????", "right", function () {
        var confirm_name = $("#shuru > .layout > input").val();
        if (confirm_name == "") {
            infor("??????????????????????????????", function () {
            });
            return;
        }
        if (confirm_name != name) {
            infor("???????????????????????????", function () {
            });
            return;
        }

        $.ajax({
            url: "/image/del_category",
            type: 'POST',
            cache: false,
            data: {
                name: confirm_name,
            },
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("??????????????????", function () {
                        // ????????????
                        refresh_categories(".nav");

                        pag_photo(1, null);

                        // ?????????????????????????????????????????????????????????????????????content??????
                        // ????????????????????????????????????0?????????????????????????????????????????????????????????content

                        var category_name = $('.category_name').html();
                        if (category_name == name) {
                            $(".content").hide();
                        }

                        if ($(".nav > li").length == 1) {
                            $(".content").hide();
                        }
                    });
                } else {
                    infor("??????????????????", function () {
                    });
                }
            },
            error: function (err) {
                infor("????????????", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* ??????????????? */
$(".nav").on('click', 'li > .rename', function () {
    var cat_dom = $(this).siblings(".cat");
    var old_name = $(cat_dom).text();

    shuru($(this), "????????????????????????", "right", function () {
        var new_name = $("#shuru > .layout > input").val().trim();
        if (new_name == "") {
            infor("????????????????????????", function () {
            });
            return;
        }

        $.ajax({
            url: "/image/rename_category",
            type: 'POST',
            cache: false,
            data: {
                old_name: old_name,
                new_name: new_name
            },
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("??????????????????", function () {
                        // ????????????
                        refresh_categories(".nav");
                        // ???????????????content???????????????????????????????????????????????????????????????????????????????????????????????????????????????
                        var category_name = $('.category_name').html();
                        if (category_name == old_name) {
                            $('.category_name').html(new_name);
                        }
                    });
                } else {
                    infor("??????????????????", function () {
                    });
                }
            },
            error: function (err) {
                infor("????????????", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* ?????????????????? */
function pag_photo(page, category_name) {
    var url = "/image/pag_photo";
    var type = 'POST';

    var look_dom = $(".look");
    if ($(look_dom).length != 0) {
        url += "?look=" + $(look_dom).attr("value");
        type = 'GET';
    }

    $.ajax({
        url: url,
        type: type,
        cache: false,
        dataType: "json",
        data: {
            page: page,
            category_name: category_name,
        },
        success: function (data) {
            if (data.status == 1) {
                $(".current_page").attr("value", page);

                var photo_list_html = "";

                for (var i = 0; i < data.data.length; i++) {
                    var title = data.data[i].title;
                    var category_name = data.data[i].category_name;
                    var url = data.data[i].url;

                    var tmp = new Date(data.data[i].date * 1000);
                    var date = tmp.toLocaleString();

                    photo_list_html += "<img src='" + url + "' category_name='" + category_name + "' title='" + title + "' date='" + date + "'alt='??????????????????????????????!'/>";
                }

                $(".photo_list").html(photo_list_html);
            } else {
                infor("????????????????????????", function () {
                });
            }
        },
        error: function (err) {
            infor("????????????", function () {
            });
        },
        async: true
    });
}

/* ????????????????????????????????? */
$(".nav").on("click", "li > .cat", function () {
    var current_category = $(".current_category").attr("value");
    if ($(this).html() != current_category) {
        $(".current_category").attr("value", $(this).html());
        $(".current_page").attr("value", "1");

        pag_photo(1, $(this).html());
    }
});

/* ???????????? */
$(".upload").click(function () {
    if($(".nav > li > .cat").length == 0) {
        infor("??????????????????", function() {
        });
        return;
    }

    refresh_categories("#upload_file > .layout > .categories");

    upload_file($(this), "", "??????????????????", "left", function () {
        var title = $("#upload_file > .layout > .upload_file_title").val().trim();
        var file_name = $("#upload_file > .layout > .upload_file_name").val();
        var category_name = $("#upload_file > .layout > .categories").val();

        if(title = '' || file_name == '' || category_name == '') {
            infor("????????????????????????", function () {
            });
            return;
        }

        var formData = new FormData($("#upload_file > .layout")[0]);

        $.ajax({
            type: 'POST',
            url: "/image/upload",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("??????????????????", function () {
                        if($(".current_category").attr("value") == category_name) {
                            pag_photo(1, category_name);
                        } else {
                            pag_photo(1, null);
                        }
                    });
                } else {
                    infor("??????????????????", function () {
                    });
                }
            },
            error: function(err) {
                reset_progress();
                infor("????????????", function () {
                });
            },
            async: true,
            xhr: progress
        });
    }, function () {
    });
});

/* ?????????????????????????????? */
$(".photo_list").on('click', 'img', function() {
    var title = $(this).attr("title");
    var src = $(this).attr("src");
    var category_name = $(this).attr('category_name');
    var date = new Date(1000 * parseFloat($(this).attr('date'))).toLocaleString();

    set_photo(title, src, category_name, date);
    $('.content').show();
});

/* ??????????????? */
$(".pre").click(function() {
    var current_page = parseInt($(".current_page").attr("value"));
    var current_category = $(".current_category").attr("value");
    if (current_page != 1) {
        if (current_category == '') {
            current_page = current_page - 1;
            $(".current_page").attr("value", current_page)

            pag_photo(current_page, null);
        } else {
            current_page = current_page - 1;
            $(".current_page").attr("value", current_page)
            pag_photo(current_page, current_category);
        }
    }
});

/* ??????????????? */
$(".nex").click(function() {
    var current_page = parseInt($(".current_page").attr("value"));
    var current_category = $(".current_category").attr("value");
    if ($(".photo_list > img").length == 10) {
        if (current_category == '') {
            current_page = current_page + 1;
            $(".current_page").attr("value", current_page)

            pag_photo(current_page, null);
        } else {
            current_page = current_page + 1;
            $(".current_page").attr("value", current_page)
            pag_photo(current_page, current_category);
        }
    }
});

/* ?????? */
$(".other > .edit").click(function() {
    var src_title = $('.content > h1').html();

    refresh_categories("#upload_file > .layout > .categories");

    upload_file($(this), src_title, "???????????????", "left", function () {
        var new_title = $("#upload_file > .layout > .upload_file_title").val().trim();
        var file_name = $("#upload_file > .layout > .upload_file_name").val();
        var category_name = $("#upload_file > .layout > .categories").val();

        if(new_title == '' || category_name == '') {
            infor("?????????????????????????????????", function () {
            });
            return;
        }

        var formData = new FormData($("#upload_file > .layout")[0]);
        formData.append("src_title", src_title);
        formData.append("new_title", new_title);
        formData.delete('title');

        $.ajax({
            type: 'POST',
            url: "/image/update_photo",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("??????????????????", function () {
                        if($(".current_category").attr("value") == category_name) {
                            pag_photo(1, category_name);
                        } else {
                            pag_photo(1, null);
                        }
                        get_photo(new_title);
                    });
                } else {
                    infor("??????????????????", function () {
                    });
                }
            },
            error: function(err) {
                reset_progress();
                infor("????????????", function () {
                });
            },
            async: true,
            xhr: progress
        });
    }, function () {
    });
});

/* ?????? */
$(".other > .del").click(function() {
    var name = $('.content > h1').html();
    shuru($(this), "???????????????????????????", "left", function () {
        var confirm_name = $("#shuru > .layout > input").val();
        if (confirm_name == "") {
            infor("??????????????????????????????", function () {
            });
            return;
        }
        if (confirm_name != name) {
            infor("???????????????????????????", function () {
            });
            return;
        }

        $.ajax({
            url: "/image/del_photo",
            type: 'POST',
            cache: false,
            data: {
                title: confirm_name,
            },
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("??????????????????", function () {
                        var current_category = $(".current_category").attr("value");
                        var current_page = parseInt($(".current_page").attr("value"));
                        if ($('.photo_list > img').length == 1) {
                            $('.content').hide();
                            pag_photo(current_page, current_category);
                        } else {
                            pag_photo(current_page, current_category);
                        }
                    });
                } else {
                    infor("??????????????????", function () {
                    });
                }
            },
            error: function (err) {
                infor("????????????", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* ?????????????????? */
$(".center > .content").on('dblclick', '.photo', function() {
    var on = 0;

    if (document.webkitfullscreenElement) {
        on = 1;
    } else if (document.mozFullscreenElement) {
        on = 2;
    } else if (document.msfullscreenElement) {
        on = 3;
    } else if (document.fullscreenElement) {
        on = 4;
    } else if (document.webkitFullscreenElement) {
        // edge????????????
        on = 5;
    }

    if (on > 0) {
        switch(on) {
            case 1:
            case 5:
                document.webkitCancelFullScreen();
                break;
            case 2:
                document.mozCancelFullScreen();
                break;
            case 3:
                document.msCancelFullScreen();
                break;
            case 4:
                if (document.webkitCancelFullScreen)
                    document.webkitCancelFullScreen();
                else if (document.mozCancelFullScreen)
                    document.mozCancelFullScreen();
                else if (document.msCancelFullScreen)
                    document.msCancelFullScreen();
                else if (document.cancelFullScreen)
                    document.cancelFullScreen();
                else
                    infor("?????????????????????????????????", function() {}, false);
                break;

            default: break;
        }
    } else {
        if ($(this)[0].webkitRequestFullScreen)
            $(this)[0].webkitRequestFullScreen();
        else if ($(this)[0].mozRequestFullScreen)
            $(this)[0].mozRequestFullScreen();
        else if ($(this)[0].msRequestFullScreen)
            $(this)[0].msRequestFullScreen();
        else
            infor("?????????????????????????????????", function() {}, false);
    }
});

function get_photo(title) {
    var look_dom = $(".look");

    var url = "/image/get_photo";
    var type = 'POST';
    if($(look_dom).length != 0) {
        url += "?look=" + $(look_dom).attr("value");
        type = 'GET';
    }

    $.ajax({
        url: url,
        type: type,
        cache: false,
        data: {
            title: title,
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                for (var i = 0; i < 1; i++) {
                    var title = data.data[i].title;
                    var category_name = data.data[i].category_name;
                    var url = data.data[i].url;

                    var tmp = new Date(data.data[i].date * 1000);
                    var date = tmp.toLocaleString();

                    set_photo(title, url, category_name, date);
                }
            } else {
                infor("??????????????????", function () {
                });
            }
        },
        error: function (err) {
            infor("????????????", function () {
            });
        },
        async: true
    });
}
