import base

from datetime import datetime

class BenchmarkResult(base.Resource):
    def __repr__(self):
        return "<BenchmarkResult: %s>" % self.resource_uri

class BenchmarkResultManager(base.Manager):
    resource_class = BenchmarkResult

    def get(self, result):
        return self._get("/benchmark-result/%s/?format=json" % \
                        base.getid(result))

    def create(self, sut, benchmark, result):
        """
        Create a new benchmark result.

        :param sut: A dict of key/value data of the system under test.
                    All keys are required.

                   e.g. sut = dict(project=(Project object),
                                   environment=(Environment object),
                                   executable=(Executable object),
                                   branch=(Branch object),
                                   revision=(Revision object))

        :param benchmark: The :class:`Benchmark` where the result was obtained.
        :param result: A dict of key/value data that stores the results for the
                       benchmark. The key `result_value` is mandatory, others
                       keys are optional.
                      e.g.
                      data = dict(result_value=4000,
                                  min=0.0,
                                  max=4500,
                                  std_dev=0.80,
                                  result_date=(datetime.today()),
                                  revision_date=(datetime.today()))
        """
        body = {
            'commitid': sut.get('revision').resource_uri,
            'branch': sut.get('branch').resource_uri,
            'project': sut.get('project').resource_uri,
            'executable': sut.get('executable').resource_uri,
            'environment': sut.get('environment').resource_uri,
            'benchmark': benchmark.resource_uri
        }

        body = dict(body.items() + result.items())
        if 'result_date' not in body:
            body['result_date'] = datetime.today()


        return self._create("/benchmark-result/", body)
