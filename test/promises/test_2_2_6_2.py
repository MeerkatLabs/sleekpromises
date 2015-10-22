"""
2.2.6: `then` may be called multiple times on the same promise.
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.2.6.js
"""
import mock
from test.promises.helpers import generate_rejected_test_case

other = {'other': 'other'}
sentinel = {'sentinel': 'sentinel'}
sentinel2 = {'sentinel2': 'sentinel2'}
sentinel3 = {'sentinel3': 'sentinel3'}
dummy = {'dummy': 'dummy'}


def multiple_boring_tests(test_case, promise, done):
    handler1 = mock.MagicMock(return_value=other)
    handler2 = mock.MagicMock(return_value=other)
    handler3 = mock.MagicMock(return_value=other)

    fulfilled = mock.MagicMock()

    def final_rejected(argument):
        test_case.assertEqual(argument, sentinel)

        handler1.assert_called_once_with(sentinel)
        handler2.assert_called_once_with(sentinel)
        handler3.assert_called_once_with(sentinel)

        fulfilled.assert_not_called()

        done()

    promise.then(fulfilled, handler1)
    promise.then(fulfilled, handler2)
    promise.then(fulfilled, handler3)
    promise.then(None, final_rejected)

def multiple_one_throws(test_case, promise, done):

    handler1 = mock.MagicMock(return_value=other)
    handler2 = mock.MagicMock(side_effect=AttributeError())
    handler3 = mock.MagicMock(return_value=other)

    fulfilled = mock.MagicMock()

    def final_rejected(argument):
        test_case.assertEqual(argument, sentinel)

        handler1.assert_called_once_with(sentinel)
        handler2.assert_called_once_with(sentinel)
        handler3.assert_called_once_with(sentinel)

        fulfilled.assert_not_called()

        done()

    promise.then(fulfilled, handler1)
    promise.then(fulfilled, handler2)
    promise.then(fulfilled, handler3)
    promise.then(None, final_rejected)

def multiple_branching_chains_each_with_own_value(test_case, promise, done):

    test_case.session['semiDone'] = 0

    def semidone():
        test_case.session['semiDone'] += 1
        if test_case.session['semiDone'] == 3:
            done()

    def branch01(value):
        return sentinel

    def branch01_final(value):
        test_case.assertIs(value, sentinel)
        semidone()

    branch02_error = TypeError()

    def branch02(value):
        raise branch02_error

    def branch02_final(value):
        test_case.assertIs(value, branch02_error)
        semidone()

    def branch03(value):
        return sentinel3

    def branch03_final(value):
        test_case.assertIs(value, sentinel3)
        semidone()

    promise.then(None, branch01).then(branch01_final)
    promise.then(None, branch02).then(None, branch02_final)
    promise.then(None, branch03).then(branch03_final)

def on_fulfilled_handlers_called_in_original_order(test_case, promise, done):

    handler_mock = mock.MagicMock(**{'handler01.return_value': sentinel,
                                     'handler02.return_value': sentinel2,
                                     'handler03.return_value': sentinel3})

    promise.then(None, handler_mock.handler01)
    promise.then(None, handler_mock.handler02)
    promise.then(None, handler_mock.handler03)

    def test_handlers(value):
        test_case.assertIs(dummy, value)

        method_calls = [a[0] for a in handler_mock.method_calls]

        test_case.assertEquals(['handler01', 'handler02', 'handler03'], method_calls)

        done()

    promise.then(None, test_handlers)

def order_manipulated_in_a_promise(test_case, promise, done):

    handler_mock = mock.MagicMock(**{'handler01.return_value': sentinel,
                                     'handler02.return_value': sentinel2,
                                     'handler03.return_value': sentinel3})

    def inject_handler_during_execution(value):
        handler_mock.handler01()
        promise.then(None, handler_mock.handler03)

    promise.then(None, inject_handler_during_execution)
    promise.then(None, handler_mock.handler02)

    def test_handlers():
        method_calls = [a[0] for a in handler_mock.method_calls]

        test_case.assertEquals(['handler01', 'handler02', 'handler03'], method_calls)

        done()

    def schedule_test(value):
        test_case.scheduler.schedule_task(test_handlers, 0.015)

    promise.then(None, schedule_test)


MultipleBoringTestCases = generate_rejected_test_case(method=multiple_boring_tests, value=sentinel,
                                                      module=__name__,
                                                      name='MultipleBoringTestCases')
MultipleOneThrowsTestCases = generate_rejected_test_case(method=multiple_one_throws, value=sentinel,
                                                         module=__name__,
                                                         name='MultipleOneThrowsTestCases')
MultipleBranchingTestCases = generate_rejected_test_case(method=multiple_branching_chains_each_with_own_value,
                                                         module=__name__,
                                                         value=dummy,
                                                         name='MultipleBranchingTestCases')
FulfilledHandlersInOrder = generate_rejected_test_case(method=on_fulfilled_handlers_called_in_original_order,
                                                       value=dummy,
                                                       module=__name__,
                                                       name='FulfilledHandlersInOrder')
OrderManipulatedInPromise = generate_rejected_test_case(method=order_manipulated_in_a_promise,
                                                        value=dummy,
                                                        module=__name__,
                                                        name='OrderManipulatedInPromise')
