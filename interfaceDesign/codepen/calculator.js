var display = document.getElementById("display");

document.onload = main();

function main() {
  for (var i=0; i<10; i++) {
    var button = document.getElementById("button-" + i);
    if (button != null) {
      button.onclick = function(e) {
        display.innerHTML = display.innerHTML + e.target.id.substring(7);
      }
    }
  }
  
}
