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


    function recalculatePrice() {
        // Базовая цена из товара
        var basePrice = parseFloat($("#product-price").data("base-price"));
        var totalPrice = basePrice;
    
        // Суммируем стоимость выбранных топпингов
        $("input[name='topping_ids[]']:checked").each(function () {
            totalPrice += parseFloat($(this).data("price"));
        });
    
        // Обновляем отображение цены
        $("#product-price").text(totalPrice.toFixed(2) + "Р");
    }


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

        // Проверяем количество выбранных молока
        var milkCount = $("input[name='topping_ids[]'][data-milk='true']:checked").length;

        if (milkCount > 1) {
            Swal.fire({
                icon: 'error',
                title: 'Ошибка!',
                text: 'Вы можете выбрать только одно молоко.',
                confirmButtonText: 'ОК',
            }).then(() => {
                $(this).prop("checked", false); // Отменяем выбор текущего чекбокса
            });
            return;
        }
        recalculateKBJU();
        recalculatePrice();
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
    document.querySelectorAll('.index_radio').forEach((radio) => {
        radio.addEventListener('change', function () {
            const orderBy = this.value;
            const url = new URL(window.location.href);
            url.searchParams.set('order_by', orderBy);
            window.location.href = url.toString();
        });
    });


    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        // Скрываем или отображаем input ввода адреса доставки
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });

});

