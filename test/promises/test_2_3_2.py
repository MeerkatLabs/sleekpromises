"""
"2.3.2: If `x` is a promise, adopt its state"
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.3.2.js
"""
import threading

from sleekxmpp.test import SleekTest

dummy = {'dummy': 'dummy'}
sentinel = {'sentinel': 'sentinel'}

class Promise_2_3_2_1_TestCase(SleekTest):
    """
    2.3.2.1: If `x` is pending, `promise` must remain pending until `x` is fulfilled or rejected.
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

    def test_fulfilled(self):
        """
        The promise shouldn't resolve until the child promise is resolved.
        :return:
        """
        def create_child_promise(value):
            return self.scheduler.promise()

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.resolved(dummy)
        wait_for_promise = start_promise.then(create_child_promise)

        #### TEST COMPONENT ####
        self.session['rejected'] = False
        self.session['fulfilled'] = False

        def waiting_fulfilled(value):
            self.session['fulfilled'] = True
            event.set()

        def waiting_rejected(value):
            self.session['rejected'] = True
            event.set()

        wait_for_promise.then(waiting_fulfilled, waiting_rejected)
        #### END TEST COMPONENT ####
        self.assertFalse(event.wait(1.0))

        self.assertFalse(self.session['rejected'])
        self.assertFalse(self.session['fulfilled'])

    def test_rejected(self):
        """
        The promise shouldn't resolve until the child promise is resolved.
        :return:
        """
        self.session['rejected'] = False
        self.session['fulfilled'] = False

        def create_child_promise(value):
            return self.scheduler.promise()

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.rejected(dummy)

        def waiting_fulfilled(value):
            self.session['fulfilled'] = True
            event.set()

        def waiting_rejected(value):
            self.session['rejected'] = True
            event.set()

        wait_for_promise = start_promise.then(None, create_child_promise)
        wait_for_promise.then(waiting_fulfilled, waiting_rejected)

        self.assertFalse(event.wait(1.0))

        self.assertFalse(self.session['rejected'])
        self.assertFalse(self.session['fulfilled'])


class Promise_2_3_2_2_TestCase(SleekTest):
    """
    2.3.2.2: If/when `x` is fulfilled, fulfill `promise` with the same value.
    """

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_already_fulfilled_fulfilled(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            promise.resolved(sentinel)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.resolved(dummy)
        wait_for_promise = start_promise.then(create_child_promise)

        #### TEST COMPONENT ####

        def waiting_fulfilled(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(waiting_fulfilled)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())

    def test_already_fulfilled_rejected(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            promise.resolved(sentinel)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.rejected(dummy)
        wait_for_promise = start_promise.then(None, create_child_promise)

        #### TEST COMPONENT ####

        def waiting_fulfilled(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(waiting_fulfilled)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())

    def test_eventually_fulfilled_fulfilled(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            self.scheduler.schedule_task(lambda: promise.resolved(sentinel), delay=0.05)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.resolved(dummy)
        wait_for_promise = start_promise.then(create_child_promise)

        #### TEST COMPONENT ####

        def waiting_fulfilled(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(waiting_fulfilled)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())

    def test_eventually_fulfilled_rejected(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            self.scheduler.schedule_task(lambda: promise.resolved(sentinel), delay=0.05)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.rejected(dummy)
        wait_for_promise = start_promise.then(None, create_child_promise)

        #### TEST COMPONENT ####

        def waiting_fulfilled(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(waiting_fulfilled)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())


class Promise_2_3_2_3_TestCase(SleekTest):
    """
    2.3.2.2: If/when `x` is fulfilled, fulfill `promise` with the same value.
    """

    def setUp(self):
        from sleekpromises import register_sleek_promises

        register_sleek_promises()

        self.session = {}
        self.stream_start(plugins=['sleekpromises_scheduler', ])
        self.scheduler = self.xmpp['sleekpromises_scheduler']

    def tearDown(self):
        self.stream_close()

    def test_already_rejected_fulfilled(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            promise.rejected(sentinel)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.resolved(dummy)
        wait_for_promise = start_promise.then(create_child_promise)

        #### TEST COMPONENT ####

        def waiting_rejected(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(None, waiting_rejected)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())

    def test_already_rejected_rejected(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            promise.rejected(sentinel)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.rejected(dummy)
        wait_for_promise = start_promise.then(None, create_child_promise)

        #### TEST COMPONENT ####

        def waiting_rejected(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(None, waiting_rejected)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())

    def test_eventually_rejected_fulfilled(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            self.scheduler.schedule_task(lambda: promise.rejected(sentinel), delay=0.05)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.resolved(dummy)
        wait_for_promise = start_promise.then(create_child_promise)

        #### TEST COMPONENT ####

        def waiting_rejected(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(None, waiting_rejected)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())

    def test_eventually_fulfilled_rejected(self):

        def create_child_promise(value):
            promise = self.scheduler.promise()
            self.scheduler.schedule_task(lambda: promise.rejected(sentinel), delay=0.05)
            return promise

        event = threading.Event()

        start_promise = self.scheduler.promise()
        start_promise.rejected(dummy)
        wait_for_promise = start_promise.then(None, create_child_promise)

        #### TEST COMPONENT ####

        def waiting_rejected(value):
            self.assertIs(value, sentinel)
            event.set()

        wait_for_promise.then(None, waiting_rejected)
        #### END TEST COMPONENT ####
        self.assertTrue(event.wait())