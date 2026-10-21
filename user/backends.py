from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class RFIDBackend(ModelBackend):
    def authenticate(self, request, rfid_card=None, **kwargs):
        if rfid_card is None:
            return None

        UserModel = get_user_model()
        try:
            # Ищем пользователя по номеру карты
            user = UserModel.objects.get(rfid_card=rfid_card)
        except UserModel.DoesNotExist:
            return None

        # Проверяем, активен ли пользователь (как в стандартном бэкенде)
        if user.is_active:
            return user
        return None