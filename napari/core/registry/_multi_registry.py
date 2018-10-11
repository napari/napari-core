from ..typing import Callable, Sequence

from ._registry import Registry


def default_check_others(others):
    pass


class MultiRegistry(Registry):
    def __init__(self, default=None,
                 check_others=default_check_others):
        super().__init__(get_callback=self._multi_get_callback,
                         push=self._multi_push)
        self._check_others = check_others
        self._default = default


    def _multi_get_callback(self, args):
        callback = None
        others = self._default

        if args:
            if isinstance(args[0], Callable):
                if len(args) > 2:
                    raise TypeError(f'arguments {args} are not of the form '
                                    '(callback), '
                                    '(callback, args), or '
                                    '(callback, [arg1, arg2, ...])')

                callback = args[0]
                try:
                    others = args[1]
                    if not isinstance(others, Sequence) or isinstance(others, str):
                        others = (others,)
                    else:
                        self._check_others(others)
                except IndexError:
                    pass
            else:
                others = args
                self._check_others(others)

        return callback, others

    def _multi_push(self, add_entry, callback, others):
        for arg in others:
            add_entry(arg, callback)
