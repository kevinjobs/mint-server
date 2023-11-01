class RespCode:
    OK = 0
    ERROR = 1
    DB_ERROR = 9001
    NOT_FOUND = 4004
    EXISTED = 5001
    NO_PERMISSION = 4000
    NOT_ALLOWED = 4007
    INVALID_INVITATION = 8001
    INVALID_TOKEN = 8002
    INCORRET_INFO = 9009


class RespMsg:
    OK = 'request success'
    ERROR = 'unknown error'
    DB_ERROR = 'database error'
    NOT_FOUND = 'the resource doesnt exist'
    EXISTED = 'the resource existed'
    NO_PERMISSION = 'no permission to access'
    NOT_ALLOWED = 'not allowed'
    INVALID_INVITATION = '无效的邀请码'
    INVALID_TOKEN = 'TOKEN 无效或者已经过期'
    INCORRET_INFO = '密码错误'


class SecretCode:
    SALT = '&(^d)daga234235gfd&*NDF9d8fa&kda(234daf))Ngd23@#%DSFGdf235'


class FilePath:
    INVITATION_FILE = 'invitations.json'
