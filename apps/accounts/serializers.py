from rest_framework import serializers

from .models import Profile, User


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "password",
            "role",
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile

        fields = [
            "id",
            "full_name",
            "phone",
            "address",
            "city",
            "profile_image",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProfileImageSerializer(serializers.ModelSerializer):

    profile_image = serializers.ImageField(
        required=True,
        allow_null=False
    )

    class Meta:
        model = Profile

        fields = [
            "profile_image",
        ]

    def validate_profile_image(self, image):

    
        if image.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image size must be less than 5 MB."
            )

        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        ]

        filename = image.name.lower()

        if not any(
            filename.endswith(extension)
            for extension in allowed_extensions
        ):
            raise serializers.ValidationError(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        return image