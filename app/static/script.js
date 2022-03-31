/* ---------------------------- TOGGLE DETECTION ---------------------------- */

$(function () {
  // Model switch
  $("a#use-model").bind("click", function () {
    $.getJSON("/request_model_switch", function (data) {
      // do nothing
    });
    return false;
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
        // console.log("plate ajax success");
        // console.log(data);
        document.getElementById("dynamic_plate").innerText = data[1];
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
        // console.log(data);
        // document.getElementById("gate-status").innerText = data[1];

        DynamicPlate = document.getElementById("dynamic_plate").innerText
        DynamicPlate = DynamicPlate.split("| ")[1]
        // console.log(DynamicPlate); //DEBUG: Check DynamicPlate element val

        if (DynamicPlate === "No owner found"){
          document.getElementById("gate-status").innerText = "Gate Status: Closed";
          document.getElementById("gate-status").style.color = "red"
        }
        else{
          document.getElementById("gate-status").innerText = "Gate Status: Open";
          document.getElementById("gate-status").style.color = "green"
        }


      },
    });
  }

});