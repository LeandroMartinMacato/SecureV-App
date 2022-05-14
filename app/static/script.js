/* ------------------------- SLIDER TOGGLE DETECTION ------------------------ */

$(document).ready(function () {
    var toggler = $(".toggle-switch");

    toggler.click(function () {
      $(this).toggleClass("active");

      /* ------------------------------ Toggle effect ----------------------------- */
      $("#videoElement").toggleClass("videoBlur");
      $(".loadingio-spinner-double-ring-sfzcndobthj").toggleClass("show");

      $.getJSON("/request_model_switch", function (data) {
      });
  });
});



/* ------------------------------- DYNAMIC JS ------------------------------- */

let DynamicPlate = document.getElementById("dynamic_plate").innerText

$(function () {
  window.setInterval(function () {
    loadNewPlate();
    loadGateStatus();
  }, 1000);
  
  function loadNewPlate() {
    $.ajax({
      url: "/update_plate",
      type: "POST",
      dataType: "json",
      success: function (data) {
        let dynamic_data = JSON.stringify(data); 
        
        // console.log("plate ajax success");

        dynamic_data = dynamic_data.split(" | ");

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
        
        if (check_owner === "Not Verified"){
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

