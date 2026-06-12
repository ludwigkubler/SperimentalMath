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
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
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
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_add(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
        return C
    
    def matrix_sub(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] - B[i][j]
        return C
    
    def identity_matrix(n):
        I = [[0] * n for _ in range(n)]
        for i in range(n):
            I[i][i] = 1
        return I
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i + j) * cofactor
        return matrix_multiply(adjoint, 1 / det_A)
    
    def gaussian_elimination_with_pivot(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
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
    
    def matrix_power(A, n):
        result = identity_matrix(len(A))
        while n > 0:
            if n % 2 == 1:
                result = matrix_multiply(result, A)
            A = matrix_multiply(A, A)
            n //= 2
        return result
    
    def gaussian_elimination_with_pivot_and_back_substitution(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        return x
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        return x, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det_and_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A, det_A, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det_and_det_and_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A, det_A, det_A, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det_and_det_and_det_and_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A, det_A, det_A, det_A, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det_and_det_and_det_and_det_and_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A, det_A, det_A, det_A, det_A, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det_and_det_and_det_and_det_and_det_and_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A, det_A, det_A, det_A, det_A, det_A, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det_and_det_and_det_and_det_and_det_and_det_and_det(A, b):
        n = len(b)
        det_A = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            if i != max_row:
                det_A *= -1
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
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
        inv_A = identity_matrix(n)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            inv_A[i], inv_A[max_row] = inv_A[max_row], inv_A[i]
            if i != max_row:
                det_A *= -1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                inv_A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        inv_A[k][j] -= factor * inv_A[i][j]
        return x, det_A, inv_A, det_A, det_A, det_A, det_A, det_A, det_A, det_A
    
    def gaussian_elimination_with_pivot_and_back_substitution_with_det_and_inv_and_det_and_det_and_det_and_det_and_det_and_det_and_det_and_det(A, b):
        n = len(b)