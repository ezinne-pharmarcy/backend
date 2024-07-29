from rest_framework.response import Response
from users.permissions import get_user
from rest_framework import status, viewsets
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import Owner, RetailStaff, AdminStaff
from sales.models import Order, OrderItem, Cart, CartItem
from sales.serializers import OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer
import logging

log = logging.getLogger('main')

class CartViewSet(viewsets.ModelViewSet):
    """
    suite for performing crud operations on the cart model
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    search_fields = ['sales_staff', 'times_tamp'] 

    def create(self, request):
        """
        creates a new cart.
        called by only retail_staff
        """
        log.info(f'instantiating create_cart function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, RetailStaff):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'cart request data has been validated and new order has been created')
                return Response({"status": status.HTTP_201_CREATED, 'data': serializer.data, 'detail' : 'new cart has been created successfully '})
            else:
                log.error(f'cart request data could not be validated so new order was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail' : 'new cart could not be created due to cart_serializer validation errors'})    

        else:
            log.error(f'requesting user does not have permission to create new cart')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to create new order'})

    def retrieve(self, request, pk=None):
        """
        handles retrieval of details of an cart instance identified by pk .
        view will be accesibble to owner, admin_staff and retail staff who created cart
        """
        log.info(f'instantiating get_cart function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        
        try:
            log.info(f'retrieving the cart instance')
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            log.error(f'cart instance cant be found on the database')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested cart does not exist'})  

        if request.user.pk == cart.sales_staff.pk or isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'cart instance has been successfully retrieved')
            serializer = self.serializer_class(cart)
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'cart has been retrieved successfully'})
                 
        else:
            log.error(f'requesting user does not have permission to retrieve cart')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to retrieve cart'})


    def list(self, request):
        """
        lists all the carts depending on the requesting user
        accesible to the retail staff who created the cart, admin users and owner
        """
        log.info(f'instantiating list_cart function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        

        if isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'retrieving the cart for {request.user.email}')
            carts = Cart.objects.all()
            if carts.count() > 0:
                log.info(f'carts with count {carts.count()} have been retrieved')
                serializer = self.serializer_class(carts, many=True)
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested carts has been retrieved successfully'})
        
        elif isinstance(request.user, RetailStaff):
            log.info(f'retrieving the carts for {request.user.email}')
            carts = Cart.objects.filter(sales_staff__pk=request.user.pk).filter(date=timezone.today())
            if carts.count() > 0:
                log.info(f'carts with count {carts.count()} have been retrieved')
                serializer = self.serializer_class(carts, many=True)
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested carts has been retrieved successfully'})

        else:
            log.error(f'requesting user does not have permission to retrieve cart')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def destroy(self, request, pk=None):
        """
        deletes an instance of a cart
        accesible to owner only
        """
        log.info(f'instantiating delete_cart function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        

        if isinstance(request.user, Owner):
            log.info(f'retrieving the cart for deletion')
            try:
                cart = Cart.objects.get(pk=pk)
            except Cart.DoesNotExist:
                log.error(f'the requested cart does not exist')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested cart does not exist'})  

            cart.delete()
            log.info(f'cart has been successfully deleted')
            return Response({'status': status.HTTP_200_OK,
                                        'detail': 'cart has been succesfully deleted'})
        
        else:
            log.error(f'requesting user does not have permission to delete cart')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})


class CartItemViewSet(viewsets.ModelViewSet):
    """
    suite for performing crud operations on the CartItem model
    """
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    search_fields = ['cart', 'drug'] 

    def create(self, request):
        """
        creates a new cart_item.
        called by only retail_staff
        """
        log.info(f'instantiating create_cart_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, RetailStaff):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'cart_item request data has been validated and new cart_item has been created')
                return Response({"status": status.HTTP_201_CREATED, 'data': serializer.data, 'detail' : 'new cart_item has been created successfully '})
            else:
                log.error(f'cart_item request data could not be validated so new cart_item was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail' : 'new cart_item could not be created due to cart_item_serializer validation errors'})    

        else:
            log.error(f'requesting user does not have permission to create new cart_item')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to create new cart_item'})

    def retrieve(self, request, pk=None):
        """
        handles retrieval of details of a cart_item instance identified by pk.
        view will be accesibble to owner, admin_staff and retail staff who created cart
        """
        log.info(f'instantiating get_cart_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        
        try:
            log.info(f'retrieving the cart_item instance')
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            log.error(f'cart_item instance cant be found on the database')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested cart_item does not exist'})  

        if request.user.pk == cart_item.cart.sales_staff.pk or isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'cart_item instance has been successfully retrieved')
            serializer = self.serializer_class(cart_item)
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'cart_item has been retrieved successfully'})
                 
        else:
            log.error(f'requesting user does not have permission to retrieve cart_item')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to retrieve cart_item'})


    def list(self, request):
        """
        lists all the cart_items for a particular cart
        accesible to the retail staff who created the cart, admin users and owner
        """
        log.info(f'instantiating list_cart_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        
        pk = request.GET.get('cart', None)
        if pk is None:
            log.error(f'pk for cart containing cart_items was not sent along with request data')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'pk for cart containing cart_items was not sent along with request data'})  

        if isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'retrieving the cart_items for {request.user.email}')
            log.info(f'retrieving the pk for the cart containing cart items')
            try:
                cart = Cart.objects.get(pk=pk)
            except Cart.DoesNotExist:
                log.error(f'cart instance cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested cart containing the cart_items does not exist'})  

            log.info(f'cart containing cart_items has been successfully retrieved')
            cart_items = CartItem.objects.filter(cart=cart)
            if cart_items.count() > 0:
                serializer = self.serializer_class(cart_items, many=True)
                log.info(f'cart_items with count {cart_items.count()} have been retrieved')
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested cart_items have been retrieved successfully'})
        
        elif isinstance(request.user, RetailStaff):
            log.info(f'retrieving the cart_items for {request.user.email}')
            log.info(f'retrieving the pk for the order containing order items')
            try:
                cart = Cart.objects.get(pk=pk)
            except Cart.DoesNotExist:
                log.error(f'cart instance cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested cart containing the cart_items does not exist'})  

            if request.user.pk == cart.sales_staff.pk:
                log.info(f'cart containing cart_items has been successfully retrieved')
                cart_items = CartItem.objects.filter(cart=cart)
                if cart_items.count() > 0:
                    log.info(f'cart_items with count {cart_items.count()} have been retrieved')
                    serializer = self.serializer_class(cart_items, many=True)
                    log.info(f'cart_items with count {cart_items.count()} have been retrieved')
                    return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested cart_items have been retrieved successfully'})

        else:
            log.error(f'requesting user does not have permission to retrieve cart_items')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def destroy(self, request, pk=None):
        """
        deletes an instance of a cart_item
        accesible to owner only
        """
        log.info(f'instantiating delete_cart_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        

        if isinstance(request.user, Owner):
            log.info(f'retrieving the cart_item for deletion')
            try:
                cart_item = CartItem.objects.get(pk=pk)
            except CartItem.DoesNotExist:
                log.error(f'the requested cart_item does not exist')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested cart_item does not exist'})  

            cart_item.delete()
            log.info(f'cart_item has been successfully deleted')
            return Response({'status': status.HTTP_200_OK,
                                        'detail': 'cart_item has been succesfully deleted'})
        
        else:
            log.error(f'requesting user does not have permission to delete cart_item')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})


class OrderViewSet(viewsets.ModelViewSet):
    """
    suite for performing crud operations on the Order model
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    search_fields = ['sales_staff', 'times_tamp'] 

    def create(self, request):
        """
        creates a new order.
        called by only retail_staff
        """
        log.info(f'instantiating create_order function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, RetailStaff):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'order request data has been validated and new order has been created')
                return Response({"status": status.HTTP_201_CREATED, 'data': serializer.data, 'detail' : 'new order has been created successfully '})
            else:
                log.error(f'order request data could not be validated so new order was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail' : 'new order could not be created due to order_serializer validation errors'})    

        else:
            log.error(f'requesting user does not have permission to create new order')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to create new order'})

    def retrieve(self, request, pk=None):
        """
        handles retrieval of details of an order instance identified by pk .
        view will be accesibble to owner, admin_staff and retail staff who created order
        """
        log.info(f'instantiating get_order function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        
        try:
            log.info(f'retrieving the order instance')
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            log.error(f'order instance cant be found on the database')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested order does not exist'})  

        if request.user.pk == order.sales_staff.pk or isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'order instance has been successfully retrieved')
            serializer = self.serializer_class(order)
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'order has been retrieved successfully'})
                 
        else:
            log.error(f'requesting user does not have permission to retrieve order')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to retrieve order'})


    def list(self, request):
        """
        lists all the orders depending on the requesting user
        accesible to the retail staff who created the order, admin users and owner
        """
        log.info(f'instantiating list_order function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        

        if isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'retrieving the order for {request.user.email}')
            orders = Order.objects.all()
            if orders.count() > 0:
                log.info(f'orders with count {orders.count()}')
                serializer = self.serializer_class(orders, many=True)
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested orders has been retrieved successfully'})
        
        elif isinstance(request.user, RetailStaff):
            log.info(f'retrieving the order for {request.user.email}')
            orders = Order.objects.filter(sales_staff__pk=request.user.pk).filter(date=timezone.today())
            if orders.count() > 0:
                log.info(f'orders with count {orders.count()} have been retrieved')
                serializer = self.serializer_class(orders, many=True)
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested orders has been retrieved successfully'})

        else:
            log.error(f'requesting user does not have permission to retrieve order')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def destroy(self, request, pk=None):
        """
        deletes an instance of an order
        accesible to owner only
        """
        log.info(f'instantiating delete_order function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        

        if isinstance(request.user, Owner):
            log.info(f'retrieving the order for deletion')
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                log.error(f'the requested order does not exist')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested order does not exist'})  

            order.delete()
            log.info(f'order has been successfully deleted')
            return Response({'status': status.HTTP_200_OK,
                                        'detail': 'order has been succesfully deleted'})
        
        else:
            log.error(f'requesting user does not have permission to delete order')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    suite for performing crud operations on the OrderItem model
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    search_fields = ['order', 'drug'] 

    def create(self, request):
        """
        creates a new order_item.
        called by only retail_staff
        """
        log.info(f'instantiating create_order_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, RetailStaff):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'order_item request data has been validated and new order_item has been created')
                return Response({"status": status.HTTP_201_CREATED, 'data': serializer.data, 'detail' : 'new order_item has been created successfully '})
            else:
                log.error(f'order_item request data could not be validated so new order_item was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail' : 'new order_item could not be created due to order_item_serializer validation errors'})    

        else:
            log.error(f'requesting user does not have permission to create new order_item')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to create new order_item'})

    def retrieve(self, request, pk=None):
        """
        handles retrieval of details of an order_item instance identified by pk.
        view will be accesibble to owner, admin_staff and retail staff who created order
        """
        log.info(f'instantiating get_order_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        
        try:
            log.info(f'retrieving the order_item instance')
            order_item = OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            log.error(f'order_item instance cant be found on the database')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested order_item does not exist'})  

        if request.user.pk == order_item.order.sales_staff.pk or isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'order_item instance has been successfully retrieved')
            serializer = self.serializer_class(order_item)
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'order_item has been retrieved successfully'})
                 
        else:
            log.error(f'requesting user does not have permission to retrieve order_item')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to retrieve order_item'})


    def list(self, request):
        """
        lists all the order_items for a particular order
        accesible to the retail staff who created the order, admin users and owner
        """
        log.info(f'instantiating list_order_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        
        pk = request.GET.get('order', None)
        if pk is None:
            log.error(f'pk for order containing order items was not sent along with request data')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'pk for order containing order items was not sent along with request data'})  

        if isinstance(request.user, Owner) or isinstance(request.user, AdminStaff):
            log.info(f'retrieving the order_items for {request.user.email}')
            log.info(f'retrieving the pk for the order containing order items')
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                log.error(f'order instance cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested order containing the order_items does not exist'})  

            log.info(f'order containing order_items has been successfully retrieved')
            order_items = OrderItem.objects.filter(order=order)
            if order_items.count() > 0:
                log.info(f'order_items with count {order_items.count()} have been retrieved')
                serializer = self.serializer_class(order_items, many=True)
                log.info(f'order_items with count {order_items.count()} have been retrieved')
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested order_items have been retrieved successfully'})
        
        elif isinstance(request.user, RetailStaff):
            log.info(f'retrieving the order_items for {request.user.email}')
            log.info(f'retrieving the pk for the order containing order items')
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                log.error(f'order instance cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested order containing the order_items does not exist'})  

            if request.user.pk == order.sales_staff.pk:
                log.info(f'order containing order_items has been successfully retrieved')
                order_items = OrderItem.objects.filter(order=order)
                if order_items.count() > 0:
                    serializer = self.serializer_class(order_items, many=True)
                    log.info(f'order_items with count {order_items.count()} have been retrieved')
                    return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail': 'the requested order_items have been retrieved successfully'})

        else:
            log.error(f'requesting user does not have permission to retrieve order_items')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def destroy(self, request, pk=None):
        """
        deletes an instance of an order_item
        accesible to owner only
        """
        log.info(f'instantiating delete_order_item function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        

        if isinstance(request.user, Owner):
            log.info(f'retrieving the order_item for deletion')
            try:
                order_item = OrderItem.objects.get(pk=pk)
            except OrderItem.DoesNotExist:
                log.error(f'the requested order_item does not exist')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'the requested order_item does not exist'})  

            order_item.delete()
            log.info(f'order_item has been successfully deleted')
            return Response({'status': status.HTTP_200_OK,
                                        'detail': 'order_item has been succesfully deleted'})
        
        else:
            log.error(f'requesting user does not have permission to delete order_item')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})
