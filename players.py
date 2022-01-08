import abc
from abc import abstractmethod


class BasePlayer(abc.ABC):
    @abstractmethod
    def get_move(self):
        raise NotImplementedError


class HumanPlayer(BasePlayer):
    pass


class ComputerPlayer(BasePlayer):
    pass
