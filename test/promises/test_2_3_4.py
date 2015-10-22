"""
2.3.4: If `x` is not an object or function, fulfill `promise` with `x`
https://github.com/promises-aplus/promises-tests/blob/2.1.1/lib/tests/2.3.4.js
"""
from test.promises.helpers import generate_fulfilled_test_case, generate_rejected_test_case

dummy = {'dummy': 'dummy'}
sentinel = {'sentinel': 'sentinel'}


def primitive_fulfilled_wrapper(primitive_value):
    def test_method(test_case, promise, done):

        def return_primitive(value):
            return primitive_value

        def retrieve_primitive(value):
            test_case.assertEqual(value, primitive_value)
            done()

        promise.then(return_primitive).then(retrieve_primitive)

    return test_method


def primitive_rejected_wrapper(primitive_value):
    def test_method(test_case, promise, done):

        def return_primitive(value):
            return primitive_value

        def retrieve_primitive(value):
            test_case.assertEqual(value, primitive_value)
            done()

        promise.then(None, return_primitive).then(retrieve_primitive)

    return test_method

None_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(None), dummy,
                                                      module=__name__,
                                                      name='None_FulfilledTestCase')
Zero_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(0), dummy,
                                                      module=__name__,
                                                      name='Zero_FulfilledTestCase')
One_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(1), dummy,
                                                     module=__name__,
                                                     name='One_FulfilledTestCase')
String_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper('asdf'), dummy,
                                                        module=__name__,
                                                        name='String_FulfilledTestCase')
EmptyString_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(''), dummy,
                                                             module=__name__,
                                                             name='EmptyString_FulfilledTestCase')
List_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(['asdf', 'value1']), dummy,
                                                      module=__name__,
                                                      name='List_FulfilledTestCase')
EmptyList_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper([]), dummy,
                                                           module=__name__,
                                                           name='EmptyList_FulfilledTestCase')
Dict_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(dict(key='value')), dummy,
                                                      module=__name__,
                                                      name='Dict_FulfilledTestCase')
EmptyDict_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(dict()), dummy,
                                                           module=__name__,
                                                           name='EmptyDict_FulfilledTestCase')
Tuple_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(('asdf', 'value1', )), dummy,
                                                       module=__name__,
                                                       name='Tuple_FulfilledTestCase')
EmptyTuple_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(()), dummy,
                                                            module=__name__,
                                                            name='EmptyTuple_FulfilledTestCase')
Object_FulfilledTestCase = generate_fulfilled_test_case(primitive_fulfilled_wrapper(object()), dummy,
                                                        module=__name__,
                                                        name='Object_FulfilledTestCase')

None_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(None), dummy,
                                                    module=__name__,
                                                    name='None_RejectedTestCase')
Zero_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(0), dummy,
                                                    module=__name__,
                                                    name='Zero_RejectedTestCase')
One_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(1), dummy,
                                                   module=__name__,
                                                   name='One_RejectedTestCase')
String_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper('asdf'), dummy,
                                                      module=__name__,
                                                      name='String_RejectedTestCase')
EmptyString_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(''), dummy,
                                                           module=__name__,
                                                           name='EmptyString_RejectedTestCase')
List_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(['asdf', 'value1']), dummy,
                                                    module=__name__,
                                                    name='List_RejectedTestCase')
EmptyList_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper([]), dummy,
                                                         module=__name__,
                                                         name='EmptyList_RejectedTestCase')
Dict_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(dict(key='value')), dummy,
                                                    module=__name__,
                                                    name='Dict_RejectedTestCase')
EmptyDict_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(dict()), dummy,
                                                         module=__name__,
                                                         name='EmptyDict_RejectedTestCase')
Tuple_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(('asdf', 'value1', )), dummy,
                                                     module=__name__,
                                                     name='Tuple_RejectedTestCase')
EmptyTuple_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(()), dummy,
                                                          module=__name__,
                                                          name='EmptyTuple_RejectedTestCase')
Object_RejectedTestCase = generate_rejected_test_case(primitive_rejected_wrapper(object()), dummy,
                                                      module=__name__,
                                                      name='Object_RejectedTestCase')
