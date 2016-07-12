/**
 * Created by WYY on 2016/7/10.
 */
$(function () {
    $("#registerSubmit").submit(function () {
        ho_name = $("#ho_name").val();
        ho_account = $("#ho_account").val();
        ho_password = $("#ho_passord").val();
        ho_mobile = $("#ho_mobile").val();
        ho_tel = $("#ho_tel").val();
        ho_email = $("#ho_email").val();
        ho_nicard = $("#ho_nicard").val();
        ho_image = $("ho_image").val();
        if (!ho_name) {
            return error("��������Ϊ��");
        }
        if (!ho_account) {
            return error("�˺Ų���Ϊ��");
        }
        if (ho_account.length < 6 || ho_account.length > 16) {
            return error("����Ҫ����6С��16");
        }
        if (!ho_password) {
            return error("��������Ϊ��");
        }
        if (ho_password.length < 6 || ho_password.length > 16) {
            return error("����Ҫ����6С��16");
        }
        if (!ho_mobile) {
            return error("�ֻ��Ų���Ϊ��,�����ο�������ϵ");
        }
        if (ho_mobile.length < 11) {
            return error("�ֻ��Ÿ�ʽ����ȷ");
        }
        if (!/^(13|15|18|17[0-9]{9})$/.test(ho_mobile)) {
            return error("�ֻ��Ÿ�ʽ����ȷ");
        }
        if (!/^(0[0-9]{3})+-([0-9]{8})$/.test(ho_mobile)) {
            return error("�ֻ��Ÿ�ʽ����ȷ");
        }
        if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(ho_mobile)) {
            return error("email��ʽ����ȷ");
        }
        $.post("/view/register", {
            "ho_name": ho_name,
            "ho_account": ho_account,
            "ho_password": ho_password,
            "ho_mobile": ho_mobile,
            "ho_tel": ho_tel,
            "ho_email": ho_email,
            "ho_nicard": ho_nicard,
            "ho_image": ho_image
        }, function (statue, data) {
        });
    });
    
});