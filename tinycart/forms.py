from django import forms
from django.contrib.contenttypes.models import ContentType


class CartItemForm(forms.Form):

    product_id = forms.IntegerField(min_value=1)
    product_type = forms.ModelChoiceField(queryset=ContentType.objects.all())

    quantity = forms.IntegerField(min_value=1, initial=1, required=False)
    is_held = forms.BooleanField(initial=False, required=False)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        return quantity if quantity is not None else 1

    def clean(self):
        product_id = self.cleaned_data.get('product_id')
        product_type = self.cleaned_data.get('product_type')
        if product_id and product_type:
            try:
                product = product_type.get_object_for_this_type(pk=product_id)
            except product_type.model_class().DoesNotExist:
                raise forms.ValidationError('Product does not exist')
            self.cleaned_data['product'] = product
        return self.cleaned_data

    def add_to_cart(self, cart):
        return cart.add(self.cleaned_data['product'],
                        self.cleaned_data['quantity'],
                        self.cleaned_data['is_held'])
