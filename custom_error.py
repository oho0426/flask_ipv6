import json


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = -1

        super().__init__(self.message)

    def __str__(self):
        error_json = json.loads('{"code": %s, "messages": %s}' % (self.code, self.message))
        return error_json
        # super().__init__(self.message)
