from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    session_key = request.session.session_key

    # If there's no session cart, nothing to do
    if not session_key:
        return

    try:
        session_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
    except Cart.DoesNotExist:
        return

    # Get or create a logged-in user cart
    user_cart, _ = Cart.objects.get_or_create(user=user)

    # Merge items from session cart to user cart
    for item in session_cart.items.all():
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart, product=item.product,
            defaults={'quantity': item.quantity}
        )
        if not created:
            user_item.quantity += item.quantity
            user_item.save()

    # Delete session cart after merge
    session_cart.delete()
