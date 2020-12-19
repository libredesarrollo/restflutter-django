from django.shortcuts import render

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .seriealizer import ButtonSerializer, ChipSerializer, TextSerializer, ImageSerializer, GroupSerializer
from widgets.models import Button, Chip, Image, Text, Group, Mix


# Create your views here.


#paginacion
class CustomPagination(PageNumberPagination):
    page_size = 5
    def get_paginated_response(self, data):
        return responseApi(
            {
                "links" : {
                "next" : self.get_next_link(),
                "prev" : self.get_previous_link()
            },
            "count": self.page.paginator.count,
            "result":data
            }
        )

 
#paginacion

#***********************************BOTONES
def responseApi(data,code=200,msj=''):
    return Response({
        "data": data,
        "code": code,
        "msj":msj
        })

class ButtonListPagination(generics.ListAPIView):
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer
    pagination_class = CustomPagination


class ButtonList(generics.ListAPIView):
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer

    def get(self, request):
        serializer = ButtonSerializer(Button.objects.all(), many=True)
        return responseApi(serializer.data)

class ButtonDetail(generics.RetrieveAPIView):
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer

    def get(self, request, pk):
        serializer = ButtonSerializer(Button.objects.get(pk=pk))
        return responseApi(serializer.data)

"""class ButtonGroup(generics.RetrieveAPIView):
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer

    def get(self, request, group_id):
        serializer = ButtonSerializer(Button.objects.filter(group=group_id), many=True)
        return responseApi(serializer.data)"""

@api_view(['GET'])
def button_group(request, group_id):
    serializer = ButtonSerializer(Button.objects.filter(group=group_id), many=True)
    return responseApi(serializer.data)

#***********************************CHIPS

class ChipListPagination(generics.ListAPIView):
    queryset = Chip.objects.all()
    serializer_class = ChipSerializer
    pagination_class = CustomPagination


class ChipList(generics.ListAPIView):
    queryset = Chip.objects.all()
    serializer_class = ChipSerializer

    def get(self, request):
        serializer = ChipSerializer(Chip.objects.all(), many=True)
        return responseApi(serializer.data)

class ChipDetail(generics.RetrieveAPIView):
    queryset = Chip.objects.all()
    serializer_class = ChipSerializer

    def get(self, request, pk):
        serializer = ChipSerializer(Chip.objects.get(pk=pk))
        return responseApi(serializer.data)

@api_view(['GET'])
def chip_group(request, group_id):
    serializer = ChipSerializer(Chip.objects.filter(group=group_id), many=True)
    return responseApi(serializer.data)

#***********************************IMAGES

class ImageListPagination(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = CustomPagination


class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get(self, request):
        serializer = ImageSerializer(Image.objects.all(), many=True)
        return responseApi(serializer.data)

class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get(self, request, pk):
        serializer = ImageSerializer(Image.objects.get(pk=pk))
        return responseApi(serializer.data)

@api_view(['GET'])
def image_group(request, group_id):
    serializer = ImageSerializer(Image.objects.filter(group=group_id), many=True)
    return responseApi(serializer.data)

#***********************************TEXTS

class TextListPagination(generics.ListAPIView):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    pagination_class = CustomPagination


class TextList(generics.ListAPIView):
    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def get(self, request):
        serializer = TextSerializer(Text.objects.all(), many=True)
        return responseApi(serializer.data)

class TextDetail(generics.RetrieveAPIView):
    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def get(self, request, pk):
        serializer = TextSerializer(Text.objects.get(pk=pk))
        return responseApi(serializer.data)

@api_view(['GET'])
def text_group(request, group_id):
    serializer = TextSerializer(Text.objects.filter(group=group_id), many=True)
    return responseApi(serializer.data)

#***********************************GRUPOS

class GroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request):
        serializer = GroupSerializer(Group.objects.all(), many=True)
        return responseApi(serializer.data)

class GroupDetail(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request, pk):
        serializer = GroupSerializer(Group.objects.get(pk=pk))
        return responseApi(serializer.data)

#***********************************MIXS

@api_view(['GET'])
def mix_group(request, group_id):
    mixs = Mix.objects.filter(group=group_id).order_by('orden')

    data = []
    for m in mixs:
        if m.widget == "button":
            o = Button.objects.get(pk=m.widget_id)
            d = ButtonSerializer(o).data
        elif m.widget == "image":
            o = Image.objects.get(pk=m.widget_id)
            d = ImageSerializer(o).data
        elif m.widget == "chip":
            o = Chip.objects.get(pk=m.widget_id)
            d = ChipSerializer(o).data
        elif m.widget == "text":
            o = Text.objects.get(pk=m.widget_id)
            d = TextSerializer(o).data

        d.update({'widget':m.widget})
        d.update({'orden':m.orden})
        data.append(d)

    return responseApi(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Usuario Inválido")

    pwd_valid = check_password(password,user.password)

    if not pwd_valid:
        return Response("Contraseña inválida")

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': "Token "+token.key})

@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def verify(request):
    
    token = Token.objects.get(user=request.user)
    return Response({'token':"Token "+token.key})






    