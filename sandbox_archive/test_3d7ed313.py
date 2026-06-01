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
    
    def generate_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [random.choice([0, 1]) for _ in range(n)] + left + right
    
    def compute_local_ring(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def measure_unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)
        return len(unit_group)
    
    def measure_monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            if all((circuit[j] == (i >> j & 1)) for j in range(n)):
                width = max(width, bin(i).count('1'))
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def matrix_inverse(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inverse = [row[n:] for row in augmented_matrix]
        return inverse
    
    def frobenius_endomorphism(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)
        return len(unit_group)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            if all((circuit[j] == (i >> j & 1)) for j in range(n)):
                width = max(width, bin(i).count('1'))
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def matrix_inverse(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inverse = [row[n:] for row in augmented_matrix]
        return inverse
    
    def frobenius_endomorphism(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)
        return len(unit_group)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            if all((circuit[j] == (i >> j & 1)) for j in range(n)):
                width = max(width, bin(i).count('1'))
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def matrix_inverse(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inverse = [row[n:] for row in augmented_matrix]
        return inverse
    
    def frobenius_endomorphism(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)
        return len(unit_group)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            if all((circuit[j] == (i >> j & 1)) for j in range(n)):
                width = max(width, bin(i).count('1'))
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def matrix_inverse(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inverse = [row[n:] for row in augmented_matrix]
        return inverse
    
    def frobenius_endomorphism(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)
        return len(unit_group)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            if all((circuit[j] == (i >> j & 1)) for j in range(n)):
                width = max(width, bin(i).count('1'))
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def matrix_inverse(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inverse = [row[n:] for row in augmented_matrix]
        return inverse
    
    def frobenius_endomorphism(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)
        return len(unit_group)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            if all((circuit[j] == (i >> j & 1)) for j in range(n)):
                width = max(width, bin(i).count('1'))
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def matrix_inverse(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inverse = [row[n:] for row in augmented_matrix]
        return inverse
    
    def frobenius_endomorphism(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)
        return len(unit_group)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(1 << n):
            if all((circuit[j] == (i >> j & 1)) for j in range(n)):
                width = max(width, bin(i).count('1'))
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def matrix_inverse(A):
        n = len(A)
        I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inverse = [row[n:] for row in augmented_matrix]
        return inverse
    
    def frobenius_endomorphism(circuit):
        n = len(circuit)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[i][i] = circuit[i]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                F[i][i + k] = (F[i][i + k - 1] * circuit[i + k - 1]) % 2
        return F
    
    def unit_group_size(F):
        n = len(F) - 1
        unit_group = set()
        for i in range(1 << n):
            if all((F[j][i] == (j >> j & 1)) for j in range(n)):
                unit_group.add(i)