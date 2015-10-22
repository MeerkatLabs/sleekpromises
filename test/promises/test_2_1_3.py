"""
2.1.3.1: When rejected, a promise: must not transition to any other state.
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.1.3.js
"""
import threading

from sleekxmpp.test import SleekTest


class Promise_2_1_3_TestCase(SleekTest):

    dummy = {}

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_already_rejected(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.assertFalse(self.session['called'])

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.rejected(self.dummy)

        promise.then(fulfilled_called, rejected_called)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_immediately_rejected(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.assertFalse(self.session['called'])

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        # Create a promise and resolve it
        promise = self.scheduler.promise()

        promise.then(fulfilled_called, rejected_called)
        promise.rejected(self.dummy)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_eventually_rejected(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.assertFalse(self.session['called'])

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        def deferred_method():
            self.session['promise'].rejected(self.dummy)

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_reject_then_immediately_fulfill(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.assertFalse(self.session['called'])

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        # Create a promise and resolve it
        promise = self.scheduler.promise()

        promise.then(fulfilled_called, rejected_called)
        promise.rejected(self.dummy)
        promise.resolved(self.dummy)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_trying_to_reject_then_fulfill_delayed(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.assertFalse(self.session['called'])

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        def deferred_method():
            self.session['promise'].rejected(self.dummy)
            self.session['promise'].resolved(self.dummy)

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_trying_to_reject_immediately_then_fulfill_delayed(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.assertFalse(self.session['called'])

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        def deferred_method():
            self.session['promise'].resolved(self.dummy)

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        promise.rejected(self.dummy)
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        event.wait(1.0)

        self.assertTrue(self.session['called'])
