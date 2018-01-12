v2
==

Model inheritance, overriding attributes
----------------------------------------

.. code:: python

  def not_implemented(*args, **kwargs):
      raise NotImplementedError


  @Attribute('parse', type=not_implemented)
  class PrometheusModel:
      @property
      def tokens(self):
          print('line, tokens:', self.parse)
          return self.parse[1]

      @property
      def original(self):
          print('line, tokens:', self.parse)
          return self.parse[0]

      @property
      def name(self):
          return self.tokens[0]

      def unparse(self):
          raise NotImplementedError


  @Model()
  @Attribute('parse', type=parse_grammar(METRIC_LINE))
  class Metric(PrometheusModel):
      def unparse(self):
          if len(self.tokens) == 3:
              return '{name}{{{labels},}} {value}'.format(
                  name=self.tokens[0], labels=','.join(self.tokens[1].asList()), value=self.tokens[2]
              )
          else:
              return '{} {}'.format(*self.tokens.asList())

will result in *not_implemented* being called, while

.. code:: python

  class PrometheusModel:
    parse = not_implemented

works as expected.
