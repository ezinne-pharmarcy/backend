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
from users.models import Owner
import logging

log = logging.getLogger('main')

class MedicationViewSet(viewsets.ModelViewSet):
    """
    a viewset suite to handle crud operations on medication model
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def create(self, request):
        """
        creates a new medication instance using the request data
        accesible to store_admin and app_admin users
        """
        log.info(f'instantiating create_medication function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            log.info(f'instantiating medication_serializer class with request data')
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'medication request data has been validated and new medication has been created')
                return Response({'status': status.HTTP_201_CREATED, 'data': serializer.data, 'detail': 'medication has been created successfully'})
            else:
                log.error(f'medication request data could not be validated so new medication was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail': 'medication could not be created due to serializer validation errors'})
        else:
            log.error(f'requesting user does not have permission to create new medication')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission access this resource'})

    def list(self, request):
        """
        retrieves a list of all available medication on the platform
        accesible to only app_admin
        """
        log.info(f'instantiating list_medications function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            users = self.queryset
            serializer = self.serializer_class(users, many=True)
            log.info(f'list of owners has been retrieved successfully')
            return Response({"status": status.HTTP_202_ACCEPTED, 'data': serializer.data, 'detail': 'list of owners has been retrieved'})
        
        log.error(f'requesting user does not have permission to list owners')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission access this resource'})

    def retrieve(self, request, pk=None):
        """
        retrieves a particular owner instance identified by pk
        accesible to either app_admin or the user themselve
        """
        log.info(f'instantiating retrieve_owner function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, Owner) and request.user.pk == pk):
            log.info(f'retrieving the owner instance')
            try:
                user = Owner.objects.get(pk=pk)
            except Owner.DoesNotExist:
                log.error(f'owner instance cant be found on the database')
                return Response({'status' : status.HTTP_400_BAD_REQUEST, 'detail': 'owner does not exist on the database'})
            serializer = self.serializer_class(user)        
            log.info(f'owner instance has been retrieved successfully')
            return Response({"status" : status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'the requested owner has been retrieved'})
        

        log.error(f'requesting user does not have permission to retrieve owner instance')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to access this resource'})

    def partial_update(self, request, pk=None):
        """
        updates a owner instance with the request data
        only accesible to the user and app admin
        """
        log.info(f'instantiating update_owner function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, Owner) and request.user.pk == pk):
            try:
                user = Owner.objects.get(pk=pk)
            except Owner.DoesNotExist:
                log.error(f'owner instance to be updated cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'owner does not exist on out database'})

            serializer = self.serializer_class(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                log.info(f'owner has been updated successfully')
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'owner has been updated successfully'})
            
            log.error(f'owner request data could not be validated so new owner was not updated')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail' : 'owner could not be updated due to serializer validation errors'})
        
        log.error(f'requesting user does not have permission to update owner instance')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to access this resource'})
        
    def destroy(self, request, pk=None):
        """
        deletes an instance of an admin_staff (identified by pk).
        accesible to admin  
        """
        log.info(f'instantiating delete_admin function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, Owner) and request.user.pk == pk):
            try:
                user = Owner.objects.get(pk=pk)
            except Owner.DoesNotExist:
                log.error(f'owner instance to be deleted cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'owner does not exist on our database'})


            user.delete()
            log.info(f'owner instance has been deleted successfully')
            return Response({'status': status.HTTP_200_OK,
                            'detail': 'owner has been succesfully deleted'})
        else:        
            log.error(f'requesting user does not have permission to delete owner instance')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})
