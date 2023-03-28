from datetime import datetime

import pydantic
from enum import Enum
from packaging.version import Version


class ProcessReturn(pydantic.BaseModel):
    stdout: str
    stderr: str
    returncode: int


class HelmReleaseStatus(Enum):
    ALL = "all"
    DEPLOYED = "deployed"
    FAILED = "failed"
    PENDING = "pending"
    SUPERSEEDED = "superseeded"
    UNINSTALLED = "uninstalled"
    UNINSTALLING = "uninstalling"


class HelmRelease(pydantic.BaseModel):
    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    @pydantic.root_validator(pre=True)
    def app_version_convert(cls, values):
        values["version"] = Version(values["app_version"])
        return values

    app_version: str
    version: Version
    chart: str
    name: str
    namespace: str
    revision: int
    status: HelmReleaseStatus
    updated: datetime
