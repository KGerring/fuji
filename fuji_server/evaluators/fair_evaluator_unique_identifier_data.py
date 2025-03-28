# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from fuji_server.evaluators.fair_evaluator import FAIREvaluator
from fuji_server.models.uniqueness import Uniqueness
from fuji_server.models.uniqueness_output import UniquenessOutput
from fuji_server.models.uniqueness_output_inner import UniquenessOutputInner


class FAIREvaluatorUniqueIdentifierData(FAIREvaluator):
    """
    A class to evaluate the globally unique identifier of the data (F1-01D). A child class of FAIREvaluator.
    ...

    Methods
    ------
    evaluate()
        This method will evaluate whether the data is assigned to a unique identifier (UUID/HASH) that folows a proper syntax or
        identifier is resolvable and follows a defined unique identifier syntax (URL, IRI).
    """

    def __init__(self, fuji_instance):
        FAIREvaluator.__init__(self, fuji_instance)
        if self.fuji.metric_helper.get_metric_version() >= 0.8:
            metric = "FsF-F1-01MD"
        else:
            metric = "FsF-F1-01DD"
        self.set_metric(metric)

    def testDataIdentifierCompliesWithUUIDorHASHorIdutilsScheme(self):
        test_status = False
        if self.isTestDefined(self.metric_identifier + "-2"):
            test_score = self.getTestConfigScore(self.metric_identifier + "-2")
            self.logger.info(
                self.metric_identifier
                + " : Using idutils schemes to identify unique or persistent identifiers for data"
            )
            found_ids = []
            content_identifiers = self.fuji.content_identifier.values()
            if content_identifiers:
                for data_identifier in content_identifiers:
                    data_id_scheme = data_identifier.get("scheme")
                    content_url = data_identifier.get("url")
                    self.logger.info(
                        self.metric_identifier + f" :Starting assessment on data identifier: {content_url}"
                    )
                    if data_id_scheme:
                        output_data_inner = UniquenessOutputInner()
                        output_data_inner.guid = content_url
                        output_data_inner.guid_scheme = data_id_scheme
                        output_data_inner.target = "data"
                        self.output.unique_identifiers.append(output_data_inner)
                        found_ids.append(data_id_scheme)
            else:
                self.logger.warning(
                    self.metric_identifier
                    + " : Could NOT find any data identifier in metadata, therefore skipping uniqueness test"
                )
            if found_ids:
                self.setEvaluationCriteriumScore(self.metric_identifier + "-2", self.total_score, "pass")
                self.maturity = self.metric_tests.get(self.metric_identifier + "-2").metric_test_maturity_config

                self.output.guid = self.fuji.id
                self.score.earned = test_score
                self.logger.log(
                    self.fuji.LOG_SUCCESS,
                    self.metric_identifier + f" : Unique data identifier schemes found: - {list(set(found_ids))}",
                )
                self.output.guid_scheme = found_ids
                test_status = True
            else:
                self.logger.info(self.metric_identifier + " : NO unique data identifier schema found")

        return test_status

    def evaluate(self):
        # ======= CHECK IDENTIFIER UNIQUENESS =======
        if self.metric_identifier in self.metrics:
            self.result = Uniqueness(
                id=self.metric_number, metric_identifier=self.metric_identifier, metric_name=self.metric_name
            )
            self.output = UniquenessOutput()
            self.output.unique_identifiers = []
            self.result.test_status = "fail"
            if self.testDataIdentifierCompliesWithUUIDorHASHorIdutilsScheme():
                self.result.test_status = "pass"
            else:
                self.result.test_status = "fail"
                self.score.earned = 0
                self.logger.warning(self.metric_identifier + " : Failed to check the identifier scheme!.")
            self.result.score = self.score
            self.result.metric_tests = self.metric_tests
            self.result.output = self.output
            self.result.maturity = self.maturity
