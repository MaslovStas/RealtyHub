from dataclasses import dataclass, field

from faker import Faker

fake = Faker()


@dataclass
class ImageFake:
    url: str = field(default_factory=fake.uri)
    public_id: str = field(default_factory=lambda: fake.lexify(text="?" * 15))
    id: int | None = None
