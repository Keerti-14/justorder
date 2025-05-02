import json
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.TextField()  # Store items as a JSON string
    total_price = models.FloatField()
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_items(self):
        """Parse the JSON string and return a list of items."""
        try:
            return json.loads(self.items)
        except json.JSONDecodeError:
            return []

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"