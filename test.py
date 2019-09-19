from deflib.lists import DynamicCoordList as DCL, DynamicMultiDimCoordList as DMDCL

A = DMDCL(2)
A[0, 5] = 'A'
A[0, 1] = 'B'
A[0, -1] = 'C'
A[0, 3] = 'D'
A[0, 5] = 'E'
print(list(A))
print(str(A))
print(repr(A))
print(A)
del A[0, 1:1, 4]
print(A)
# A[1: 4] = iter([5, 6, 7])
print(A)
print(A[0, -1:1, 3])
print(A)
A[0, 2] = 5
B = DCL()
B[0] = 0
B[1] = B
# A[1:3] = [0, 1]
print(B)

while True:
    exec(input())
