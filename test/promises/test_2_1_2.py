"""
2.1.2.1 When fulfilled, a promise: must not transition to any other state.
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.1.2.js
"""
import threading

from sleekxmpp.test import SleekTest


class Promise_2_1_2_TestCase(SleekTest):

    dummy = {}

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_already_fulfilled(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session)

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.resolved(self.dummy)

        promise.then(fulfilled_called, rejected_called)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_immediately_fulfilled(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session)

        # Create a promise and resolve it
        promise = self.scheduler.promise()

        promise.then(fulfilled_called, rejected_called)
        promise.resolved(self.dummy)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_eventually_fulfilled(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session)

        def deferred_method():
            self.session['promise'].resolved(self.dummy)

        # Create a promise and store it off
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_fulfill_then_immediately_reject(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session)

        # Create a promise and resolve it
        promise = self.scheduler.promise()

        promise.then(fulfilled_called, rejected_called)
        promise.resolved(self.dummy)
        promise.rejected(self.dummy)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_trying_to_fulfill_then_reject_delayed(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session)

        def deferred_method():
            self.session['promise'].resolved(self.dummy)
            self.session['promise'].rejected(self.dummy)

        # Create a promise and store it off
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_trying_to_fulfill_immediately_then_reject_delayed(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session)

        def deferred_method():
            self.session['promise'].rejected(self.dummy)

        # Create a promise and store it off
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        self.session['promise'].resolved(self.dummy)
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        event.wait(1.0)

        self.assertTrue(self.session['called'])
