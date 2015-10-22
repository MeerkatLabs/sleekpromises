"""
2.2.1: Both `onFulfilled` and `onRejected` are optional arguments.
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.2.1.js
"""
import threading

from sleekxmpp.test import SleekTest


class Promise_2_2_1_1_TestCase(SleekTest):
    """
    2.2.1.1: If `onFulfilled` is not a function, it must be ignored.
    """

    dummy = {}

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_applied_to_rejected_promise(self):

        self.session['called'] = False

        event = threading.Event()

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.rejected(self.dummy)

        promise.then(None, rejected_called)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_applied_to_a_promise_rejected_then_chained_off_of(self):
        self.session['called'] = False

        event = threading.Event()

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.rejected(self.dummy)

        promise.then(lambda s: s, None).then(None, rejected_called)

        event.wait(1.0)

        self.assertTrue(self.session['called'])


class Promise_2_2_1_2_TestCase(SleekTest):
    """
    class Promise_2_2_1_1_TestCase(SleekTest):
    """

    dummy = {}

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_applied_to_resolved_promise(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.resolved(self.dummy)

        promise.then(fulfilled_called, None)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_applied_to_fulfilled_and_then_chained_off_of(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.resolved(self.dummy)

        promise.then(None, lambda s: s).then(fulfilled_called, None)

        event.wait(1.0)

        self.assertTrue(self.session['called'])
