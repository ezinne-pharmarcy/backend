from stock.models import Medication
from rest_framework.response import Response
from stock.serializers import MedicationSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import get_user
from rest_framework import status, viewsets
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import Owner, RetailStaff, AdminStaff
from sales.models import Order, OrderItem
from sales.serializers import OrderSerializer, OrderItemSerializer
import logging

log = logging.getLogger('main')

class OrderViewSet(viewsets.ModelViewSet):
    """
    suite for performing crud operations on the Order model
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request):
        """
        creates a new test order.
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
        handles retrieval of details of a order instance identified by pk .
        view will be accesibble to owner, admin_staff and retail staff who created order
        """
        log.info(f'instantiating list_order function')
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
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to create new order'})


    def list(self, request):
        """
        lists all the test orders placed by a client.
        accesible to the client, and app admin.
        when called by the app admin, the client of interest will be passed alongside the request data
        """
        request.user = get_user(request)
        if request.user is None:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, Client):
            try:
                orders = ClientTestOrder.objects.filter(client=request.user)
            except ClientTestOrder.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_orders do not exist'})  
            serializer = self.serializer_class(orders, many=True)
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data})
        
        elif request.user.is_staff == True:  
            try:
                client = Client.objects.get(pk=request.data.get('client'))
            except Client.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client does not exist'})  

            try:
                orders = ClientTestOrder.objects.filter(client=client)
            except ClientTestOrder.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_orders do not exist'})  

            serializer = self.serializer_class(orders, many=True)
            # look out for an error in this view ddue to difficulty processing the list data by the serializer
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data})

        else:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def destroy(self, request, pk=None):
        """
        deletes an instance of an order by a client
        accesible to admin  
        """
        request.user = get_user(request)
        if request.user is None:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if request.user.is_staff == True:
            try:
                order = ClientTestOrder.objects.get(pk=pk)
            except ClientTestOrder.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_order does not exist'})  

            order.delete()
            return Response({'status': status.HTTP_200_OK,
                                        'detail': 'order has been succesfully deleted'})
        
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})


class ClientTestOrderItemViewSet(viewsets.ModelViewSet):

    """
    suite for performing crud operations on the client test order item class
    """
    queryset = ClientTestOrderItem.objects.all()
    serializer_class = ClientTestOrderItemSerializer
    search_fields = ['order']

    def create(self, request):
        """
        handles creation of a new client test order item instance.
        uses the request data to create instance.
        accesible to clients.
        view also updates the total_price attribute of the order object to which the order_item belongs
        """
        request.user = get_user(request)
        if request.user is None:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, Client):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                try:
                    order = ClientTestOrder.objects.get(pk=request.data.get('order'))
                except ClientTestOrder.DoesNotExist:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_order does not exist'})  

                try:
                    test = Investigation.objects.get(pk=request.data.get('investigation'))   
                except Investigation.DoesNotExist:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested investigation does not exist'})  

                if int(request.data['quantity']) > 1:
                    order.total_price =+ ((test.price) * int(request.data['quantity']))
                else:
                    order.total_price =+ test.price
                order.save()
                return Response({"status": status.HTTP_201_CREATED, 'data': serializer.data})
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors})               
        else:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def list(self, request):
        """
        lists all the test order items for a particular client's order.
        accesible to the client, lab admin and scientist.
        the order instance is obtained from the request data.
        """
        request.user = get_user(request)
        if request.user is None:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        
        try:
            order = ClientTestOrder.objects.get(pk=request.GET.get('order'))
        except ClientTestOrder.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_order does not exist'})  
        
        if (isinstance(request.user, Client) and request.user.pk == order.client.pk) or isinstance(request.user, Scientist):
            try:
                order_items = ClientTestOrderItem.objects.filter(order=order)
            except ClientTestOrderItem.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_order items do not exist'})              
            
            serializer = self.serializer_class(order_items, many=True)
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data})
        else:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def partial_update(self, request, pk=None):
        """
        view for updating an order item instance identified by pk
        view will be called by a scientist and lab admin following sample collection/completion of an investigation
        view updates the sample_collection_status and sample_collection_date attributes of the instance
        this view is for updating a single instance
        """    
        request.user = get_user(request)
        if request.user is None:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, Scientist):
            try:
                order_item = ClientTestOrderItem.objects.get(pk=pk)
            except ClientTestOrderItem.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_order_item does not exist'})              

            order_item.sample_collection_status = True
            order_item.sample_collection_date = timezone.localdate()
            order_item.save()
            serializer = self.serializer_class(order_item)
            return Response({"status": status.HTTP_201_CREATED, 'data': serializer.data})
        
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def retrieve(self, request, pk=None):
        """
        handles retrieval of a particular order item instance identified by pk
        accesible to the client, lab & app admin, and scientist
        """
        request.user = get_user(request)
        if request.user is None:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, Client) or isinstance(request.user, Scientist) or request.user.is_staff == True or request.user.is_lab_admin == True:
            try:
                order_item = ClientTestOrderItem.objects.get(pk=pk)
            except ClientTestOrderItem.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_order_item does not exist'})              

            serializer = self.serializer_class(order_item)
            return Response({"status": status.HTTP_200_OK, 'data': serializer.data})
        
        else:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

    def destroy(self, request, pk=None):
        """
        deletes an instance of an order item (identified by pk) by a client
        accesible to admin  
        """
        request.user = get_user(request)
        if request.user is None:
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if request.user.is_staff == True:
            try:
                order_item = ClientTestOrderItem.objects.get(pk=pk)
            except ClientTestOrderItem.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': 'the requested client_test_order_item does not exist'})              

            order_item.delete()
            return Response({'status': status.HTTP_200_OK,
                                        'detail': 'order item has been succesfully deleted'})
        
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

