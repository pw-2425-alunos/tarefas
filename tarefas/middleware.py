from django.http import JsonResponse


class ErrosJsonApiMiddleware:
    """Converte 404 e 405 gerados fora do Ninja em JSON nas rotas /api/."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/"):
            return response
        if response.status_code == 405 and "json" not in response.get("Content-Type", ""):
            novo = JsonResponse({"detail": "Método não permitido."}, status=405)
            if response.has_header("Allow"):
                novo["Allow"] = response["Allow"]
            return novo
        if response.status_code == 404 and "json" not in response.get("Content-Type", ""):
            return JsonResponse({"detail": "Recurso não encontrado."}, status=404)
        return response
