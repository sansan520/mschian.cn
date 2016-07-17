/**
 * Created by WYY on 2016/7/10.
 */
$(function () {
    $("#registerSubmit").submit(function () {
        var ho_name = $("#ho_name").val();
        var user_account = $("#ho_account").val();
        var user_password = $("#ho_passord").val();
        var user_mobile = $("#ho_mobile").val();
        var ho_tel = $("#ho_tel").val();
        var ho_email = $("#ho_email").val();
        var ho_nicard = $("#ho_nicard").val();
        var user_headimg = $("user_headimg").val();
        $(".input-text").focus(function(){
            var labelId = $(this).attr(id)+"Error";
            $("#"+labelId).text("");
            showError($("#"+labelId));
        });

        if (!ho_name) {
            alter("姓名不能为空");
        }
        if (!user_account) {
            alter("账号不能为空");
        }
        if (user_account.length < 6 || user_account.length > 16) {
            alter("账号长度大于6小于16");
        }
        if (!user_password) {
            alter("密码不能为空");
        }
        if (user_password.length < 6 || user_password.length > 16) {
            alter("密码长度大于6小于16");
        }
        if (!user_mobile) {
            alter("手机号不能为空");
        }
        if (user_mobile.length < 11) {
            alter("手机号不能小于11");
        }
        if (!/^(13|15|18|17[0-9]{9})$/.test(user_mobile)) {
           alter("手机号格式不正确");
        }
        if (!/^(0[0-9]{3})+-([0-9]{8})$/.test(ho_tel)) {
            alter("电话格式不正确");
        }
        if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(ho_email)) {
            alter("邮箱格式不正确");
        }

        switch(type){
            case 0:
                $.ajax({url: "/do_ho_register",
                data: JSON.stringify({
                "ho_name": ho_name,
                "user_account":user_account,
                "user_password":user_password,
                "user_mobile": user_mobile,
                "ho_tel": ho_tel,
                "ho_email": ho_email,
                "ho_nicard": ho_nicard,
                "user_headimg":user_headimg
            }),
            contentType: "application/json",
            success:function (data) {
                if(data.code == 0){
                alert("注册失败");
            }else if(data.code == 1){
                location.href = "/index";
            }
            }

        });
            case 1:
                $.ajax({url: "/do_user_register",
                data: JSON.stringify({
                "user_account": user_account,
                "user_password": user_password,
                "user_mobile": user_mobile,
                "user_headimg":user_headimg
                }),
                contentType: "application/json",
                success:function (data) {
                    if(data.code == 0){
                        alert("注册失败");
                    }else if(data.code == 1){
                        location.href = "/index";
                    }
                }

            });
        }
    });
    
});
function showError(ele){
    var text = ele.text();
    if (!text){
        ele.css("display","none");
    }else{
        ele.css("display","");
    }
}