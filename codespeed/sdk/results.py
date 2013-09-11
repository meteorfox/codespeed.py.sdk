import base

class Result(base.Resource):
    def __repr__(self):
        return "<Result: {id=%s, benchmark=%s, value=%s}>" % \
               (self.id, self.benchmark, self.value)

class ResultManager(base.Manager):
    resource_class = Result

    def get(self, result):
        return self._get("/result/%s/?format=json" % base.getid(result))

    def list(self):
        return self._list("/result/?format=json", "objects")
