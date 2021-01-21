from rest_framework.utils.serializer_helpers import ReturnDict


class CustomErrorSerializer(object):
    # Overiding the default error message
    @property
    def errors(self):
        error_msg = ''
        ret = super().errors
        if isinstance(ret, list) and len(ret) == 1 and getattr(ret[0], 'code', None) == 'null':
            # Edge case. Provide a more descriptive error than
            # "this field may not be null", when no data is passed.
            detail = ErrorDetail('No data provided', code='null')
            ret = {api_settings.NON_FIELD_ERRORS_KEY: [detail]}

        # print(str(ret.items()))
        # my_dict = {'foo': 'bar', 'spam': 'eggs'}

        if not ret:
            return
        first_error = next(iter(ret))

        # if len(ret.keys()) > 1:
        #     obj_error = next(iter(ret[first_error]))
        #     msg = ret[first_error][obj_error][0]
        #     print(msg)
        #     error_msg = msg.replace('This field', first_error)
        #     context = {
        #         'error_msg': error_msg
        #     }
        #     return ReturnDict(context, serializer=self)

        try:
            # print(ret)
            msg = ret[first_error][0]
            msg = f'{first_error.title()}: {msg}'
        except KeyError:
            print(ret[first_error])
            obj_error = next(iter(ret[first_error]))
            msg = ret[first_error][obj_error][0]
            # msg.replace('This field', first_error)
            # error_msg = msg.replace('Invalid pk', first_error)

        # password_length_error = 'Password must be a minimum of None characters.'
        # if error_msg == password_length_error:
        #     error_msg = 'Password is too weak'
        if 'This field' in msg:
            error_msg = msg.replace('This field', first_error)
        elif 'Invalid pk' in msg:
            error_msg = msg.replace('Invalid pk', first_error)
        else:
            print(msg)
            error_msg = msg

        context = {
            'error_msg': error_msg
        }
        return ReturnDict(context, serializer=self)