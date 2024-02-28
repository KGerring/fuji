# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

# coding: utf-8

from datetime import date, datetime  # noqa: F401

from fuji_server import util
from fuji_server.models.base_model_ import Model


class MetadataPreservedOutput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, metadata_preservation_method: list[str] | None = None):
        """MetadataPreservedOutput - a model defined in Swagger

        :param metadata_preservation_method: The metadata_preservation_method of this MetadataPreservedOutput.  # noqa: E501
        :type metadata_preservation_method: List[str]
        """
        self.swagger_types = {"metadata_preservation_method": list[str]}

        self.attribute_map = {"metadata_preservation_method": "metadata_preservation_method"}
        self._metadata_preservation_method = metadata_preservation_method

    @classmethod
    def from_dict(cls, dikt) -> "MetadataPreservedOutput":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MetadataPreserved_output of this MetadataPreservedOutput.  # noqa: E501
        :rtype: MetadataPreservedOutput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def metadata_preservation_method(self) -> list[str]:
        """Gets the metadata_preservation_method of this MetadataPreservedOutput.


        :return: The metadata_preservation_method of this MetadataPreservedOutput.
        :rtype: List[str]
        """
        return self._metadata_preservation_method

    @metadata_preservation_method.setter
    def metadata_preservation_method(self, metadata_preservation_method: list[str]):
        """Sets the metadata_preservation_method of this MetadataPreservedOutput.


        :param metadata_preservation_method: The metadata_preservation_method of this MetadataPreservedOutput.
        :type metadata_preservation_method: List[str]
        """
        allowed_values = ["datacite", "tombstone"]
        if not set(metadata_preservation_method).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `metadata_preservation_method` [{}], must be a subset of [{}]".format(
                    ", ".join(map(str, set(metadata_preservation_method) - set(allowed_values))),
                    ", ".join(map(str, allowed_values)),
                )
            )

        self._metadata_preservation_method = metadata_preservation_method
