/*********** ---------------------------------------------|
 \\\//////  http://www.zhangyongfeng.com/                |
 | @   @ |  ---------------------------------------------|
 |   L   |  Zhang Yongfeng <artwc@outlook.com>           |
 (   v   )  Created by 2019/1/4                           |
 \_____/   _____________________________________________|
 * @license GPL
 * @version 1.0.0
 * @fileOverview for .html
 */
function set17kHeaderInfo(e){k("#header_login_user").html('<div class="tit"><img src="'+e.avatarUrl+'" onerror="this.src=\'//static.17k.com/pic/default_user_avatar.jpg\'"><a href="//user.17k.com">'+e.nickname+'</a></div><div class="exit"><a href="javascript:k.logout();">退出登录</a></div>'),k.isLogin()&&setInterval(function(){k.api("/ck/user/message/unreadCount").get().send(function(e){(e.msgNum||e.noticeNum)&&k("#header_17k_message a").className("new")})},3e4)}k.isLogin()?set17kHeaderInfo(k.loginInfo()):k.loginCallbacks.push(set17kHeaderInfo);