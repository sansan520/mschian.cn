/**
 * Created by WYY on 2016/7/10.
 */
$(function () {
    $("#registerSubmit").submit(function () {
        var ho_name = $("#ho_name").val();
        var ho_account = $("#ho_account").val();
        var ho_password = $("#ho_passord").val();
        var ho_mobile = $("#ho_mobile").val();
        var ho_tel = $("#ho_tel").val();
        var ho_email = $("#ho_email").val();
        var ho_nicard = $("#ho_nicard").val();
        var ho_image = $("ho_image").val();
        if (!ho_name) {
            alter("姓名不能为空");
        }
        if (!ho_account) {
            alter("账号不能为空");
        }
        if (ho_account.length < 6 || ho_account.length > 16) {
            alter("账号长度大于6小于16");
        }
        if (!ho_password) {
            alter("密码不能为空");
        }
        if (ho_password.length < 6 || ho_password.length > 16) {
            alter("密码长度大于6小于16");
        }
        if (!ho_mobile) {
            alter("手机号不能为空");
        }
        if (ho_mobile.length < 11) {
            alter("手机号不能小于11");
        }
        if (!/^(13|15|18|17[0-9]{9})$/.test(ho_mobile)) {
           alter("手机号格式不正确");
        }
        if (!/^(0[0-9]{3})+-([0-9]{8})$/.test(ho_tel)) {
            alter("电话格式不正确");
        }
        if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(ho_email)) {
            alter("邮箱格式不正确");
        }
        $.post("/do_ho_register", {
            "ho_name": ho_name,
            "ho_account": ho_account,
            "ho_password": ho_password,
            "ho_mobile": ho_mobile,
            "ho_tel": ho_tel,
            "ho_email": ho_email,
            "ho_nicard": ho_nicard,
            "ho_image": ho_image
        }, function (data) {
            if(data.code == 0){
                alert("注册失败");
            }else if(data.code == 1){
                location.href = "/index";
            }

        });
    });
    
});