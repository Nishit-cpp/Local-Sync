async function loadReminders() {

    try {

        const reminders =
            await apiRequest(
                "/api/reminders"
            );


        const container =
            document.getElementById(
                "remindersList"
            );


        if (!reminders.length) {

            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">✓</div>

                    <h3>
                        No consumption cycles
                    </h3>

                    <p>
                        Add customer purchase data to begin tracking restocks.
                    </p>
                </div>
            `;

            return;
        }


        container.innerHTML =
            reminders.map(reminder => `

                <div class="reminder-card">

                    <div class="reminder-person">

                        <div class="person-avatar large">
                            ${getInitials(reminder.customer_name)}
                        </div>


                        <div>

                            <strong>
                                ${escapeHtml(reminder.customer_name)}
                            </strong>

                            <span>
                                ${escapeHtml(reminder.phone)}
                            </span>

                        </div>

                    </div>


                    <div class="reminder-product">

                        <strong>
                            ${escapeHtml(reminder.product_name)}
                        </strong>

                        <span>
                            ₹${reminder.price}
                        </span>

                    </div>


                    <div class="cycle-box">

                        <span>
                            Current cycle
                        </span>

                        <strong>
                            ${reminder.cycle_days} days
                        </strong>

                    </div>


                    <div class="reminder-date">

                        <span>
                            Next reminder
                        </span>

                        <strong>
                            ${formatDate(reminder.next_reminder_date)}
                        </strong>

                    </div>


                    <button
                        class="remind-button"
                        onclick="openReminderDemo(${reminder.id}, '${escapeAttribute(reminder.customer_name)}', '${escapeAttribute(reminder.product_name)}', ${reminder.cycle_days})"
                    >

                        Open chat

                    </button>

                </div>

            `).join("");

    }

    catch (error) {

        showToast(
            error.message,
            "error"
        );

    }

}


function openReminderDemo(
    id,
    customer,
    product,
    cycle
) {

    const existing =
        document.getElementById(
            "whatsappModal"
        );

    if (existing) {
        existing.remove();
    }


    const modal =
        document.createElement("div");

    modal.id =
        "whatsappModal";

    modal.className =
        "modal";


    modal.innerHTML = `

        <div class="whatsapp-modal">

            <div class="whatsapp-header">

                <div class="wa-back">
                    ←
                </div>

                <div class="wa-avatar">
                    ${getInitials(customer)}
                </div>

                <div class="wa-person">

                    <strong>
                        ${escapeHtml(customer)}
                    </strong>

                    <span>
                        online
                    </span>

                </div>

                <button
                    class="wa-close"
                    onclick="closeWhatsApp()"
                >
                    ×
                </button>

            </div>


            <div class="whatsapp-chat">

                <div class="chat-date">
                    TODAY
                </div>


                <div class="message merchant-message">

                    <span>
                        Sharma Provisions
                    </span>

                    <p>
                        Namaste ${escapeHtml(customer)} ji!
                        Your ${escapeHtml(product)}
                        may be running low.
                    </p>

                    <p>
                        What would you like to do?
                    </p>

                    <div class="chat-options">

                        <button
                            onclick="sendReminderResponse(${id}, '1')"
                        >
                            <strong>1</strong>
                            Place order
                        </button>

                        <button
                            onclick="sendReminderResponse(${id}, '2')"
                        >
                            <strong>2</strong>
                            Self pickup
                        </button>

                        <button
                            onclick="sendReminderResponse(${id}, '3')"
                        >
                            <strong>3</strong>
                            Still have stock
                        </button>

                    </div>

                    <small>
                        6:30 PM
                    </small>

                </div>


                <div class="cycle-info">

                    Current consumption cycle:
                    <strong>${cycle} days</strong>

                </div>

            </div>

        </div>

    `;


    document.body.appendChild(modal);

}


async function sendReminderResponse(
    id,
    response
) {

    try {

        const result =
            await apiRequest(
                `/api/reminders/${id}/respond`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            response: response
                        })
                }
            );


        showToast(
            result.message
        );


        closeWhatsApp();

        loadReminders();

    }

    catch (error) {

        showToast(
            error.message,
            "error"
        );

    }

}


function closeWhatsApp() {

    const modal =
        document.getElementById(
            "whatsappModal"
        );

    if (modal) {
        modal.remove();
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


function escapeAttribute(value) {

    return String(value)
        .replace(/'/g, "\\'");
}


loadReminders();