from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    try:
        if response.status_code == 403:
            response.data = {'error_msg': response.data['detail']}

        elif response.status_code == 400 or response.status_code == 401:
            response.data = {'error_msg': response.data['detail']}
    except:
        pass

    return response