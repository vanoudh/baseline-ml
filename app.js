
"use strict";

var user_id = null;
var target = null;
var result = null;
var timer = null;

var email_regex = new RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i);

$("#feedback_ctn").hide();
$(".alert").hide();
$("#register_ctn").hide();
$("#logout").hide();
$("#upload_ctn").hide();
$("#run").hide();

$("#feedback_show").click(function(e) {
  gtag('event', 'screen_view', {'screen_name': 'feedback'});
  $("#feedback_ctn").toggle();
});

$("#login").click(function(e) {
  gtag('event', 'login', {'method': 'email'});
  model_post_login();
});

$("#logout").click(function(e) {
  gtag('event', 'logout');
  model_post_logout();
});

$("#register").click(function(e) {
  $("#register_ctn").show();
  $('#login').hide();
  $('#logout').hide();
  $('#register').hide();
});

$("#register_confirm").click(function(e) {
  gtag('event', 'sign_up', {'method': 'email'});
  model_post_register();
});

$("#run").click(function(e) {
  gtag('event', 'run');
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
      if (data == null)
        $("#file").text("You have no file yet");
      else {
        $("#file").text(data.source_filename);
      }
    }
  };
  $.ajax(p);
}

function set_upload() {
  // console.log(user_id);
  $('#fileupload').fileupload({
      url: '/upload/' + user_id,
      dataType: 'json',
      add: function (e, data) {
          // data.context = $('<p/>').text('uploading...').appendTo('#file');
          data.context = $('#file').text('uploading...');
          data.submit();
          gtag('event', 'upload');
        },
      done: function (e, data) {
          console.log(data);
          var fname = data.result['name'];
          data.context.text(fname);
          result = null;
          view_put_result();
          model_get_target();
      },
      progressall: function (e, data) {
          var progress = parseInt(data.loaded / data.total * 100, 10);
          $('#progress .progress-bar').css('width', progress + '%');
      }
  }).prop('disabled', !$.support.fileInput)
      .parent().addClass($.support.fileInput ? undefined : 'disabled');
}

function index_checked(usage) {
  if (usage == 'p') return 3;
  if (usage == 't') return 4;
  if (usage == 'i') return 2;
  return -1;
}

function view_put_target() {
  // console.log(target)
  var e = $("#target")[0];
  var cln = e.children[0].cloneNode(true);
  e.innerHTML = null;
  var j = 1;
  var tl = target == null ? ['---x'] : target.target.split(',');
  for (var v in tl) {
    cln.children[0].innerText = j;
    cln.children[1].innerText = tl[v].slice(0, -1);
    var i_checked = index_checked(tl[v].slice(-1));
    for (var i=2; i<=4; i++) {
      cln.children[i].children[0].name = 'radio' + j;
      cln.children[i].children[0].checked = i==i_checked;
    }
    e.appendChild(cln);
    cln = e.children[0].cloneNode(true);
    j++;
  }
  if (target)
    if (result)
      if (result.done)
        $("#run").show();
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
    }
  };
  $.ajax(p);
}

function model_put_target() {
  // console.log(target);
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
      timer = setInterval(model_get_result, 5000);
    }
  };
  $.ajax(p);
}

function view_put_result() {
  var r = result == null ? {'zero': '---', 'linear': '---', 'tree': '---', 'forest': '---', } : result;
  for (var m in r)
    if (m != 'done')
      $("#" + m)[0].innerText = r[m];
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
      if (result.done) {
        clearInterval(timer);
        $("#upload_ctn").show();
        if (target)
          $("#run").show();
      }
    }
  };
  $.ajax(p);
}

function myalert(msg) {
  $("#user_alert_text").text(msg);
  $(".alert").show();
}

function check_email_password(email, password) {
  if (!email_regex.test(email)) {
    myalert('Invalid email');
    return false;
  }
  if (password.length < 8) {
    myalert('Password is too short');
    return false;
  }
  return true;
}

function model_post_login() {
  var email = $("#email_input")[0].value;
  var password = $("#password_input")[0].value;
  if (!check_email_password(email, password))
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

function model_post_logout() {
  var p = {
    type: 'POST',
    url: "/logout/" + user_id,
    dataType: "JSON",
    data: { 'email': $("#email_input")[0].value },
    success: function(data) { logout_callback(data); }
  };
  $.ajax(p);
}

function model_post_register() {
  var email = $("#email_input")[0].value;
  var password = $("#password_input")[0].value;
  var company = $("#company_input")[0].value;
  var job_title = $("#job_title_input")[0].value;
  if (!check_email_password(email, password))
      return;
  var p = {
    type: 'POST',
    url: "/register/" + email, 
    dataType: "JSON",
    data: { 'email': email, 'password': password, 'company': company, 'job_title': job_title },
    success: function(data) { login_callback(data); }
  };
  $.ajax(p);
}

function login_callback(data) {
  console.log(data);
  if (data.auth) {
    user_id = data.user_id;
    $("#email_input").prop('disabled', true);
    $("#password_ctn").hide();
    $("#register_ctn").hide();
    $("#login").hide();
    $("#logout").show();
    $("#register").hide();
    model_get_file();
    model_get_target();
    model_get_result();
    timer = setInterval(model_get_result, 5000);
  }
  else
    myalert(data.message)
}

function logout_callback(data) {
  console.log(data);
  if (data.logout) {
    // not smart but safer
    location.reload();
  }
}