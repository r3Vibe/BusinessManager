$(document).ready(function () {
  // update time form main script

  setInterval(() => {
    $.post("/gettime", { data: "gettime" }, function (res) {
      $("#uptime").html("Time: " + res);
    });
  }, 1000);

  //################  bootstrap form validation  ################//
  // Example starter JavaScript for disabling form submissions if there are invalid fields
  (function () {
    "use strict";

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll(".needs-validation");

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function (form) {
      form.addEventListener(
        "submit",
        function (event) {
          if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
          }

          form.classList.add("was-validated");
        },
        false
      );
    });
  })();
});
