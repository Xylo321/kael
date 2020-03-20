/* 信息对话框 */
function infor(message, callback, fight) {
    $("#infor > .message").text(message);

    $("#infor > .message").css({
        "margin-top": $("#infor").height() / 2 - $("#infor > .message").height() / 2,
        "margin-left": $("#infor").width() / 2 - $("#infor > .message").width() / 2
    });

    $("#infor").show();

    if(fight != true) {
        $("#infor > .button").click(function () {
            callback();
            $("#infor").hide();
            $(this).unbind();
        });
    } else {
        $("#infor > .button").hide();

        document.getElementById('bm').pause();
        document.getElementById('88').play();
        setTimeout(function() {
            callback();
            $("#infor").hide();
            $(this).unbind();
        }, 120 * 1000);
    }
}

$(window).resize(function() {
    if($("#infor").is(":visible")) {
        $("#infor > .message").css({
            "margin-top": $("#infor").height() / 2 - $("#infor > .message").height() / 2,
            "margin-left": $("#infor").width() / 2 - $("#infor > .message").width() / 2
        });
    }

    if($("#shuru").is(":visible")) {
        $("#shuru").hide();
    }
});

/* 输入对话框 */
function shuru(sender, message, position, conirm_callback, cancel_callback) {
    $("#shuru").show();
    switch(position) {
        case "right":
            $("#shuru > .layout").css({
                "margin-top": $(sender).offset().top - $(document).scrollTop(),
                "margin-left": $(sender).offset().left - $(document).scrollLeft()
            });
            break;
        case "left":
            $("#shuru > .layout").css({
                "margin-top": $(sender).offset().top - $(document).scrollTop(),
                "margin-left": $(sender).offset().left - $(document).scrollLeft() - $("#shuru > .layout").width() + $(sender).width()
            });
            break;
        default:
            break;
    }

    $("#shuru > .layout > input").val("");
    $("#shuru > .layout > input").focus();
    $("#shuru > .layout > input").attr("placeholder", message);

    $("#shuru > .layout > .confirm").click(function() {
        conirm_callback();
        $("#shuru").hide();

        $(this).unbind();
        $("#shuru > .layout > .cancel").unbind();
    });

    $("#shuru > .layout > .cancel").click(function() {
        cancel_callback();
        $("#shuru").hide();

        $("#shuru > .layout > .confirm").unbind();
        $(this).unbind();
    });
}

/* 上传文件对话框 */
function upload_file(sender, message, position, conirm_callback, cancel_callback) {
    $("#upload_file > .layout > input").val("");
    $("#upload_file > .layout > input").focus();
    $("#upload_file > .layout > input").attr("placeholder", message);

    $("#upload_file").show();
    switch(position) {
        case "right":
            $("#upload_file > .layout").css({
                "margin-top": $(sender).offset().top - $(document).scrollTop(),
                "margin-left": $(sender).offset().left - $(document).scrollLeft()
            });
            break;
        case "left":
            $("#upload_file > .layout").css({
                    "margin-top": $(sender).offset().top - $(document).scrollTop(),
                    "margin-left": $(sender).offset().left - $("#upload_file > .layout").width()
                });
            break;
        default:
            break;
    }

    $("#upload_file > .layout > .confirm").click(function() {
        conirm_callback();
        $("#upload_file").hide();

        $(this).unbind();
        $("#upload_file > .layout > .cancel").unbind();
    });

    $("#upload_file > .layout > .cancel").click(function() {
        cancel_callback();
        $("#upload_file").hide();

        $("#upload_file > .layout > .confirm").unbind();
        $(this).unbind();
    });
}


/* 上传视频对话框 */
function upload_video(sender, conirm_callback, cancel_callback) {
    $("#upload_video > .layout > input").focus();
    $("#upload_video").show();

    $("#upload_video > .layout > .confirm").click(function () {
        conirm_callback();
        $("#upload_video").hide();

        $(this).unbind();
        $("#upload_video > .layout > .cancel").unbind();

        $("#upload_video > .layout > input").val("");
        $("#upload_video > .layout > textarea").val("");
    });

    $("#upload_video > .layout > .cancel").click(function () {
        cancel_callback();
        $("#upload_video").hide();

        $("#upload_video > .layout > .confirm").unbind();
        $(this).unbind();

        $("#upload_video > .layout > input").val("");
        $("#upload_video > .layout > textarea").val("");
    });
}

function xhr_on_progress(fun) {
  xhr_on_progress.onprogress = fun; //绑定监听
  //使用闭包实现监听绑
  return function() {
    //通过$.ajaxSettings.xhr();获得XMLHttpRequest对象
    var xhr = $.ajaxSettings.xhr();
    //判断监听函数是否为函数
    if (typeof xhr_on_progress.onprogress !== 'function')
      return xhr;
    //如果有监听函数并且xhr对象支持绑定时就把监听函数绑定上去
    if (xhr_on_progress.onprogress && xhr.upload) {
      xhr.upload.onprogress = xhrOnProgress.onprogress;
    }
    return xhr;
  }
}