"""
2.2.4: `onFulfilled` or `onRejected` must not be called until the execution context stack contains only platform code.
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.2.4.js

I don't know if this is testable since this implementation is currently running in a multi-threaded environment, unlike
the javascript environment that the proimse tests and spec were developed for.
"""
