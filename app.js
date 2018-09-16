
"use strict";
var user_id = null;
var job = null;
var target = null;
var result = null;
var timer = null;
var returnmessage = {null:'Running', 0:'Success', 1:'Error'}

function index_checked(usage) {
  if (usage == 'predictor') return 3;
  if (usage == 'target') return 4;
  if (usage == 'ignored') return 2;
  return -1;
}

function view_put_target() {
  var e = $("#target")[0];
  var cln = e.children[0].cloneNode(true);
  e.innerHTML = null;
  var j = 1;
  var t = target == null ? {'---': '---'} : target;
  for (var v in target) {
    cln.children[0].innerText = j;
    cln.children[1].innerText = v;
    var i_checked = index_checked(target[v]);
    for (var i=2; i<=4; i++) {
      cln.children[i].children[0].name = 'radio' + j;
      cln.children[i].children[0].checked = i==i_checked;
    }
    e.appendChild(cln);
    cln = e.children[0].cloneNode(true);
    j++;
  }
  document.getElementById("run").disabled = false;
}

function view_get_target() {
  target = {};
  var e = $("#target")[0];
  for (var i=0; i<e.children.length; i++) {
    var c = e.children[i];
    var v = c.children[1].innerText;
    if (v == '---') {
      target = null;
      return;
    }
    if (c.children[3].children[0].checked)
      target[v] = 'predictor';
    else if (c.children[4].children[0].checked)
      target[v] = 'target';
    else
      target[v] = "ignored";
  }
}

function view_put_result() {
  var e = $("#result")[0];
  var cln = e.children[0].cloneNode(true);
  e.innerHTML = null;
  var j = 1;
  var r = result == null ? {'---': '---'} : result;
  for (var m in r) {
    cln.children[0].innerText = j;
    cln.children[1].innerText = m;
    cln.children[2].innerText = r[m];
    e.appendChild(cln);
    cln = e.children[0].cloneNode(true);
    j++;
  }
}

function view_put_job() {
  console.log(job);
  if (job == null)
    $("#job")[0].innerText = '---';
  else if (job.error)
    $("#job")[0].innerText = job.error;
  else
    $("#job")[0].innerText = returnmessage[job.returncode];
}

function model_put_job() {
  var p = {
    type: 'PUT',
    url: "/job/" + user_id,
    dataType: "JSON",
    data: job,
    success: function(data) {
      job = data;
      view_put_job();
    }
  };
  $.ajax(p);
}

function model_get_job() {
  var p = {
    type: 'GET',
    url: "/job/" + user_id,
    dataType: "JSON",
    success: function(data) {
      console.log(data)
      job = data;
      view_put_job();
      if (job.returncode == 0) {
        console.log('job OK')
        model_get_result();
        clearInterval(timer);
      }
      else if (job.returncode > 0) {
        console.log('job error')
        model_get_result();
        clearInterval(timer);
      }
    }
  };
  $.ajax(p);
}

function login_callback(data) {
  console.log(data);
  if (data.auth) {
    user_id = data.user_id;
    $("#login").prop('disabled', true);
    $("#register").prop('disabled', true);
    $("#inputEmail4").prop('disabled', true);
    $("#logout").prop('disabled', false);
    $("#password-block").hide()
    model_get_file();
  }
  else
    alert(data.message)
}

function logout_callback(data) {
  console.log(data);
  if (data.logout) {
    user_id = null;
    set_upload();
    $("#login").prop('disabled', false);
    $("#register").prop('disabled', false);
    $("#inputEmail4").prop('disabled', false);
    $("#logout").prop('disabled', true);
    $("#password-block").show()
  }
}

function model_post_register(){
  var p = {
    type: 'POST',
    url: "/register",
    dataType: "JSON",
    data: {
      'email': $("#inputEmail4")[0].value,
      'password': $("#inputPassword4")[0].value
    },
    success: function(data) {
      login_callback(data);
    }
  };
  // console.log(p);
  $.ajax(p);
}

function model_post_login(){
  var p = {
    type: 'POST',
    url: "/login",
    dataType: "JSON",
    data: {
      'email': $("#inputEmail4")[0].value,
      'password': $("#inputPassword4")[0].value
    },
    success: function(data) {
      login_callback(data);
    }
  };
  // console.log(p);
  $.ajax(p);
}

function model_post_logout(){
  var p = {
    type: 'POST',
    url: "/logout",
    dataType: "JSON",
    data: {
      'email': $("#inputEmail4")[0].value
    },
    success: function(data) {
      logout_callback(data);
    }
  };
  // console.log(p);
  $.ajax(p);
}

function model_get_file(){
  var p = {
    type: 'GET',
    url: "/user_file/" + user_id,
    dataType: "JSON",
    success: function(data) {
      console.log(data);
      set_upload();
      if (data == null)
        $("#file").text("you have no file yet");
      else {
        $("#file").text(data.filename);
        model_get_target()
      }
    }
  };
  $.ajax(p);
}

function model_get_target(){
  var p = {
    type: 'GET',
    url: "/target/" + user_id,
    dataType: "JSON",
    success: function(data) {
      console.log(data);
      target = data;
      job = null;
      result = null;
      view_put_job();
      view_put_result();
      view_put_target();
    }
  };
  $.ajax(p);
}

function model_put_target() {
  console.log(target);
  var p = {
    type: 'PUT',
    url: "/target/" + user_id,
    dataType: "JSON",
    data: target,
    success: function(data) {
      console.log(data);
      job = {'control': 'start'};
      // result = null;
      view_put_job();
      // view_put_result();
      model_put_job();
      timer = setInterval(model_get_job, 4000);
    }
  };
  $.ajax(p);
}

function model_get_result(){
  var p = {
    type: 'GET',
    url: "/result/" + user_id,
    dataType: "JSON",
    success: function(data) {
      result = data;
      view_put_result();
    }
  };
  $.ajax(p);
}

function set_upload() {
  console.log(user_id);
  $('#fileupload').fileupload({
      url: '/upload/' + user_id,
      dataType: 'json',
      add: function (e, data) {
          // data.context = $('<p/>').text('uploading...').appendTo('#file');
          data.context = $('#file').text('uploading...');
          data.submit();
      },
      done: function (e, data) {
          var fname = data.result['name'];
          data.context.text(fname);
          model_get_target();
      },
      progressall: function (e, data) {
          var progress = parseInt(data.loaded / data.total * 100, 10);
          $('#progress .progress-bar').css('width', progress + '%');
      }
  }).prop('disabled', !$.support.fileInput)
      .parent().addClass($.support.fileInput ? undefined : 'disabled');
}
$("#login").click(function(e) {
  model_post_login();
});
$("#register").click(function(e) {
  model_post_register();
});
$("#logout").click(function(e) {
  model_post_logout();
});
$("#get_target").click(function(e) {
  model_get_target();
});
$("#run").click(function(e) {
  job = null;
  result = null;
  view_put_job();
  view_put_result();
  view_get_target()
  model_put_target();
});
