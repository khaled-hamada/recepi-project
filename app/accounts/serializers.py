from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """ user object serailzer """
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        #extra fields settings , review doc.
        extra_kwargs = {
            'password':{'write_only':True, 'min_length':6}
            }
        
    def create(self, validated_data):
        """ override create to user our create function
            so we can hash the password before saving it 
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ override update function to hash password before saving it """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        #if user supply a new password , then update it
        if password:
            user.set_password(password)
            user.save()
        
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ serializer for user authentication object """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False
        )
    
    def validate(self, attrs):
        """ Validate and authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password  = password
        )
        #in case of failure
        if not user:
            msg = _("Unable to authenticate user with provided"
                " credentials wrong user name or password ")
            
            raise serializers.ValidationError(msg , code ='authentication' )
        
        # in case of success
        attrs['user'] = user
        return attrs