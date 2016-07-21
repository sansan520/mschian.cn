$(document).ready(function(){

    dropdownOpen();//index 调用

    
    

});


function ms_login_check_name() {
    var u_name = $(".username-input").val();

    if (u_name ==''){
        $("#name_label").show();
        v.name.focus();
        $("#int_name").style.borderColor='#FF0000';
        $("#username-img").style.borderColor='#FF0000';
        $("#username-img").className="username-img0";
        $("#int_name").style.borderLeft="0px";
    }else{
        // $("#int_name").style.borderColor='#949393';
        $("#name_label").html("");
    }
}

function ms_login_check_password() {
     var u_password = $(".pwd-input").val();
    if (u_password ==''){
        $("#password_label").show();
        v.name.focus();
        $("#int_pass").style.borderColor='#FF0000';
        $("#pwd-img").style.borderColor='#FF0000';
        $("#pwd-img").className="pwd-img0";
        $("#int_name").style.borderLeft="0px";
    }else{
        // $("#int_name").style.borderColor='#949393';
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


