from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from datetime import datetime
from .models import Passageiro, Voo, Portao  
from .serializers import PassageiroSerializer, VooSerializer, PortaoSerializer


class PortaoViewSet(viewsets.ModelViewSet):
    queryset = Portao.objects.all()  
    serializer_class = PortaoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            portao = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        portao = self.get_object()
        serializer = self.get_serializer(portao, data=request.data, partial=True)
        if serializer.is_valid():
            portao = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        portao = self.get_object()
        portao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VooViewSet(viewsets.ModelViewSet):
    queryset = Voo.objects.all()
    serializer_class = VooSerializer

    def perform_create(self, serializer):
        voo = serializer.save()
        if voo.portao_id:
            voo.portao_id.disponivel = False
            voo.portao_id.save()

    def perform_update(self, serializer):
        voo_antigo = self.get_object()
        portao_antigo = voo_antigo.portao_id

        voo = serializer.save()
        if portao_antigo and portao_antigo != voo.portao_id:
            portao_antigo.disponivel = True
            portao_antigo.save()

        if voo.portao_id:
            voo.portao_id.disponivel = False
            voo.portao_id.save()

        if voo.status == 'concluido' and voo.portao_id:
            voo.portao_id.disponivel = True
            voo.portao_id.save()

    def perform_destroy(self, instance):
        
        if instance.portao_id:
            instance.portao_id.disponivel = True
            instance.portao_id.save()

      
        instance.delete()

    @action(detail=False, methods=['get'])
    def voos_hoje(self, request):
        
        pass


class PassageiroViewSet(viewsets.ModelViewSet):
    queryset = Passageiro.objects.all()  # Usando o MongoEngine, as consultas são feitas com `.objects`
    serializer_class = PassageiroSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            passageiro = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        passageiro = self.get_object()
        serializer = self.get_serializer(passageiro, data=request.data, partial=True)
        if serializer.is_valid():
            passageiro = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        passageiro = self.get_object()
        passageiro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def relatorio_voos_hoje(request):
    hoje = datetime.now().date()
    voos = Voo.objects(status="programado", dataHoraPartida__gte=datetime.combine(hoje, datetime.min.time()), dataHoraPartida__lte=datetime.combine(hoje, datetime.max.time()))

    resultado = []
    for voo in voos:
        passageiros = Passageiro.objects(voo_id=voo.id)  # A referência ao Voo no MongoEngine é feita dessa maneira
        resultado.append({
            'numero_voo': voo.numero_voo,
            'origem': voo.origem,
            'destino': voo.destino,
            'data_partida': voo.dataHoraPartida.strftime('%Y-%m-%d %H:%M'),
            'portao': voo.portao_id.codigo if voo.portao_id else None,
            'status': voo.status,
            'passageiros': [
                {
                    'nome': p.nome,
                    'cpf': p.cpf,
                    'statusCheckIn': p.statusCheckIn
                }
                for p in passageiros
            ]
        })

    return Response(resultado)
