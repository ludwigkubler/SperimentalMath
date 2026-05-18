# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from collections import defaultdict
from fractions import Fraction

def matrix_mult(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in A[1:]]
        det += ((-1) ** col) * A[0][col] * matrix_determinant(minor)
    return det

def matrix_inverse(A):
    n = len(A)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        if A[col][col] == 0:
            for row in range(col+1, n):
                if A[row][col] != 0:
                    A[col], A[row] = A[row], A[col]
                    I[col], I[row] = I[row], I[col]
                    break
        pivot = A[col][col]
        for i in range(n):
            A[col][i] = Fraction(A[col][i], pivot)
            I[col][i] = Fraction(I[col][i], pivot)
        for row in range(n):
            if row != col and A[row][col] != 0:
                factor = A[row][col]
                for i in range(n):
                    A[row][i] -= factor * A[col][i]
                    I[row][i] -= factor * I[col][i]
    return I

def matrix_rank(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for row in range(n):
        if rank >= m:
            break
        i = row
        while i < n and A[i][rank] == 0:
            i += 1
        if i == n:
            continue
        A[row], A[i] = A[i], A[row]
        pivot = A[row][rank]
        for j in range(rank, m):
            A[row][j] = Fraction(A[row][j], pivot)
        for i in range(n):
            if i != row and A[i][rank] != 0:
                factor = A[i][rank]
                for j in range(rank, m):
                    A[i][j] -= factor * A[row][j]
        rank += 1
    return rank

def matrix_padded_determinant(A, m):
    n = len(A)
    if m == 0:
        return matrix_determinant(A)
    if m >= n:
        return 0
    det = 0
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        det += ((-1) ** i) * A[0][i] * matrix_padded_determinant(minor, m-1)
    return det

def matrix_padded_determinant_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand(A, m):
    n = len(A)
    if m == 0:
        return matrix_determinant(A)
    if m >= n:
        return 0
    det = 0
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        det += ((-1) ** i) * A[0][i] * matrix_padded_determinant_expand(minor, m-1)
    return det

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)
        for terms, val in minor_coeffs.items():
            new_terms = (i,) + terms
            coeffs[new_terms] += ((-1) ** i) * val
    return coeffs

def matrix_padded_determinant_expand_coeffs(A, m):
    n = len(A)
    if m == 0:
        return {(): matrix_determinant(A)}
    if m >= n:
        return {}
    coeffs = defaultdict(int)
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in A[1:]]
        minor_coeffs = matrix_padded_determinant_expand_coeffs(minor, m-1)