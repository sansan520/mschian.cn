$(function(){
var croppicContaineroutputOptions = {
				uploadUrl:'/crop_uploadPic',
				cropUrl:'/crop_cutPic',
				outputUrlId:'cropOutput',
				modal:false,
				loaderHtml:'<div class="loader bubblingG"><span id="bubblingG_1"></span><span id="bubblingG_2"></span><span id="bubblingG_3"></span></div> ',
				onBeforeImgUpload: function(){ console.log('onBeforeImgUpload') },
				onAfterImgUpload: function(){ console.log('onAfterImgUpload') },
				onImgDrag: function(){ console.log('onImgDrag') },
				onImgZoom: function(){ console.log('onImgZoom') },
				onBeforeImgCrop: function(){ console.log('onBeforeImgCrop') },
				onAfterImgCrop:function(){ console.log('onAfterImgCrop') },
				onReset:function(){ console.log('onReset') },
				onError:function(errormessage){ console.log('onError:'+errormessage) }
		}
    var cropContaineroutput = new Croppic('cropContaineroutput', croppicContaineroutputOptions);


    $("#user_account").blur(function () {
         var user_account = $("#user_account").val();
         if (user_account != ""){
             $.ajax({
                url: "/check_user_account", type: 'POST',
                data: JSON.stringify({"user_account": user_account}),
                contentType: "application/json",
                success:function (data) {
                    if(data.code == 0){
                        layer.msg('该账号可以使用');
                    }else if(data.code == 1){
                        layer.msg('该账号已经存在,请换一个试试...');
                        this.focus();
                    }
                }
         });
         return false;
         }
    });

    $("#mobile").blur(function () {
        var user_mobile = $("#mobile").val();
         if (user_mobile != ""){
             $.ajax({
                url: "/check_user_mobile", type: 'POST',
                data: JSON.stringify({"user_mobile": user_mobile}),
                contentType: "application/json",
                success:function (data) {
                    if(data.code == 1){
                        layer.msg('该手机号已经存在,请换一个试试...');
                        this.focus();
                    }
                }
         });
         return false;
         }
    });

    // 房东注册-第一步
    $(".btn_ho_reg").click(function () {
        var user_account = $("#user_account").val();
        var user_password = $("#user_password").val();
        var user_mobile = $("#mobile").val();
        var user_headimg = $("#cropOutput").val();
        var checklist = $(".checkbox .checked ");
        if (!user_account) {
            layer.msg("账号不能为空");
            return false;
        }
        if (user_account.length < 6 || user_account.length > 16) {
            layer.msg("账号长度大于6小于16");
            return false;
        }
        if (!user_password) {
            layer.msg("密码不能为空");
            return false;
        }
        if (user_password.length < 6 || user_password.length > 16) {
            layer.msg("密码长度大于6小于16");
            return false;
        }
        if (!user_mobile) {
            layer.msg("手机号不能为空");
            return false;
        }
        if (user_mobile.length < 11) {
            layer.msg("手机号不能小于11");
            return false;
        }

        if (!/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1})|(17[0-9]{1}))+\d{8})$/.test(user_mobile)) {
            layer.msg("手机号格式不正确");
            return false;
        }
        if (checklist <= 0){
            layer.msg("请同意条款");
            return false;
        }
        $.ajax({url: "/do_user_register",
            type: 'POST',
            data: JSON.stringify({
                "user_account": user_account,
                "user_password": user_password,
                "user_mobile": user_mobile,
                "user_headimg":user_headimg,
                "user_type" :0
            }),
            contentType: "application/json",
            success:function (data) {
                var data = JSON.parse(data);
                if(data.code == 0){
                    alert("注册失败");
                }else if(data.code == 1){
                    location.href = "/ho_next_register";
                }
            }
        });
    });

    //房东注册第二步
    $(".btn_ho_finish_reg").click(function () {
        var ho_name = $("#ho_name").val();
        var ho_email = $("#ho_email").val();
        var ho_tel = $("#ho_tel").val();
        var ho_nicard = $("#filesContainer").find('img').attr('src');
        if (!ho_name) {
            layer.msg("账号不能为空");
            layer.msg("请填写真实姓名");
        }
        if(!ho_nicard){
            layer.msg("请上传身份证件照!");
        }
        // $.ajax({url: "/do_ho_register",
        //     type: 'POST',
        //     data: JSON.stringify({
        //         "ho_name": ho_name,
        //         "ho_email": ho_email,
        //         "ho_tel": ho_tel,
        //         "ho_nicard":ho_nicard
        //         }),
        //         contentType: "application/json",
        //         success:function (data) {
        //             if(data.code == 0){
        //                 layer.msg("注册失败");
        //             }else if(data.code == 1){
        //                 //alert("注册成功");
        //                 location.href = "/index";
        //             }
        //         }
        // });
    });



    // 游客注册
    $(".btn-reg").click(function () {
        var user_account = $("#user_account").val();
        var user_password = $("#user_password").val();
        var user_mobile = $("#mobile").val();
        var user_headimg = $("#cropOutput").val();
        var isChecked = $("input[type='checkbox']").is(':checked');

        if (!user_account) {
            layer.msg("账号不能为空");
             $("#user_account").focus();
            return false;
        }
        if (user_account.length < 6 || user_account.length > 16) {
            layer.msg("账号长度大于6小于16");
            return false;
        }
        if (!user_password) {
            layer.msg("密码不能为空");
            return false;
        }
        if (user_password.length < 6 || user_password.length > 16) {
            layer.msg("密码长度大于6小于16");
            return false;
        }
        if (!user_mobile) {
            layer.msg("手机号不能为空");
            return false;
        }
        if (user_mobile.length < 11) {
            layer.msg("手机号不能小于11");
            return false;
        }

        if (!/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1})|(17[0-9]{1}))+\d{8})$/.test(user_mobile)) {
            layer.msg("手机号格式不正确");
            return false;
        }

        if(!isChecked){
            layer.msg("请同意条款");
            return false;
        }
        $.ajax({url: "/do_user_register",
                    type: 'POST',
                    data: JSON.stringify({
                        "user_account": user_account,
                        "user_password": user_password,
                        "user_mobile": user_mobile,
                        "user_headimg":user_headimg,
                        "user_type" :1
                        }),
                        contentType: "application/json",
                        success:function (data) {
                            var data = JSON.parse(data);
                            if(data.code == 0){
                                alert("注册失败");
                                return false;
                            }else if(data.code == 1){
                                location.href = "/index";
                            }
                        }
                    });
        });
});