from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import IIIF2
from .dataclass_utils import parse_item

## IIIF Presentation 2


@dataclass()
class IIIFPresentation2(IIIF2):
    pass


@dataclass()
class Annotation2(IIIFPresentation2):
    context: Any
    id: Any
    type: Any
    resource: Any = None
    on: Any = None
    other_metadata: dict = field(default_factory=dict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        resource: Any = None,
        on: Any = None,
        **kwargs,
    ):
        if id is None:
            print("[WARNING] Annotation is missing 'id' field.")
        if type is None:
            print("[WARNING] Annotation is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.resource = resource
        self.on = on
        self.other_metadata = kwargs

    def collect_annotations(self):
        return [self]

    def get_image_url(self):
        return self.resource["service"]["id"]


@dataclass()
class AnnotationList2(IIIFPresentation2):
    context: Any
    id: Any
    type: Any
    resources: list[Annotation2] = field(default_factory=list)
    other_metadata: dict = field(default_factory=dict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        resources: list[Annotation2 | Any] = [],
        **kwargs,
    ):
        if id is None:
            print("[WARNING] AnnotationList is missing 'id' field.")
        if type is None:
            print("[WARNING] AnnotationList is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.resources = [parse_item(resource, Annotation2) for resource in resources]
        self.other_metadata = kwargs

    def collect_annotations(self):
        annotations = []
        for resource in self.resources:
            annotations += resource.collect_annotations()
        return annotations


@dataclass()
class Canvas2(IIIFPresentation2):
    context: Any
    id: Any
    type: Any
    images: list[Annotation2] = field(default_factory=list)
    otherContent: list[AnnotationList2] = field(default_factory=list)
    other_metadata: dict = field(default_factory=dict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        images: list[Annotation2 | Any] = [],
        otherContent: list[AnnotationList2 | Any] = [],
        **kwargs,
    ):
        if id is None:
            print("[WARNING] Canvas is missing 'id' field.")
        if type is None:
            print("[WARNING] Canvas is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.images = [parse_item(image, Annotation2) for image in images]
        self.otherContent = [
            parse_item(content, AnnotationList2) for content in otherContent
        ]
        self.other_metadata = kwargs

    def collect_annotations(self):
        # TODO: Not sure which annotations to collect here??
        annotations = []
        for image in self.images:
            annotations += image.collect_annotations()
        for content in self.otherContent:
            annotations += content.collect_annotations()
        return annotations


@dataclass()
class Range2(IIIFPresentation2):
    context: Any
    id: Any
    type: Any
    ranges: list[Any] = field(default_factory=list)  # a list of ranges, they self loop
    canvases: list[Canvas2] = field(default_factory=list)
    other_metadata: dict = field(default_factory=dict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        ranges: list[Any] = [],
        canvases: list[Canvas2 | Any] = [],
        **kwargs,
    ):

        if context is None:
            print("[WARNING] Range is missing 'context' field.")
        if id is None:
            print("[WARNING] Range is missing 'id' field.")
        if type is None:
            print("[WARNING] Range is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.ranges = ranges
        self.canvases = [parse_item(canvas, Canvas2) for canvas in canvases]
        self.other_metadata = kwargs

    def collect_annotations(self):
        annotations = []
        for canvas in self.canvases:
            annotations += canvas.collect_annotations()
        return annotations


@dataclass()
class Sequence2(IIIFPresentation2):
    context: Any
    id: Any
    type: Any
    canvases: list[Canvas2] = field(default_factory=list)
    other_metadata: dict = field(default_factory=dict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        canvases: list[Canvas2 | Any] = [],
        **kwargs,
    ):
        if id is None:
            print("[WARNING] Sequence is missing 'id' field.")
        if type is None:
            print("[WARNING] Sequence is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.canvases = [parse_item(canvas, Canvas2) for canvas in canvases]
        self.other_metadata = kwargs

    def collect_annotations(self):
        annotations = []
        for canvas in self.canvases:
            annotations += canvas.collect_annotations()
        return annotations


@dataclass()
class Manifest2(IIIFPresentation2):
    context: Any
    id: Any
    type: Any
    startCanvas: Any = None
    sequences: list[Sequence2] = field(default_factory=list)
    structures: list[Range2] = field(default_factory=list)
    metadata: list[Any] = field(default_factory=list)
    other_metadata: dict = field(default_factory=dict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        startCanvas: Any = None,
        sequences: list[Sequence2 | Any] = [],
        structures: list[Range2 | Any] = [],
        metadata: list[Any] = [],
        **kwargs,
    ):
        if id is None:
            print("[WARNING] Manifest is missing 'id' field.")
        if type is None:
            print("[WARNING] Manifest is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.startCanvas = startCanvas
        self.sequences = [parse_item(sequence, Sequence2) for sequence in sequences]
        self.structures = [parse_item(structure, Range2) for structure in structures]
        self.metadata = metadata
        self.other_metadata = kwargs

    def collect_annotations(self):
        # TODO: Not sure which annotations to collect here??
        annotations = []
        for sequence in self.sequences:
            annotations += sequence.collect_annotations()
        for structure in self.structures:
            annotations += structure.collect_annotations()
        return annotations


@dataclass()
class Collection2(IIIFPresentation2):
    context: Any
    id: Any
    type: Any
    collections: list[Any] = field(
        default_factory=list
    )  # a list of collections, they self loop
    manifests: list[Manifest2] = field(default_factory=list)
    other_metadata: dict = field(default_factory=dict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        collections: list[Any] = [],
        manifests: list[Manifest2 | Any] = [],
        **kwargs,
    ):
        if id is None:
            print("[WARNING] Collection is missing 'id' field.")
        if type is None:
            print("[WARNING] Collection is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.collections = collections
        self.manifests = [parse_item(manifest, Manifest2) for manifest in manifests]
        self.other_metadata = kwargs

    def collect_annotations(self):
        annotations = []
        for manifest in self.manifests:
            annotations += manifest.collect_annotations()
        return annotations
