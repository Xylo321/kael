$('#forgetPassword').click(function () {
    location.href = "/account/forget_password";
});

$('#register').click(function () {
    location.href = "/account/register";
});

$("#sendCheckCode").click(function () {
    email = $('#email').val().trim();
    if (email == "") {
        infor("发送邮箱不能为空", function () {
        });
        return;
    }

    $.ajax({
        url: "/account/send_check_code",
        type: 'POST',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        data: {
            "email": email
        },
        dataType: "json",
        success: function (data) {
            console.log(data);
            if (data.status == 1) {
                infor("验证码发送成功", function () {
                })
            } else {
                infor("验证码发送失败", function () {
                })
            }
        },
        error: function (err) {
            infor("网络错误", function () {
            })
        },
        async: true
    });
});

$('#login_button').click(function () {
    var name = $('#name').val().trim();
    var passwd = $('#passwd').val();

    if (name == "" || passwd == "") {
        infor("表单不能为空", function () {
        });
    }

    $.ajax({
        url: "/account/login",
        type: 'POST',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        data: {
            name: name,
            passwd: passwd
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                infor("登陆成功", function () {
                    location.href = '/search/index';
                });
            } else {
                infor("账号密码错误", function () {
                });
            }
        },
        error: function (err) {
            // TODO
        },
        async: true
    });
});

$('#register_button').click(function () {
    var name = $('#name').val().trim();
    var passwd = $('#passwd').val();
    var re_passwd = $('#re_passwd').val();

    var email = $('#email').val().trim();
    var check_code = $('#check_code').val().trim();

    if (name == "" || email == "" || check_code == "" || passwd == "" || re_passwd == "" || check_code == "") {
        infor("表单不能为空", function () {
        });
        return;
    }

    if (passwd != re_passwd) {
        infor("密码与确认密码不一致", function () {
        });
        return;
    }
    $.ajax({
        url: "/account/register",
        type: 'POST',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        data: {
            name: name,
            passwd: passwd,
            email: email,
            check_code: check_code
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                infor("注册成功", function () {
                    location.href = "/account/login";
                });
            } else {
                infor("注册失败", function () {
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

$("#forget_password_button").click(function () {
    var name = $("#name").val().trim();
    var email = $("#email").val().trim();
    var check_code = $("#check_code").val().trim();
    var new_passwd = $("#new_passwd").val().trim();
    var re_new_passwd = $("#re_new_passwd").val().trim();

    if (name == "" || email == "" || check_code == "" || new_passwd == "" || re_new_passwd == "") {
        infor("表单不能为空", function () {
        });
        return;
    }
    if (new_passwd != re_new_passwd) {
        infor("密码与确认密码不一致", function () {
        });
        return;
    }

    $.ajax({
        url: "/account/forget_password",
        type: 'POST',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        data: {
            name: name,
            email: email,
            check_code: check_code,
            new_passwd: new_passwd,
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                infor("改密成功", function () {
                    location.href = "/account/login";
                });
            } else {
                infor("改密失败", function () {
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