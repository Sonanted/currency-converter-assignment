import requests as r

from rest_framework.exceptions import APIException, ParseError
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from .models import RateModel
from .serializers import RateSerializer

ENDPOINT = "https://www.cbr-xml-daily.ru/daily_json.js"


class RateAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "from",
                openapi.IN_QUERY,
                description="Код валюты, из которой необходимо конвертировать",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "to",
                openapi.IN_QUERY,
                description="Код валюты, в которую необходимо конвертировать",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "value",
                openapi.IN_QUERY,
                description="Количество валюты, которую необходимо конвертировать",
                type=openapi.TYPE_NUMBER,
            ),
        ],
        responses={
            200: openapi.Response("Результат конвертации валют", RateSerializer)
        },
    )
    def get(self, request):
        try:
            response = r.get(ENDPOINT)
        except Exception as error:
            raise APIException(
                "Ошибка при обращени к эндпоинту с информацией о валютах. Повторите попытку позже."
            )

        if response.status_code != 200:
            raise APIException(
                f"Некорректный ответ от эндпоинта с информацией о валютах. Код ответа: {response.status_code}"
            )

        for key in ("from", "to", "value"):
            if key not in request.GET:
                raise ParseError(f"Обязательный параметр {key} отсутствует в запросе.")

        valutes = response.json()["Valute"]
        if request.GET["from"] not in valutes and request.GET["from"] != "RUB":
            raise ParseError(
                f'Неизвестный код валюты в параметре from={request.GET["from"]}. Невозможно конвертировать валюту.'
            )

        if request.GET["to"] not in valutes and request.GET["to"] != "RUB":
            raise ParseError(
                f'Неизвестный код валюты в параметре to={request.GET["to"]}. Невозможно конвертировать валюту'
            )

        currency_from_value = (
            valutes[request.GET["from"]].get("Value")
            if request.GET["from"] != "RUB"
            else 1
        )
        currency_to_value = (
            valutes[request.GET["to"]].get("Value") if request.GET["to"] != "RUB" else 1
        )
        result = currency_from_value / currency_to_value * float(request.GET["value"])

        rate = RateModel(result=result)
        serializer = RateSerializer(rate)
        return Response(serializer.data)
