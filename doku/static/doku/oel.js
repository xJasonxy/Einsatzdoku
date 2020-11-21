function showInfo(infoId) {
    var info = document.getElementById(infoId);
        info.style.display = "block";
}

$(".Einsatzstellen-Info-Wrapper").click(function(event){
    event.stopPropagation();
    this.style.display = "none";
});
$(".Einsatzstellen-Info-Wrapper").children().click(function(event){
    event.stopPropagation();
});

$('textarea').each(function () {
  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});
