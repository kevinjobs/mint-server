class Response:
    OK = (0, "请求成功")
    ERROR = (1, "未知错误")

    NO_PERMISSION = (4000, "没有权限")
    PARAMS_MISSING = (4001, "缺少参数")
    NOT_FOUND = (4004, "查找的资源不存的")
    NOT_ALLOWED = (4007, "不被允许的操作")

    EXISTED = (5001, "资源已经存在")

    INVALID_USER_INFO = (8000, "账户或密码错误")
    INVALID_INVITATION = (8001, "无效的邀请码")
    INVALID_TOKEN = (8002, "TOKEN 无效或者已经过期")

    DB_ERROR = (9001, "数据库发生错误")


class SecretCode:
    SALT = "&(^d)daga234235gfd&*NDF9d8fa&kda(234daf))Ngd23@#%DSFGdf235"


class FilePath:
    INVITATION_FILE = "invitations.json"


class DBConfig:
    PATH = "sqlite:///mintforge.sqlite"
