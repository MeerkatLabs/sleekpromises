"""
Promise objects.
"""
import logging
logger = logging.getLogger(__name__)


class Promise:
    """
    Promise Object.  A promise is a means of getting the results of a method that will be executed at some time.
    """

    def __init__(self, scheduler):
        """
        Constructor.
        :param scheduler: the scheduler that will be used to schedule the notification of the results.
        """
        self._queue = []

        self._resolved = False
        self._rejected = False

        self._result = None
        self._error = None
        self._scheduler = scheduler
        self._child_promise = None

    def then(self, fulfilled=None, rejected=None):

        new_promise = Promise(self._scheduler)

        # If the promise hasn't been resolved, add it to the queue, otherwise fire off the new deferred.

        if self._resolved:
            if fulfilled:
                deferred = Deferred(self._generate_wrapper(fulfilled, self._result), self._scheduler, new_promise)
            else:
                deferred = Deferred(lambda: self._result, self._scheduler, new_promise)
            self._scheduler.schedule_task(deferred, delay=0.0)
        elif self._rejected:
            if rejected:
                deferred = Deferred(self._generate_wrapper(rejected, self._error), self._scheduler, new_promise)
                self._scheduler.schedule_task(deferred, delay=0.0)
            else:
                self._scheduler.schedule_task(lambda: new_promise.rejected(self._error), delay=0.0)
        else:
            self._queue.append((fulfilled, rejected, new_promise))

        return new_promise

    def resolved(self, result):

        if not(self._resolved or self._rejected):
            self._resolved = True
            self._result = result

            # schedule the fulfilled method call.
            for fulfilled, rejected, promise in self._queue:
                if fulfilled:
                    deferred = Deferred(self._generate_wrapper(fulfilled, self._result), self._scheduler, promise)
                else:
                    deferred = Deferred(lambda: self._result, self._scheduler, promise)

                self._scheduler.schedule_task(deferred, delay=0.0)

        self._queue = None

    def _generate_wrapper(self, function, arg):
        """
        Generate a wrapper.
        :param function: function to call
        :param arg: arg to use
        """
        def method():
            return function(arg)
        return method

    def rejected(self, error):

        if not (self._resolved or self._rejected):
            self._rejected = True
            self._error = error
            # schedule the rejected method call
            for fulfilled, rejected, promise in self._queue:
                if rejected:
                    deferred = Deferred(self._generate_wrapper(rejected, self._error), self._scheduler, promise)
                    self._scheduler.schedule_task(deferred, delay=0.0)
                else:
                    self._scheduler.schedule_task(lambda: promise.rejected(self._error), delay=0.0)

        self._queue = None


class PromiseList:
    """
    Create a single promise that will be resolved or rejected when all of the defined promises are completed.
    """

    def __init__(self, promises, scheduler):
        """
        Constructor that will create all of the book keeping.
        """
        self._promises = promises
        self._results = []
        self._resolved = []
        self._errors = False
        self._scheduler = scheduler
        self._promise = scheduler.promise()

        for index, promise in enumerate(self._promises):
            self._results.append(None)
            self._resolved.append(False)
            promise.then(scheduler.generate_promise_handler(self._resolve_promise, index),
                         scheduler.generate_promise_handler(self._reject_promise, index))

    def _resolve_promise(self, result, index):
        """
        One of the sub promises was resolved/rejected so store the result and determine if all of the work is finished.
        """
        self._results[index] = result
        self._resolved[index] = True

        if False not in self._resolved:
            if self._errors:
                self._promise.rejected(self._results)
            else:
                self._promise.resolved(self._results)

    def _reject_promise(self, result, index):
        """
        Mark that this promise should be rejected once all of the values are returned.
        """
        self._errors = True
        self._resolve_promise(result, index)

    @property
    def promise(self):
        return self._promise


class Deferred:
    """
    A deferred is a method wrapper that will execute a method later and provides a promise that the results will be
    delivered to.
    """

    def __init__(self, method_call, scheduler, promise=None):
        """
        Constructor.
        :param method_call: the method to call.
        :param scheduler: the scheduler that will be used to generate promises if necessary
        :param promise: a specified promise that will be used to notify requesters.
        """
        self._method_call = method_call
        if promise:
            self._promise = promise
        else:
            self._promise = Promise(scheduler)

    def promise(self):
        """
        Retrieve the promise that will be used to notify of the results.
        :return promise
        """
        return self._promise

    def __call__(self):
        logger.debug('Executing call method: %s' % self._method_call)

        try:
            result = self._method_call()

            # 2.3.1
            if result == self._promise:
                raise TypeError

            try:
                result.then(_generate_promise_fulfilled_ripple(self._promise),
                            _generate_promise_rejected_ripple(self._promise))
            except AttributeError:
                self._promise.resolved(result)
        except Exception as e:
            if logger.isEnabledFor(logging.DEBUG):
                logger.exception('Rejecting promise')
            self._promise.rejected(e)


def _generate_promise_fulfilled_ripple(child_promise):
    """
    Generates a method that will resolve the child promise with the result value.  This is used when a promise returns
    a promise.
    :param child_promise: promise to notify.
    :return: generated method.
    """
    def fulfilled(result):
        child_promise.resolved(result)

    return fulfilled


def _generate_promise_rejected_ripple(child_promise):
    """
    Generates a method that will reject the child promise with the rejected value.  This is used when a promise returns
    a promise.
    :param child_promise: promise to reject.
    :return: generated method.
    """
    def rejected(error):
        child_promise.rejected(error)

    return rejected
