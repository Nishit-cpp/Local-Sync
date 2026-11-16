async function loadDashboard() {

    try {

        const data =
            await apiRequest(
                "/api/dashboard"
            );


        document.getElementById(
            "customersCount"
        ).textContent =
            data.customers;


        document.getElementById(
            "productsCount"
        ).textContent =
            data.products;


        document.getElementById(
            "ordersCount"
        ).textContent =
            data.orders;


        document.getElementById(
            "remindersCount"
        ).textContent =
            data.reminders;


        renderReminders(
            data.due_reminders
        );


        renderOrders(
            data.recent_orders
        );

    }

    catch (error) {

        showToast(
            error.message,
            "error"
        );

    }

}


function renderReminders(reminders) {

    const container =
        document.getElementById(
            "dashboardReminders"
        );


    if (!reminders.length) {

        container.innerHTML = `
            <div class="empty-state compact">
                <div class="empty-icon">✓</div>

                <h3>
                    Everything looks clear
                </h3>

                <p>
                    No customer restocks are due right now.
                </p>
            </div>
        `;

        return;
    }


    container.innerHTML =
        reminders.map(reminder => `

            <div class="activity-row">

                <div class="activity-avatar">
                    ${getInitials(reminder.customer_name)}
                </div>

                <div class="activity-info">

                    <strong>
                        ${escapeHtml(reminder.customer_name)}
                    </strong>

                    <span>
                        ${escapeHtml(reminder.product_name)}
                    </span>

                </div>

                <div class="activity-meta">

                    <strong>
                        ${reminder.cycle_days} days
                    </strong>

                    <span>
                        Cycle
                    </span>

                </div>

            </div>

        `).join("");

}


function renderOrders(orders) {

    const container =
        document.getElementById(
            "recentOrders"
        );


    if (!orders.length) {

        container.innerHTML = `
            <div class="empty-state compact">
                <div class="empty-icon">↗</div>

                <h3>
                    No orders yet
                </h3>

                <p>
                    Orders will appear here when customers respond to reminders.
                </p>
            </div>
        `;

        return;
    }


    container.innerHTML =
        orders.map(order => `

            <div class="activity-row">

                <div class="activity-avatar order-avatar">
                    ↗
                </div>

                <div class="activity-info">

                    <strong>
                        ${escapeHtml(order.customer_name)}
                    </strong>

                    <span>
                        ${escapeHtml(order.product_name)}
                    </span>

                </div>

                <div class="activity-meta">

                    <strong>
                        ${formatCurrency(order.total_amount)}
                    </strong>

                    <span>
                        ${escapeHtml(order.fulfilment)}
                    </span>

                </div>

            </div>

        `).join("");

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


loadDashboard();
