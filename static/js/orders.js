async function loadOrders() {

    try {

        const orders =
            await apiRequest(
                "/api/orders"
            );


        const table =
            document.getElementById(
                "ordersTable"
            );


        if (!orders.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="6">

                        <div class="table-empty">

                            No orders yet.

                            <br>

                            Orders will appear here when customers respond to restock reminders.

                        </div>

                    </td>
                </tr>
            `;

            return;
        }


        table.innerHTML =
            orders.map(order => `

                <tr>

                    <td>

                        <strong>
                            #LS-${String(order.id).padStart(4, "0")}
                        </strong>

                    </td>


                    <td>
                        ${escapeHtml(order.customer_name)}
                    </td>


                    <td>
                        ${escapeHtml(order.product_name)}
                    </td>


                    <td>

                        <span class="language-tag">
                            ${escapeHtml(order.fulfilment)}
                        </span>

                    </td>


                    <td>

                        <strong>
                            ${formatCurrency(order.total_amount)}
                        </strong>

                    </td>


                    <td>

                        <span class="status pending">
                            ${escapeHtml(order.status)}
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


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;

}


loadOrders();