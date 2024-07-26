import logging
from rest_framework import serializers
from stock.models import Medication
import bleach

log = logging.getLogger('main')

class MedicationSerializer(serializers.ModelSerializer):
    """
    This class defines the serializer for the medication model.
    """
    class Meta:
        model = Medication
        fields = '__all__'
    
    def validate(self, data):
        """
        Validates request data.
        """
        log.info(f'validating medication data from request')
        
        name = data.get('name', None)
        if name is not None:
            name = bleach.clean(name, strip=True)
            if len(name) > 100:
                log.error(f'validation of medication data from request failed because name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        price = data.get('price', None)
        if price is not None:
            price = bleach.clean(price, strip=True)
            if len(price) > 50:
                log.error(f'validation of medication data from request failed because price exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        quantity = data.get('quantity', None)
        if type(quantity) != type(12):
            log.error(f'validation of medication data from request failed because quantity data type is incorrect')
            raise serializers.ValidationError("You have inputed invalid characters")   

        if name != data.get('name', None) or price != data.get('price', None):
            log.error(f'validation of medication data from request failed because a field is missing')
            raise serializers.ValidationError("You have entered invalid characters.")
        
        log.info(f'retail_staff data has been validated')
        return data

    def create(self, validated_data):
        """
        creates a new medication.
        """
        log.info(f'creating a new medication using the request data via the medication_serializer class')
        log.info(f'new medication has been created successfully via the medication_serializer class')
        return super(MedicationSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing medication.
        """
        log.info(f'updating an existing medication using the request data via the medication_serializer class')
        log.info(f'existing medication has been updated successfully via the medication_serializer class')
        return super(MedicationSerializer, self).update(instance, validated_data)
