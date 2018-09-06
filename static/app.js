function populateTarget(t) {
  console.log('xxx')
  var e = $("#target")[0];
  for (var i=1; i<e.children.length) {
    e.removeChild(e.childNodes[i]);
  }
  j = 1;
  for (var v in t) {
    console.log(v)
    if (j==1) {
      var cln = $("#targetline")[0];
      cln.children[1].innerText = v;
    }
    else {
      var cln = $("#targetline")[0].cloneNode(true);
      cln.children[0].innerText = j;
      cln.children[1].innerText = v;
      for (var i=2; i<=4; i++) {
        cln.children[i].children[0].name = 'radio' + j;
      }
      e.appendChild(cln);
    }
    j++;
  }
}
