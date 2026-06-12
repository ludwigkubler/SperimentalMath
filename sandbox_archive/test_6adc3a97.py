# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b

    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_inv(A, mod):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
                I[i][j] = (I[i][j] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                        I[k][j] = (I[k][j] - factor * I[i][j]) % mod
        return I

    def matrix_sub(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C

    def matrix_add(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] + B[i][j]) % mod
        return C

    def matrix_mul_scalar(A, scalar, mod):
        n = len(A)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B[i][j] = (A[i][j] * scalar) % mod
        return B

    def matrix_trace(A):
        n = len(A)
        trace = 0
        for i in range(n):
            trace += A[i][i]
        return trace

    def matrix_det(A, mod):
        n = len(A)
        if n == 1:
            return A[0][0] % mod
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * matrix_det(submatrix, mod)
            sign *= -1
        return det % mod

    def gaussian_elimination_mod(A, b, mod):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
            b[i] = (b[i] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                    b[k] = (b[k] - factor * b[i]) % mod
        return b

    def matrix_mult_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C

    def matrix_inv_mod(A, mod):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
                I[i][j] = (I[i][j] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                        I[k][j] = (I[k][j] - factor * I[i][j]) % mod
        return I

    def matrix_sub_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C

    def matrix_add_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] + B[i][j]) % mod
        return C

    def matrix_mul_scalar_mod(A, scalar, mod):
        n = len(A)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B[i][j] = (A[i][j] * scalar) % mod
        return B

    def matrix_trace_mod(A, mod):
        n = len(A)
        trace = 0
        for i in range(n):
            trace += A[i][i]
        return trace % mod

    def matrix_det_mod(A, mod):
        n = len(A)
        if n == 1:
            return A[0][0] % mod
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * matrix_det_mod(submatrix, mod)
            sign *= -1
        return det % mod

    def gaussian_elimination_mod(A, b, mod):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
            b[i] = (b[i] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                    b[k] = (b[k] - factor * b[i]) % mod
        return b

    def matrix_mult_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C

    def matrix_inv_mod(A, mod):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
                I[i][j] = (I[i][j] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                        I[k][j] = (I[k][j] - factor * I[i][j]) % mod
        return I

    def matrix_sub_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C

    def matrix_add_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] + B[i][j]) % mod
        return C

    def matrix_mul_scalar_mod(A, scalar, mod):
        n = len(A)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B[i][j] = (A[i][j] * scalar) % mod
        return B

    def matrix_trace_mod(A, mod):
        n = len(A)
        trace = 0
        for i in range(n):
            trace += A[i][i]
        return trace % mod

    def matrix_det_mod(A, mod):
        n = len(A)
        if n == 1:
            return A[0][0] % mod
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * matrix_det_mod(submatrix, mod)
            sign *= -1
        return det % mod

    def gaussian_elimination_mod(A, b, mod):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
            b[i] = (b[i] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                    b[k] = (b[k] - factor * b[i]) % mod
        return b

    def matrix_mult_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C

    def matrix_inv_mod(A, mod):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
                I[i][j] = (I[i][j] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                        I[k][j] = (I[k][j] - factor * I[i][j]) % mod
        return I

    def matrix_sub_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C

    def matrix_add_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] + B[i][j]) % mod
        return C

    def matrix_mul_scalar_mod(A, scalar, mod):
        n = len(A)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B[i][j] = (A[i][j] * scalar) % mod
        return B

    def matrix_trace_mod(A, mod):
        n = len(A)
        trace = 0
        for i in range(n):
            trace += A[i][i]
        return trace % mod

    def matrix_det_mod(A, mod):
        n = len(A)
        if n == 1:
            return A[0][0] % mod
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * matrix_det_mod(submatrix, mod)
            sign *= -1
        return det % mod

    def gaussian_elimination_mod(A, b, mod):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
            b[i] = (b[i] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                    b[k] = (b[k] - factor * b[i]) % mod
        return b

    def matrix_mult_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C

    def matrix_inv_mod(A, mod):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
                I[i][j] = (I[i][j] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                        I[k][j] = (I[k][j] - factor * I[i][j]) % mod
        return I

    def matrix_sub_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C

    def matrix_add_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] + B[i][j]) % mod
        return C

    def matrix_mul_scalar_mod(A, scalar, mod):
        n = len(A)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B[i][j] = (A[i][j] * scalar) % mod
        return B

    def matrix_trace_mod(A, mod):
        n = len(A)
        trace = 0
        for i in range(n):
            trace += A[i][i]
        return trace % mod

    def matrix_det_mod(A, mod):
        n = len(A)
        if n == 1:
            return A[0][0] % mod
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * matrix_det_mod(submatrix, mod)
            sign *= -1
        return det % mod

    def gaussian_elimination_mod(A, b, mod):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
            b[i] = (b[i] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                    b[k] = (b[k] - factor * b[i]) % mod
        return b

    def matrix_mult_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C

    def matrix_inv_mod(A, mod):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]) % mod)
            A[i], A[max_row] = A[max_row], A[i]
            I[i], I[max_row] = I[max_row], I[i]
            factor = pow(A[i][i], -1, mod)
            for j in range(n):
                A[i][j] = (A[i][j] * factor) % mod
                I[i][j] = (I[i][j] * factor) % mod
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] = (A[k][j] - factor * A[i][j]) % mod
                        I[k][j] = (I[k][j] - factor * I[i][j]) % mod
        return I

    def matrix_sub_mod(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]