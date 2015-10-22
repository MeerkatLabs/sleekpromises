"""
2.3.1: If `promise` and `x` refer to the same object, reject `promise` with a `TypeError' as the reason.
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.3.1.js
"""
import threading

from sleekxmpp.test import SleekTest


class Promise_2_3_1_TestCase(SleekTest):

    dummy = {}

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_fulfilled_returns_promise_cycle(self):

        event = threading.Event()

        def promise_resolved(value):
            return promise

        def catch_rejection(value):
            self.assertEqual(type(value), TypeError)
            event.set()

        start_promise = self.scheduler.promise()
        start_promise.resolved(True)

        promise = start_promise.then(promise_resolved)
        promise.then(None, catch_rejection)

        self.assertTrue(event.wait(1.0))

    def test_rejected_returns_promise_cycle(self):

        event = threading.Event()

        def promise_rejected(value):
            return promise

        def catch_rejection(value):
            self.assertEqual(type(value), TypeError)
            event.set()

        start_promise = self.scheduler.promise()
        start_promise.rejected(True)

        promise = start_promise.then(None, promise_rejected)
        promise.then(None, catch_rejection)

        self.assertTrue(event.wait(1.0))


