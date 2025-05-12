from mongoengine import (
    Document, StringField, BooleanField, ReferenceField,
    DateTimeField, ValidationError, CASCADE
)
from datetime import datetime
import re


def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in [9, 10]:
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[i]):
            return False
    return True


class Portao(Document):
    codigo = StringField(required=True, unique=True)
    disponivel = BooleanField(default=True)

    def clean(self):
        if not self.codigo:
            raise ValidationError("Código do portão é obrigatório.")

    def __str__(self):
        return f'Portão {self.codigo} - {"Disponível" if self.disponivel else "Ocupado"}'


class Voo(Document):
    numeroVoo = StringField(required=True, unique=True)
    origem = StringField(required=True)
    destino = StringField(required=True)
    dataHoraPartida = DateTimeField(required=True)
    portao_id = ReferenceField('Portao', required=True)
    status = StringField(choices=['programado', 'embarque', 'concluido'], default='programado')

    def clean(self):
        super(Voo, self).clean() 
        
        if self.portao_id and not self.portao_id.disponivel:
            raise ValidationError(f'O portão {self.portao_id.codigo} não está disponível para este voo.')


class Passageiro(Document):
    nome = StringField(required=True)
    cpf = StringField(required=True, unique=True)
    vooID = ReferenceField(Voo, reverse_delete_rule=CASCADE)
    statusCheckIn = StringField(choices=['pendente', 'realizado'], default='pendente')

    def clean(self):
        if not validar_cpf(self.cpf):
            raise ValidationError("CPF inválido.")
        if self.statusCheckIn == 'realizado':
            if not self.vooID:
                raise ValidationError("Passageiro não está vinculado a um voo.")
            if self.vooID.status != 'embarque':
                raise ValidationError("Check-in só pode ser realizado se o voo estiver em 'embarque'.")

    def __str__(self):
        return f'{self.nome} - CPF: {self.cpf}'
