from users.models import Owner, AdminStaff, RetailStaff
from django.test import TestCase, Client as Clientt
from rest_framework import status
from datetime import date


class TestOwnerView(TestCase):
    """
    test suite for the owner_viewset
    """
    def setUp(self):
        """Run once before all tests"""
        self.client = Clientt()
        for owner in Owner.objects.all():
            owner.delete()

    def tearDown(self):
        """Run once after all tests"""
        self.client = None

    def test_create_owner_view(self):
        """
        tests the create_owner url 
        send a post request containing the neccesary data to '/api/v1/owner/'
        """

        staff = self.client.post('/api/v1/login/', data={'email':'kanu@mail.com', 'password':'kanu1234'})
        self.assertEqual(staff.status_code, 201, "Could not login admin user")
        token = staff.data['access']
        cookies = {'jwt': token}

        self.client.cookies.load(cookies)
        data = {'email' : 'participant@gmail.com', 'is_staff': False, 'is_active':False, 'first_name':'participant', 'last_name':'kanu', 'username':'participant', 'date_of_birth':date.today(), 'password':'12345678', 'confirm_password': '12345678'}
        response = self.client.post('/api/v1/owner/', data=data)
        self.assertEqual(response.data['status'], status.HTTP_201_CREATED, "Could not create owner")
        self.assertEqual(str(Owner.objects.all().count()), '1')
        owner = Owner.objects.get(email=data['email'])
        self.assertEqual(owner.first_name, data['first_name'])

#         """
#         testing the list participants route
#         sends a get request to '/api/v1/participant/
#         also tests login feature
#         """
#         data = {'email': 'participant@gmail.com', 'is_staff': False, 'is_active':True, 'first_name':'participant', 'last_name':'kanu', 'username':'participant', 'date_of_birth':date.today(), 'password':'12345678', 'confirm_password': '12345678'}
#         data1 = {'email': 'participant1@gmail.com', 'is_staff': False, 'is_active':True, 'first_name':'participant1', 'last_name':'kanu1', 'username':'participant1', 'date_of_birth':date.today(), 'password':'12345678', 'confirm_password': '12345678'}
#         data2 = {'email': 'participant2@gmail.com', 'is_staff': False, 'is_active':True, 'first_name':'participant2', 'last_name':'kanu2', 'username':'participant2', 'date_of_birth':date.today(), 'password':'12345678', 'confirm_password': '12345678'}
#         clients = [data, data1, data2]
#         for item in clients:
#             self.client.post('/api/v1/participant/', data=item)
#         self.assertEqual(Participant.objects.all().count(), 3)
#         response = self.client.post('/api/v1/login/', data={'email':data['email'], 'password': data['password']})
#         self.assertEqual(response.status_code, 201, "Could not create test client")
#         token = response.data['access']
#         cookies = {'jwt': token}
#         self.client.cookies.clear()
#         response = self.client.get('/api/v1/participant/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         self.client.cookies.load(cookies)
#         response = self.client.get('/api/v1/participant/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         user = Participant.objects.get(email=data['email'])
#         user.is_staff = True
#         user.save()
#         response = self.client.get('/api/v1/participant/')
#         self.assertEqual(response.data['status'], status.HTTP_202_ACCEPTED, "Could not create test scientist")
#         self.assertEqual(len(response.data['data']), 3,  "Could not retrieve test client")

#         """
#         tests the retrieve participant route
#         send a get request to '/api/v1/participant/{pk}/'
#         pk identifies the participant to
#         """
#         self.client.cookies.clear()
#         response = self.client.get(f'/api/v1/participant/{user.id}/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         self.client.cookies.load(cookies)
#         response = self.client.get(f'/api/v1/participant/{user.id}/')
#         self.assertEqual(response.data['status'], status.HTTP_200_OK, 'You dont have permission access this resource')

#         """
#         testing partial update of a participant
#         sends a patch request to '/api/v1/participant/{pk}/'
#         pk identifies the participant to
#         """
#         update_data = {'email': 'participant@gmail.com', 'is_staff': False, 'is_active':True, 'first_name':'participant', 'last_name':'idan', 'username':'participant', 'date_of_birth':date.today(), 'password':'12345678', 'confirm_password': '12345678'}
#         self.client.cookies.clear()
#         response = self.client.patch(f'/api/v1/participant/{user.id}/', content_type='application/json', data=update_data)
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         self.client.cookies.load(cookies)
#         response = self.client.patch(f'/api/v1/participant/{user.id}/', content_type='application/json', data=update_data)
#         self.assertEqual(response.data['status'], status.HTTP_200_OK, 'You dont have permission access this resource')
#         user = Participant.objects.get(email=update_data['email'])
#         self.assertEqual(user.is_active, False, 'You dont have permission access this resource')
#         self.assertEqual(user.last_name, 'idan', 'You dont have permission access this resource')

#         """
#         testing delete a participant
#         sends a patch request to '/api/v1/participant/{pk}/'
#         pk identifies the participant to
#         """
#         self.client.cookies.clear()
#         response = self.client.delete(f'/api/v1/participant/{user.id}/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         self.client.cookies.load(cookies)
#         response = self.client.delete(f'/api/v1/participant/{user.id}/')
#         self.assertEqual(response.data['status'], status.HTTP_200_OK, 'You dont have permission access this resource')
#         self.assertEqual(Participant.objects.all().count(), 2)
#         self.assertEqual(Participant.objects.filter(email=user.email).exists(), False, 'You dont have permission access this resource')



# class TestConsultantView(TestCase):
#     """
#     test suite for the consultant_view
#     uses the ClientFactory class
#     """
#     def setUp(self):
#         """Run once before all tests"""
#         self.client = Clientt()
#         for client in Consultant.objects.all():
#             client.delete()

#     def tearDown(self):
#         """Run once after all tests"""
#         self.client = None

#     def test_create_consultant_view(self):
#         """
#         tests the create_consultant url 
#         send a post request containing the neccesary data to '/api/v1/consultant/'
#         """
#         data = {'email':'consultant@gmail.com', 'is_staff': False, 'is_active': False, 'first_name':'consultant', 'last_name':'taiwo', 'username':'consultant', 'date_of_birth':date.today(), 'profession':'OnG', 'years_of_experience':3, 'password':'12345678', 'confirm_password': '12345678'}
#         response = self.client.post('/api/v1/consultant/', data=data)
#         self.assertEqual(response.data['status'], status.HTTP_201_CREATED, "Could not create test client")
#         self.assertEqual(Consultant.objects.all().count(), 1)
#         client = Consultant.objects.get(email=data['email'])
#         self.assertEqual(client.first_name, data['first_name'])

#     def test_list_consultant_view(self):
#         """
#         tests the list_consultant url
#         sends a get request to '/api/v1/consultant/'
#         also tests the consultant login feature
#         """
#         data = {'email':'consultant@gmail.com', 'is_staff': False, 'is_active': False, 'first_name':'consultant', 'last_name':'taiwo', 'username':'consultant', 'date_of_birth':date.today(), 'profession':'OnG', 'years_of_experience':3, 'password':'12345678', 'confirm_password': '12345678'}
#         data1 = {'email':'consultant1@gmail.com', 'is_staff': False, 'is_active': False, 'first_name':'consultant1', 'last_name':'taiwo1', 'username':'consultant1', 'date_of_birth':date.today(), 'profession':'OnG', 'years_of_experience':3, 'password':'12345678', 'confirm_password': '12345678'}
#         data2 = {'email':'consultant2@gmail.com', 'is_staff': False, 'is_active': False, 'first_name':'consultant2', 'last_name':'taiwo2', 'username':'consultant2', 'date_of_birth':date.today(), 'profession':'OnG', 'years_of_experience':3, 'password':'12345678', 'confirm_password': '12345678'}
#         clients = [data, data1, data2]
#         for item in clients:
#             self.client.post('/api/v1/consultant/', data=item)
#         self.assertEqual(Consultant.objects.all().count(), 3)
#         response = self.client.post('/api/v1/login/', data={'email':data['email'], 'password': data['password']})
#         self.assertEqual(response.status_code, 201, "Could not create test client")
#         self.assertIsNotNone(response.data['access'])
#         token = response.data['access']
#         cookies = {'jwt': token}
#         self.client.cookies.clear()
#         response = self.client.get('/api/v1/consultant/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         self.client.cookies.load(cookies)
#         response = self.client.get('/api/v1/consultant/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         user = Consultant.objects.get(email=data['email'])
#         user.is_staff = True
#         user.save()
#         response = self.client.get('/api/v1/consultant/')
#         self.assertEqual(response.data['status'], status.HTTP_202_ACCEPTED, "Could not retrieve test client")
#         self.assertEqual(len(response.data['data']), 3,  "Could not retrieve test client")

#         """
#         now testing the retrieve consultant route
#         sends a get request to '/api/v1/consultant/{pk}/'
#         pk identifies the consultant instance to retrieve
#         """
#         self.client.cookies.clear()
#         response = self.client.get(f'/api/v1/consultant/{user.pk}/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         self.client.cookies.load(cookies)
#         user.is_staff = False
#         user.save()
#         response = self.client.get(f'/api/v1/consultant/{user.pk}/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         user = Consultant.objects.get(email=data['email'])
#         user.is_staff = True
#         user.save()
#         response = self.client.get(f'/api/v1/consultant/{user.pk}/')
#         self.assertEqual(response.data['status'], status.HTTP_200_OK, "Could not retrieve test client")

#         """
#         testing delete a consultant
#         sends a patch request to '/api/v1/consultant/{pk}/'
#         pk identifies the participant to
#         """
#         self.client.cookies.clear()
#         response = self.client.delete(f'/api/v1/consultant/{user.id}/')
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not retrieve test client")
#         self.client.cookies.load(cookies)
#         response = self.client.delete(f'/api/v1/consultant/{user.id}/')
#         self.assertEqual(response.data['status'], status.HTTP_200_OK, 'You dont have permission access this resource')
#         self.assertEqual(Consultant.objects.all().count(), 2)
#         self.assertEqual(Consultant.objects.filter(email=user.email).exists(), False, 'You dont have permission access this resource')


# class TestUserLogoutView(TestCase):
#     """
#     test suite for the user_logout view
#     """
#     def test_participant_logout_view(self):
#         """
#         tests the participant logout view
#         sends a post request to '/api/v1/logout/
#         """
#         data = {'email': 'participant@gmail.com', 'is_staff': True, 'is_active':True, 'first_name':'participant', 'last_name':'kanu', 'username':'participant', 'date_of_birth':date.today(), 'password':'12345678', 'confirm_password': '12345678'}
#         response = self.client.post('/api/v1/participant/', data=data)
#         self.assertEqual(response.data['status'], status.HTTP_201_CREATED, "Could not create test client")
#         response = self.client.post('/api/v1/login/', data={'email':data['email'], 'password': data['password']})
#         self.assertEqual(response.status_code, 201, "Could not create test client")
#         token = response.data['access']
#         cookies = {'jwt': token}
#         self.client.cookies.clear()
#         response = self.client.post('/api/v1/logout/', cookies=cookies)
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not logout test client")
#         self.client.cookies.load(cookies)
#         response = self.client.post('/api/v1/logout/', cookies=cookies)
#         self.assertEqual(response.data['status'], status.HTTP_200_OK, "Could not logout test client")
#         self.assertEqual(len(response.cookies), 0, "Could not logout test client")

#     def test_consultant_logout_view(self):
#         """
#         tests the consultant logout view
#         sends a post request to '/api/v1/logout/
#         """
#         data = {'email':'consultant@gmail.com', 'is_staff':True, 'is_active':True, 'first_name':'consultant', 'last_name':'taiwo', 'username':'consultant', 'date_of_birth':date.today(), 'profession':'OnG', 'years_of_experience':3, 'password':'12345678', 'confirm_password': '12345678'}
#         response = self.client.post('/api/v1/consultant/', data=data)
#         self.assertEqual(response.data['status'], status.HTTP_201_CREATED, "Could not create test client")
#         response = self.client.post('/api/v1/login/', data={'email':data['email'], 'password': data['password']})
#         self.assertEqual(response.status_code, 201, "Could not create test client")
#         token = response.data['access']
#         cookies = {'jwt': token}
#         self.client.cookies.clear()
#         response = self.client.post('/api/v1/logout/', cookies=cookies)
#         self.assertEqual(response.data['status'], status.HTTP_403_FORBIDDEN, "Could not logout test client")
#         self.client.cookies.load(cookies)
#         response = self.client.post('/api/v1/logout/', cookies=cookies)
#         self.assertEqual(response.data['status'], status.HTTP_200_OK, "Could not logout test client")
#         self.assertEqual(len(response.cookies), 0, "Could not logout test client")
