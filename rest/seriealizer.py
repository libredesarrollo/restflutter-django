from rest_framework import serializers

from widgets.models import Button, Chip, Image, Text, Group, Mix, Behavior, Note

class BehaviorSerializer(serializers.ModelSerializer):
    behavioral_type = serializers.ReadOnlyField(default="Hola")

    def to_representation(self, obj):
        data = super().to_representation(obj)

        #print(data['content_1'])
        #print(obj.content_object)
        #print(isinstance(obj.content_object, Chip))

        if(isinstance(obj.content_object, Button)):
            data['behavioral_type'] = "App\Button"
        elif(isinstance(obj.content_object, Chip)):
            data['behavioral_type'] = "App\Chip"
        elif(isinstance(obj.content_object, Image)):
            data['behavioral_type'] = "App\Image"
        elif(isinstance(obj.content_object, Text)):
            data['behavioral_type'] = "App\Text"
            
        return data

    class Meta:
        model = Behavior
        fields = ('content_1','content_2','behavioral_model','behavioral_type')

    

class ButtonSerializer(serializers.ModelSerializer):
    behavior = BehaviorSerializer(many=True)

    class Meta:
        model = Button
        fields = '__all__'

class ChipSerializer(serializers.ModelSerializer):
    behavior = BehaviorSerializer(many=True)

    class Meta:
        model = Chip
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    behavior = BehaviorSerializer(many=True)

    class Meta:
        model = Image
        fields = '__all__'

class TextSerializer(serializers.ModelSerializer):

    class Meta:
        model = Text
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

class MixSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mix
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'
