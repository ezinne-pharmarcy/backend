from rest_framework import serializers
from sales.models import Order, OrderItem, CartItem, Cart
import bleach
import logging


log = logging.getLogger('main')

class CartSerializer(serializers.ModelSerializer):
    """
    serializes the cart model
    """

    class Meta:
        model = Cart
        fields = '__all__'

    def validate(self, attrs):
        """
        validates the data entered into the serializer class
        """
        log.info(f'validating cart data from request')
        total_price = bleach.clean(attrs['total_price'], strip=True)

        if total_price != attrs['total_price']:
            log.error(f'validation of cart data from request failed because invalid total_price characters were entered')
            raise serializers.ValidationError("You have entered invalid characters")   
        
        if len(total_price) > 20:
            log.error(f'validation of cart data from request failed because the character limit for total_price was exceeded')
            raise serializers.ValidationError("You have exceeded the allowed characters")   
                
        return attrs

    def create(self, validated_data):
        """
        creates a new cart
        """
        log.info(f'creating a new cart using the request data via the order_serializer class')
        log.info(f'new cart has been created successfully via the order_serializer class')
        return super(CartSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing cart
        """
        log.info(f'updating an existing cart using the request data via the cart_serializer class')
        log.info(f'existing cart has been updated successfully via the cart_serializer class')
        return super(CartSerializer, self).update(instance, validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    """
    serializes the cart_item model
    """

    class Meta:
        model = CartItem
        fields = '__all__'

    def validate(self, attrs):
        """
        validates the data entered into the serializer class
        """
        log.info(f'validating cart_item data from request')
        price = bleach.clean(attrs['price'], strip=True)

        if price != attrs['price']:
            log.error(f'validation of cart_item data from request failed because invalid price characters were entered')
            raise serializers.ValidationError("You have entered invalid price characters")   
        
        if len(price) > 20:
            log.error(f'validation of cart_item data from request failed because the character limit for price was exceeded')
            raise serializers.ValidationError("You have exceeded the allowed characters")   
                
        return attrs

    def create(self, validated_data):
        """
        creates a new cart_item
        """
        log.info(f'creating a new cart_item using the request data via the cart_item_serializer class')
        log.info(f'new cart_item has been created successfully via the cart_item_serializer class')
        return super(CartItemSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing cart_item
        """
        log.info(f'updating an existing cart_item using the request data via the cart_item_serializer class')
        log.info(f'existing cart_item has been updated successfully via the cart_item_serializer class')
        return super(CartItemSerializer, self).update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    """
    serializes the order model
    """

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        """
        validates the data entered into the serializer class
        """
        log.info(f'validating order data from request')
        total_price = bleach.clean(attrs['total_price'], strip=True)

        if total_price != attrs['total_price']:
            log.error(f'validation of order data from request failed because invalid total_price characters were entered')
            raise serializers.ValidationError("You have entered invalid characters")   
        
        if len(total_price) > 20:
            log.error(f'validation of order data from request failed because the character limit for total_price was exceeded')
            raise serializers.ValidationError("You have exceeded the allowed characters")   
                
        return attrs

    def create(self, validated_data):
        """
        creates a new order
        """
        log.info(f'creating a new order using the request data via the order_serializer class')
        log.info(f'new order has been created successfully via the order_serializer class')
        return super(OrderSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing order
        """
        log.info(f'updating an existing order using the request data via the order_serializer class')
        log.info(f'existing order has been updated successfully via the order_serializer class')
        return super(OrderSerializer, self).update(instance, validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    """
    serializes the order_item model
    """

    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate(self, attrs):
        """
        validates the data entered into the serializer class
        """
        log.info(f'validating order_item data from request')
        price = bleach.clean(attrs['price'], strip=True)

        if price != attrs['price']:
            log.error(f'validation of order data from request failed because invalid price characters were entered')
            raise serializers.ValidationError("You have entered invalid price characters")   
        
        if len(price) > 20:
            log.error(f'validation of order data from request failed because the character limit for price was exceeded')
            raise serializers.ValidationError("You have exceeded the allowed characters")   
                
        return attrs

    def create(self, validated_data):
        """
        creates a new order_item
        """
        log.info(f'creating a new order_item using the request data via the order_item_serializer class')
        log.info(f'new order_item has been created successfully via the order_item_serializer class')
        return super(OrderItemSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing order_item
        """
        log.info(f'updating an existing order_item using the request data via the order_item_serializer class')
        log.info(f'existing order_item has been updated successfully via the order_item_serializer class')
        return super(OrderItemSerializer, self).update(instance, validated_data)
