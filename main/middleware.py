from django.utils import timezone
from main.models import Nutricionista

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                nutricionista = Nutricionista.objects.get(user=request.user)
                nutricionista.last_seen = timezone.now()
                nutricionista.save(update_fields=['last_seen'])
            except Nutricionista.DoesNotExist:
                pass

        return self.get_response(request)