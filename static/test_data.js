"use strict";

console.log(`IP Address: ${ipAddress}`);
console.log(`Port: ${portep}`);

// Fetch data from the barrier endpoint and populate the table
async function fetchDataAndPopulateTable() {
    try {
        const response = await fetch(`http://${ipAddress}:${portep}/Barrier`);
        const data = await response.json();
        const barriersTable = document.getElementById("barriersTable");

        if (data && data.barriers && data.barriers.length > 0) {
            data.barriers.forEach(barrier => {
                const newRow = document.createElement("tr");

                // Hardcoded commands
                const open_cmd = "55 03 01 01 00 B8 B4";
                const close_cmd = "55 03 01 02 00 ED E7";
                const lock_cmd = "55 03 01 01 01 A8 95";
                const unlock_cmd = "55 03 01 01 02 98 F6";

                // Create cells for barrier properties and commands
                newRow.appendChild(createCell(barrier.id, true));
                newRow.appendChild(createCell(barrier.ip, true));
                newRow.appendChild(createCell(barrier.port, true));
    

                newRow.appendChild(createCell(open_cmd, true));
                newRow.appendChild(createCell(close_cmd, true));
                newRow.appendChild(createCell(lock_cmd, true));
                newRow.appendChild(createCell(unlock_cmd, true));

                console.log(barrier)


                // Create input field for extra data
                const inputCell = document.createElement("td");
                const input = document.createElement("input");
                input.type = "text";
                input.placeholder = "Enter extra data";
                input.classList.add("form-control", "form-control-solid", "w-150px");
                inputCell.appendChild(input);
                newRow.appendChild(inputCell);

                // Create action cell with buttons for each barrier
                newRow.appendChild(createActionCell(barrier.id, open_cmd, close_cmd, lock_cmd, unlock_cmd, input));

                // Append the new row to the table
                barriersTable.appendChild(newRow);
            });
        } else {
            const noDataMessage = document.createElement("p");
            noDataMessage.textContent = "No barriers found";
            barriersTable.appendChild(noDataMessage);
        }
    } catch (error) {
        console.error("Error fetching data:", error);

        const barriersTable = document.getElementById("barriersTable");
        const errorMessage = document.createElement("p");
        errorMessage.textContent = "Error fetching barriers data. Please try again later.";
        barriersTable.appendChild(errorMessage);
    }
}

// Function to create a table cell with optional text classes
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

// Function to create an action cell with buttons for barrier actions
function createActionCell(barrierId, openCmd, closeCmd, lockCmd, unlockCmd, inputField) {
    const cell = document.createElement("td");

    // Helper function to create a button with an icon
    const createButton = (imgSrc, altText, width, height, btnClass, clickHandler) => {
        const button = document.createElement("button");
        button.classList.add("btn", "btn-sm", "fw-bold", btnClass);
        const img = document.createElement("img");
        img.src = imgSrc;
        img.alt = altText;
        img.width = width;
        img.height = height;
        button.appendChild(img);
        button.addEventListener("click", () => {
            Swal.fire({
                title: "Connecting to the barrier...",
                didOpen: () => {
                    Swal.showLoading();
                },
            });
            clickHandler();
        });
        return button;
    };

    // Create buttons for open, close, lock, and unlock actions
    cell.appendChild(createButton("/static/br_open.svg", "", 30, 30, "btn", () => handleBarrierAction("open", barrierId, openCmd, inputField.value)));
    cell.appendChild(document.createTextNode("\u00A0"));
    cell.appendChild(createButton("/static/br_closed.svg", "", 30, 30, "btn", () => handleBarrierAction("close", barrierId, closeCmd, inputField.value)));
    cell.appendChild(document.createTextNode("\u00A0"));
    cell.appendChild(createButton("/static/lock.svg", "", 30, 30, "btn", () => handleBarrierAction("lock", barrierId, lockCmd, inputField.value)));
    cell.appendChild(document.createTextNode("\u00A0"));
    cell.appendChild(createButton("/static/unlock.svg", "", 30, 30, "btn", () => handleBarrierAction("unlock", barrierId, unlockCmd, inputField.value)));

    return cell;
}

// Function to handle barrier actions (open, close, lock, unlock)
async function handleBarrierAction(action, barrierId, command, extraData) {
    const endpoint = `http://${ipAddress}:${portep}/${action}/${barrierId}`;
    const requestBody = { command: command, extra_data: extraData };

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            body: JSON.stringify(requestBody),
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const data = await response.json();
            Swal.fire({
                icon: "success",
                title: `${action.toUpperCase()} Successful!`,
                text: `Barrier ${barrierId} ${action}ed successfully`,
                showConfirmButton: false,
                timer: 1500
            });
        } else {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Error ${action}ing barrier ${barrierId}:`, error);
        Swal.fire({
            icon: "error",
            title: `Error ${action}ing Barrier`,
            text: `An error occurred while ${action}ing Barrier ${barrierId}`,
            showConfirmButton: false,
            timer: 1500
        });
    }
}

// Execute the function to fetch data and populate the table when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function () {
    fetchDataAndPopulateTable();
});
