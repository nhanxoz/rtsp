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
    var mo = today.getMonth();
    var y = today.getFullYear();
    document.getElementById('time').innerHTML = d + '/' + mo + '/' + y +'-'+ h + ":" + m + ":" + s;
    t = setTimeout(function() {
      startTime()
    }, 500);
  }
  startTime();