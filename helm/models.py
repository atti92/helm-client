from datetime import datetime
from enum import Enum
from typing import Optional

import pydantic
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


class DataModel(pydantic.BaseModel):
    class Config:
        extra = "allow"
        arbitrary_types_allowed = True


class HelmRelease(DataModel):
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


class OciUrl(pydantic.AnyUrl):
    allowed_schemes = {"oci"}

    __slots__ = ()


class HelmRepo(DataModel):
    name: str
    url: pydantic.HttpUrl | OciUrl

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class HelmChartInfo(DataModel):
    @pydantic.root_validator(pre=True)
    def name_or_url(cls, values):
        if not values.get("name") and not values.get("url"):
            raise ValueError("name or url must be specified!")
        if "name" not in values:
            values["name"] = str(values["url"])
        return values

    name: str
    version: str
    description: str
    app_version: Optional[str] = pydantic.Field(alias="appVersion")
    api_version: Optional[str] = pydantic.Field(alias="apiVersion")
    url: Optional[pydantic.HttpUrl | OciUrl]
    repository: Optional[HelmRepo]
