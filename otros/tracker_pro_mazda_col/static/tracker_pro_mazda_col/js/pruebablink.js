$(document).ready(function blinker() {
 
    $("#active").fadeOut('slow');
    $("#active").fadeIn('slow');
    setInterval(blinker() ,2000);
    
});
