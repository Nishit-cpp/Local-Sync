async function loadCustomers() {

    const search =
        document.getElementById(
            "customerSearch"
        ).value;


    try {

        const customers =
            await apiRequest(
                `/api/customers?search=${encodeURIComponent(search)}`
            );


        document.getElementById(
            "customerTotal"
        ).textContent =
            `${customers.length} customer${customers.length === 1 ? "" : "s"}`;


        const table =
            document.getElementById(
                "customersTable"
            );


        if (!customers.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="5">

                        <div class="table-empty">
                            No customers found.
                        </div>

                    </td>
                </tr>
            `;

            return;
        }


        table.innerHTML =
            customers.map(customer => `

                <tr>

                    <td>

                        <div class="table-person">

                            <div class="person-avatar">
                                ${getInitials(customer.name)}
                            </div>

                            <div>

                                <strong>
                                    ${escapeHtml(customer.name)}
                                </strong>

                                <small>
                                    Customer #${customer.id}
                                </small>

                            </div>

                        </div>

                    </td>


                    <td>
                        ${escapeHtml(customer.phone)}
                    </td>


                    <td>

                        <span class="language-tag">
                            ${escapeHtml(customer.language)}
                        </span>

                    </td>


                    <td>
                        ${escapeHtml(customer.address || "—")}
                    </td>


                    <td>

                        <span class="status active">
                            Active
                        </span>

                    </td>

                </tr>

            `).join("");

    }

    catch (error) {

        showToast(
            error.message,
            "error"
        );

    }

}


function openCustomerModal() {

    document
        .getElementById("customerModal")
        .classList.remove("hidden");

}


function closeCustomerModal() {

    document
        .getElementById("customerModal")
        .classList.add("hidden");

}


async function createCustomer(event) {

    event.preventDefault();


    const customer = {

        name:
            document.getElementById(
                "customerName"
            ).value,

        phone:
            document.getElementById(
                "customerPhone"
            ).value,

        language:
            document.getElementById(
                "customerLanguage"
            ).value,

        address:
            document.getElementById(
                "customerAddress"
            ).value

    };


    try {

        const result =
            await apiRequest(
                "/api/customers",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(customer)
                }
            );


        showToast(
            result.message
        );


        document
            .getElementById("customerForm")
            .reset();


        closeCustomerModal();

        loadCustomers();

    }

    catch (error) {

        showToast(
            error.message,
            "error"
        );

    }

}


function getInitials(name) {

    return name
        .split(" ")
        .slice(0, 2)
        .map(word => word[0])
        .join("")
        .toUpperCase();

}


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;

}


loadCustomers();