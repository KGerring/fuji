# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from lxml import etree

from fuji_server.helper.metadata_provider import MetadataProvider
from fuji_server.helper.request_helper import AcceptTypes, RequestHelper


class OAIMetadataProvider(MetadataProvider):
    """A metadata provider class to provide the metadata from OAI

    ...

    Methods
    -------
    getMetadataStandards()
        Method will return the metadata standards in the namespaces
    getMetadata(queryString)
        Method that will return schemas of OAI
    getNamespaces()
        Method to get namespaces

    """

    oai_namespaces = {"oai": "http://www.openarchives.org/OAI/2.0/"}

    def getMetadata(self):
        # http://ws.pangaea.de/oai/provider?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:pangaea.de:doi:10.1594/PANGAEA.66871
        # The nature of a resource identifier is outside the scope of the OAI-PMH.
        # To facilitate access to the resource associated with harvested metadata, repositories should use an element in
        # #metadata records to establish a linkage between the record (and the identifier of its item) and the identifier
        # URL, URN, DOI, etc.) of the associated resource.
        # #The mandatory Dublin Core format provides the identifier element that should be used for this purpose
        return None

    def getMetadataStandards(self):
        """Method to get the metadata schema from the OAI namespaces

        Returns
        -------
        dict
            A dictionary of schemas in OAI
        """
        filter = []
        # filter = ['datacite.org', 'openarchives.org', 'purl.org/dc/']  # TODO expand filters
        # http://ws.pangaea.de/oai/provider?verb=ListMetadataFormats
        oai_endpoint = self.endpoint.split("?")[0]
        # oai_endpoint = oai_endpoint.rstrip('/')
        oai_listmetadata_url = oai_endpoint + "?verb=ListMetadataFormats"
        requestHelper = RequestHelper(url=oai_listmetadata_url, logInst=self.logger)
        requestHelper.setAcceptType(AcceptTypes.xml)
        response_type, xml = requestHelper.content_negotiate(self.metric_id)
        schemas = {}
        if xml:
            try:
                root = etree.fromstring(requestHelper.response_content)
                metadata_nodes = root.xpath(
                    "//oai:OAI-PMH/oai:ListMetadataFormats/oai:metadataFormat",
                    namespaces=OAIMetadataProvider.oai_namespaces,
                )
                for node in metadata_nodes:
                    ele = etree.XPathEvaluator(node, namespaces=OAIMetadataProvider.oai_namespaces)  # .evaluate
                    metadata_prefix = ele(
                        "string(oai:metadataPrefix/text())"
                    )  # <metadataPrefix>oai_dc</metadataPrefix>
                    metadata_schema = ele(
                        "string(oai:schema/text())"
                    )  # <schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>
                    metadata_schema = metadata_schema.strip()
                    self.namespaces.append(metadata_schema)
                    # TODO there can be more than one OAI-PMH endpoint, https://www.re3data.org/repository/r3d100011221
                    if not any(s in metadata_schema for s in filter):
                        schemas[metadata_prefix] = metadata_schema
                    else:
                        self.logger.info(
                            "{} : Skipped domain-agnostic standard listed in OAI-PMH endpoint -: {}".format(
                                self.metric_id, metadata_prefix
                            )
                        )
            except Exception as e:
                self.logger.info(
                    f"{self.metric_id} : Could not parse XML response retrieved from OAI-PMH endpoint: " + str(e)
                )
                print("OAI-PMH Parsing Error: ", e)

        return schemas

    def getNamespaces(self):
        return self.namespaces
