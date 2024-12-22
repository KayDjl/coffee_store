from .models import Cart

def get_user_carts(request):
    """
    Возвращает корзину пользователя или сессии.
    """
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related("product")

    # Создаем сессию, если её ещё нет
    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).select_related("product")