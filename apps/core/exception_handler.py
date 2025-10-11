from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        code = response.status_code

        if code == status.HTTP_400_BAD_REQUEST:
            response.data = {'detail': 'So‘rov noto‘g‘ri yuborilgan.'}
        elif code == status.HTTP_401_UNAUTHORIZED:
            response.data = {'detail': 'Tizimga kirish maʼlumotlari taqdim etilmagan.'}
        elif code == status.HTTP_403_FORBIDDEN:
            response.data = {'detail': 'Sizda bu amalni bajarish uchun ruxsat yo‘q.'}
        elif code == status.HTTP_404_NOT_FOUND:
            response.data = {'detail': 'So‘ralgan manba topilmadi.'}
        elif code == status.HTTP_405_METHOD_NOT_ALLOWED:
            response.data = {'detail': 'Ushbu so‘rov turi (method) ruxsat etilmagan.'}
        elif code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            response.data = {'detail': 'Serverda kutilmagan xatolik yuz berdi.'}

    return response
