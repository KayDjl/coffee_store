(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})();


// Когда html документ готов (прорисован)
$(document).ready(function () {

    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        // Сбор всех выбранных топпингов
        var topping_ids = [];
        $("input[name='topping_ids[]']:checked").each(function () {
            topping_ids.push($(this).val());
        });
        console.log("Отправляемые topping_ids:", topping_ids);

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                'topping_ids[]': topping_ids,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html); 
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });


    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    
    function recalculateKBJU() {
        // Начальные значения из товара
        var baseCalories = parseFloat($("#calories").data("base-value"));
        var baseProteins = parseFloat($("#protein").data("base-value"));
        var baseFats = parseFloat($("#fats").data("base-value"));
        var baseCarbs = parseFloat($("#carb").data("base-value"));

        var totalCalories = baseCalories;
        var totalProteins = baseProteins;
        var totalFats = baseFats;
        var totalCarbs = baseCarbs;


        // Суммируем КБЖУ выбранных топпингов
        $("input[name='topping_ids[]']:checked").each(function () {
            totalCalories += parseFloat($(this).data("calories"));
            totalProteins += parseFloat($(this).data("protein"));
            totalFats += parseFloat($(this).data("fats"));
            totalCarbs += parseFloat($(this).data("carb"));
        });

        // Обновляем значения в таблице
        $("#calories").text(totalCalories.toFixed(1) + " ккал");
        $("#protein").text(totalProteins.toFixed(1) + " г");
        $("#fats").text(totalFats.toFixed(1) + " г");
        $("#carb").text(totalCarbs.toFixed(1) + " г");
    }

    // Установка базовых значений КБЖУ из товара
    $("#calories").data("base-value", parseFloat($("#calories").text()));
    $("#protein").data("base-value", parseFloat($("#protein").text()));
    $("#fats").data("base-value", parseFloat($("#fats").text()));
    $("#carb").data("base-value", parseFloat($("#carb").text()));

    // Событие изменения для чекбоксов
    $(document).on("change", "input[name='topping_ids[]']", function () {
        // const selectedToppings = $("input[name='toping_ids[]']:checked").toArray();

        // // Проверяем количество молока
        // const selectedMilk = selectedToppings.filter(cb => $(cb).attr("data-milk") === "true");
        // if (selectedMilk.length > 1) {
        //     Swal.fire({
        //         icon: 'error',
        //         title: 'Ошибка',
        //         text: 'Вы можете выбрать только одно молоко.',
        //         confirmButtonText: 'Ок'
        //     });
        //     $(this).prop("checked", false);
        //     return;
        // }
        recalculateKBJU();
    });
    

    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 3000);
    }

    // При клике по значку корзины открываем всплывающее(модальное) окно
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });


    $(window).scroll(function () {
        if ($(this).scrollTop() > 500) {
            $('#top').fadeIn();
        } else {
            $("#top").fadeOut();
        }
    });

    $('#top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 100);
        return false;
    });
    

    //Обновление URL сортировки по цене на главной странице
    document.querySelectorAll('.form-check-input').forEach((radio) => {
        radio.addEventListener('change', function () {
            const orderBy = this.value;
            const url = new URL(window.location.href);
            url.searchParams.set('order_by', orderBy);
            window.location.href = url.toString();
    });
});

});













    // // Функция ра счетра кбжу, стоимости продукта и валидации на молоко
    // const productPageElem = document.getElementById("product-page");
    // if (!productPageElem) {
    //     return;
    // }

    // const toppingCheckboxes = document.querySelectorAll(".btn-check");
    // const caloriesElem = document.getElementById("calories");
    // const proteinElem = document.getElementById("protein");
    // const fatsElem = document.getElementById("fats");
    // const carbElem = document.getElementById("carb");
    // const buyButton = document.querySelector(".product-add2cart a");

    // // Начальные значения из продукта
    // const baseCalories = parseFloat(caloriesElem.textContent) || 0;;
    // const baseProtein = parseFloat(proteinElem.textContent) || 0;;
    // const baseFats = parseFloat(fatsElem.textContent) || 0;;
    // const baseCarb = parseFloat(carbElem.textContent) || 0;;
    // const basePrice = parseFloat(buyButton.dataset.basePrice) || 0;;

    // toppingCheckboxes.forEach(checkbox => {
    //     checkbox.addEventListener("change", function () {
    //         let totalCalories = baseCalories;
    //         let totalProtein = baseProtein;
    //         let totalFats = baseFats;
    //         let totalCarb = baseCarb;
    //         let totalPrice = basePrice;

            // // Проверяем все выбранные топпинги
            // const selectedToppings = Array.from(toppingCheckboxes).filter(cb => cb.checked);

            // // Проверяем количество молока
            // const selectedMilk = selectedToppings.filter(cb => cb.dataset.milk === "true");
            // if (selectedMilk.length > 1) {
            //     Swal.fire({
            //         icon: 'error',
            //         title: 'Ошибка',
            //         text: 'Вы можете выбрать только одно молоко.',
            //         confirmButtonText: 'Ок'
            //     });
            //     this.checked = false;
            //     return;
            // }

    //         // Обновляем КБЖУ и цену
    //         selectedToppings.forEach(cb => {
    //             totalCalories += parseFloat(cb.dataset.calories) || 0;;
    //             totalProtein += parseFloat(cb.dataset.protein) || 0;;
    //             totalFats += parseFloat(cb.dataset.fats) || 0;;
    //             totalCarb += parseFloat(cb.dataset.carb) || 0;;
    //             totalPrice += parseFloat(cb.dataset.price) || 0;
    //         });

    //         // Обновляем значения на странице
    //         caloriesElem.textContent = `${totalCalories.toFixed(1)} ккал`;
    //         proteinElem.textContent = `${totalProtein.toFixed(1)} г`;
    //         fatsElem.textContent = `${totalFats.toFixed(1)} г`;
    //         carbElem.textContent = `${totalCarb.toFixed(1)} г`;
    //         buyButton.innerHTML = `<i class="fas fa-shopping-cart"></i> Купить ${totalPrice.toFixed(2)}р`;
    //     });
    // });
