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


    $(".btn-reg").click(function () {
        var user_account = $("#user_account").val();
        var user_password = $("#user_password").val();
        var user_mobile = $("#mobile").val();
        var user_headimg = $("#cropOutput").val();
        var isChecked = $("input[type='checkbox']").is(':checked');

        if (!user_account) {
            layer.msg("账号不能为空");
        }
        if (user_account.length < 6 || user_account.length > 16) {
            layer.msg("账号长度大于6小于16");
        }
        if (!user_password) {
            layer.msg("密码不能为空");
        }
        if (user_password.length < 6 || user_password.length > 16) {
            layer.msg("密码长度大于6小于16");
        }
        if (!user_mobile) {
            layer.msg("手机号不能为空");
        }
        if (user_mobile.length < 11) {
            layer.msg("手机号不能小于11");
        }

        if (!/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1})|(17[0-9]{1}))+\d{8})$/.test(user_mobile)) {
            layer.msg("手机号格式不正确");
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
                            }else if(data.code == 1){
                                if (data.user_type == 1)
                                {
                                   location.href = "/index";
                                }else if (data.user_type == 0){
                                    location.href = "/ho_next_register";
                                }
                            }
                        }
                    });
        });
});