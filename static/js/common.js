$(document).ready(function(){

    dropdownOpen();//index 调用


    $("#userLogin").click(function () {
        var account = $("#u_account").val();
        var password = $("#u_password").val();

        var data = {
            data: JSON.stringify({"account":account,"password":password})
        };

        $.ajax({
            url:"/login",
               type: 'POST',
               data: data,
               success: function(data){
                   alert(data.message);
                   if(data.code==1){
                       $('#myModalDL').modal('hide');  //隐藏模态窗口
                       // $("#myModalDL").fadeOut(function () {
                       //     $("#modal-backdrop").remove();
                       // });
                   }
               }
        });
        // alert("what the fuck");
    })

});
 /**
 * 鼠标划过就展开子菜单，免得需要点击才能展开
 */
 function dropdownOpen() {
    var $dropdownLi = $('li.dropdown');
    $dropdownLi.mouseover(function() {
          $(this).addClass('open');
    }).mouseout(function() {
         $(this).removeClass('open');
    });
 }



