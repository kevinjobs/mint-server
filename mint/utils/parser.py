from flask import request


class Parser:
    @staticmethod
    def parse_args(**kw):
        "query"
        return Parser.parse('args', **kw)

    @staticmethod
    def parse_json(**kw):
        "body -> json"
        return Parser.parse('json', **kw)

    @staticmethod
    def parse_value(**kw):
        "form + query"
        return Parser.parse('values', **kw)

    @staticmethod
    def parse(x9dt4: str, **kw):
        params = {}

        for k, v in kw.items():
            if x9dt4 == 'args':
                value = request.args.get(k)
            if x9dt4 == 'json':
                value = request.json.get(k)
            if x9dt4 == 'values':
                value = request.values.get(k)

            if value:
                params[k] = v(value)
        return params
