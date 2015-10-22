import unittest
import time

from sleekxmpp.test import SleekTest
import mock


class SchedulerTester(SleekTest):

    def tearDown(self):
        self.stream_close()

    def test_simple_schedule(self):

        from sleekpromises import register_sleek_promises
        register_sleek_promises()

        self.stream_start(plugins=['sleekpromises_scheduler', ])

        callback = mock.MagicMock()
        delay = 0.0

        self.xmpp['sleekpromises_scheduler'].schedule_task(callback, delay=delay)

        time.sleep(delay + 0.1)

        self.assertEqual(callback.call_count, 1)

    def test_cancel(self):

        from sleekpromises import register_sleek_promises
        register_sleek_promises()

        self.stream_start(plugins=['sleekpromises_scheduler', ])

        callback = mock.MagicMock()
        delay = 4.0

        cancel_handler = self.xmpp['sleekpromises_scheduler'].schedule_task(callback, delay=delay)

        time.sleep(delay/2)

        cancel_handler()

        time.sleep(delay + 1)

        self.assertEqual(callback.call_count, 0)

    def test_defer(self):

        from sleekpromises import register_sleek_promises
        register_sleek_promises()

        self.stream_start(plugins=['sleekpromises_scheduler', ])

        return_value = 'return_value'

        callback = mock.Mock()
        callback.return_value = return_value

        promise_result = mock.Mock()

        promise = self.xmpp['sleekpromises_scheduler'].defer(callback).then(promise_result)

        time.sleep(1.0)

        self.assertEqual(callback.call_count, 1)
        self.assertEqual(promise_result.call_count, 1)

        args, kwargs = promise_result.call_args
        self.assertEqual(args[0], return_value)


suite = unittest.TestLoader().loadTestsFromTestCase(SchedulerTester)
