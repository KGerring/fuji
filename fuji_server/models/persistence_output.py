from fuji_server import util
from fuji_server.models.base_model_ import Model
from fuji_server.models.persistence_output_inner import PersistenceOutputInner


class PersistenceOutput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, persistent_identifiers: list[PersistenceOutputInner] | None = None):
        """PersistenceOutput - a model defined in Swagger

        :param persistent_identifiers: The persistent_identifiers of this PersistenceOutput.  # noqa: E501
        :type persistent_identifiers: List[PersistenceOutputInner]
        """
        self.swagger_types = {"persistent_identifiers": list[PersistenceOutputInner]}

        self.attribute_map = {"persistent_identifiers": "persistent_identifiers"}
        self._persistent_identifiers = persistent_identifiers

    @classmethod
    def from_dict(cls, dikt) -> "PersistenceOutput":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Persistence_output of this PersistenceOutput.  # noqa: E501
        :rtype: PersistenceOutput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def persistent_identifiers(self) -> list[PersistenceOutputInner]:
        """Gets the persistent_identifiers of this PersistenceOutput.


        :return: The persistent_identifiers of this PersistenceOutput.
        :rtype: List[PersistenceOutputInner]
        """
        return self._persistent_identifiers

    @persistent_identifiers.setter
    def persistent_identifiers(self, persistent_identifiers: list[PersistenceOutputInner]):
        """Sets the persistent_identifiers of this PersistenceOutput.


        :param persistent_identifiers: The persistent_identifiers of this PersistenceOutput.
        :type persistent_identifiers: List[PersistenceOutputInner]
        """

        self._persistent_identifiers = persistent_identifiers
