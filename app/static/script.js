/* ------------------------- SLIDER TOGGLE DETECTION ------------------------ */

$(document).ready(function () {
    var toggler = $(".toggle-switch");

    toggler.click(function () {
        $(this).toggleClass("active");
        // $("#videoElement").css("filter" , "blur(2px)"); //Apply blur
        $.getJSON("/request_model_switch", function (data) {
      });
      console.log("TEST ON PRESS TOGGLE")
      // $("#test").hide();
  });
});


/* ------------------------------- DYNAMIC JS ------------------------------- */

let DynamicPlate = document.getElementById("dynamic_plate").innerText

$(function () {
  window.setInterval(function () {
    loadNewPlate();
    loadGateStatus();
  }, 3000);
  
  function loadNewPlate() {
    $.ajax({
      url: "/update_plate",
      type: "POST",
      dataType: "json",
      success: function (data) {
        let dynamic_data = JSON.stringify(data); 
        
        // console.log("plate ajax success");

        dynamic_data = dynamic_data.split(" | ");
        console.log(dynamic_data);

        // Manipulate String
        dynamic_data[0] = dynamic_data[0].substring(5);
        dynamic_data[1] = dynamic_data[1].slice(0 , -2);

        // Change frontend
        document.getElementById("dynamic_plate").innerText = dynamic_data[0];
        document.getElementById("dynamic_owner").innerText =  dynamic_data[1];
      },
    });
  }
  
  function loadGateStatus() {
    $.ajax({
      url: "/update_gate",
      type: "POST",
      dataType: "json",
      success: function (data) {
        // console.log("--gate ajax function--");
        
        check_owner = document.getElementById("dynamic_owner").innerText
        
        if (check_owner === "No owner found"){
          document.getElementById("gate-status-container").innerText = "Gate Status: Closed";
          document.getElementById("gate-status-container").style.color = "red"
        }
        else{
          document.getElementById("gate-status-container").innerText = "Gate Status: Open";
          document.getElementById("gate-status-container").style.color = "green"
        }
        
      },
    });
  }
  
});


/* ---------------------------- BUTTON TOGGLE DETECTION ---------------------------- */

// $(function () {
//   // Model switch
//   $("a#use-model").bind("click", function () {
//     $.getJSON("/request_model_switch", function (data) {
//       // do nothing
//     });
//     return false;
//   });
// });