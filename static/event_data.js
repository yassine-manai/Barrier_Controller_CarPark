console.log(`IP Address: ${ipAddress}`);
console.log(`Port: ${portep}`);

fetch(`http://${ipAddress}:${portep}/Barrier`)

document.addEventListener("DOMContentLoaded", function() {
    fetch(`http://${ipAddress}:${portep}/Event`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            const eventsTable = document.getElementById("eventsTable");
            if (data.length === 0) {
                const noDataMessage = document.createElement("p");
                noDataMessage.textContent = "No events found";
                eventsTable.appendChild(noDataMessage);
            } else {
                data.forEach(eventData => {
                    const newRow = document.createElement("tr");

                    // Create and append cells for each data item
                    eventData.forEach(eventAttribute => {
                        const cell = createCell(eventAttribute, true);
                        newRow.appendChild(cell);
                    });

                    eventsTable.querySelector("tbody").appendChild(newRow);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });

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
});


			// Function to update table with events based on search input
		async function updateTableBySearchInput() 
		{
			const searchInput = document.querySelector('[data-kt-customer-table-filter="search"]');
			const searchText = searchInput.value.trim().toLowerCase(); // Get the search text

			try {
				let endpoint = `http://${ipAddress}:${portep}/Event`;

				if (searchText) {
					endpoint += `/${searchText}`;
				}

				const response = await fetch(endpoint);
				if (response.status === 404) {
					const eventsTable = document.getElementById("eventsTable");
					const tableBody = eventsTable.querySelector("tbody");
					tableBody.innerHTML = ""; // Clear existing table rows
					
					const noDataMessageRow = document.createElement("tr");
					const noDataMessageCell = document.createElement("td");
					const span = document.createElement("span");

					
					//span.textContent = `No event found with this id ${searchText}`;
                    span.textContent = "No event found";
					span.classList.add("text-dark", "fw-bold", "text-hover-primary", "d-block", "mb-1", "fs-6");
					noDataMessageCell.appendChild(span);
					noDataMessageCell.colSpan = 5; // Span across all columns
					noDataMessageCell.style.textAlign = "center"; // Center the text
					noDataMessageRow.appendChild(noDataMessageCell);
					tableBody.appendChild(noDataMessageRow);

					return; // Exit function early if no data found
				}
				
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				const events = await response.json();

				const eventsTable = document.getElementById("eventsTable");
				const tableBody = eventsTable.querySelector("tbody");
				tableBody.innerHTML = ""; // Clear existing table rows

				if (events.length === 0 && searchText) {
					const noDataMessageRow = document.createElement("tr");
					const noDataMessageCell = document.createElement("td");
					const span = document.createElement("span");
					span.textContent = "No data found";
					span.classList.add("text-dark", "fw-bold", "text-hover-primary", "d-block", "mb-1", "fs-6");
					noDataMessageCell.appendChild(span);
					noDataMessageCell.colSpan = 5; // Span across all columns
					noDataMessageCell.style.textAlign = "center"; // Center the text
					noDataMessageRow.appendChild(noDataMessageCell);
					tableBody.appendChild(noDataMessageRow);
				} else {
					events.forEach(event => {
						const newRow = document.createElement("tr");
						newRow.innerHTML = `
							<td class="text-dark fw-bold">${event[0]}</td>
							<td class="text-dark fw-bold">${event[1]}</td>
							<td class="text-dark fw-bold">${event[2]}</td>
							<td class="text-dark fw-bold">${event[3]}</td>
							<td class="text-dark fw-bold">${event[4]}</td>
						`;
						tableBody.appendChild(newRow);
					});
				}
			} catch (error) {
				console.error("Error fetching events:", error);
			}
		}

		// Add event listener to search input
		document.addEventListener("DOMContentLoaded", function() {
			const searchInput = document.querySelector('[data-kt-customer-table-filter="search"]');
			searchInput.addEventListener("input", updateTableBySearchInput);

			// Initial table update on page load
			updateTableBySearchInput();
		});
	
