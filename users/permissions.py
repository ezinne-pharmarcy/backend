import jwt
from django.conf import settings
from users.models import Owner, AdminStaff, RetailStaff
from datetime import datetime, timedelta
from django.utils import timezone
import logging

log = logging.getLogger('main')


def get_user(request):
        """
        retrieves the requesting user instance from the jwt cookie
        """ 
        log.info(f"verifying requesting user's permissions via the get_user function")
        token = request.COOKIES.get('jwt', None)
        if token is None:
            log.error(f"verification failed due to absence of jwt token in request cookie")
            return None
            
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            log.error(f"verification failed due to jwt token issues")
            user = None

        log.info(f"jwt token & payload sorted successsfully, now retrieveing requesting user")
        try:
            user = Owner.objects.get(id=payload['user_id'])
        except:

            try: 
                user = AdminStaff.objects.get(id=payload['user_id'])
            except:

                try:
                    user = RetailStaff.objects.get(id=payload['user_id'])
                except:
                    user = None                

        if user is not None:
            if user.is_authenticated == False:
                log.error(f"verification failed because requesting user is not logged in")
                return None
                                   
            expiration = user.last_login + timedelta(minutes=5)
            if timezone.now() < expiration:    
                user.last_login = datetime.now()
                user.save()
                log.info(f"requesting user has been retrieved and verified successfully")
                return user
            else:
                user.is_authenticated = False
                user.save()
                log.error(f"verification failed because requesting user's session has expired")
                return None           
        else:
            log.error(f"verification failed because requesting user couldn't be found on the database")
            return None


