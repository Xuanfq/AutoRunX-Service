
from collections.abc import Callable, Iterable, Mapping
from threading import Thread
from typing import Any


class ThreadWithReturnValue(Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return

    def get_return(self):
        return self._return


def sync_function_call(function, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None):
    t = ThreadWithReturnValue(target=function, args=args, kwargs=kwargs)
    t.start()
    return t.join()
