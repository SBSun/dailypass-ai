from sqlalchemy import String, TypeDecorator


class EnumType(TypeDecorator):
    impl = String

    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if isinstance(value, self.enum_class):
            # Enum의 code 값 반환
            return value.get_code
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            # DB에서 가져온 값을 Enum 객체로 변환
            return self.enum_class(value)
        return value