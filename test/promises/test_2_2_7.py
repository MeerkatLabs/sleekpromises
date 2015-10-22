"""
2.2.7: `then` must return a promise: `promise2 = promise1.then(onFulfilled, onRejected)`
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.2.7.js
"""

from sleekxmpp.test import SleekTest
from test.promises.helpers import generate_fulfilled_test_case, generate_rejected_test_case

sentinel = {'sentinel': 'sentinel'}


class Promise_2_2_7(SleekTest):
    """
    is a promise.
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

    def test_is_a_promise(self):

        promise1 = self.scheduler.promise()
        promise2 = promise1.then()

        self.assertIsNotNone(promise2)
        self.assertTrue(hasattr(promise2, 'then'))
        self.assertTrue(hasattr(promise2.then, '__call__'))

def on_fulfilled_throws_exception_promise_is_rejected(test_case, promise, done):

    error = TypeError()

    def promise1_fulfilled(value):
        raise error

    def promise2_rejected(_error):
        test_case.assertIs(_error, error)
        done()

    promise2 = promise.then(promise1_fulfilled)
    promise2.then(None, promise2_rejected)


def on_rejected_throws_exception_promise_is_rejected(test_case, promise, done):

    error = TypeError()

    def promise1_rejected(value):
        raise error

    def promise2_rejected(_error):
        test_case.assertIs(_error, error)
        done()

    promise2 = promise.then(None, promise1_rejected)
    promise2.then(None, promise2_rejected)


def on_fulfilled_not_a_function_pass_through(test_case, promise, done):

    def promise2_handler(value):
        test_case.assertIs(value, sentinel)
        done()

    promise2 = promise.then()
    promise2.then(promise2_handler)


def on_rejected_not_a_function_pass_through(test_case, promise, done):

    def promise2_handler(value):
        test_case.assertIs(value, sentinel)
        done()

    promise2 = promise.then()
    promise2.then(None, promise2_handler)

FulfilledThrowsExceptionPromise = generate_fulfilled_test_case(method=on_fulfilled_throws_exception_promise_is_rejected,
                                                               value=dict(),
                                                               module=__name__,
                                                               name='FulfilledThrowsExceptionPromise')
RejectedThrowsExceptionPromise = generate_rejected_test_case(method=on_rejected_throws_exception_promise_is_rejected,
                                                             value=dict(),
                                                             module=__name__,
                                                             name='RejectedThrowsExceptionPromise')
FulfilledPassThrough = generate_fulfilled_test_case(method=on_fulfilled_not_a_function_pass_through,
                                                    value=sentinel,
                                                    module=__name__,
                                                    name='FulfilledPassThrough')
RejectedPassTrough = generate_rejected_test_case(method=on_rejected_not_a_function_pass_through,
                                                 value=sentinel,
                                                 module=__name__,
                                                 name='RejectedPassTrough')
