/**
 * Created by WYY on 2016/7/10.
 */
$(function(){
    $("#registerSubmit").submit(function () {
        var bool = true;
        if(!ajaxValidateName()){
            return false;
        }
        if(!ajaxVallidateAccount()){
            return false;
        }
        if(!ajaxVallidatePassword()){
            return false;
        }
        if(!ajaxVallidateMobile()){
            return false;
        }
        if(!ajaxVallidateEmail()){
            return false;
        }
        if(!ajaxValidateTel()){
        return false;
    }
    });
    return bool;
});

function ajaxValidateName(){
    ho_name = $("#ho_name").val();
    if(!ho_name){
        return error("��������Ϊ��");
    }
    $.ajax({
        url:"/do_ho_register",
        data:{method:"ajaxValidateName",ho_name:value},
        type:"POST",
        dataType:"json",
        async:false,
        cache:false,
        success:function (result) {
            if(!result){
                return false;
            }

        }
    });
    return true;
}

function ajaxVallidateAccount(){
    ho_account = $("#ho_account").val();
    if (!ho_account){
        return error("�˺Ų���Ϊ��");
    }
    if(ho_account.length < 6 || ho_account.length > 16){
        return error("����Ҫ����6С��16");
    }
    $.ajax({
        url:"/do_ho_register",
        data:{method:"ajaxValidateAccount",ho_account:value},
        type:"POST",
        dataType:"json",
        async:false,
        cache:false,
        success:function (result) {
            if(!result){
                return false;
            }

        }
    });
    return true;
}

function ajaxValidatePassword(){
    ho_password = $("#ho_passord").val();
    if(!ho_password ){
        return error("��������Ϊ��");
    }
    if(ho_password.length < 6 || ho_password.length > 16){
        return error("����Ҫ����6С��16");
    }
    $.ajax({
        url:"/do_ho_register",
        data:{method:"ajaxValidatePassword",ho_password:value},
        type:"POST",
        dataType:"json",
        async:false,
        cache:false,
        success:function (result) {
            if(!result){
                return false;
            }

        }
    });
    return true;
}

function ajaxValidateMobile(){
    ho_mobile = $("#ho_mobile").val();
    if(!ho_mobile){
        return error("�ֻ��Ų���Ϊ��,�����ο�������ϵ");
    }
    if(ho_mobile.length < 11){
        return error("�ֻ��Ÿ�ʽ����ȷ");
    }
    if(!/^(13|15|18|17[0-9]{9})$/.test(ho_mobile)){
        return error("�ֻ��Ÿ�ʽ����ȷ");
    }
    $.ajax({
        url:"/do_ho_register",
        data:{method:"ajaxValidateMobile",ho_mobile:value},
        type:"POST",
        dataType:"json",
        async:false,
        cache:false,
        success:function (result) {
            if(!result){
                return false;
            }

        }
});

function ajaxValidateTel(){
    ho_tel = $("#ho_tel").val();
    if(!/^(0[0-9]{3})+-([0-9]{8})$/.test(ho_mobile)){
        return error("�ֻ��Ÿ�ʽ����ȷ");
    }
    $.ajax({
        url:"/do_ho_register",
        data:{method:"ajaxValidateTel",ho_tel:value},
        type:"POST",
        dataType:"json",
        async:false,
        cache:false,
        success:function (result) {
            if(!result){
                return false;
            }

        }
    });
    return true;
}

function ajaxValidateEmail(){
    ho_email = $("#ho_email").val();
    if(!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(ho_mobile)){
        return error("email��ʽ����ȷ");
    }
    $.ajax({
        url:"/do_ho_register",
        data:{method:"ajaxValidateEmail",ho_email:value},
        type:"POST",
        dataType:"json",
        async:false,
        cache:false,
        success:function (result) {
            if(!result){
                return false;
            }

        }
    });
    return true;
}
