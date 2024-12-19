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


$(document).ready(function (){
    $(window).scroll(function (){
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

document.querySelectorAll('.form-check-input').forEach((radio) => {
    radio.addEventListener('change', function() {
        const orderBy = this.value;
        const url = new URL(window.location.href);
        url.searchParams.set('order_by', orderBy);
        window.location.href = url.toString();
    });
});

