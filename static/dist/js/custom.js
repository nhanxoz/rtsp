function checkTime(i) {
  if (i < 10) {
    i = "0" + i;
  }
  return i;
}

function startTime() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  var d = today.getDate();
  // add a zero in front of numbers<10
  m = checkTime(m);
  s = checkTime(s);
  d = checkTime(d);
  var mo = today.getMonth() + 1;
  var y = today.getFullYear();
  document.getElementsByClassName('time').innerHTML = d + '/' + mo + '/' + y + ' - ' + h + ":" + m + ":" + s;
  t = setTimeout(function () {
    startTime()
  }, 500);
}
startTime();
function code_html(i){
  return  `<div class="card-noti-parent">
  <div class="card-noti">
      <div class="card-info">
          <div class="time-lapse">` + i.time+`</div>
          <div class="object-name">`+i.person_name+`</div>
          <div class="combo-1">
              <div class="score">`+i.score+`</div>
              <div class="cam-location">`+i.cam+` - `+i.location+`</div>
          </div>
      </div>
      <div class="card-image"><img src="./static/image/jisoo.png" alt="" /></div>

  </div>
</div>`
}
function addNoti() {
  
  const parse = Range.prototype.createContextualFragment.bind(document.createRange());
  fetch('/noti-5-secs')
    .then((response) => response.json())
    .then((data) => data.notification.map(i => document.getElementById('cam-list').prepend(parse(code_html(i)))));
  t = setTimeout(function () {
    addNoti()
  }, 3000)
}
addNoti()