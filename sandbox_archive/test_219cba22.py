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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def matrix_add(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m, n = len(A), len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        det = determinant(A)
        if det == 0:
            return None
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * minor
        return matrix_mul(adjoint, Fraction(1, det))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]