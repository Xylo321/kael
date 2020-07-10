$(function () {
    // play('mp4', '/static/video/杨幂原视频源码13分钟.mp4');

    if($(".video_title").length != 0) {
        var video_title = $(".video_title").attr("value");
        get_video(video_title);

        refresh_categories(".nav");
        pag_video(1, null);
    } else {
        refresh_categories(".nav");
        pag_video(1, null);
        load_first_video();
    }

    responsive();
});

function load_first_video() {
    var si = setInterval(function () {
        if ($("td.title").length > 0) {
            var video_title = $("td.title").attr("title");
            get_video(video_title);

            clearInterval(si);
        }
    }, 100);
}

$(window).resize(function () {
    responsive();
});

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
            "left": "250px"
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
            "right": "250px"
        });
    }
});

function img_video_responsive() {
    $("img").css({
        "width": $(".center").width() * 0.99
    })

    $("video").css({
        "width": $(".center").width(),
        "height": $(".center").width() * 0.7
    })
}

/* 自适应窗口大小 */
function responsive() {
    var width = $(window).width();
    var height = $(window).height();

    if (width < 1080) {
        $(".left").hide();
        $(".right").hide();
        $(".left_control").show();
        $(".right_control").show();

        $('.center').css({
            "width": "100%",
            "margin-left": "0",
            "margin-right": "0",
        });
        $(".left_control").css({
            "left": "0"
        });
        $(".right_control").css({
            "right": "0"
        });

        $(".content").css({
            "width": width,
        });
    } else if (width < 1440) {
        $(".right").hide();
        $(".left").show();
        $(".left_control").hide();
        $(".right_control").show();

        $('.center').css({
            "width": width - 250,
            "margin-left": "250px",
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
                "width": width - 250,
                "margin-left": "150px",
                "margin-right": "150px",
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
            "width": width - 500,
            "margin-left": "250px",
            "margin-right": "250px"
        });

        if(height / width > 0.65 || height / width < 0.5) {
            $(".left").hide();
            $(".right").hide();
            $(".left_control").show();
            $(".left_control").css({
                "left": "0"
            });

            $('.center').css({
                "width": width - 250,
                "margin-left": "150px",
                "margin-right": "150px",
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
            "width": width - 500,
            "margin-left": 250,
            "margin-right": 250
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

    img_video_responsive()
}

/* 拉取视屏列表 */
function pag_video(page, category_name) {
    var url = "/video/pag_video";
    var type = 'POST';

    var look_dom = $(".look");
    if($(look_dom).length != 0) {
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

                var al_html = "<caption>文章列表</caption>";
                for (var i = 0; i < data.data.length; i++) {
                    var tmp = new Date(data.data[i].date * 1000);
                    var date = tmp.toLocaleDateString();
                    var time = tmp.toLocaleTimeString();
                    al_html += "<tr><td class='title' title='" + data.data[i].title + "'><a >" + data.data[i].title + "</a></td>" +
                        "<td class='date'><a title='" + time + "'>" + date + "</a></td></tr>";
                }

                $(".video_list > .data").html(al_html);
            } else {
                infor("拉取文章失败", function () {
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

/* 文章下一页 */
$("#nex_page").click(function () {
    var current_category = $(".current_category").attr("value");
    var current_page = parseInt($(".current_page").attr("value"));
    if ($("td.title").length == 10)
        pag_video(current_page + 1, current_category);
});

/* 文章上一页 */
$("#pre_page").click(function () {
    var current_category = $(".current_category").attr("value");
    var current_page = parseInt($(".current_page").attr("value"));
    if (current_page > 1)
        pag_video(current_page - 1, current_category);
});

/* 新建视频 */
$(".newvideo").click(function () {
    if($(".nav > li > .cat").length == 0) {
        infor("请增加栏目后再增加视频", function() {
        });
    } else {
        refresh_categories("#upload_video > .layout > .categories");

        upload_video($(this), function () {
            var title = $("#upload_video > .layout > .upload_file_title").val().trim();
            var file_name = $("#upload_video > .layout > .upload_file_name").val();
            var category_name = $("#upload_video > .layout > .categories").val();

            if(title = '' || file_name == '' || category_name == '') {
                infor("上传参数不能为空", function () {
                });
                return;
            }

            var formData = new FormData($("#upload_video > .layout")[0]);

            $.ajax({
                type: 'POST',
                url: "/video/upload",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                dataType: "json",
                success: function (data) {
                    if (data.status == 1) {
                        infor("上传视频成功", function () {
                            if ($(".current_category").attr("value") == category_name) {
                                pag_video(1, category_name);
                            } else {
                                pag_video(1, null);
                            }
                        });
                    } else {
                        infor("上传视频失败", function () {
                        });
                    }
                },
                error: function (err) {
                    reset_progress();
                    infor("网络错误", function () {
                    });
                },
                async: true,
                xhr: progress
            });
        }, function () {
        });
    }
});

/* 退出登陆 */
$(".log_out > a.exit").click(function () {
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
        async: false
    });
});

/* 回家 */
$(".log_out > a.back_home").click(function () {
    location.href = "/video/home";
});

function refresh_categories(selector, selected) {
    var url = "/video/get_categories";
    var type = 'POST';

    var look_dom = $(".look");
    if($(look_dom).length != 0) {
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
                            if($(look_dom).length == 0) {
                                nav_html += '<li><a class="cat">' + data.data[i].name + '</a><a  class="del" title="删除栏目及该栏目所有视频">&sup1;</a><a  class="rename" title="重命名该栏目">&sup2;</a></li>';
                            }else {
                                nav_html += '<li><a class="cat">' + data.data[i].name + '</a></li>';
                            }
                        }

                        if($(look_dom).length == 0)
                            nav_html += "<li><a  class='add' title='增加栏目'>+</a></li>";

                        $(selector).html(nav_html);
                        break;
                    case "#upload_video > .layout > .categories":
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
        async: false
    });
}

/* 点击栏目名获取栏目列表 */
$(".nav").on("click", "li > .cat", function () {
    var current_category = $(".current_category").attr("value");
    if ($(this).html() != current_category) {
        $(".current_category").attr("value", $(this).html());
        $(".current_page").attr("value", "1");

        pag_video(1, $(this).html());
    }
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
            url: "/video/rename_category",
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
                        refresh_categories(".nav", null);

                        // 如果旧文章内容显示面板可见，则更新旧文章区域
                        if($(".content > .title").html() != "") {
                            var title = $(".content > .title").html();
                            get_video(title);
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
            url: "/video/del_category",
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

                        // 更新列表
                        var current_category = $(".current_category").attr("value");
                        var current_page = parseInt($(".current_page").attr("value"));
                        pag_video(current_page, null);

                        var si = setInterval(function () {
                            if ($("td.title").length > 0) {
                                var video_title = $("td.title > a").html().trim();
                                get_video(video_title);

                                clearInterval(si);
                            }
                            else {
                                $(".content").hide();
                            }
                        }, 100);
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
            url: "/video/add_category",
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
                        refresh_categories(".center > .content > .new_video > .edit_panel > .opera > .opera_left > .category_name", null);
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

/* 删除视频 */
$(".base_infor > .del").click(function () {
    shuru($(this), "确认删除视频名", "left", function () {
        var src_title = $(".content > .title").html();

        var your_title = $("#shuru > .layout > input").val().trim();
        if (your_title == "") {
            infor("确认删除视频名不能为空", function () {
            });
            return;
        }

        if (your_title != src_title) {
            infor("确认删除视频名不正确", function () {
            });
            return;
        }

        $.ajax({
            url: "/video/del_video",
            type: 'POST',
            cache: false,
            data: {
                title: your_title,
            },
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("视频删除成功", function () {
                        $(".content").hide();

                        /* 重新拉取列表 */
                        var current_category = $(".current_category").attr("value");
                        var current_page = parseInt($(".current_page").attr("value"));
                        pag_video(current_page, current_category);

                        load_first_video();
                    });
                } else {
                    infor("视频删除失败", function () {
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

/* 点击视频列表里的视频 */
$(".video_list > .data").on('click', '.title > a', function() {
    var video_title = $(this).parent().attr("title");
    get_video(video_title);
});

function get_video(video_title) {
    var look_dom = $(".look");

    var url = "/video/get_video";
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
            title: video_title
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                var title = data.data[0].title;
                var category_name = data.data[0].category_name;
                var description = data.data[0].description;
                var url = data.data[0].url;
                var file_extension = data.data[0].file_extension;

                var tmp = new Date(data.data[0].date * 1000);
                var date = tmp.toLocaleString();

                $(".content > .title").html(title);
                $(".content > .base_infor > .category_name").html(category_name);
                $(".content > .base_infor > .pub_date").html(date);
                $(".content > .description").html(description);

                play(file_extension.toLowerCase(), url);

                $(".content").show();

                img_video_responsive()
            } else {
                infor("获取视频详情失败", function() {
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

function play(type, url) {
    switch(type) {
        case "avi":
            alert("无法播放avi，我该怎么办？需要我去像当年的flv.js的作者去开发一个avi.js吗？");
            break;
        case 'mp4':
        case 'flv':
            if (flvjs.isSupported()) {
                var videoElement = document.getElementById('videoElement');
                var flvPlayer = flvjs.createPlayer({
                    type: type,
                    url: url,
                });
                flvPlayer.attachMediaElement(videoElement);
                flvPlayer.load();
                flvPlayer.play();
            }
            break;
        default:
            alert('不支持的类型');
            break
    }
}

$(".base_infor > .edit").click(function () {
    var src_title = $(".content > .title").html().trim();
    refresh_categories("#upload_video > .layout > .categories");

    $("#upload_video > .layout > .upload_file_title").val(src_title);
    var description = $(".content > .description").html();
    $("#upload_video > .layout > .description").val(description);

    var category_name = $(".content > .base_infor > .category_name").html();
    $("#upload_video > .layout > .categories").find("option:contains('" + category_name +"')").attr("selected", true);

    upload_video($(this), function () {
        var new_title = $("#upload_video > .layout > .upload_file_title").val().trim();
        var file_name = $("#upload_video > .layout > .upload_file_name").val();
        var category_name = $("#upload_video > .layout > .categories").val();

        if(new_title == '' || category_name == '') {
            infor("文件名和分类名不能为空", function () {
            });
            return;
        }

        var formData = new FormData($("#upload_video > .layout")[0]);
        formData.append("src_title", src_title);
        formData.append("new_title", new_title);
        formData.delete("title");

        $.ajax({
            type: 'POST',
            url: "/video/update_video",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("更新视频成功", function () {
                        if($(".current_category").attr("value") == category_name) {
                            pag_video(1, category_name);
                        } else {
                            pag_video(1, null);
                        }
                        get_video(new_title);
                    });
                } else {
                    infor("更新视频失败", function () {
                    });
                }
            },
            error: function(err) {
                reset_progress();
                infor("网络错误", function () {
                });
            },
            async: true,
            xhr: progress
        });
    }, function () {

    });
});