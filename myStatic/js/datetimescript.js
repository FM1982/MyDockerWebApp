const monthnames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December'];

const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

function  startTime() {
    //let lbrk = "<br>";
    let today = new Date();
    let d = today.getDate();
    let wd = weekdays[today.getDay() - 1];
    let mo = monthnames[today.getMonth()];
    let y = today.getFullYear();
    let h = today.getHours();
    let m = today.getMinutes();
    let s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('date').innerHTML = "Current Date: " + wd + " the " + d + " " + mo + " of " + y;
    //"Current Date: " + wd + " the " + d + " " + mo + " of " + y + lbrk + " Current Time: " + h + ":" + m + ":" + s;
    document.getElementById('time').innerHTML = "Current Time: " + h + ":" + m + ":" + s;
    //"Current Date: " + wd + " the " + d + " " + mo + " of " + y + " Current Time: " + h + ":" + m + ":" + s;
    let t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}