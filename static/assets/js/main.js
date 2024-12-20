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

//Быстрый скролл вверх на главной странице
$(document).ready(function () {
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

// Функция ра счетра кбжу, стоимости продукта и валидации на молоко
document.addEventListener("DOMContentLoaded", function () {

    const productPageElem = document.getElementById("product-page");
    if (!productPageElem) {
        return;
    }

    const toppingCheckboxes = document.querySelectorAll(".btn-check");
    const caloriesElem = document.getElementById("calories");
    const proteinElem = document.getElementById("protein");
    const fatsElem = document.getElementById("fats");
    const carbElem = document.getElementById("carb");
    const buyButton = document.querySelector(".product-add2cart button");

    // Начальные значения из продукта
    const baseCalories = parseFloat(caloriesElem.textContent);
    const baseProtein = parseFloat(proteinElem.textContent);
    const baseFats = parseFloat(fatsElem.textContent);
    const baseCarb = parseFloat(carbElem.textContent);
    const basePrice = parseFloat(buyButton.textContent.match(/\d+/)[0]);

    toppingCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            let totalCalories = baseCalories;
            let totalProtein = baseProtein;
            let totalFats = baseFats;
            let totalCarb = baseCarb;
            let totalPrice = basePrice;

            // Проверяем все выбранные топпинги
            const selectedToppings = Array.from(toppingCheckboxes).filter(cb => cb.checked);

            // Проверяем количество молока
            const selectedMilk = selectedToppings.filter(cb => cb.dataset.milk === "true");
            if (selectedMilk.length > 1) {
                Swal.fire({
                    icon: 'error',
                    title: 'Ошибка',
                    text: 'Вы можете выбрать только одно молоко.',
                    confirmButtonText: 'Ок'
                });
                this.checked = false;
                return;
            }

            // Обновляем КБЖУ и цену
            selectedToppings.forEach(cb => {
                totalCalories += parseFloat(cb.dataset.calories);
                totalProtein += parseFloat(cb.dataset.protein);
                totalFats += parseFloat(cb.dataset.fats);
                totalCarb += parseFloat(cb.dataset.carb);
                totalPrice += parseFloat(cb.value);
            });

            // Обновляем значения на странице
            caloriesElem.textContent = `${totalCalories.toFixed(1)} ккал`;
            proteinElem.textContent = `${totalProtein.toFixed(1)} г`;
            fatsElem.textContent = `${totalFats.toFixed(1)} г`;
            carbElem.textContent = `${totalCarb.toFixed(1)} г`;
            buyButton.innerHTML = `<i class="fas fa-shopping-cart"></i> Купить ${totalPrice.toFixed(2)}р`;
        });
    });
});