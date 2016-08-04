/**
 * Created by WYY on 2016/7/17.
 */

     var maxsize = 2*1024*1024;//2M
     var errMsg = "上传的附件文件不能超过2M！！！";
     var tipMsg = "您的浏览器暂不支持计算上传文件的大小，确保上传文件不要超过2M，建议使用IE、FireFox、Chrome浏览器。";
     var  browserCfg = {};
     var ua = window.navigator.userAgent;
     if (ua.indexOf("MSIE")>=1){
         browserCfg.ie = true;
     }else if(ua.indexOf("Firefox")>=1){
         browserCfg.firefox = true;
     }else if(ua.indexOf("Chrome")>=1){
         browserCfg.chrome = true;
     }

    //"cropContaineroutput_imgUploadField"
    function checkUploadfile(inputFileId){
            try{
                var obj_file = document.getElementById(inputFileId);
                if(obj_file.value==""){
                    alert("请先选择上传文件");
                    return false;
                }


                if(!/\.(jpg|jpeg|png|JPG|PNG)$/.test(obj_file.value))
                {
                  alert("图片类型必须是.gif,jpeg,jpg,png中的一种")
                  return false;
                }
                var filesize = 0;
                if(browserCfg.firefox || browserCfg.chrome ){
                    filesize = obj_file.files[0].size;
                }else if(browserCfg.ie){
                    var obj_img = document.getElementById('tempimg');
                    obj_img.dynsrc=obj_file.value;
                    filesize = obj_img.fileSize;
                }else{
                    alert(tipMsg);
                    return false;
                }
                if(filesize==-1){
                    alert(tipMsg);
                    return false;
                }else if(filesize>maxsize){
                    alert(errMsg);
                    return false;
                }else{
                    return true;
                }
            }catch(e){
                alert(e);
            }
    }

//$(function () {


//     function uploadImage(){
//         var imgPath = $("#uploadFile").val();
//         if (imgPath == ""){
//             alert("请上传图片!");
//             return;
//         }
//         var strExtension = imgPath.substr(imgPath.lastIndexOf('.') + 1);
//         if (strExtension != 'jpg' && strExtension != 'jpeg' && strExtension != 'png'){
//             alert("只支持jpg,jpeg,png格式的图片");
//             return
//         }
//         $.ajax({url:"/uploadfile",
//             data:{imgPath : $("#uploadFile").val()},
//             type:"POST",
//             cache : false,
//             success:function (data) {
//                 if (data.code == 1){
//                     alert("上传成功");
//                     $("#imgDiv").empty();
//                     $("#imgDiv").html(data);
//                     $("#imgDiv").show();
//                 }
//
//             },
//             error:function(XMLHttpRequest,textStatus,errorThrown){
//                 alert("上传失败，请检查网络后重试");
//             }
//         });
//     }
//
// });
