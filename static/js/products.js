async function loadProducts() {

    const search =
        document.getElementById(
            "productSearch"
        ).value;


    try {

        const products =
            await apiRequest(
                `/api/products?search=${encodeURIComponent(search)}`
            );


        document.getElementById(
            "productTotal"
        ).textContent =
            `${products.length} product${products.length === 1 ? "" : "s"}`;


        const grid =
            document.getElementById(
                "productsGrid"
            );


        if (!products.length) {

            grid.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">▣</div>
                    <h3>No products found</h3>
                    <p>
                        Try another search or add a new product.
                    </p>
                </div>
            `;

            return;
        }


        grid.innerHTML =
            products.map(product => `

                <div class="product-card">

                    <div class="product-top">

                        <div class="product-icon">
                            ${getProductIcon(product.category)}
                        </div>

                        <span class="status active">
                            Available
                        </span>

                    </div>


                    <h3>
                        ${escapeHtml(product.name)}
                    </h3>


                    <span class="product-category">
                        ${escapeHtml(product.category)}
                    </span>


                    <div class="product-bottom">

                        <div>

                            <strong>
                                ${formatCurrency(product.price)}
                            </strong>

                            <small>
                                / ${escapeHtml(product.unit)}
                            </small>

                        </div>


                        <div class="stock">

                            <span>
                                Stock
                            </span>

                            <strong>
                                ${product.stock}
                            </strong>

                        </div>

                    </div>

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


function getProductIcon(category) {

    const icons = {

        "Staples": "▦",

        "Dairy": "◉",

        "Beverages": "◒",

        "Cooking Oil": "◈",

        "Snacks": "◇",

        "Grocery": "▣"

    };

    return icons[category] || "▣";

}


function openProductModal() {

    document
        .getElementById("productModal")
        .classList.remove("hidden");

}


function closeProductModal() {

    document
        .getElementById("productModal")
        .classList.add("hidden");

}


async function createProduct(event) {

    event.preventDefault();


    const product = {

        name:
            document.getElementById(
                "productName"
            ).value,

        category:
            document.getElementById(
                "productCategory"
            ).value,

        price:
            document.getElementById(
                "productPrice"
            ).value,

        stock:
            document.getElementById(
                "productStock"
            ).value,

        unit:
            document.getElementById(
                "productUnit"
            ).value

    };


    try {

        const result =
            await apiRequest(
                "/api/products",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(product)
                }
            );


        showToast(
            result.message
        );


        closeProductModal();

        event.target.reset();

        loadProducts();

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


loadProducts();