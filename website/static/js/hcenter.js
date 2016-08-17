/**
 * Created by HuaisanWang on 16/8/15.
 */

$("#user_log_out").click(function () {
            $.ajax({
            url:"/do_logout",
            type: 'POST',
            contentType: 'application/json',
            success: function(data){
                if(data.code==0){
                    alert(data.message);
                }else if(data.code==1){
                    alert(data.message);
                    location.href="/index";
                }
            }
        });
});

// 删除图片(假删除,将要删除的图片地址保存到表中,以后做定时任务删除表中图片)
function postDelImgs(delArr,locationUrl) {
    if(delArr.length>0){
        // var imgUrls = delArr.join();
        var imgUrls ="";
        for(i=0;i<delArr.length;i++){
            imgUrls+=delArr[i]+"|";
        }
        if(imgUrls.length>0){
            imgUrls = imgUrls.substring(0,imgUrls.lastIndexOf('|'));
            $.ajax({
                url: "/upload_delete_image",   // croppictest.py
                type: 'POST',
                data: JSON.stringify({
                    "del_image":imgUrls
                }),
                contentType: "application/json",
                success:function (data) {
                    if(data.code == 0){
                        layer.msg("程序错误");
                        return false;
                    }else if(data.code == 1){
                        if(locationUrl) locaton.href=locationUrl;
                    }
                }
            });
        }

    }
}


