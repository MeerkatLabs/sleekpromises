"""
2.2.2: If `onFulfilled` is a function
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.2.2.js
"""
import threading

from sleekxmpp.test import SleekTest


class Promise_2_2_2_1_TestCase(SleekTest):
    """
    2.2.2.1: it must be called after `promise` is fulfilled, with `promise`'s fulfillment value as its first argument.
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

    def test_already_fulfilled(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            self.assertIs(self.sentinel, arg)
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session['called'])

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        promise.resolved(self.sentinel)

        promise.then(fulfilled_called, rejected_called)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_immediately_fulfilled(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            self.assertIs(self.sentinel, arg)
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session['called'])

        # Create a promise and resolve it
        promise = self.scheduler.promise()

        promise.then(fulfilled_called, rejected_called)
        promise.resolved(self.sentinel)

        event.wait(1.0)

        self.assertTrue(self.session['called'])

    def test_eventually_fulfilled(self):
        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            self.assertIs(self.sentinel, arg)
            event.set()

        def rejected_called(arg):
            self.assertFalse(self.session['called'])

        def deferred_method():
            self.session['promise'].resolved(self.sentinel)

        # Create a promise and store it off
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called, rejected_called)

        # Schedule it on a different thread.
        self.scheduler.schedule_task(deferred_method, delay=0.1)

        event.wait(1.0)

        self.assertTrue(self.session['called'])


class Promise_2_2_2_2_TestCase(SleekTest):
    """
    2.2.2.2: it must not be called before `promise` is fulfilled
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

    def test_fulfilled_after_a_delay(self):

        self.session['afterResolve'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.assertTrue(self.session['afterResolve'])
            event.set()

        def deferred():
            promise.resolved(self.dummy)
            self.session['afterResolve'] = True

        # Create a promise and resolve it
        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_called)

        self.scheduler.schedule_task(deferred, delay=0.05)

        event_wait = event.wait(1.0)

        self.assertTrue(self.session['afterResolve'])
        self.assertTrue(event_wait)

    def test_never_fulfilled(self):

        self.session['called'] = False

        event = threading.Event()

        def fulfilled_called(arg):
            self.session['called'] = True
            event.set()

        promise = self.scheduler.promise()
        promise.then(fulfilled_called)

        event_wait = event.wait(0.150)

        self.assertFalse(self.session['called'])
        self.assertFalse(event_wait)


class Promise_2_2_2_3_TestCase(SleekTest):
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

    def test_already_fulfilled(self):

        self.session['times_called'] = 0

        event = threading.Event()

        def fulfilled(arg):
            self.session['times_called'] += 1
            event.set()

        promise = self.scheduler.promise()
        promise.resolved(self.dummy)

        promise.then(fulfilled)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_trying_to_fulfill_a_pending_promise_more_than_once_immediately(self):
        self.session['times_called'] = 0

        event = threading.Event()

        def fulfilled(arg):
            self.session['times_called'] += 1
            event.set()

        promise = self.scheduler.promise()
        promise.then(fulfilled)
        promise.resolved(self.dummy)
        promise.resolved(self.dummy)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_trying_to_fulfill_a_pending_promise_more_than_once_delayed(self):
        self.session['times_called'] = 0

        event = threading.Event()

        def fulfilled(arg):
            self.session['times_called'] += 1
            event.set()

        def deferred():
            promise = self.session['promise']
            promise.resolved(self.dummy)
            promise.resolved(self.dummy)

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled)

        self.scheduler.schedule_task(deferred, delay=0.50)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_trying_to_fulfill_a_pending_promise_more_than_once_immediately_then_delayed(self):
        self.session['times_called'] = 0

        event = threading.Event()

        def fulfilled(arg):
            self.session['times_called'] += 1
            event.set()

        def deferred():
            promise = self.session['promise']
            promise.resolved(self.dummy)

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled)

        promise.resolved(self.dummy)
        self.scheduler.schedule_task(deferred, delay=0.50)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual(1, self.session['times_called'])

    def test_when_multiple_then_calls_are_made_spaced_apart_in_time(self):
        self.session['times_called'] = [0, 0, 0]

        event = threading.Event()

        def fulfilled_0(arg):
            self.session['times_called'][0] += 1

        def fulfilled_1(arg):
            self.session['times_called'][1] += 1

        def fulfilled_2(arg):
            self.session['times_called'][2] += 1
            event.set()

        def resolve_function():
            promise = self.session['promise']
            promise.resolved(self.dummy)

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_0)

        self.scheduler.schedule_task(lambda: promise.then(fulfilled_1), delay=0.05)
        self.scheduler.schedule_task(lambda: promise.then(fulfilled_2), delay=0.10)

        self.scheduler.schedule_task(resolve_function, delay=0.50)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual([1, 1, 1], self.session['times_called'])

    def test_when_then_is_interleaved_with_fulfillment(self):
        self.session['times_called'] = [0, 0]

        event = threading.Event()

        def fulfilled_0(arg):
            self.session['times_called'][0] += 1

        def fulfilled_1(arg):
            self.session['times_called'][1] += 1
            event.set()

        promise = self.scheduler.promise()
        self.session['promise'] = promise

        promise.then(fulfilled_0)

        promise.resolved(self.dummy)

        promise.then(fulfilled_1)

        event_set = event.wait(1.0)

        self.assertTrue(event_set)
        self.assertEqual([1, 1], self.session['times_called'])
