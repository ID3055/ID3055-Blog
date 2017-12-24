/*$(function(){ 
  $(".nav-main li").hover(function(){
    $("ul",this).slideDown(300)
  },function(){
    $("ul",this).hide();
    });
}); 
/*$(function(){ 
  $(".i_user").hover(function(){
    $("img",this).animate({top:'12px',
                            width:'66px',
                            height:'66px',
                            left:'-13px',
                            },'200');
    $(".i_menu",this).slideDown(500);
  },function(){
    $("img",this).animate({top:'0px',
                            width:'40px',
                            height:'40px',
                            left:'0px',
                            },'200');
    $(".i_menu",this).hide();
    });
}); 
*/

// 线程 IDs
var mouseover_tid = [];
var mouseout_tid = [];
var hoverTime = 200;//鼠标覆盖时间，单位ms
var outTime = 200;//鼠标离开时间，单位ms
$(function(){
        $('.profile-info').hover(
            // 鼠标进入
            function(){
                var _self = this;
                // 停止卷起事件
                clearTimeout(mouseout_tid[0]);
                // 当鼠标进入超过hoverTime毫秒, 展开菜单, 并记录到线程 ID 中
                mouseover_tid[0] = setTimeout(function() {
                    $(".i-face",_self).animate({top:'13px',
                            width:'66px',
                            height:'66px',
                            left:'-15px',
                            },100);//头像动画
					$(".face",_self).animate({
							borderWidth:"2px",
                            },100);
                    $(".dd-bubble",_self).show();
					$(".profile-m",_self).show();
					$(".dd-bubble",_self).animate({opacity:1,top:'42px'},200);
                }, hoverTime);
            },
 
            // 鼠标离开
            function(){
                var _self = this;
                // 停止展开事件
                clearTimeout(mouseover_tid[0]);
                // 当鼠标离开超过outTime毫秒, 卷起菜单, 并记录到线程 ID 中
                mouseout_tid[0] = setTimeout(function() {
                    $(".i-face",_self).animate({top:'3px',
                            width:'36px',
                            height:'36px',
                            left:'0px',
                            },100);
					$(".face",_self).animate({
							borderWidth:"0px"
                            },100);
					$(".dd-bubble",_self).animate({opacity:0,top:'47px'},200);
					$(".dd-bubble",_self).hide();
                }, outTime);
            }
        );
		
});

