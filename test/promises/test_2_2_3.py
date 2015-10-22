"""
2.2.3: If `onRejected` is a function,
 https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.2.3.js
"""
import threading

from sleekxmpp.test import SleekTest


class Promise_2_2_3_1_TestCase(SleekTest):
    """
    2.2.3.1: it must be called after `promise` is rejected, with `promise`'s rejection reason as its first argument.
    """

    dummy = {'dummy': 'dummy'}
    sentinel = {'sentinel': 'sentinel'}

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

        def rejected_called(arg):
            self.session['called'] = True
            self.assertIs(self.sentinel, arg)
            event.set()

        def fulfilled_called(arg):
            self.assertFalse(self.session['called'])

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.rejected(self.sentinel)

        promise.then(fulfilled_called, rejected_called)

        self.assertTrue(event.wait(1.0))
        self.assertTrue(self.session['called'])

    def test_immediately_rejected(self):
        self.session['called'] = False

        event = threading.Event()

        def rejected_called(arg):
            self.session['called'] = True
            self.assertIs(self.sentinel, arg)
            event.set()

        def fulfilled_called(arg):
            self.assertFalse(self.session)

        # Create a promise and resolve it
        promise = self.scheduler.promise()

        promise.then(fulfilled_called, rejected_called)
        promise.rejected(self.sentinel)

        self.assertTrue(event.wait(1.0))
        self.assertTrue(self.session['called'])

    def test_eventually_rejected(self):
        self.session['called'] = False

        event = threading.Event()

        def rejected_called(arg):
            self.session['called'] = True
            self.assertIs(self.sentinel, arg)
            event.set()

        def fulfilled_called(arg):
            self.assertFalse(self.session)

        def deferred_method():
            self.session['promise'].rejected(self.sentinel)

        # Create a promise and store it off
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        self.assertTrue(event.wait(1.0))
        self.assertTrue(self.session['called'])


class Promise_2_2_3_2_TestCase(SleekTest):
    """
    2.2.3.2: it must not be called before `promise` is rejected
    """

    dummy = {'dummy': 'dummy'}
    sentinel = {'sentinel': 'sentinel'}

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_rejected_after_a_delay(self):

        self.session['afterResolve'] = False

        event = threading.Event()

        def rejected_call(arg):
            self.assertTrue(self.session['afterResolve'])
            event.set()

        def deferred():
            promise.rejected(self.dummy)
            self.session['afterResolve'] = True

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(None, rejected_call)

        self.scheduler.schedule_task(deferred, delay=0.05)

        event_wait = event.wait(1.0)

        self.assertTrue(self.session['afterResolve'])
        self.assertTrue(event_wait)

    def test_never_rejected(self):

        self.session['called'] = False

        event = threading.Event()

        def rejected_called(arg):
            self.session['called'] = True
            event.set()

        promise = self.scheduler.promise()
        promise.then(None, rejected_called)

        event_wait = event.wait(0.150)

        self.assertFalse(self.session['called'])
        self.assertFalse(event_wait)


class Promise_2_2_3_3_TestCase(SleekTest):
    """
    2.2.2.3: it must not be called more than once.
    """

    dummy = {'dummy': 'dummy'}
    sentinel = {'sentinel': 'sentinel'}

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_already_rejected(self):

        self.session['times_called'] = 0

        event = threading.Event()

        def rejected(arg):
            self.session['times_called'] += 1
            event.set()

        promise = self.scheduler.promise()
        promise.rejected(self.dummy)

        promise.then(None, rejected)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_trying_to_reject_a_pending_promise_more_than_once_immediately(self):
        self.session['times_called'] = 0

        event = threading.Event()

        def rejected(arg):
            self.session['times_called'] += 1
            event.set()

        promise = self.scheduler.promise()
        promise.then(None, rejected)
        promise.rejected(self.dummy)
        promise.rejected(self.dummy)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_trying_to_reject_a_pending_promise_more_than_once_delayed(self):
        self.session['times_called'] = 0

        event = threading.Event()

        def rejected(arg):
            self.session['times_called'] += 1
            event.set()

        def deferred():
            promise = self.session['promise']
            promise.rejected(self.dummy)
            promise.rejected(self.dummy)

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(None, rejected)

        self.scheduler.schedule_task(deferred, delay=0.50)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_trying_to_reject_a_pending_promise_more_than_once_immediately_then_delayed(self):
        self.session['times_called'] = 0

        event = threading.Event()

        def rejected(arg):
            self.session['times_called'] += 1
            event.set()

        def deferred():
            promise = self.session['promise']
            promise.rejected(self.dummy)

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(None, rejected)

        promise.rejected(self.dummy)
        self.scheduler.schedule_task(deferred, delay=0.50)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_when_multiple_then_calls_are_made_spaced_apart_in_time(self):
        self.session['times_called'] = [0, 0, 0]

        event = threading.Event()

        def rejected_0(arg):
            self.session['times_called'][0] += 1

        def rejected_1(arg):
            self.session['times_called'][1] += 1

        def rejected_2(arg):
            self.session['times_called'][2] += 1
            event.set()

        def reject_function():
            promise = self.session['promise']
            promise.rejected(self.dummy)

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(None, rejected_0)

        self.scheduler.schedule_task(lambda: promise.then(None, rejected_1), delay=0.05)
        self.scheduler.schedule_task(lambda: promise.then(None, rejected_2), delay=0.10)

        self.scheduler.schedule_task(reject_function, delay=0.50)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual([1, 1, 1], self.session['times_called'])

    def test_when_then_is_interleaved_with_fulfillment(self):
        self.session['times_called'] = [0, 0]

        event = threading.Event()

        def rejected_0(arg):
            self.session['times_called'][0] += 1

        def rejected_1(arg):
            self.session['times_called'][1] += 1
            event.set()

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(None, rejected_0)

        promise.rejected(self.dummy)

        promise.then(None, rejected_1)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual([1, 1], self.session['times_called'])
