/**
 * Created by WYY on 2016/7/17.
 */
$(function () {
    function uploadImage(){
        var imgPath = $("#uploadFile").val();
        if (imgPath == ""){
            alert("请上传图片!");
            return;
        }
        var strExtension = imgPath.substr(imgPath.lastIndexOf('.') + 1);
        if (strExtension != 'jpg' && strExtension != 'jpeg' && strExtension != 'png'){
            alert("只支持jpg,jpeg,png格式的图片");
            return
        }
        $.ajax({url:"/uploadfile",
            data:{imgPath : $("#uploadFile").val()},
            type:"POST",
            cache : false,
            success:function (data) {
                if (data.code == 1){
                    alert("上传成功");
                    $("#imgDiv").empty();
                    $("#imgDiv").html(data);
                    $("#imgDiv").show();
                }

            },
            error:function(XMLHttpRequest,textStatus,errorThrown){
                alert("上传失败，请检查网络后重试");
            }
        });
    }

});
