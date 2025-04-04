# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from urllib.parse import urlparse

from fuji_server.evaluators.fair_evaluator import FAIREvaluator
from fuji_server.models.standardised_protocol_metadata import StandardisedProtocolMetadata
from fuji_server.models.standardised_protocol_output import StandardisedProtocolOutput
from fuji_server.models.standardised_protocol_output_inner import StandardisedProtocolOutputInner


class FAIREvaluatorStandardisedProtocolMetadata(FAIREvaluator):
    """
    A class to evaluate whether the metadata is accessible through a standardized communication protocol (A1.1).
    A child class of FAIREvaluator.
    ...

    Methods
    ------
    evaluate()
        This method will evaluate whether the URI's scheme is based on
        a shared application protocol.

    """

    def __init__(self, fuji_instance):
        FAIREvaluator.__init__(self, fuji_instance)
        if self.fuji.metric_helper.get_metric_version() >= 0.8:
            self.set_metric("FsF-A1.1-01MD")
        else:
            self.set_metric("FsF-A1-02M")
        self.metadata_output = []

    def testStandardProtocolMetadataUsed(self):
        test_status = False
        if self.isTestDefined(self.metric_identifier + "-1"):
            test_score = self.getTestConfigScore(self.metric_identifier + "-1")
            # parse the URL and return the protocol which has to be one of Internet RFC on
            # Relative Uniform Resource Locators

            for meta_url in set([self.fuji.landing_url, self.fuji.origin_url, self.fuji.pid_url]):
                if meta_url:
                    metadata_parsed_url = urlparse(meta_url)
                    metadata_url_scheme = metadata_parsed_url.scheme
                    if metadata_url_scheme in self.fuji.STANDARD_PROTOCOLS:
                        self.logger.log(
                            self.fuji.LOG_SUCCESS,
                            self.metric_identifier
                            + " : Standard protocol for access to metadata which is assumed to be present found in link -: "
                            + str(meta_url)
                            + str(metadata_url_scheme),
                        )
                        test_status = True
                        output_inner = StandardisedProtocolOutputInner()
                        output_inner.protocol_type = metadata_url_scheme
                        output_inner.found_in = meta_url
                        output_inner.target = "metadata"
                        self.metadata_output.append(output_inner)

            if test_status:
                self.score.earned += test_score
                self.setEvaluationCriteriumScore(self.metric_identifier + "-1", test_score, "pass")
                self.maturity = self.getTestConfigMaturity(self.metric_identifier + "-1")
            else:
                self.logger.warning(
                    self.metric_identifier
                    + " : NO standard protocol detected that leads to metadata which is assumed to be present"
                )
        return test_status

    def testStandardProtocolDataUsed(self):
        test_status = False
        if self.isTestDefined(self.metric_identifier + "-2"):
            test_score = self.getTestConfigScore(self.metric_identifier + "-2")
            content_identifiers = self.fuji.content_identifier.values()
            if content_identifiers:
                if len(content_identifiers) > 0:
                    # here we only test the first content identifier
                    for data_link in content_identifiers:
                        data_url = data_link.get("url")
                        if data_url:
                            data_parsed_url = urlparse(data_url)
                            data_url_scheme = data_parsed_url.scheme
                            if data_url_scheme in self.fuji.STANDARD_PROTOCOLS:
                                self.logger.log(
                                    self.fuji.LOG_SUCCESS,
                                    self.metric_identifier
                                    + " : Standard protocol for access to data object found -: "
                                    + data_url_scheme,
                                )
                                test_status = True
                                output_inner = StandardisedProtocolOutputInner()
                                output_inner.protocol_type = data_url_scheme
                                output_inner.found_in = data_url
                                output_inner.target = "data"
                                self.metadata_output.append(output_inner)
                                break
                    if test_status:
                        # self.data_output = {data_url_scheme: self.fuji.STANDARD_PROTOCOLS.get(data_url_scheme)}
                        self.setEvaluationCriteriumScore(self.metric_identifier + "-2", test_score, "pass")
                        self.maturity = self.getTestConfigMaturity(self.metric_identifier + "-2")
                        self.score.earned += test_score

            else:
                self.logger.warning(
                    self.metric_identifier
                    + " : Skipping protocol test for data since NO content (data) identifier is given in metadata"
                )
        return test_status

    def evaluate(self):
        self.result = StandardisedProtocolMetadata(
            id=self.metric_number,
            metric_identifier=self.metric_identifier,
            metric_name=self.metric_name,
            output=StandardisedProtocolOutput(),
        )
        test_status = "fail"

        if self.testStandardProtocolMetadataUsed():
            test_status = "pass"
        if self.testStandardProtocolDataUsed():
            test_status = "pass"
        self.result.score = self.score
        self.result.output.standard_protocol = self.metadata_output
        self.result.metric_tests = self.metric_tests
        self.result.maturity = self.maturity
        self.result.test_status = test_status
