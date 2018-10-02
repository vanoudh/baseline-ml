console.log("wadell");

"use strict";

var user_id = null;
var target = null;
var result = null;
var timer = null;
var run_clicked = false;

const MODEL_LIST = 'zero linear tree forest'.split(' ');

const email_regex = new RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i);

$("#feedback_ctn").hide();
$(".alert").hide();
$("#register_ctn").hide();
$("#logout").hide();
$("#delete").hide();
$("#upload_ctn").hide();
$("#run").hide();

function track_page(title) {
  gtag('config', 'UA-126501644-1', {
    'page_title': 'API - ' + title, 
    'page_path': '/' + title.toLowerCase()
  });
}

function track_event(action, category, label, value) {
  gtag('event', action, {
    'event_category': category,
    'event_label': label,
    'value': value
  });
}

$("#feedback_show").click(function(e) {
  track_page('Feedback');
  $("#feedback_ctn").toggle();
});

$("#login").click(function(e) {
  model_post_login();
});

$("#logout").click(function(e) {
  model_post_logout('logout');
});

$("#delete").click(function(e) {
  model_post_logout('delete');
});

$("#register").click(function(e) {
  track_page('SignUp');
  $("#register_ctn").show();
  $('#login').hide();
  $('#logout').hide();
  $('#register').hide();
});

$("#register_confirm").click(function(e) {
  model_post_register();
});

$("#run").click(function(e) {
  run_clicked = true;
  track_page('Run');
  $("#run").hide();
  $("#upload_ctn").hide();
  view_get_target()
  model_put_target();
});

function model_get_file(){
  var p = {
    type: 'GET',
    url: "/user_file/" + user_id,
    dataType: "JSON",
    success: function(data) {
      console.log(data);
      set_upload();
      var txt = data == null ? "You have no file yet" : data.source_filename;
      $("#file").text(txt);
    }
  };
  $.ajax(p);
}

function set_upload() {
  var p = {
    url: '/upload/' + user_id,
    dataType: 'json',
    add: function (e, data) {
        // data.context = $('<p/>').text('uploading...').appendTo('#file');
        data.context = $('#file').text('uploading...');
        data.submit();
        track_page('Upload');
      },
    done: function (e, data) {
        console.log(data);
        var fname = data.result['name'];
        data.context.text(fname);
        model_get_target();
    },
    progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .progress-bar').css('width', progress + '%');
    }
  }
  $('#fileupload').fileupload(p)
    .prop('disabled', !$.support.fileInput)
    .parent().addClass($.support.fileInput ? undefined : 'disabled');
}

const index_type = 'ipt';

function view_put_target() {
  var e = $("#target")[0];
  var cln = e.children[0].cloneNode(true);
  e.innerHTML = null;
  var i = 1;
  var tl = target == null ? ['---x'] : target.target.split(',');
  for (var v in tl) {
    var varname = tl[v].slice(0, -1);
    var vartype = tl[v].slice(-1);
    cln.children[0].innerText = i;
    cln.children[1].innerText = varname;
    for (var j=2; j<=4; j++) {
      cln.children[j].children[0].name = 'radio' + i;
      cln.children[j].children[0].checked = index_type[j-2] == vartype;
      cln.children[j].children[0].id = varname + index_type[j-2];
    }
    e.appendChild(cln);
    cln = e.children[0].cloneNode(true);
    i++;
  }
}

function view_get_target() {
  var tl = [];
  var e = $("#target")[0];
  for (var i=0; i<e.children.length; i++) {
    var c = e.children[i];
    var v = c.children[1].innerText;
    if (v == '---') {
      target = null;
      return;
    }
    if (c.children[3].children[0].checked)
      tl[i] = v + 'p';
    else if (c.children[4].children[0].checked)
      tl[i] = v + 't';
    else
      tl[i] = v + 'i';
  }
  target = {'target': tl.join(',')}
}

function model_get_target(){
  var p = {
    type: 'GET',
    url: "/target/" + user_id,
    dataType: "JSON",
    success: function(data) {
      console.log(data);
      target = data;
      view_put_target();
      result = null;
      view_put_result();
    }
  };
  $.ajax(p);
}

function model_put_target() {
  var p = {
    type: 'PUT',
    url: "/target/" + user_id,
    dataType: "JSON",
    data: target,
    success: function(data) {
      console.log(data);
      model_post_job();
    }
  };
  $.ajax(p);
}

function model_post_job() {
  var p = {
    type: 'POST',
    url: "/job/" + user_id,
    dataType: "JSON",
    data: {},
    success: function(data) {
      console.log(data);
      result = data;
      view_put_result();
    }
  };
  $.ajax(p);
}

function view_put_result() {
  var status_count = {'ok': 0, 'error': 0, 'running': 0};
  for (var i in MODEL_LIST) {
    var m = MODEL_LIST[i];
    var v = '---';
    if (result != null) {
      var r = result[m];
      if (r != null) {
        v = r.value;
        status_count[r.status]++;
        if (r.status == 'error') {
          track_event('ml_error', 'error', v);
        }  
      }
    }
    $("#" + m)[0].innerText = v;
  }
  var running = status_count['running'] > 0;
  if (running) {
    $("#run").hide();
    $("#upload_ctn").hide();
    if (!timer)
      timer = setInterval(model_get_result, 5000);
  }
  else {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
    if (run_clicked) {
      track_page('Result');
      if (status_count['ok'] == 4)
        track_page('ResultOk');
      run_clicked = false;
    }
    $("#upload_ctn").show();
    if (target)
      $("#run").show();
  }
  if (result && result['score_desc'])
    $("#score_desc").text(result['score_desc'])
}

function model_get_result() {
  var p = {
    type: 'GET',
    url: "/result/" + user_id,
    dataType: "JSON",
    success: function(data) {
      console.log(data)
      result = data;
      view_put_result();
    }
  };
  $.ajax(p);
}

function myalert(msg) {
  $("#user_alert_text").text(msg);
  $(".alert").show();
  track_event('login_error', 'error', msg);
}

function check_login(email, password, first_name, last_name) {
  if (!email_regex.test(email)) {
    myalert('Invalid email');
    return false;
  }
  if (password.length < 8) {
    myalert('Password should be at least 8 characters');
    return false;
  }
  if (!first_name) {
    myalert('Please enter your first name');
    return false;
  }
  if (!last_name) {
    myalert('Please enter your last name');
    return false;
  }
  return true;
}

function model_post_login() {
  var email = $("#email_input")[0].value;
  var password = $("#password_input")[0].value;
  if (!check_login(email, password, 'not needed', 'not needed'))
    return;
  var p = {
    type: 'POST',
    url: "/login/" + email,
    dataType: "JSON",
    data: { 'email': email, 'password': password },
    success: function(data) { login_callback(data); }
  };
  $.ajax(p);
}

function model_post_logout(logout_option) {
  var p = {
    type: 'POST',
    url: "/logout/" + user_id,
    dataType: "JSON",
    data: { 'email': $("#email_input")[0].value, 'logout_option': logout_option },
    success: function(data) { logout_callback(data); }
  };
  $.ajax(p);
}

function model_post_register() {
  var email = $("#email_input")[0].value;
  var password = $("#password_input")[0].value;
  var first_name = $("#first_name_input")[0].value;
  var last_name = $("#last_name_input")[0].value;
  if (!check_login(email, password, first_name, last_name))
      return;
  var p = {
    type: 'POST',
    url: "/register/" + email, 
    dataType: "JSON",
    data: { 'email': email, 'password': password, 'first_name': first_name, 'last_name': last_name },
    success: function(data) { login_callback(data); }
  };
  $.ajax(p);
}

function login_callback(data) {
  console.log(data);
  if (data.auth) {
    track_page('Login');
    user_id = data.user_id;
    $('.alert').hide();
    $('#welcome').text(data.first_name);
    $("#login_ctn").hide();
    $("#register_ctn").hide();
    $("#login").hide();
    $("#logout").show();
    $("#delete").show();
    $("#register").hide();
    model_get_file();
    model_get_target();
    model_get_result();
  }
  else
    myalert(data.message)
}

function logout_callback(data) {
  console.log(data);
  if (data.logout) {
    if (data.logout_option == 'delete')
      track_page('Delete');
    track_page('Logout');
    // not smart but safer
    location.reload();
  }
}