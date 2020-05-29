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

    if (width < 1080) {
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
    } else if (width < 1440) {
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

        if(height / width > 0.65 || height / width < 0.5) {
            $(".left").hide();
            $(".left_control").show();
            $(".left_control").css({
                "left": "0"
            });

            $('.center').css({
                "width": width - 400,
                "margin-left": "200px",
                "margin-right": "200px",
            });

            $(".right_control").css({
                "right": "0"
            });
        }
    } else if(width < 1800){
        $(".left").show();
        $(".right").show();
        $(".left_control").hide();
        $(".right_control").hide();

        $('.center').css({
            "width": width - 400,
            "margin-left": "200px",
            "margin-right": "200px"
        });

        if(height / width > 0.65 || height / width < 0.5) {
            $(".left").hide();
            $(".right").hide();
            $(".left_control").show();
            $(".left_control").css({
                "left": "0"
            });

            $('.center').css({
                "width": width - 400,
                "margin-left": "200px",
                "margin-right": "200px",
            });

            $(".right_control").css({
                "right": "0"
            });
        }
    } else {
        $(".left").hide();
        $(".right").hide();
        $(".left_control").show();
        $(".right_control").show();

        $('.center').css({
            "width": width - 400,
            "margin-left": 200,
            "margin-right": 200
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

/* 左侧隐藏控制 */
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

/* 右侧显示隐藏控制 */
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

/* 回家 */
$(".opera > a.back_home").click(function () {
    location.href = "/image/home";
});

/* 退出登陆 */
$("a.exit").click(function () {
    $.ajax({
        url: "/account/logout",
        type: 'GET',
        cache: false,
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                infor("退出成功", function () {
                    location.href = "/account/login";
                }, true);
            } else {
                infor("退出失败", function () {
                });
            }
        },
        error: function (err) {
            infor("网络错误", function () {
            });
        },
        async: true
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
                        // 加载导航栏里的分类列表 dom
                        var nav_html = "";
                        for (var i = 0; i < data.data.length; i++) {
                            if ($(look_dom).length == 0) {
                                nav_html += '<li><a class="cat">' + data.data[i].name + '</a><a  class="del" title="删除栏目及该栏目所有文章">&sup1;</a><a  class="rename" title="重命名该栏目">&sup2;</a></li>';
                            } else {
                                nav_html += '<li><a class="cat">' + data.data[i].name + '</a></li>';
                            }
                        }

                        if ($(look_dom).length == 0)
                            nav_html += "<li><a  class='add' title='增加栏目'>+</a></li>";

                        $(selector).html(nav_html);
                        break;
                    case "#upload_file > .layout > .categories":
                        if (data.data.length == 0) {
                            infor("请先创建栏目", function () {
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
            infor("网络错误", function () {
            });
        },
        async: true
    });
}

/* 增加栏目 */
$(".nav").on('click', 'li > .add', function () {
    shuru($(this), "要增加的栏目名", "right", function () {
        var name = $("#shuru > .layout > input").val().trim();
        if (name == "") {
            infor("新栏目名不能为空", function () {
            });
            return;
        }

        if (name.length > 4) {
            infor("新栏目名长度最多为4", function () {
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
                    infor("栏目增加成功", function () {
                        refresh_categories(".nav");
                    });
                } else {
                    infor("栏目增加失败", function () {
                    });
                }
            },
            error: function (err) {
                infor("网络错误", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* 删除栏目 */
$(".nav").on('click', 'li > .del', function () {
    var cat_dom = $(this).siblings(".cat");
    var name = $(cat_dom).text().trim();

    shuru($(this), "确认要删除的栏目名", "right", function () {
        var confirm_name = $("#shuru > .layout > input").val();
        if (confirm_name == "") {
            infor("删除的栏目名不能为空", function () {
            });
            return;
        }
        if (confirm_name != name) {
            infor("删除的栏目名不正确", function () {
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
                    infor("栏目删除成功", function () {
                        // 更新导航
                        refresh_categories(".nav");

                        pag_photo(1, null);

                        // 判断当前图片的分类是否是删掉的栏目，如果是则将content隐藏
                        // 判断栏目列表的个数是否为0，如果是则表示该用户没有任何栏目，隐藏content

                        var category_name = $('.category_name').html();
                        if (category_name == name) {
                            $(".content").hide();
                        }

                        if ($(".nav > li").length == 1) {
                            $(".content").hide();
                        }
                    });
                } else {
                    infor("栏目删除失败", function () {
                    });
                }
            },
            error: function (err) {
                infor("网络错误", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* 重命名栏目 */
$(".nav").on('click', 'li > .rename', function () {
    var cat_dom = $(this).siblings(".cat");
    var old_name = $(cat_dom).text();

    shuru($(this), "重命名后的栏目名", "right", function () {
        var new_name = $("#shuru > .layout > input").val().trim();
        if (new_name == "") {
            infor("新栏目名不能为空", function () {
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
                    infor("栏目修改成功", function () {
                        // 刷新导航
                        refresh_categories(".nav");
                        // 查看当前的content中的图片的栏目名是否和被重命名之前的栏目名相同，如果相同则用新的栏目名替换
                        var category_name = $('.category_name').html();
                        if (category_name == old_name) {
                            $('.category_name').html(new_name);
                        }
                    });
                } else {
                    infor("栏目修改失败", function () {
                    });
                }
            },
            error: function (err) {
                infor("网络错误", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* 拉取图片列表 */
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
                    var category_name = data.data[i].name;
                    var local_url = data.data[i].local_url;
                    var remote_url = data.data[i].remote_url;

                    var tmp = new Date(data.data[i].date * 1000);
                    var date = tmp.toLocaleString();

                    var view_url = '/image/view_photo/';
                    if(local_url != null && local_url != "") view_url += local_url;
                    else if(remote_url != null && remote_url != "") view_url = remote_url;

                    photo_list_html += "<img src='" + view_url + "' category_name='" + category_name + "' title='" + title + "' date='" + date + "'alt='抱歉图片可能自己飞了!'/>";
                }

                $(".photo_list").html(photo_list_html);
            } else {
                infor("拉取图片列表失败", function () {
                });
            }
        },
        error: function (err) {
            infor("网络错误", function () {
            });
        },
        async: true
    });
}

/* 点击栏目名获取栏目列表 */
$(".nav").on("click", "li > .cat", function () {
    var current_category = $(".current_category").attr("value");
    if ($(this).html() != current_category) {
        $(".current_category").attr("value", $(this).html());
        $(".current_page").attr("value", "1");

        pag_photo(1, $(this).html());
    }
});

/* 点击上传 */
$(".upload").click(function () {
    if($(".nav > li > .cat").length == 0) {
        infor("请先创建栏目", function() {
        });
        return;
    }

    refresh_categories("#upload_file > .layout > .categories");

    upload_file($(this), "", "上传文件标题", "left", function () {
        var title = $("#upload_file > .layout > .upload_file_title").val().trim();
        var file_name = $("#upload_file > .layout > .upload_file_name").val();
        var category_name = $("#upload_file > .layout > .categories").val();

        if(title = '' || file_name == '' || category_name == '') {
            infor("上传参数不能为空", function () {
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
                    infor("上传图片成功", function () {
                        if($(".current_category").attr("value") == category_name) {
                            pag_photo(1, category_name);
                        } else {
                            pag_photo(1, null);
                        }
                    });
                } else {
                    infor("上传文件失败", function () {
                    });
                }
            },
            error: function(err) {
                infor("网络错误", function () {
                });
            },
            async: true,
            xhr: progress
        });
    }, function () {
    });
});

/* 点击图片列表里的图片 */
$(".photo_list").on('click', 'img', function() {
    var title = $(this).attr("title");
    var src = $(this).attr("src");
    var category_name = $(this).attr('category_name');
    var date = new Date(1000 * parseFloat($(this).attr('date'))).toLocaleString();

    set_photo(title, src, category_name, date);
    $('.content').show();
});

/* 点击上一页 */
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

/* 点击下一页 */
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

/* 编辑 */
$(".other > .edit").click(function() {
    var src_title = $('.content > h1').html();

    refresh_categories("#upload_file > .layout > .categories");

    upload_file($(this), src_title, "新文件标题", "left", function () {
        var new_title = $("#upload_file > .layout > .upload_file_title").val().trim();
        var file_name = $("#upload_file > .layout > .upload_file_name").val();
        var category_name = $("#upload_file > .layout > .categories").val();

        if(new_title == '' || category_name == '') {
            infor("文件名和分类名不能为空", function () {
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
                    infor("更新图片成功", function () {
                        if($(".current_category").attr("value") == category_name) {
                            pag_photo(1, category_name);
                        } else {
                            pag_photo(1, null);
                        }
                        get_photo(new_title);
                    });
                } else {
                    infor("更新图片失败", function () {
                    });
                }
            },
            error: function(err) {
                infor("网络错误", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* 删除 */
$(".other > .del").click(function() {
    var name = $('.content > h1').html();
    shuru($(this), "确认要删除的图片名", "left", function () {
        var confirm_name = $("#shuru > .layout > input").val();
        if (confirm_name == "") {
            infor("删除的图片名不能为空", function () {
            });
            return;
        }
        if (confirm_name != name) {
            infor("删除的图片名不正确", function () {
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
                    infor("图片删除成功", function () {
                        var current_category = $(".current_category").attr("value");
                        var current_page = parseInt($(".current_page").attr("value"));
                        if ($('.photo_list > img').length == 1) {
                            $('.content').hide();
                            pag_photo(current_page, current_category);
                        } else {
                            pag_photo(current_page, current_category);
                            load_first_img()
                        }
                    });
                } else {
                    infor("图片删除失败", function () {
                    });
                }
            },
            error: function (err) {
                infor("网络错误", function () {
                });
            },
            async: true
        });
    }, function () {
    });
});

/* 全屏图片切换 */
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
        // edge浏览器下
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
                    infor("该浏览器不支持全屏接口", function() {}, false);
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
            infor("该浏览器不支持全屏接口", function() {}, false);
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
                    var category_name = data.data[i].name;
                    var local_url = data.data[i].local_url;
                    var remote_url = data.data[i].remote_url;

                    var tmp = new Date(data.data[i].date * 1000);
                    var date = tmp.toLocaleString();

                    var view_url = '/image/view_photo/';
                    if(local_url != null && local_url != "") view_url += local_url;
                    else if(remote_url != null && remote_url != "") view_url = remote_url;

                    set_photo(title, view_url, category_name, date);
                }
            } else {
                infor("获取图片失败", function () {
                });
            }
        },
        error: function (err) {
            infor("网络错误", function () {
            });
        },
        async: true
    });
}
