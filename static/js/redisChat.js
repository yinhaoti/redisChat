// 频道和消息

var logSwitch = 1;

var chatStore = {
    'Home': [],
    'Game': [],
    'Channel One': [],
    'Channel Two': [],
};

var currentChannel = '';

var log = function(){
  if(logSwitch){
    console.log(arguments);
  }
};


var chatItemTemplate = function(chat) {
    var name = chat.name;
    var content = chat.content;
    var time = chat.created_time;
    // js的模板字符串 ${}  跟jinja很像 不过不能用for了  变量替换
    var t =
    `
    <li class="rc-chat-item">
        <a class="rc-chat-avatar" href="#">
            <img id="id-rc-chat-avatar" class="media-object img-circle " src="/static/img/avatar.jpeg" alt="avatar">
        </a>
        <div class="media-body">
            <small class="text-muted">${name} &nbsp | &nbsp <time data-time="${time}"></time></small>
            <br>
            ${content}
            <hr>
        </div>
    </li>
    `;

    return t;
};


// 滚动到底部
var scrollToBottom = function(selector){
    var height = $(selector).prop("scrollHeight");
     // 第一个是动画效果，第二个是动画时间
     $(selector).animate({
        scrollTop: height
    }, );
}


var insertChats = function(chats) {
    var selector = '#id-div-chats'
    var chatsDiv = $(selector);
    var html = chats.map(chatItemTemplate);
    // [chatItemTemplate(c) for c in chats]
    chatsDiv.append(html.join(''));
    scrollToBottom(selector);
};


var sendMessage = function(){
  var name = 'Anonymous' //$('#id-input-name').val();
  var content = $('#id-input-content').val();
  var message = {
    name: name,
    content: content,
    channel: currentChannel,
  };

   // ajax 发送请求
  var request = {
    url: '/chat/add',
    type: 'post',
    contentType: 'application/json',
    data: JSON.stringify(message),
    success: function(r){
      log('success', r);
    },
    error: function(err) {
      log('error', err);
    }
  };
  $.ajax(request);
};


var changeChannel = function(channel) {
    document.title = '聊天室 - ' + channel;
    currentChannel = channel;
};


var bindActions = function(){
  $('#id-button-send').on('click', function(){
    sendMessage();
    // 清空input的值
    $('#id-input-content').val('');
    // 清楚focus
    $('#id-button-send').blur()
  });
  $('#id-input-content').bind('keydown',function(event){
    // Enter事件绑定
    if(event.keyCode == "13") {
        sendMessage();
        // 清空input的值
        $('#id-input-content').val('');
    }
});
  // 频道切换
  $('.rc-channel').on('click', function(e){
      e.preventDefault();
      //
      var channel = $(this).text();
      changeChannel(channel);
      // 切换显示
      $('.rc-channel').removeClass('active');
      $(this).addClass('active');
      // reload 信息
      $('#id-div-chats').empty();
      var chats = chatStore[currentChannel];
      insertChats(chats);
  })
};

var insertChatItem = function(chat) {
    var selector = '#id-div-chats';
    var chatsDiv = $(selector);
    log('chatsDiv', chatsDiv)
    var t = chatItemTemplate(chat);
    chatsDiv.append(t);
    scrollToBottom(selector);
};


var chatResponse = function(r) {
    
    // 把字符串解释成对象
    var chat = JSON.parse(r);
    log('chat', chat);
    // 加了一个对象
    chatStore[chat.channel].push(chat);
    log('chatStore[chat.channel]', chatStore[chat.channel]);
    log('currentChannel', currentChannel);
    // 如果insert的是当前平频道，就insert进去
    if(chat.channel == currentChannel) {
        log('insert的是当前平频道');
        insertChatItem(chat);
    }
};


var subscribe = function() {
  // 向服务器请求一个 sse 订阅
  var sse = new EventSource("/subscribe");
  log('向服务器请求一个 sse 订阅')
  // 收到消息后 就会调用的函数
  sse.onmessage = function(e) {
    log('收到消息', e, e.data);
    chatResponse(e.data);
  };
};


// long time ago
var longTimeAgo = function() {
  var timeAgo = function(time, ago) {
    return Math.round(time) + ago;
  };

  $('time').each(function(i, e){
    var past = parseInt(e.dataset.time);
    var now = Math.round(new Date().getTime() / 1000);
    var seconds = now - past;
    var ago = seconds / 60;
    // log('time ago', e, past, now, ago);
    var oneHour = 60;
    var oneDay = oneHour * 24;
    // var oneWeek = oneDay * 7;
    var oneMonth = oneDay * 30;
    var oneYear = oneMonth * 12;
    var s = '';
    if(seconds < 60) {
        s = timeAgo(seconds, ' 秒前')
    } else if (ago < oneHour) {
        s = timeAgo(ago, ' 分钟前');
    } else if (ago < oneDay) {
        s = timeAgo(ago/oneHour, ' 小时前');
    } else if (ago < oneMonth) {
        s = timeAgo(ago / oneDay, ' 天前');
    } else if (ago < oneYear) {
        s = timeAgo(ago / oneMonth, ' 月前');
    }
    $(e).text(s);
  });
};


var __main = function(){
  // 订阅
  subscribe();
  // 给按钮绑定事件
  bindActions();
  // 选中第一个 channel 作为默认 channel   模拟点击了一下
  $('.rc-channel')[0].click();
  // 更新时间的函数  每隔1000ms，调用一次longTimeAgo函数
  setInterval(function () {
      longTimeAgo();
  }, 1000);
};


$(document).ready(function(){
  __main();
});
