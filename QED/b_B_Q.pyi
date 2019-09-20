from decimal import Decimal
from ..lists import DynamicMultiDimCoordList as DMDCL
from typing import Union, Set, Iterable, List, Tuple, TypeVar

Float = TypeVar('Float', Decimal, float)

def B_table(M_up: Set[Tuple[int, int]],
            M_bypass: Set[Tuple[int, int]] = ...,
            mass: Float = ...)\
        -> DMDCL: ...

def b_table(M_up: Set[Tuple[int, int]],
            M_bypass: Set[Tuple[int, int]] = ...,
            mass: Float = ...)\
        -> DMDCL: ...

def Q_table(M_up: Set[Tuple[int, int]],
            M_bypass: Set[Tuple[int, int]] = ...,
            mass: Float = ...)\
        -> DMDCL: ...

def vec_B(t: int,
          u: int,
          M_bypass: Set[Tuple[int, int]] = ...,
          mass: Float = ...,
          sign: Union[str, None] = ...)\
        -> Tuple[Float]: ...

def vec_b(t: int,
          u: int,
          M_bypass: Set[Tuple[int, int]] = ...,
          mass: Float = ...,
          sign: Union[str, None] = ...)\
        -> Tuple[Float]: ...

def Q(t: int,
          u: int,
          M_bypass: Set[Tuple[int, int]] = ...,
          mass: Float = ...,
          sign: Union[str, None] = ...): ...

def Q_set(M: Set[Tuple[int, int]],
          M_bypass: Set[Tuple[int, int]] = ...,
          mass: Float = ...)\
        -> Float: ...
