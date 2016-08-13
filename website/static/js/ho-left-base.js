/**
 * Created by HuaisanWang on 16/8/13.
 */

/* http://layer.layui.com/  关于layer */
var myArray = new Array();

    // 左侧房源点击事件
    function click_func(hs_id,obj,frmWhichPage) {
        $(obj).parent("li").siblings().removeClass("active");
        $(obj).parent("li").addClass("active");
        if(hs_id>0){
            for(i=0;i<myArray.length;i++){
                item = myArray[i];
                if(item.hs_id == hs_id){
                    insertContainer(item,frmWhichPage);
                    break;
                }
            }
        }
    }
    //(当前对象,is_default_page,is_from_house_page,is_from_room_page)
    function insertContainer(object,frmWhichPage) {
        if(frmWhichPage==0 || frmWhichPage==undefined) {
            if (object != undefined) {
                $(".msMag-nr-detail").html('');
            }
            var content = '';

            content += '<div class="msMag-blockM-top-col clearfix"><div class="pull-right mT13">';
            content += '<button type="button" class="btn btn-mag" id="btn_edit_house" onClick="func_edit_house(' + object.hs_id + ')">编辑房源</button>';
            content += '<button type="button" class="btn btn-mag" id="btn_del_house" onClick="func_del_house(' + object.hs_id + ')">删除房源</button>';
            content += '<button type="button" class="btn btn-mag" id="btn_manage_room" onClick="func_manage_room(' + object.hs_id + ')">管理客房</button>';
            content += '</div></div>';


            //房源名称
            content += '<div class="row"><div class="col-xs-2 text-right msMagND-name">房源名称：</div><div class="col-xs-10 text-left msMagND-txt">' + object.hs_name + '</div></div>';
            //状态
            content += '<div class="row"><div class="col-xs-2 text-right msMagND-name">状态：</div>';
            if (object.hs_status == 1) {
                content += '<div class="col-xs-10 text-left msMagND-txt">开启</div></div>';
            } else {
                content += '<div class="col-xs-10 text-left msMagND-txt">关闭</div></div>';
            }

            //房源民宿地址
            var address = '';
            address += object.hs_province + object.hs_city + object.hs_country + object.hs_address;
            content += '<div class="row"><div class="col-xs-2 text-right msMagND-name">房源民宿地址：</div>';
            content += '<div class="col-xs-10 text-left msMagND-txt">' + address + '</div></div>';
            //简介
            content += '<div class="row"><div class="col-xs-2 text-right msMagND-name">简介：</div>';
            content += '<div class="col-xs-10 text-left msMagND-txt">' + object.hs_intro + '</div></div>';

            //图片
            var imglist = new Array();
            imglist = object.hs_images.split('|');
            content += '<div class="row"><div class="col-xs-2 text-right msMagND-name">民宿概览图：</div>';
            content += '<div class="col-xs-10 text-left msMagND-txt">';
            for (i = 0; i < imglist.length; i++) {
                content += '<img src= "' + imglist[i] + '" width="200" height="160" style="margin-left:5px;margin-bottom: 5px;"/>';
            }
            content += '</div></div>';

            $(".msMag-nr-detail").html(content);
        }else if(frmWhichPage==1) {
            showEditHouseDialog(object.hs_id);
        }else if(frmWhichPage==2) {
            showManageRoomDialog(object.hs_id);
        }
    }

    function showManageRoomDialog(hs_id) {
        layer.confirm('您确定要切换房源?', {
            btn: ['确定','取消'] //按钮
        }, function(){
            location.href = "/room_default/"+hs_id;
        }, function(){
            layer.msg('取消当前操作',{ time: 1000});
        });
    }
    // 弹出修改房源的对话框
    function showEditHouseDialog(hs_id) {
        //询问框
        layer.confirm('要修改当前房源吗?', {
          btn: ['去修改','取消'] //按钮
        }, function(){
            location.href = "/house_edit/"+hs_id;
            // layer.msg('马上进入修改房源页面', {icon: 1},{
            //     time: 2000,
            //     end: function(){
            //         alert("ok");
            //     }
            // });
        }, function(){
            layer.msg('取消当前操作',{ time: 1000});
        });
    }

    function load_resource_by_user_id(frmWhichPage,hs_id) {
        $.ajax({
            url:"/get_resource_by_user_id",
            type: 'post',
            data: JSON.stringify({"user_id":$("#hid_user_id").val()}),
            contentType: 'application/json',
            success: function(data){
                if(data.code==1){
                    var tmp='';
                    myArray = data.message;
                    if(myArray.length>0){
                        var default_hs_id = 0;
                        for(i=0;i<myArray.length;i++) {
                            item = myArray[i];
                            default_hs_id = item.hs_id;
                            if(frmWhichPage==0){
                                if (i == 0) {
                                    tmp += '<li role="presentation" class="active"><a id="' + item.hs_id + '" onClick="click_func(' + item.hs_id + ',this,' + frmWhichPage + ')">' + item.hs_name + '</a></li>';
                                } else {
                                    tmp += '<li role="presentation"><a id="' + item.hs_id + '" onClick="click_func(' + item.hs_id + ',this,' + frmWhichPage + ')">' + item.hs_name + '</a></li>';
                                }
                            }else{
                                if(hs_id==item.hs_id){
                                    tmp += '<li role="presentation" class="active"><a id="' + item.hs_id + '" onClick="click_func(' + item.hs_id + ',this,' + frmWhichPage + ')">' + item.hs_name + '</a></li>';
                                } else {
                                    tmp += '<li role="presentation"><a id="' + item.hs_id + '" onClick="click_func(' + item.hs_id + ',this,' + frmWhichPage + ')">' + item.hs_name + '</a></li>';
                                }
                            }

                        }

                        $(".nav-stacked").append(tmp);
                        if(frmWhichPage==0){
                             click_func(default_hs_id,null,0);// 获取改房东默认第一个房源信息
                        }


                    }
                }
            }
    });
    }