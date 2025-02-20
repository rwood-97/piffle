from __future__ import annotations

from dataclasses import dataclass

import addict


class OtherMetadataDict(addict.Dict):
    """Base attrdict class for all other metadata dictionaries."""

    def __missing__(self, key):
        raise KeyError(key)


@dataclass()
class IIIF3:
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(
                name
            )  # try to get the attribute from the class
        except AttributeError:
            return self.other_metadata[
                name
            ]  # get the attribute from the other_metadata dictionary


@dataclass()
class IIIF2:
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(
                name
            )  # try to get the attribute from the class
        except AttributeError:
            return self.other_metadata[
                name
            ]  # get the attribute from the other_metadata dictionary
