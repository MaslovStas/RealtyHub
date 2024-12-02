from dataclasses import InitVar, dataclass, field

from faker import Faker
from faker.providers import DynamicProvider

from src.fake_generators import ImageFake
from src.realty.models import RealtyType

realty_type_provider = DynamicProvider(
    provider_name="realty_type", elements=list(RealtyType.__members__.values())
)

fake = Faker()
fake.add_provider(realty_type_provider)


@dataclass
class RealtyFake:
    title: str = field(default_factory=lambda: fake.text(20)[:-1])
    description: str = field(default_factory=lambda: fake.text(30)[:-1])
    price: int = field(default_factory=lambda: fake.random_int(1000, 2000, 100))
    area: int = field(default_factory=lambda: fake.random_int(30, 60))
    floor: int | None = field(default_factory=lambda: fake.random_int(1, 9))
    rooms: int | None = field(default_factory=lambda: fake.random_int(1, 4))
    city: str = field(default_factory=fake.city)
    state: str = field(default_factory=fake.state)
    type: RealtyType = field(default_factory=fake.realty_type)
    is_active: bool = True
    number_images: InitVar[int] = 5
    images: list[ImageFake] = field(default_factory=list)

    def __post_init__(self, number_images: int) -> None:
        if not self.images:
            self.images = [ImageFake() for _ in range(number_images)]
