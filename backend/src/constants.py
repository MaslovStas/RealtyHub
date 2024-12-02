from enum import StrEnum


class Environment(StrEnum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"
    STAGING = "STAGING"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL, self.TESTING, self.STAGING)

    @property
    def is_testing(self) -> bool:
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)
