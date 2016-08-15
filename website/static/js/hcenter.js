/**
 * Created by HuaisanWang on 16/8/15.
 */

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
                        locaton.href=locationUrl;
                    }
                }
            });
        }

    }
}


