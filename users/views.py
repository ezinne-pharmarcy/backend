from django.shortcuts import render

# Create your views here.
from users.models import Owner, AdminStaff, RetailStaff
from rest_framework.response import Response
from users.serializers import OwnerSerializer, AdminSerializer, RetailSerializer, UserLoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import get_user
from rest_framework import status, viewsets
from datetime import datetime, timedelta
from django.utils import timezone
import logging

log = logging.getLogger('main')

class OwnerViewSet(viewsets.ModelViewSet):
    """
    a viewset suite to handle crud operations on owner model
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def create(self, request):
        """
        creates a new owner instance using the request data
        accesible to app_admin users
        """
        log.info(f'instantiating create_owner function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if request.user.is_staff == True: #isinstance(request.user, AppPersonnel) and request.user.is_app_admin == True:
            log.info(f'instantiating owner_serializer class with request data')
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'owner request data has been validated and new owner has been created')
                return Response({'status': status.HTTP_201_CREATED, 'data': serializer.data, 'detail': 'owner has been created successfully'})
            else:
                log.error(f'owner request data could not be validated so new owner was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail': 'owner could not be created due to serializer validation errors'})
        else:
            log.error(f'requesting user does not have permission to create new owner')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission access this resource'})

    def list(self, request):
        """
        retrieves a list of all available owners on the platform
        accesible to only app_admin
        """
        log.info(f'instantiating list_owners function')
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

        if (isinstance(request.user, Owner) and request.user.pk == pk) or ((isinstance(request.user, Owner) and request.user.is_store_admin == True)):
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

        if (isinstance(request.user, Owner) and request.user.pk == pk) or (instance(request.user, Owner) and request.user.is_store_admin == True):
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


class AdminStaffViewSet(viewsets.ModelViewSet):
    """
    a viewset suite to handle crud operations on admin_staff model
    """
    queryset = AdminStaff.objects.all()
    serializer_class = AdminSerializer

    def create(self, request):
        """
        creates a new admin_staff instance using the request data
        accesible to app_admin users
        """
        log.info(f'instantiating create_admin_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, Owner) and request.user.is_store_admin == True:
            log.info(f'instantiating admin_staff_serializer class with request data')
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'admin_staff request data has been validated and new admin_staff has been created')
                return Response({'status': status.HTTP_201_CREATED, 'data': serializer.data, 'detail': 'admin_staff has been created successfully'})
            else:
                log.error(f'admin_staff request data could not be validated so new admin_staff was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail': 'admin_staff could not be created due to serializer validation errors'})
        else:
            log.error(f'requesting user does not have permission to create new admin_staff')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission access this resource'})

    def list(self, request):
        """
        retrieves a list of all available admin_staff on the platform
        accesible to only app_admin
        """
        log.info(f'instantiating list_admin_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            users = self.queryset
            serializer = self.serializer_class(users, many=True)
            log.info(f'list of admin_staff has been retrieved successfully')
            return Response({"status": status.HTTP_202_ACCEPTED, 'data': serializer.data, 'detail': 'list of admin_staff has been retrieved'})
        
        log.error(f'requesting user does not have permission to list admin_staff')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission access this resource'})

    def retrieve(self, request, pk=None):
        """
        retrieves a particular admin_staff instance identified by pk
        accesible to either app_admin or the user themselve
        """
        log.info(f'instantiating retrieve_admin_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, AdminStaff) and request.user.pk == pk) or (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            log.info(f'retrieving the admin_staff instance')
            try:
                user = AdminStaff.objects.get(pk=pk)
            except AdminStaff.DoesNotExist:
                log.error(f'admin_staff instance cant be found on the database')
                return Response({'status' : status.HTTP_400_BAD_REQUEST, 'detail': 'admin_staff does not exist on out database'})
            serializer = self.serializer_class(user)        
            log.info(f'admin_staff instance has been retrieved successfully')
            return Response({"status" : status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'the requested admin_staff has been retrieved'})
        

        log.error(f'requesting user does not have permission to retrieve admin_staff instance')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to access this resource'})

    def partial_update(self, request, pk=None):
        """
        updates an admin_staff instance with the request data
        only accesible to the user and app admin
        """
        log.info(f'instantiating update_admin_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, AdminStaff) and request.user.pk == pk):
            try:
                user = AdminStaff.objects.get(pk=pk)
            except AdminStaff.DoesNotExist:
                log.error(f'admin_staff instance to be updated cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'admin_staff does not exist on the database'})

            serializer = self.serializer_class(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                log.info(f'admin_staff has been updated successfully')
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'admin_staff has been updated successfully'})
            
            log.error(f'admin_staff request data could not be validated so new admin_staff was not updated')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail' : 'admin_staff could not be updated due to serializer validation errors'})
        
        log.error(f'requesting user does not have permission to update admin_staff instance')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to access this resource'})
        
    def destroy(self, request, pk=None):
        """
        deletes an instance of a admin_staff (identified by pk).
        accesible to admin  
        """
        log.info(f'instantiating delete_admin_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, AdminStaff) and request.user.pk == pk) or (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            try:
                user = AdminStaff.objects.get(pk=pk)
            except AdminStaff.DoesNotExist:
                log.error(f'admin_staff instance to be deleted cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'admin_staff does not exist on the database'})


            user.delete()
            log.info(f'admin_staff instance has been deleted successfully')
            return Response({'status': status.HTTP_200_OK,
                            'detail': 'admin_staff has been succesfully deleted'})
        else:        
            log.error(f'requesting user does not have permission to delete admin_staff instance')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

class RetailStaffViewSet(viewsets.ModelViewSet):
    """
    a viewset suite to handle crud operations on retail_staff model
    """
    queryset = RetailStaff.objects.all()
    serializer_class = RetailSerializer

    def create(self, request):
        """
        creates a new retail_staff instance using the request data
        accesible to app_admin users
        """
        log.info(f'instantiating create_retail_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if isinstance(request.user, Owner) and request.user.is_store_admin == True:
            log.info(f'instantiating retail_staff_serializer class with request data')
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'retail_staff request data has been validated and new retail_staff has been created')
                return Response({'status': status.HTTP_201_CREATED, 'data': serializer.data, 'detail': 'retail_staff has been created successfully'})
            else:
                log.error(f'retail_staff request data could not be validated so new admin_staff was not created')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail': 'retail_staff could not be created due to serializer validation errors'})
        else:
            log.error(f'requesting user does not have permission to create new retail_staff')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission access this resource'})

    def list(self, request):
        """
        retrieves a list of all available retail_staff on the platform
        accesible to only app_admin and store admin
        """
        log.info(f'instantiating list_retail_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            users = self.queryset
            serializer = self.serializer_class(users, many=True)
            log.info(f'list of retail_staff has been retrieved successfully')
            return Response({"status": status.HTTP_202_ACCEPTED, 'data': serializer.data, 'detail': 'list of retail_staff has been retrieved'})
        
        log.error(f'requesting user does not have permission to list retail_staff')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission access this resource'})

    def retrieve(self, request, pk=None):
        """
        retrieves a particular retail_staff instance identified by pk
        accesible to either app_admin or the user themselve
        """
        log.info(f'instantiating retrieve_retail_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, RetailStaff) and request.user.pk == pk) or (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            log.info(f'retrieving the retail_staff instance')
            try:
                user = RetailStaff.objects.get(pk=pk)
            except RetailStaff.DoesNotExist:
                log.error(f'retail_staff instance cant be found on the database')
                return Response({'status' : status.HTTP_400_BAD_REQUEST, 'detail': 'retail_staff does not exist on out database'})
            serializer = self.serializer_class(user)        
            log.info(f'retail_staff instance has been retrieved successfully')
            return Response({"status" : status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'the requested retail_staff has been retrieved'})
        

        log.error(f'requesting user does not have permission to retrieve retail_staff instance')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to access this resource'})

    def partial_update(self, request, pk=None):
        """
        updates an retail_staff instance with the request data
        only accesible to the user and app admin
        """
        log.info(f'instantiating update_retail_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, RetailStaff) and request.user.pk == pk):
            try:
                user = RetailStaff.objects.get(pk=pk)
            except RetailStaff.DoesNotExist:
                log.error(f'retail_staff instance to be updated cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'retail_staff does not exist on the database'})

            serializer = self.serializer_class(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                log.info(f'retail_staff has been updated successfully')
                return Response({"status": status.HTTP_200_OK, 'data': serializer.data, 'detail' : 'retail_staff has been updated successfully'})
            
            log.error(f'retail_staff request data could not be validated so new admin_staff was not updated')
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors, 'detail' : 'retail_staff could not be updated due to serializer validation errors'})
        
        log.error(f'requesting user does not have permission to update retail_staff instance')
        return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'You dont have permission to access this resource'})
        
    def destroy(self, request, pk=None):
        """
        deletes an instance of a retail_staff (identified by pk).
        accesible to admin  
        """
        log.info(f'instantiating delete_retail_staff function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           

        if (isinstance(request.user, RetailStaff) and request.user.pk == pk) or (isinstance(request.user, Owner) and request.user.is_store_admin == True):
            try:
                user = RetailStaff.objects.get(pk=pk)
            except RetailStaff.DoesNotExist:
                log.error(f'retail_staff instance to be deleted cant be found on the database')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'retail_staff does not exist on the database'})


            user.delete()
            log.info(f'retail_staff instance has been deleted successfully')
            return Response({'status': status.HTTP_200_OK,
                            'detail': 'retail_staff has been succesfully deleted'})
        else:        
            log.error(f'requesting user does not have permission to delete retail_staff instance')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you dont have the permission to perform this action'})

class LoginView(APIView):
    """ 
    User login and authentication view.
    """

    def post(self, request):
        """Authenticates and logs in a user."""
        log.info(f'instantiating user_login function')
        serializer = UserLoginSerializer(data=request.data)
        log.info(f'validating login request data via the user_login_serializer class')
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            log.info(f'retrieving the requesting user for loggin in')
            try:
                user = Owner.objects.get(email=email)
            except:
                
                try:
                    user = RetailStaff.objects.get(email=email)
                except:
                    
                    try:
                        user = AdminStaff.objects.get(email=email)
                    except:
                        user = None
                            
            response = Response()
            if user is None:
                log.error(f'requesting user could not be logged in because the user cant be found on the database')
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'detail': 'This user does not exit'})
            
            if not user.check_password(serializer.validated_data.get('password')):
                log.error(f'requesting user could not be logged in because the inputed password is incorrect')
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'detail': 'This login details entered are incorrect'})
            
            refresh = RefreshToken.for_user(user)
            log.info(f'requesting user has been retrieved successfully')

            """ checking already logged in """
            expiration = user.last_login + timedelta(minutes=5)
            if user.is_authenticated == True:
                if timezone.now() < expiration:
                    log.error(f'requesting user is already logged in')
                    return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'This user is already logged in'})
                
            """ updating the user's last-login attribute and authentication status """
            log.info(f'updating the last_login attribute for the requesting user')
            user.last_login = datetime.now()
            user.is_authenticated = True
            user.save()

            """ adding the jwt token to the cookie """
            log.info(f'setting the token for logged in user to the request cookie')
            response.set_cookie(key='jwt', value=refresh.access_token, httponly=True)

            response.data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'status': status.HTTP_202_ACCEPTED
            }
            response.status_code = 201

            log.info(f'requesting user has been logged in successfully')
            return response



        log.error(f'requesting user could not be logged in due to validation errors with inputed date')
        return Response({"status": status.HTTP_400_BAD_REQUEST,
                         "error": serializer.errors, 'detail' : 'requesting user could not be logged in due to validation errors with inputed date'})


class LogoutView(APIView):
    """ 
    User logout view.
    """
    def post(self, request):
        """ Logs out the current user and deletes session """
        log.info(f'instantiating logout function')
        log.info(f'validating requesting user')
        request.user = get_user(request)
        if request.user is None:
            log.error(f'requesting user could not be validated')
            return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'you need to login to access this resource'})           
        response = Response()
        
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        request.user.is_authenticated = False
        request.user.save()

        return Response({'status': status.HTTP_200_OK, 'detail': 'user has been logged out successfully'})
