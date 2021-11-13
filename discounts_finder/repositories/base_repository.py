from abc import ABCMeta
from typing import Any, Union, Dict


class BaseRepository(metaclass=ABCMeta):
    def create(self, obj: Any):
        raise NotImplementedError()

    def read(self, obj_id: Union[str, int]):
        raise NotImplementedError()

    def update(self, obj_id: Any, fields: Dict[str, Any], allow_none: bool = False):
        raise NotImplementedError()

    def delete(self, obj_id: Union[str, int]):
        raise NotImplementedError()

    def read_all(self):
        raise NotImplementedError()
