// Когда HTML документ готов
document.addEventListener('DOMContentLoaded', () => {

    // Элемент для уведомлений
    const successMessage = document.getElementById('jq-notification');

    // Получение CSRF-токена Django
    function getCSRFToken() {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    }

    // Показ уведомления
    function showMessage(message) {
        if (!successMessage) return;

        successMessage.innerHTML = message;
        successMessage.style.display = 'block';

        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 7000);
    }

    // Делегирование кликов
    document.addEventListener('click', (e) => {

        /* ---------- ДОБАВИТЬ В КОРЗИНУ ---------- */
        const addBtn = e.target.closest('.add-to-cart');
        if (addBtn) {
            e.preventDefault();
            console.log('Зашли в функцию');
            const productId = addBtn.dataset.productId;
            console.log(productId);
            const url = addBtn.getAttribute('href');

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken()
                },
                body: new URLSearchParams({
                    product_id: productId,
                    csrfmiddlewaretoken: getCSRFToken()
                })
            })
            .then(res => res.json())
            .then(data => {
                showMessage(data.message);

                const cartItems = document.getElementById('cart-items-container');
                cartItems.innerHTML = data.cart_items_html;
            })
            .catch(() => {
                console.log('Ошибка при добавлении товара в корзину');
            });

            return;
        }

        /* ---------- УДАЛИТЬ ИЗ КОРЗИНЫ ---------- */
        const removeBtn = e.target.closest('.remove-from-cart');
        if (removeBtn) {
            e.preventDefault();

            const cartId = removeBtn.dataset.cartId;
            const url = removeBtn.getAttribute('href');

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken()
                },
                body: new URLSearchParams({
                    cart_id: cartId,
                    csrfmiddlewaretoken: getCSRFToken()
                })
            })
            .then(res => res.json())
            .then(data => {
                showMessage(data.message);

                const cartItems = document.getElementById('cart-items-container');
                cartItems.innerHTML = data.cart_items_html;
            })
            .catch(() => {
                console.log('Ошибка при удалении товара из корзины');
            });

            return;
        }

        /* ---------- УМЕНЬШЕНИЕ КОЛИЧЕСТВА ---------- */
        const decrementBtn = e.target.closest('.decrement');
        if (decrementBtn) {
            e.preventDefault();

            const url = decrementBtn.dataset.cartChangeUrl;
            const cartID = decrementBtn.dataset.cartId;

            const block = decrementBtn.closest('.col_cart.col-qty');
            const input = block.querySelector('input.number_cl');
            const currentValue = parseInt(input.value);

            if (currentValue > 1) {
                updateCart(cartID, currentValue - 1, url);
            }
            return;
        }

        /* ---------- УВЕЛИЧЕНИЕ КОЛИЧЕСТВА ---------- */
        const incrementBtn = e.target.closest('.increment');
        if (incrementBtn) {
            e.preventDefault();

            const url = incrementBtn.dataset.cartChangeUrl;
            const cartID = incrementBtn.dataset.cartId;

            const block = incrementBtn.closest('.col_cart.col-qty');
            const input = block.querySelector('input.number_cl');
            const currentValue = parseInt(input.value);

            updateCart(cartID, currentValue + 1, url);
        }
    });

    /* ---------- ОБНОВЛЕНИЕ КОРЗИНЫ ---------- */
    function updateCart(cartID, quantity, url) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken()
            },
            body: new URLSearchParams({
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: getCSRFToken()
            })
        })
        .then(res => res.json())
        .then(data => {
            showMessage(data.message);

            const cartItems = document.getElementById('cart-items-container');
            cartItems.innerHTML = data.cart_items_html;
        })
        .catch(() => {
            console.log('Ошибка при обновлении корзины');
        });
    }

    /* ---------- УВЕДОМЛЕНИЕ ОТ DJANGO ---------- */
    const notification = document.getElementById('notification');
    if (notification) {
        setTimeout(() => {
            notification.remove();
        }, 7000);
    }

});