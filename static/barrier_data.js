console.log(`IP Address: ${ipAddress}`);
console.log(`Portiii: ${portep}`);

const open_cmd = "55 03 01 01 00 B8 B4";
const close_cmd = "55 03 01 02 00 ED E7";
const lock_cmd = "55 03 01 01 01 A8 95";
const unlock_cmd = "55 03 01 01 02 98 F6";

fetch(`http://${ipAddress}:${portep}/Barrier`)
  .then((response) => response.json())
  .then((data) => {
    console.log(data); 

    const barriers = data.barriers; 
    const barriersTable = document.getElementById("barriersTable");

    if (barriers.length === 0) {
      // Display message if no barriers are found
      const noDataMessageRow = document.createElement("tr");
      const noDataMessageCell = document.createElement("td");
      const span = document.createElement("span");
      span.textContent = "No barrier found";
      span.classList.add("text-dark", "fw-bold", "text-hover-primary", "d-block", "mb-1", "fs-6");
      noDataMessageCell.appendChild(span);
      noDataMessageCell.colSpan = 10; 
      noDataMessageCell.style.textAlign = "center";
      noDataMessageRow.appendChild(noDataMessageCell);
      barriersTable.appendChild(noDataMessageRow);
    } else {
    
      barriers.forEach((barrier) => {
        const newRow = document.createElement("tr");

        newRow.appendChild(createCell(barrier.id, true));
        newRow.appendChild(createCell(barrier.name, true));
        
        if(barrier.barrierType == "entry")
        {
          newRow.appendChild(createCell("Entry", true));
        }
        if(barrier.barrierType == "exit")
        {
          newRow.appendChild(createCell("Exit", true));
        }
        newRow.appendChild(createCell(barrier.ip, true));
        newRow.appendChild(createCell(barrier.port, true));
        newRow.appendChild(createCell(open_cmd, true)); 
        newRow.appendChild(createCell(close_cmd, true));
        newRow.appendChild(createCell(lock_cmd, true)); 
        newRow.appendChild(createCell(unlock_cmd, true));

        newRow.appendChild(createActionCell(barrier.id));

        barriersTable.appendChild(newRow);
      });
    }
  })
  .catch((error) => console.error("Error fetching data:", error));

function createCell(content, addTextClasses) {
  const cell = document.createElement("td");
  if (addTextClasses) {
    const span = document.createElement("span");
    span.classList.add("text-dark", "fw-bold", "text-hover-primary", "d-block", "mb-1", "fs-6");
    span.textContent = content;
    cell.appendChild(span);
  } else {
    cell.textContent = content;
  }
  return cell;
}

function createActionCell(barrierId) {
  const cell = document.createElement("td");

  const modifyButton = document.createElement("button");
  modifyButton.classList.add("btn", "btn-sm", "fw-bold", "btn-primary");
  modifyButton.innerHTML = `
    <i class="ki-duotone ki-pencil fs-2">
      <span class="path1"></span>
      <span class="path2"></span>
    </i>
  `;
  modifyButton.addEventListener("click", function () {
    modifyBarriers(barrierId);
  });
  cell.appendChild(modifyButton);

  cell.appendChild(document.createTextNode("\u00A0"));

  const deleteButton = document.createElement("button");
  deleteButton.classList.add("btn", "btn-sm", "fw-bold", "btn-danger");
  deleteButton.innerHTML = `
    <i class="ki-duotone ki-trash fs-2">
      <span class="path1"></span>
      <span class="path2"></span>
      <span class="path3"></span>
      <span class="path4"></span>
      <span class="path5"></span>
    </i>
  `;
  deleteButton.addEventListener("click", function () {
    deleteBarrier(barrierId);
  });
  cell.appendChild(deleteButton);

  return cell;
}

function deleteBarrier(barrierId) {
  Swal.fire({
    text: "Are you sure you want to delete?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "No, cancel",
    buttonsStyling: false,
    customClass: {
      confirmButton: "btn btn-danger",
      cancelButton: "btn btn-secondary",
    },
  }).then((result) => {
    if (result.isConfirmed) {
      fetch(`http://${ipAddress}:${portep}/delete/${barrierId}`, {
        method: "DELETE",
      })
        .then((response) => {
          if (response.ok) {
            Swal.fire({
              text: "Deleted Successfully",
              icon: "success",
              buttonsStyling: false,
              showConfirmButton: false,
              timer: 1500,
            }).then(() => {
              KTUtil.scrollTop();
                location.reload();

            });
          } else {
            Swal.fire({
              text: " Error",
              icon: "error",
              buttonsStyling: false,
              confirmButtonText: "Ok, got it!",
              customClass: { confirmButton: "btn btn-dark" },
            }).then(() => {
              KTUtil.scrollTop();
            });
          }
        })
        .catch((error) =>
          console.error(`Error deleting barrier with id ${barrierId}:`, error)
        );
    }
  });
}

function modifyBarriers(barrierId) {
  fetch(`http://${ipAddress}:${portep}/Barrier/${barrierId}`)
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to fetch barrier data");
      }
    })
    .then((data) => {
      const modifyNameInput = document.getElementById("name_modify");
      const modifyIdInput = document.getElementById("id_modify");
      const modifyTypeInput = document.getElementById("type_modify");
      const modifyIpInput = document.getElementById("ip_modify");
      const modifyPortInput = document.getElementById("port_modify");
      const modifyOpenCodeInput = document.getElementById("open_modify");
      const modifyCloseCodeInput = document.getElementById("close_modify");
      const modifyLockCodeInput = document.getElementById("lock_modify");
      const modifyUnlockCodeInput = document.getElementById("unlock_modify");

      if (
        !modifyIdInput ||
        !modifyNameInput ||
        !modifyTypeInput ||
        !modifyIpInput ||
        !modifyPortInput ||
        !modifyOpenCodeInput ||
        !modifyCloseCodeInput ||
        !modifyLockCodeInput ||
        !modifyUnlockCodeInput
      ) {
        return;
      }




      modifyNameInput.value = data.name || "";
      modifyIdInput.value = data.id || "";
      modifyTypeInput.value = data.type || "";
      modifyIpInput.value = data.ip || "";
      modifyPortInput.value = data.port || "";
      
      modifyOpenCodeInput.value = open_cmd;
      modifyCloseCodeInput.value = close_cmd;
      modifyLockCodeInput.value = lock_cmd;
      modifyUnlockCodeInput.value = unlock_cmd;

      console.log(modifyCloseCodeInput.value);

      const modifyModal = new bootstrap.Modal(
        document.getElementById("kt_modal_modify")
      );
      modifyModal.show();
    })

    .catch((error) => {
      Swal.fire({
        icon: "error",
        title: "Failed !",
        showConfirmButton: false,
        timer: 1500,
      });
    });

  document.getElementById("modify").addEventListener("click", function (event) {
    event.preventDefault();

    const name = document.getElementById("name_modify").value;
    const type = document.getElementById("type_modify").value;
    const id = document.getElementById("id_modify").value;
    const ip = document.getElementById("ip_modify").value;
    const port = document.getElementById("port_modify").value;
    const opCmd = document.getElementById("open_modify").value;
    const clCmd = document.getElementById("close_modify").value;
    const lkCmd = document.getElementById("lock_modify").value;
    const ukCmd = document.getElementById("unlock_modify").value;

    const requestBody = {
      name: name,
      id: id,
      type: type,
      ip: ip,
      port: port,
      op_cmd: opCmd,
      cl_cmd: clCmd,
      lk_cmd: lkCmd,
      uk_cmd: ukCmd,
    };

    fetch(`http://${ipAddress}:${portep}/modify/${barrierId}`, 
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => {
        if (response.ok) {
          Swal.fire({
            icon: "success",
            title: "Barrier Modified Successfully",
            showConfirmButton: false,
            timer: 1500,
          }).then(function () {
            KTUtil.scrollTop();
           location.reload();

          });
        } else {
          throw new Error("Failed to modify barrier data");
          Swal.fire({
            icon: "error",
            title: "Failed to modify barrier data",
            showConfirmButton: false,
            timer: 1500,
          });
        }
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "Failed",
          test: "Try again !",
          showConfirmButton: false,
          timer: 1500,
        });
      });

    const modifyModal = new bootstrap.Modal(
      document.getElementById("kt_modal_modify")
    );
    modifyModal.hide();
  });
}
