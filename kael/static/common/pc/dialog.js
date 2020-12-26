/* 信息对话框 */
function infor(message, callback, fight) {
    $("#infor > .message").text(message);
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
        document.getElementById('idea').pause();

        document.getElementById('88').play();
        setTimeout(function() {
            callback();
            $("#infor").hide();
            $(this).unbind();
        }, 120 * 1000);
    }
}

$(window).resize(function() {
    if($("#shuru").is(":visible")) {
        $("#shuru").hide();
    }

    if($("#upload_file").is(":visible")) {
        $("#upload_file").hide();
    }

    if($("#upload_video").is(":visible")) {
        $("#upload_video").hide();
    }

    show_hide_ad();
});

$(function () { show_hide_ad(); });
function show_hide_ad() {
    var width = $(window).width();
    var height = $(window).height();
    if (width > 1430) {
        show_ad();
    } else {
        hide_ad();
    }
}

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

/* ad */
function hide_ad() {
    hide_ad_tip();

    var v = document.getElementById("ad_video");
    v.pause();

    if ($("#ad").is(":visible")) {
        $("#ad").hide();
    }
}

function show_ad() {
    show_ad_tip();
    setTimeout(function () {
        hide_ad_tip();
    }, 2000);
    var v = document.getElementById("ad_video");
    // "/static/search/某民族的最后一个人.mp4"
    var ads = ["/static/search/宇宙有多大.mp4"];
    var random_num = Math.floor(Math.random() * 1);
    $(".ad_temp").attr("value", ads[random_num]);
    $("#ad_video").attr("src", ads[random_num]);
    v.play();
    $("#ad").show();
}

function hide_ad_tip() {
    if($(".ad_tip").is(":visible")) {
        $(".ad_tip").hide();
    }
}

function show_ad_tip() {
    $(".ad_tip").show();
}

/* 上传文件对话框 */
function upload_file(sender, src_title, message, position, conirm_callback, cancel_callback) {
    $("#upload_file > .layout > .upload_file_title").val(src_title);
    $("#upload_file > .layout > .upload_file_title").focus();
    $("#upload_file > .layout > .upload_file_title").attr("placeholder", message);
    $("#upload_file > .layout > .upload_file_name").val('');

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
                    "margin-left": $(sender).offset().left - $("#upload_file > .layout").width() + $("#upload_file > .layout > a").width()
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

/* 进度条不知道如何做对话框 */
function set_progress(num) {
    $("#upload_progressbar > .layout > meter").attr("value", num);
}

function show_progress() {
    $("#upload_progressbar").show();
}

function reset_progress() {
    $("#upload_progressbar").hide();
    $("#upload_progressbar > .layout > meter").attr("value", "0");
}

function progress() {
    show_progress();
    xhr_obj = new XMLHttpRequest();
    if(xhr_obj.upload){ // check if upload property exists
        xhr_obj.upload.addEventListener('progress',function(e){
            var loaded = e.loaded; //已经上传大小情况
            var total = e.total; //附件总大小
            var percent = Math.abs(100 * loaded / total);
            set_progress(percent);

            if (percent == 100) {
                reset_progress();
            }
        }, false); // for handling the progress of the upload
    }

    return xhr_obj;
}