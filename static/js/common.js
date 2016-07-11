$(document).ready(function(){

    dropdownOpen();//index 调用

    $("#login_click_l").click(function () {
        var u_name = $("#int_name").val();
        var u_password = $("#int_pass").val();
        $.ajax({
            url:"/do_login",
            type: 'POST',
            data: JSON.stringify({"ho_account":u_name,"ho_password":u_password}),
            contentType: 'application/json',
            success: function(data){
                if(data.code==0){
                    alert(data.message);
                }
            }
        });
        return false;
    });

});

/** 用户登录验证http://localhost:8000/login * */
function ms_user_login(v) {
    var u_name = v.name.val();

    if (u_name ==''){
        $("#name_label").show();
        v.name.focus();
        $("#int_name").style.borderColor='#FF0000';
        $("#username-img").style.borderColor='#FF0000';
        $("#username-img").className="username-img0";
        $("#int_name").style.borderLeft="0px";
    }else{
        $("#int_name").style.borderColor='#949393'
        $("#name_label").html("");
    }

    var u_password = v.pass.val;
    if (u_password ==''){
        $("#password_label").show();
        v.name.focus();
        $("#int_pass").style.borderColor='#FF0000';
        $("#pwd-img").style.borderColor='#FF0000';
        $("#pwd-img").className="pwd-img0";
        $("#int_name").style.borderLeft="0px";
    }else{
        $("#int_name").style.borderColor='#949393'
        $("#password_label").html("");
    }


}

/** 鼠标划过就展开子菜单，免得需要点击才能展开 */
function dropdownOpen() {
    var $dropdownLi = $('li.dropdown');
    $dropdownLi.mouseover(function() {
          $(this).addClass('open');
    }).mouseout(function() {
         $(this).removeClass('open');
    });
}

    // $("#userLogin").click(function () {
    //     var account = $("#u_account").val();
    //     var password = $("#u_password").val();
    //
    //     var data = {
    //         data: JSON.stringify({"account":account,"password":password})
    //     };
    //
    //     $.ajax({
    //         url:"/login",
    //            type: 'POST',
    //            data: data,
    //            success: function(data){
    //                alert(data.message);
    //                if(data.code==1){
    //                    $('#myModalDL').modal('hide');  //隐藏模态窗口
    //                    // $("#myModalDL").fadeOut(function () {
    //                    //     $("#modal-backdrop").remove();
    //                    // });
    //                }
    //            }
    //     });
    //     // alert("what the fuck");
    // })

