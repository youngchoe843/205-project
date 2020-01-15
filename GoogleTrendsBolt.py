from streamparse import Bolt

class GoogleTrendsBolt(Bolt):
    def initialize(self, storm_conf, context):
        self.counts = Counter()

    def process(self, tup):
        # TODO replace with Spark insert
        self.log(", ".join([str(i) for i in tup]))