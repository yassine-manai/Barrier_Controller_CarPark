"use strict";

var KTCreateApp = (function () {
  var stepper, form, validator;

  var initStepper = function () {
    stepper = new KTStepper(document.getElementById("kt_modal_create_app_stepper"));
    form = document.getElementById("kt_modal_create_app_form");
    validator = FormValidation.formValidation(form, {
      fields: {
        name: {
          validators: {
            notEmpty: {
              message: "Barrier Name is required"
            }
          }
        },
        id: {
          validators: {
            notEmpty: {
              message: "Lane ID is required"
            },
            numeric: {
              message: "Lane ID must be a number"
            }
          }
        },
        ip: {
          validators: {
            notEmpty: {
              message: "Barrier IP is required"
            },
            numeric: {
              message: "Barrier IP must be a number"
            }
          }
        },
        port: {
          validators: {
            notEmpty: {
              message: "Barrier Port is required"
            },
            numeric: {
              message: "Barrier Port must be a number"
            }
          }
        },
        open: {
          validators: {
            notEmpty: {
              message: "Barrier Open Code is required"
            }
          }
        },
        close: {
          validators: {
            notEmpty: {
              message: "Barrier Close Code is required"
            }
          }
        },
        lock: {
          validators: {
            notEmpty: {
              message: "Barrier Lock Code is required"
            }
          }
        },
        unlock: {
          validators: {
            notEmpty: {
              message: "Barrier Unlock Code is required"
            }
          }
        }
      },
    
      plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap: new FormValidation.plugins.Bootstrap5({
          rowSelector: ".fv-row",
          eleInvalidClass: "",
          eleValidClass: "",
        }),
      },
    });
  };

  var initEventListeners = function () {
    document.getElementById("add").addEventListener("click", function () {
      var dropdown = document.getElementById("barrierType");
      var selectedBarrierType = dropdown.value;

      console.log("Selected Barrier Type:", selectedBarrierType);

      validator.validate().then(function (status) {
        if (status === "Valid") {
          var name = document.getElementById("name").value;
          var id = document.getElementById("id").value;
          var barrierType = dropdown.value;
          var ip = document.getElementById("ip").value;
          var port = document.getElementById("port").value;
          var op_cmd = document.getElementById("open").value;
          var cl_cmd = document.getElementById("close").value;
          var lk_cmd = document.getElementById("lock").value;
          var uk_cmd = document.getElementById("unlock").value;

          var formData = {
            name: name,
            id: id,
            barrierType:barrierType,
            ip: ip,
            port: port,
            op_cmd: op_cmd,
            cl_cmd: cl_cmd,
            lk_cmd: lk_cmd,
            uk_cmd: uk_cmd,
          };

          fetch(`http://${ipAddress}:${portep}/add`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
          })
          .then(response => {
            if (response.status === 400) {
              throw new Error('Barrier with the same ID already exists');
            } else if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            Swal.fire({
              icon: 'success',
              title: 'Barrier Added Successfully',
              showConfirmButton: false,
              timer: 1500
            }).then(function () {
              KTUtil.scrollTop();
              setTimeout(function () {
                location.reload();
              }, 300);
            });
          })
          .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            Swal.fire({
              title: error.message || "Error!",
              text: "Please try again",
              icon: "error",
              buttonsStyling: false,
              showConfirmButton: false,
              timer: 1500
            })
          });
        } else {
          Swal.fire({
            text: "Sorry, looks like there are some errors detected, please fill all the fields.",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: { confirmButton: "btn btn-dark" },
          }).then(function () {
            KTUtil.scrollTop();
          });
        }
      });
    });
  };

  return {
    init: function () {
      initStepper();
      initEventListeners();
    }
  };
})();

KTUtil.onDOMContentLoaded(function () {
  KTCreateApp.init();
});
