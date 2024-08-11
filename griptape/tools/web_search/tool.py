from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field
from schema import Literal, Schema

from griptape.artifacts import ErrorArtifact, ListArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity

if TYPE_CHECKING:
    from griptape.drivers import BaseWebSearchDriver


@define
class WebSearch(BaseTool):
    web_search_driver: BaseWebSearchDriver = field(kw_only=True)

    @activity(
        config={
            "description": "Can be used for searching the web via the {{ _self.web_search_driver.__class__.__name__}}.",
            "schema": Schema(
                {
                    Literal(
                        "query",
                        description="Search engine request that returns a list of pages with titles, descriptions, and URLs",
                    ): str,
                },
            ),
        },
    )
    def search(self, props: dict) -> ListArtifact | ErrorArtifact:
        values = props["values"]
        query = values["query"]
        extra_keys = {k: values[k] for k in values.keys() - {"query"}}

        try:
            return self.web_search_driver.search(query, **extra_keys)
        except Exception as e:
            return ErrorArtifact(f"Error searching '{query}' with {self.web_search_driver.__class__.__name__}: {e}")
