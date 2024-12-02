from dataclasses import InitVar, dataclass, field

from faker import Faker

fake = Faker()


@dataclass
class UserFake:
    username: str = field(default_factory=fake.user_name)
    email: str = field(default_factory=fake.email)
    password: str = field(default_factory=fake.password)
    phone: str = field(default_factory=fake.phone_number)
    is_test_user: InitVar[bool] = False

    def __post_init__(self, is_test_user: bool) -> None:
        if is_test_user:
            self.email = "test@mail.com"
            self.password = "secret"
