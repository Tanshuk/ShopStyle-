from django.db import models
from django.conf import settings


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'wishlists'
        verbose_name        = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'

    def __str__(self):
        return f"Wishlist of {self.user.email}"
