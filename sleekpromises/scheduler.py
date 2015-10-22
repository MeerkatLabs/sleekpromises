"""
Wraps scheduling functionality.
"""
import uuid
import logging

from sleekxmpp.plugins.base import base_plugin

from sleekpromises.promises import Promise, PromiseList, Deferred

logger = logging.getLogger(__name__)


def _generate_cancel_method(scheduler_name, scheduler):
    """
    Handler that will be used to interact with the tasks that are going to be executed or not.
    """
    def cancel():
        """
        Cancel the task.
        :return:
        """
        scheduler.remove(scheduler_name)

    return cancel


class _Scheduler(base_plugin):
    """
    Scheduler plugin that will wrap the scheduling functionality for the bots that are being defined.
    """

    name = 'sleekpromises_scheduler'
    dependencies = {}
    description = 'Sleek Promises Scheduler'

    def plugin_init(self):
        """
        Initialize the scheduler.
        :return:
        """

    def post_init(self):
        """
        Patch builtin plugins to work with promises without breaking current functionality.
        :return:
        """
        if self.xmpp['xep_0050']:
            _patch_command_processing(self.xmpp['xep_0050'])

    def schedule_task(self, callback, delay=1.0, repeat=False, execute_now=False):
        """
        Schedule a task that is to be executed by the scheduling thread of the bot.
        :param callback: callback that is to be executed.
        :param delay: delay time that will be waited before executing
        :param repeat: should the task be repeated
        :param execute_now: execute the task immediately
        :return: cancel method
        """
        task_name = str(uuid.uuid4())

        self.xmpp.schedule(task_name, delay, callback, repeat=repeat)

        return _generate_cancel_method(task_name, self.xmpp.scheduler)

    def defer(self, method, *args, **kwargs):
        """
        Defer the method execution till a later time, but return a promise that will be used to notify listeners of the
        results.
        :param method: method to execute.
        :param args: args associated with the method to execute.
        :param kwargs: kwargs associated with the method to execute.
        :return: promise associated with the deferred.
        """
        def execution_method():
            return method(*args, **kwargs)

        deferred = Deferred(execution_method, self)

        self.schedule_task(deferred, delay=0.0)

        return deferred.promise()

    def promise(self):
        """
        Generate a promise for this scheduler without providing a deferred.
        :return:
        """
        return Promise(self)

    def generate_callback_promise(self, _promise):
        """
        Generate a callback that can be used with iq.send(callback) in order to use promises.
        :param _promise: promise to resolve when the call back is returned.
        """
        def method(result):
            _promise.resolved(result)

        return method

    def generate_promise_handler(self, method, *args, **kwargs):
        """
        This will generate a promise method that can take multiple arguments for execution.  It makes the assumption
        that the method that is being wrapped will take the result of the called promise as the first argument.
        :param method: callable to wrap
        :param args: additional args
        :param kwargs: additional kwargs
        :return: wrapped method.
        """
        def new_method(result):
            return method(result, *args, **kwargs)

        return new_method

    def create_promise_list(self, *promises):
        """
        Create a promise list based on the promises provided.
        """
        return PromiseList(promises, self).promise


# Define the plugin that will be used to access this plugin.
sleekpromises_scheduler = _Scheduler


def _patch_command_processing(command_plugin):
    """
    Patches the command processing functionality to work with promises.
    :param command_plugin: command plugin to modify.
    :return:
    """

    if hasattr(command_plugin.__class__, '_old_process_command_response'):
        logger.debug('Already patched')
        return

    command_plugin.__class__._old_process_command_response = command_plugin.__class__._process_command_response

    def new_command_response(self, iq, session):

        promise_or_session = session

        # Can assume that the promise_or_session is a promise.
        if hasattr(promise_or_session, 'then'):
            logger.debug('Handling a promise')

            def promise_handler(_session):
                logger.debug('Promise resolved')
                self._old_process_command_response(iq, _session)

            promise_or_session.then(promise_handler)
        else:
            logger.debug('Handling default path')
            self._old_process_command_response(iq, promise_or_session)

    command_plugin.__class__._process_command_response = new_command_response

    logger.debug('Patching the command processing plugin')
