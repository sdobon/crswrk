var display = document.getElementById("display");
var pre_display = "0";
var contains_dec = false;

document.onload = main();

function main() {
  //display = null;
  for (var i=0; i<10; i++) {
    var button = document.getElementById("button-" + i);
    if (button != null) {
      button.onclick = function(b) {
        handle_press(b.target.id.substring(7));
      }
    }
  }
  var clear = document.getElementById("button-clear");
  clear.onclick = function(b) {
    handle_press(b.target.id.substring(7));
  }

  var decimal = document.getElementById("button-decimal");
  decimal.onclick = function(b) {
    handle_press(b.target.id.substring(7));
  }

  var plusmn = document.getElementById("button-plusmn")
  plusmn.onclick = function(b) {
    handle_press(b.target.id.substring(7));
  }


}

function handle_press(b) {
  if (b == "clear") {
    pre_display = "0";
    contains_dec = false;
  }

  else if (pre_display == "0" & b != "plusmn") {
    if (b == "decimal" & contains_dec == false) {
      pre_display = pre_display + ".";
      contains_dec = true;
    }
    else {
      pre_display = b;
    }
  }

  else if (b == "plusmn") {
    if (pre_display != "0" & pre_display != "0.") {
      if (pre_display[0] == "-") {
        pre_display = pre_display.substring(1);
      }
      else {
        pre_display = "-" + pre_display;
      }
    }
  }

  else {
    if (b == "decimal" & contains_dec == false) {
      pre_display = pre_display + ".";
      contains_dec = true;
    }

    else if (b != "decimal") {
      pre_display = pre_display + b;
    }
  }


  display.innerHTML = pre_display;
  //alert(b);
}


//display.innerHTML =
