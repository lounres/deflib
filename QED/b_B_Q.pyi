from decimal import Decimal
from typing import Union, Set, Iterable, List, Tuple, TypeVar

Float = TypeVar('Float', Decimal, float)

def B_table(M_up: Set[Tuple[int]],
            M_bypass: Set[Tuple[int]] = ...,
            mass: Float = ...)\
        -> ...: ...

def b_table(M_up: Set[Tuple[int]],
            M_bypass: Set[Tuple[int]] = ...,
            mass: Float = ...)\
        -> ...: ...

def Q_table(M_up: Set[Tuple[int]],
            M_bypass: Set[Tuple[int]] = ...,
            mass: Float = ...)\
        -> ...: ...

def vec_B(t: int,
          u: int,
          M_bypass: Set[Tuple[int]] = ...,
          mass: Float = ...,
          sign: Union[str, None] = ...)\
        -> Tuple[Float]: ...

def vec_b(t: int,
          u: int,
          M_bypass: Set[Tuple[int]] = ...,
          mass: Float = ...,
          sign: Union[str, None] = ...)\
        -> Tuple[Float]: ...

def Q(t: int,
          u: int,
          M_bypass: Set[Tuple[int]] = ...,
          mass: Float = ...): ...

def Q_set(M: Set[Tuple[Float]],
          M_bypass: Set[Tuple[int]] = ...,
          mass: Float = ...)\
        -> Float: ...
