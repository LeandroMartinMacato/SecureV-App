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
let is_verified = false;
let futureDate = new Date(new Date().getTime() - 1000000); 
let minutestoadd = 1;
let current_plate = "";


$(function () {
  window.setInterval(function () {
    loadNewPlate();
    loadGateStatus();
  }, 500);
  
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

        current_plate = dynamic_data[0];
      },
    });
  }
  
  function loadGateStatus() {
    $.ajax({
      url: "/update_gate",
      type: "POST",
      dataType: "json",
      success: function (data) {
        let current_time = new Date();
        let info_container_element = document.getElementById("flex-item-2");
        let toast_plate = document.getElementById("toast_plate");
        let toast_date = document.getElementById("toast_date");


        check_owner = document.getElementById("dynamic_owner").innerText
        
        if (check_owner !== "Not Verified" && check_owner !== ""){
          document.getElementById("gate-status-container").innerText = "Gate Status: Open";
          document.getElementById("gate-status-container").style.color = "green";
          info_container_element.style.border = "6px solid #77e189";
          info_container_element.style.borderRadius = "15px";
          is_verified = true;
        }
        else{
          document.getElementById("gate-status-container").innerText = "Gate Status: Closed";
          document.getElementById("gate-status-container").style.color = "#9e1c13"
          info_container_element.style.border = "6px solid #4d1210";
          info_container_element.style.borderRadius = "15px";
          is_verified = false;
        }

        
        if (is_verified){
          if (current_time >= futureDate){
            futureDate = new Date(current_time.getTime() + minutestoadd * 60000);
            create_notif_toast()
            toast_plate.innerText = current_plate 
            toast_date.innerText = current_time

          }
          else{
            console.log("At cooldown")
          }
        }
      },
    });
  }

	function create_notif_toast()
	{
		console.log("PRESSED BUTTON")
    var option = 
    {
      animation : true,
      delay : 10000
    };

		var toastHTMLElement = document.getElementById( 'EpicToast' );
		
		var toastElement = new bootstrap.Toast( toastHTMLElement, option );
		
		toastElement.show( );
	}
  
});

