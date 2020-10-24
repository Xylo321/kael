$(function () {
    if($(".article_title").length != 0) {
        var article_title = $(".article_title").attr("value");
        get_article(article_title);

        refresh_categories(".nav");
        pag_article(1, null);
    } else {
        refresh_categories(".nav");
        pag_article(1, null);
        /* 当博客打开时，自动获取文章列表当第一篇博客 */
        load_first_article();
    }

    responsive();
});

function load_first_article() {
    var si = setInterval(function () {
        if ($("td.title").length > 0) {
            $(".new_article").hide();
            $(".newArticle").show();

            if ($("td.title").length > 0) {
                var article_title = $("td.title")[0].innerText;
                get_article(article_title);
            }

            clearInterval(si);
        }
    }, 100);
}

$(window).resize(function () {
    responsive();

    if ($(".center > .content > .new_article > .edit_panel > .editor > textarea").is(":visible")) {
        $(".center > .content > .new_article > .edit_panel > .editor > textarea").css({
            "height": $(window).height() - $(".center > .content > .new_article > .edit_panel > .opera > .opera_left").height()
        });
    }

    if ($(".center > .content > .old_article > .edit_panel > .editor > textarea").is(":visible")) {
        $(".center > .content > .old_article > .edit_panel > .editor > textarea").css({
            "height": $(window).height() - $(".center > .content > .old_article > .edit_panel > .opera > .opera_left").height()
        });
    }
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

function img_iframe_responsive() {
    $("img, pre, video").css({
        "width": $(".center").width() - 20,
        'margin-left': '10px',
        'margin-right': '10px',
    })

    $("iframe, video").css({
        "width": $(".center").width(),
        "height": $(".center").width() * 0.7
    })

    // $("img").css({
    //     "height": $(".center").width() * 0.7
    // })

    $(".article_preview > a, .article_preview > h1, .article_preview > h3, .article_preview > h4, .article_preview > h5, .article_preview > h6").css({
        "width": $(".center").width(),
        "text-overflow": "ellipsis",
        "overflow": "hidden",
        "white-space": "nowrap"
    })
}

/* 自适应窗口大小 */
function responsive() {
    var width = $(window).width();
    var height = $(window).height();

    if (width < 960) {
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
    } else if (width < 1366) {
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
    } else if(width < 1616){
        $(".left").show();
        $(".right").show();
        $(".left_control").hide();
        $(".right_control").hide();

        $('.center').css({
            "width": width - 500,
            "margin-left": "250px",
            "margin-right": "250px"
        });
    } else {
        $(".left").hide();
        $(".right").hide();
        $(".left_control").show();
        $(".right_control").show();

        $('.center').css({
            "width": 960,
            "margin-left": (width - 960) / 2,
            "margin-right": (width - 960) / 2
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

    img_iframe_responsive()
}

/* 拉取文章列表 */
function pag_article(page, category_name) {
    var url = "/blog/pag_article";
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

                $(".article_list > .data").html(al_html);
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
        pag_article(current_page + 1, current_category);
});

/* 文章上一页 */
$("#pre_page").click(function () {
    var current_category = $(".current_category").attr("value");
    var current_page = parseInt($(".current_page").attr("value"));
    if (current_page > 1)
        pag_article(current_page - 1, current_category);
});

/* 打开便利工具 */
$(".notepad").click(function() {
    location.href = '/blog/notepad';
});

/* 新建文章 */
$(".newArticle").click(function () {
    if($(".nav > li > .cat").length == 0) {
        infor("请增加栏目后再写文章", function() {
        });
    } else {
        $(".old_article").hide();
        $(".center > .content > .new_article > .edit_panel > .editor > textarea").val("");
        $(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .title").val("");
        $(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .category_name").val("");

        $(".center > .content > .new_article").show();
        refresh_categories(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .category_name");
        $(".center > .content > .new_article > .edit_panel > .editor > textarea").css({
            "height": $(window).height() - $(".center > .content > .new_article > .edit_panel > .opera > .opera_left").height()
        });

        $(".center > .content > .new_article > .preview_panel").hide();
        $(this).hide();
    }
});

/* 新建-预览 */
$(".center > .content > .new_article > .edit_panel > .opera > .opera_right > .debug").click(function () {
    $(".center > .content > .new_article > .edit_panel").hide();
    var html_markdown = $(".center > .content > .new_article > .edit_panel > .editor > textarea").val().trim();

    hljs.initHighlightingOnLoad();
    var rendererMD = new marked.Renderer();
        marked.setOptions({
          renderer: rendererMD,
          gfm: true,
          tables: true,
          breaks: false,
          pedantic: false,
          sanitize: false,
          smartLists: true,
          smartypants: false
        });
        var markdownString = html_markdown;
        marked.setOptions({
            highlight: function (code) {
            return hljs.highlightAuto(code).value;
          }
        });

    $(".center > .content > .new_article > .preview_panel > .article_preview").html(marked(html_markdown));
    $(".center > .content > .new_article > .preview_panel").show();

    img_iframe_responsive()
});

/* 编辑-预览 */
$(".center > .content > .old_article > .edit_panel > .opera > .opera_right > .debug").click(function () {
    $(".center > .content > .old_article > .edit_panel").hide();
    var html_markdown = $(".center > .content > .old_article > .edit_panel > .editor > textarea").val().trim();
    $(".center > .content > .old_article > .preview_panel > .article_preview").html(marked(html_markdown));
    $(".center > .content > .old_article > .preview_panel").show();

    $(".center > .content > .old_article > .preview_panel > .opera > .edit").show();
    $(".center > .content > .old_article > .preview_panel > .opera > .view").hide();

    img_iframe_responsive()
});

/* 编辑-预览-返回 */
$(".center > .content > .old_article > .preview_panel > .opera > .edit > .back").click(function () {
    $(".center > .content > .old_article > .edit_panel").show();
    $(".center > .content > .old_article > .preview_panel").hide();
});

/* 编辑-关闭 */
$(".center > .content > .old_article > .edit_panel > .opera > .opera_right > .close").click(function () {
    $(".old_article > .edit_panel").hide();
    $(".old_article > .preview_panel").show();
    $(".old_article > .preview_panel > .opera > .view").show();
    $(".old_article > .preview_panel > .opera > .edit").hide();

    $(".newArticle").show();
});

/* 新建-预览-返回 */
$(".center > .content > .new_article > .preview_panel > .opera > .back").click(function () {
    $(".center > .content > .new_article > .edit_panel").show();
    $(".center > .content > .new_article > .preview_panel").hide();
});

/* 新建-关闭 */
$(".center > .content > .new_article > .edit_panel > .opera > .opera_right > .close").click(function () {
    $(".new_article").hide();
    $(".newArticle").show();
    if($(".old_article > .preview_panel > .article_preview").html() != "")
        $(".old_article").show();
});

/* 增加文章 */
$(".center > .content > .new_article > .edit_panel > .opera > .opera_right > .save").click(function () {
    var html_markdown = $(".center > .content > .new_article > .edit_panel > .editor > textarea").val().trim();
    var article_title = $(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .title").val().trim();
    var article_category_name = $(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .category_name").val();
    var is_public = $(".center > .content > .new_article > .edit_panel > .opera > .opera_right > .is_public").val().trim();

    if (html_markdown == "") {
        infor("文章内容不能为空", function () {
        });
        return;
    }

    if (article_title == "") {
        infor("文章标题不能为空", function () {
        });
        return;
    }

    $.ajax({
        url: "/blog/add_article",
        type: 'POST',
        cache: false,
        dataType: "json",
        data: {
            title: article_title,
            category_name: article_category_name,
            is_public: is_public,
            content: html_markdown
        },
        success: function (data) {
            if (data.status == 1) {
                infor("增加文章成功", function () {
                    $(".new_article").hide();
                    $(".newArticle").show();
                    if($(".preview_panel > .article_preview").html() != "")
                        $(".old_article").show();

                    var current_category = $(".current_category").attr("value");
                    var current_page = parseInt($(".current_page").attr("value"));
                    pag_article(current_page, current_category);

                    var si = setInterval(function () {
                        if ($("td.title").length > 0) {
                            $(".new_article").hide();
                            $(".newArticle").show();

                            var article_title = $("td.title").attr("title");
                            get_article(article_title);

                            clearInterval(si);
                        }
                    }, 100);
                });
            } else {
                infor("增加文章失败", function () {
                    // TODO
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

/* 更新文章 */
$(".center > .content > .old_article > .edit_panel > .opera > .opera_right > .save").click(function () {
    var src_article_title = $(".base > .title").attr("value");
    var new_article_title = $(".center > .content > .old_article > .edit_panel > .opera > .opera_left > .title").val().trim();
    var is_public = $(".center > .content > .old_article > .edit_panel > .opera > .opera_right > .is_public").val().trim();
    var content = $(".center > .content > .old_article > .edit_panel > .editor > textarea").val().trim();

    var article_category_name = $(".center > .content > .old_article > .edit_panel > .opera > .opera_left > .category_name").val();

    if (content == "") {
        infor("文章内容不能为空", function () {
        });
        return;
    }

    if (new_article_title == "") {
        infor("文章标题不能为空", function () {
        });
        return;
    }

    $.ajax({
        url: "/blog/update_article",
        type: 'POST',
        cache: false,
        dataType: "json",
        data: {
            src_title: src_article_title,
            new_title: new_article_title,
            category_name: article_category_name,
            is_public: is_public,
            content: content
        },
        success: function (data) {
            if (data.status == 1) {
                infor("修改文章成功", function () {
                    var current_category = $(".current_category").attr("value");
                    var current_page = parseInt($(".current_page").attr("value"));
                    pag_article(current_page, current_category);

                    get_article(new_article_title);
                });
            } else {
                infor("修改文章失败", function () {
                });

                infor("登录超时或被测试", function () {
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
    location.href = "/blog/home";
});

function refresh_categories(selector, selected) {
    var url = "/blog/get_categories";
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
                                nav_html += '<li><a class="cat" title="' + data.data[i].name + '">' + data.data[i].name + '</a><a  class="del" title="删除栏目及该栏目所有文章">&sup1;</a><a  class="rename" title="重命名该栏目">&sup2;</a></li>';
                            }else {
                                nav_html += '<li><a class="cat" title="' + data.data[i].name +'">' + data.data[i].name + '</a></li>';
                            }
                        }

                        if($(look_dom).length == 0)
                            nav_html += "<li><a  class='add' title='增加栏目'>+</a></li>";

                        $(selector).html(nav_html);
                        break;
                    case '.center > .content > .new_article > .edit_panel > .opera > .opera_left > .category_name':
                        // 加载编辑器里的分类列表 dom
                        var select_html = "";
                        for (var i = 0; i < data.data.length; i++) {
                            select_html += "<option value='" + data.data[i].name + "'>" + data.data[i].name + "</option>";
                        }
                        $(selector).html(select_html);
                        break;
                    case '.center > .content > .old_article > .edit_panel > .opera > .opera_left > .category_name':
                        // 加载编辑器里的分类列表 dom
                        var select_html = "";
                        for (var i = 0; i < data.data.length; i++) {
                            select_html += "<option value='" + data.data[i].name + "'>" + data.data[i].name + "</option>";
                        }
                        $(selector).html(select_html);

                        $(selector).val(selected);
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

/* 点击栏目名获取栏目列表 */
$(".nav").on("click", "li > .cat", function () {
    var current_category = $(".current_category").attr("value");
    if ($(this).html() == '仲夏辰星') {
        document.getElementById('bm').pause();
        document.getElementById('idea').play();
    } else {
        document.getElementById('idea').pause();
        document.getElementById('bm').play();
    }
    if ($(this).html() != current_category) {
        $(".current_category").attr("value", $(this).html());
        $(".current_page").attr("value", "1");

        pag_article(1, $(this).html());
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
            url: "/blog/rename_category",
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

                        // 如果新建面板编辑区可见则更新编辑区里的文章分类select
                        if($(".center > .content > .new_article > .edit_panel").is(":visible"))
                            refresh_categories(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .category_name", null);

                        // 如果旧文章编辑面板可见，则更新旧文章的文章分类select，并选中最新的栏目名
                        if($(".center > .content > .old_article > .edit_panel").is(":visible")) {
                            var title = $(".base > .title").attr("value");
                            update_article_category_name(title);
                        }

                        // 如果旧文章内容显示面板可见过，则更新旧文章区域
                        if($(".base > .title").attr("value") != "") {
                            var title = $(".base > .title").attr("value");
                            get_article(title);
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
            url: "/blog/del_category",
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
                        pag_article(current_page, null);

                        // 如果新建文章面板可见，则更新新建面板里的select文章栏目列表
                        if($(".center > .content > .new_article").is(":visible")) {
                            refresh_categories(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .category_name", null);
                        }
                        // 如果旧文章面板可见，而且当前被删除当栏目名与旧文章面板当栏目名相同，则隐藏旧文章面板
                        if($(".center > .content > .old_article").is(":visible")) {
                            var category_name = $(".base > .category_name").html();
                            if(category_name == name) {
                                $(".center > .content > .old_article").hide();
                                $(".base > .category_name").html("");
                                $(".base > .date").val("");
                                $(".base > title").attr("title", "");
                            }
                        }

                        var si = setInterval(function () {
                            if ($("td.title").length > 0) {
                                $(".new_article").hide();
                                $(".newArticle").show();

                                var article_title = $("td.title").attr("title");
                                get_article(article_title);

                                clearInterval(si);
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

        $.ajax({
            url: "/blog/add_category",
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
                        refresh_categories(".center > .content > .new_article > .edit_panel > .opera > .opera_left > .category_name", null);
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

/* 删除文章 */
$(".other > .delete").click(function () {
    shuru($(this), "确认删除文章名", "left", function () {
        var src_title = $(".base > .title").attr("value").trim();

        var your_title = $("#shuru > .layout > input").val().trim();
        if (your_title == "") {
            infor("确认删除文章名不能为空", function () {
            });
            return;
        }

        if (your_title != src_title) {
            infor("确认删除文章名不正确", function () {
            });
            return;
        }

        $.ajax({
            url: "/blog/del_article",
            type: 'POST',
            cache: false,
            data: {
                title: your_title,
            },
            dataType: "json",
            success: function (data) {
                if (data.status == 1) {
                    infor("文章删除成功", function () {
                        /* 重新拉取列表 */
                        var current_category = $(".current_category").attr("value");
                        var current_page = parseInt($(".current_page").attr("value"));
                        pag_article(current_page, current_category);

                        $(".old_article").hide();
                        load_first_article();
                    });
                } else {
                    infor("文章删除失败", function () {
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

/* 点击文章列表里的文章 */
$(".article_list > .data").on('click', '.title > a', function() {
    if(!$(".edit_panel").is(":visible")) {
        $(".new_article").hide();
        $(".newArticle").show();
        var article_title = $($(this).parent()).text();
        get_article(article_title);
    } else {
        infor("正在编辑中", function() {
        });
    }
});

function get_article(article_title) {
    var look_dom = $(".look");

    var url = "/blog/get_article";
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
            title: article_title
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                var title = data.data[0].title;
                var date = data.data[0].date;
                var content = data.data[0].content;
                var category_name = data.data[0].category_name;
                var is_public = data.data[0].is_public;

                $(".newArticle").show();
                $(".center > .content > .old_article").show();
                $(".center > .content > .old_article > .edit_panel").hide();
                $(".center > .content > .old_article > .preview_panel").show();
                $(".center > .content > .old_article > .preview_panel > .opera > .edit").hide();
                $(".center > .content > .old_article > .preview_panel > .opera > .view").show();

                hljs.initHighlightingOnLoad();
                var rendererMD = new marked.Renderer();
                    marked.setOptions({
                      renderer: rendererMD,
                      gfm: true,
                      tables: true,
                      breaks: false,
                      pedantic: false,
                      sanitize: false,
                      smartLists: true,
                      smartypants: false
                    });
                    var markdownString = content;
                    marked.setOptions({
                        highlight: function (code) {
                        return hljs.highlightAuto(code).value;
                      }
                    });

                $(".center > .content > .old_article > .preview_panel > .article_preview").html(marked(content));
                $(".center > .content > .old_article > .preview_panel > .backup").attr("value", content);
                $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .category_name").html(category_name);
                $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .date").html(new Date(date * 1000).toLocaleString());
                $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .title").attr("value", title);
                $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .is_public").attr("value", is_public);
                img_iframe_responsive()
            } else {
                infor("获取文章详情失败", function() {
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

/* 更新旧文章的标题 */
function update_article_category_name(article_title) {
    $.ajax({
        url: "/blog/get_article",
        type: 'POST',
        cache: false,
        data: {
            title: article_title
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                var title = data.data[0].title;
                var date = data.data[0].date;
                var content = data.data[0].content;
                var category_name = data.data[0].category_name;

                $(".center > .content > .old_article > .preview_panel > .article_preview")
                    .html(marked(content));
                $(".center > .content > .old_article > .preview_panel > .backup").attr("value", content);
                $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .category_name").html(category_name);
                $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .date").html(new Date(date * 1000).toLocaleString());
                $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .title").attr("value", title);

                var category_name = $(".base > .category_name").html();
                refresh_categories(".center > .content > .old_article > .edit_panel > .opera > .opera_left > .category_name", category_name);
            } else {
                infor("获取文章详情失败", function() {
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

/* 旧文章编辑 */
$(".other > .update").click(function() {
    $(".newArticle").hide();
    /* 获取旧文章内容 */
    var content = $(".center > .content > .old_article > .preview_panel > .backup").attr("value");
    var title = $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .title").attr("value");
    var is_public = $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .is_public").attr("value");
    var category_name = $(".center > .content > .old_article > .preview_panel > .opera > .view > .base > .ccategory_name").html();

    $(".center > .content > .old_article > .preview_panel").hide();
    $(".center > .content > .old_article > .edit_panel").show();

    $(".center > .content > .old_article > .edit_panel > .editor > textarea").css({
        "height": $(window).height() - $(".center > .content > .old_article > .edit_panel > .opera > .opera_left").height()
    });
    $(".center > .content > .old_article > .edit_panel > .editor > textarea").val(content);

    $(".center > .content > .old_article > .edit_panel > .opera > .opera_left > .title").val(title);

    $(".center > .content > .old_article > .edit_panel > .opera > .opera_right > .is_public").val(is_public);

    var category_name = $(".base > .category_name").html();

    refresh_categories(".center > .content > .old_article > .edit_panel > .opera > .opera_left > .category_name", category_name);
});

//div全屏之后样式背景色和前景色全都为黑的了
// $(".content").on("dblclick", ".article_preview", function () {
//     var on = 0;
//
//     if (document.webkitfullscreenElement) {
//         on = 1;
//     } else if (document.mozFullscreenElement) {
//         on = 2;
//     } else if (document.msfullscreenElement) {
//         on = 3;
//     } else if (document.fullscreenElement) {
//         on = 4;
//     } else if (document.webkitFullscreenElement) {
//         // edge浏览器下
//         on = 5;
//     }
//
//     if (on > 0) {
//         switch(on) {
//             case 1:
//             case 5:
//                 document.webkitCancelFullScreen();
//                 break;
//             case 2:
//                 document.mozCancelFullScreen();
//                 break;
//             case 3:
//                 document.msCancelFullScreen();
//                 break;
//             case 4:
//                 var j = 0;
//                 if (document.webkitCancelFullScreen)
//                     document.webkitCancelFullScreen();
//                 else if (document.mozCancelFullScreen)
//                     document.mozCancelFullScreen();
//                 else if (document.msCancelFullScreen)
//                     document.msCancelFullScreen();
//                 else if (document.cancelFullScreen)
//                     document.cancelFullScreen();
//                 else {
//                     infor("该浏览器不支持全屏接口", function () {
//                     }, false);
//                     j = 1;
//                 }
//                 if(j == 0) {
//                     $(".content").css({
//                         "color": "green",
//                         "background": "black"
//                     })
//                 }
//
//                 break;
//
//             default: break;
//         }
//     } else {
//         if ($(this)[0].webkitRequestFullScreen)
//             $(this)[0].webkitRequestFullScreen();
//         else if ($(this)[0].mozRequestFullScreen)
//             $(this)[0].mozRequestFullScreen();
//         else if ($(this)[0].msRequestFullScreen)
//             $(this)[0].msRequestFullScreen();
//         else
//             infor("该浏览器不支持全屏接口", function() {}, false);
//     }
// });