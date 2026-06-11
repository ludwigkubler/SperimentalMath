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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        return [b[i] for i in range(n)]

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def gaussian_elimination_with_pivoting(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        return [b[i] for i in range(n)]

    def matrix_multiplication_with_pivoting(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            B[i], B[max_idx] = B[max_idx], B[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for k in range(n):
                B[k][i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                        B[k][j] -= factor * B[k][i]
        return [B[i] for i in range(n)]

    def gaussian_elimination_with_pivoting_and_back_substitution(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x

    def gaussian_elimination_with_pivoting_and_back_substitution_with_pivot_and_scale_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation_and_scaling_and_permutation(A, b):
        n = len(b)
        for i in range(n):
            max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_idx] = A[max_idx], A[i]
            b[i], b[max_idx] = b[max_idx], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor