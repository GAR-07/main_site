var theme = document.getElementById("theme-link");
var btn = document.getElementById("theme-button");
let darkTheme = "static/styles/dark.css";
let lightTheme = "static/styles/light.css";

if(localStorage.getItem('theme') === 'dark') {
    theme.href = darkTheme;
}

document.body.onload = function() {
    setTimeout(function() {
        var preloader = document.getElementById('page-preloader');
        if (!preloader.classList.contains('done')) {
            preloader.classList.add('done');
        }
    }, 1);
}

btn.onclick = function () {
    if(localStorage.getItem('theme') === 'dark') {
        localStorage.removeItem('theme');
   	    theme.href = lightTheme;
    }
    else {    
        localStorage.setItem('theme', 'dark')
   	    theme.href = darkTheme;
    }
}