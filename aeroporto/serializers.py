from rest_framework import serializers
from .models import Passageiro, Voo, Portao

class PassageiroSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nome = serializers.CharField()
    cpf = serializers.CharField()
    voo_id = serializers.CharField()
    status_checkin = serializers.ChoiceField(choices=["pendente", "realizado"])

    def create(self, validated_data):
        passageiro = Passageiro(**validated_data)
        passageiro.save()
        return passageiro

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class VooSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    numero_voo = serializers.CharField(source='numeroVoo')
    origem = serializers.CharField()
    destino = serializers.CharField()
    data_hora_partida = serializers.DateTimeField(source='dataHoraPartida')
    portao_id = serializers.PrimaryKeyRelatedField(queryset=Portao.objects.all())
    status = serializers.ChoiceField(choices=["programado", "embarque", "concluido"])


    def create(self, validated_data):
        voo = Voo(**validated_data)
        voo.save()
        return voo

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PortaoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    codigo = serializers.CharField()
    disponivel = serializers.BooleanField()

    def create(self, validated_data):
        portao = Portao(**validated_data)
        portao.save()
        return portao

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

from rest_framework import serializers
from bson import ObjectId

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
       
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_internal_value(self, data):
        
        if isinstance(data, str):
            return ObjectId(data)
        return data