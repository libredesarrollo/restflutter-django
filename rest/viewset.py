
from rest_framework import viewsets

from widgets.models import Note

from .seriealizer import NoteSerializer




class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

"""    def list (self, request):
        queryset = Note.objects.all()
        serializer = NoteSerializer(queryset, many=True)
        return responseApi(serializer.data)"""
