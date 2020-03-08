import asyncio

import tornado.web
import tornado_opentracing
from opentracing.mocktracer import MockTracer
from tornado_opentracing import ScopeManager, trace_context

tracing = tornado_opentracing.TornadoTracing(MockTracer(ScopeManager()))

class ScopeHandler(tornado.web.RequestHandler):
    async def do_something(self):
        tracing = self.settings.get('opentracing_tracing')
        with tracing.tracer.start_active_span('Child'):
            tracing.tracer.active_span.set_tag('start', 0)
            await asyncio.sleep(0)
            tracing.tracer.active_span.set_tag('end', 1)

    async def get(self):
        tracing = self.settings.get('opentracing_tracing')
        span = tracing.get_span(self.request)
        assert span is not None
        assert tracing.tracer.active_span is span

        await self.do_something()

        assert tracing.tracer.active_span is span
        self.write('{}')
