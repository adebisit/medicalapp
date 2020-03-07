from rest_framework import serializers


class PatientSerializer(serializers.Serializer):
    full_name = serializers.CharField(source='get_name')
    patient_url = serializers.URLField(source='get_patient_view_url')
    age = serializers.CharField(source='get_age')
    weight_status = serializers.CharField(source='get_weight_status')
    blood_group = serializers.CharField(source='get_blood_group_display')
    genotype = serializers.CharField(source='get_genotype_display')