$(function () {
    $("#signup-tab").click(function () {
        $("#signin-tab").removeClass("is-active");
        $("#signin-tab a").removeAttr("aria-selected");
        $("#signin-panel").removeClass("is-active");
        $("#signup-tab").addClass("is-active");
        $("#signup-tab a").attr("aria-selected", "true");
        $("#signup-panel").addClass("is-active");
    });
    $("#signin-tab").click(function () {
        $("#signup-tab").removeClass("is-active");
        $("#signup-tab a").removeAttr("aria-selected");
        $("#signup-panel").removeClass("is-active");
        $("#signin-tab").addClass("is-active");
        $("#signin-tab a").attr("aria-selected", "true");
        $("#signin-panel").addClass("is-active");
    });
    $("#signin-submit").click(function () {
        $("#signin-alert").hide();
        $("#signin-alert").empty();
        var signin_form = {};
        signin_form.email = $("#signin-email").val();
        signin_form.password = $("#signin-password").val();
        result = check_signin(signin_form);
        if (result != "success") {
            $("#signin-alert").text(result);
            $("#signin-alert").slideDown(300);
            return;
        }
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1/signin.do",
            dataType: "json",
            data: signin_form,
            success: function (data) {
                if (data == "success") {
                    location.href = "http://127.0.0.1/monitor";
                }
                else {
                    $("#signin-alert").text("Your e-mail address or password is invalid");
                    $("#signin-alert").slideDown(300);
                }
            }
        });
    });
    $("#signup-submit").click(function () {
        $("#signup-alert").hide();
        $("#signup-alert").empty();
        var signup_form = {};
        signup_form.email = $("#signup-email").val();
        signup_form.password = $("#signup-password").val();
        signup_form.confirm = $("#signup-confirm").val();
        var result = check_signup(signup_form);
        if (result != "success") {
            $("#signup-alert").text(result);
            $("#signup-alert").slideDown(300);
            return;
        }
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1/signup.do",
            dataType: "json",
            data: signup_form,
            success: function (data) {
                if (data == "success") {
                    $("#signup-success").text("Sign up successful!");
                    $("#signup-success").slideDown(300);
                    setTimeout(function () { location.href = "http://127.0.0.1/monitor"; }, 2000);
                    return;
                }
                $("#signup-alert").text("Username already sign up");
                $("#signup-alert").slideDown(300);
            }
        });
    });
});

function check_signin(signin_form) {
    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    if (!reg.test(signin_form.email) || signin_form.email.indexOf(" ") != -1) {
        return "Unvalid e-mail address";
    }
    else if (signin_form.password.length == 0) {
        return "Password shouldn't be null"
    }
    else {
        return "success";
    }
}

function check_signup(signup_form) {
    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    if (!reg.test(signup_form.email) || signin_form.email.indexOf(" ") != -1) {
        return "Unvalid e-mail address";
    }
    else if (signup_form.password.length == 0 || signup_form.confirm.length == 0) {
        return "Password shouldn't be null";
    }
    else if (signup_form.password != signup_form.confirm) {
        return "Your password can't be confirmed";
    }
    else {
        return "success";
    }
}
