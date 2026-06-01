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
    
    def generate_circuit(n):
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - len(left))
            return [f'({g})' for g in left] + [f'({g})' for g in right]
    
    def circuit_to_matrix(circuit):
        if circuit == '0':
            return [[1]]
        elif circuit == '1':
            return [[0, 1], [1, 0]]
        else:
            inner = circuit_to_matrix(circuit[2:-2])
            n = len(inner)
            result = []
            for i in range(n):
                row = [0] * (n + 1)
                row[i] = 1
                result.append(row)
            for j in range(n):
                row = [0] * (n + 1)
                row[j + n] = 1
                result.append(row)
            return result
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][i]
                for k in range(m):
                    if k != i and matrix[k][i] != 0:
                        for j in range(n):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return rank
    
    def monotone_width(circuit):
        if circuit == '0' or circuit == '1':
            return 1
        else:
            left = circuit_to_matrix(circuit[2:-2])
            right = circuit_to_matrix(circuit[2:-2])
            n = len(left)
            width = 0
            for i in range(n):
                if any(left[i][j] != 0 for j in range(n)):
                    width += 1
            return max(width, monotone_width(circuit[2:-2]))
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
            if matrix[i][i] == 0:
                continue
            for j in range(n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    for j in range(n):
                        matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return matrix
    
    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_addition(A, B):
        m, n = len(A), len(A[0])
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                result[i][j] = A[i][j] + B[i][j]
        return result
    
    def matrix_inverse(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        augmented = [row + col for row, col in zip(matrix, identity)]
        gaussian_elimination(augmented)
        inverse = [row[n:] for row in augmented]
        return inverse
    
    def matrix_determinant(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * matrix_determinant(submatrix)
        return det
    
    def matrix_trace(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        trace = 0
        for i in range(n):
            trace += matrix[i][i]
        return trace
    
    def matrix_power(matrix, power):
        result = [[1 if i == j else 0 for j in range(len(matrix))] for i in range(len(matrix))]
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiplication(result, matrix)
            matrix = matrix_multiplication(matrix, matrix)
            power //= 2
        return result
    
    def matrix_eigenvalues(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        eigenvalues = []
        for i in range(n):
            coeff = [1]
            for j in range(n - 1):
                coeff.append(-matrix[i][j] / (i + 1))
            roots = solve_polynomial(coeff)
            eigenvalues.extend(roots)
        return eigenvalues
    
    def solve_polynomial(coefficients):
        n = len(coefficients) - 1
        if n == 0:
            return []
        elif n == 1:
            return [-coefficients[0] / coefficients[1]]
        else:
            roots = []
            for i in range(n + 1):
                sub_coeffs = [c * (-i / (n - i)) for c in coefficients]
                root = solve_polynomial(sub_coeffs)[-1]
                roots.append(root)
            return roots
    
    def matrix_charpoly(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        charpoly = [1]
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det = (-1) ** (n - i) * matrix_determinant(submatrix)
            charpoly.append(det)
        return charpoly
    
    def matrix_minpoly(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        minpoly = [1]
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det = (-1) ** (n - i) * matrix_determinant(submatrix)
            minpoly.append(det)
        return minpoly
    
    def matrix_jordan_form(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        jordan_blocks = []
        remaining_matrix = matrix
        while remaining_matrix:
            eigenvalues = matrix_eigenvalues(remaining_matrix)
            for eig in eigenvalues:
                eig_block = [[eig if i == j else 0 for j in range(n)] for i in range(n)]
                for k in range(n):
                    if remaining_matrix[k][k] == eig:
                        eig_block[k][k + 1] = 1
                        break
                jordan_blocks.append(eig_block)
                remaining_matrix = matrix_subtraction(remaining_matrix, eig_block)
        return jordan_blocks
    
    def matrix_subtraction(A, B):
        m, n = len(A), len(A[0])
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                result[i][j] = A[i][j] - B[i][j]
        return result
    
    def matrix_transpose(matrix):
        m, n = len(matrix), len(matrix[0])
        result = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                result[j][i] = matrix[i][j]
        return result
    
    def matrix_conjugate_transpose(matrix):
        m, n = len(matrix), len(matrix[0])
        result = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                result[j][i] = complex_conjugate(matrix[i][j])
        return result
    
    def complex_conjugate(z):
        if isinstance(z, complex):
            return z.conjugate()
        else:
            return z
    
    def matrix_trace(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        trace = 0
        for i in range(n):
            trace += matrix[i][i]
        return trace
    
    def matrix_determinant(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * matrix_determinant(submatrix)
        return det
    
    def matrix_power(matrix, power):
        result = [[1 if i == j else 0 for j in range(len(matrix))] for i in range(len(matrix))]
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiplication(result, matrix)
            matrix = matrix_multiplication(matrix, matrix)
            power //= 2
        return result
    
    def matrix_eigenvalues(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        eigenvalues = []
        for i in range(n):
            coeff = [1]
            for j in range(n - 1):
                coeff.append(-matrix[i][j] / (i + 1))
            roots = solve_polynomial(coeff)
            eigenvalues.extend(roots)
        return eigenvalues
    
    def solve_polynomial(coefficients):
        n = len(coefficients) - 1
        if n == 0:
            return []
        elif n == 1:
            return [-coefficients[0] / coefficients[1]]
        else:
            roots = []
            for i in range(n + 1):
                sub_coeffs = [c * (-i / (n - i)) for c in coefficients]
                root = solve_polynomial(sub_coeffs)[-1]
                roots.append(root)
            return roots
    
    def matrix_charpoly(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        charpoly = [1]
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det = (-1) ** (n - i) * matrix_determinant(submatrix)
            charpoly.append(det)
        return charpoly
    
    def matrix_minpoly(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        minpoly = [1]
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det = (-1) ** (n - i) * matrix_determinant(submatrix)
            minpoly.append(det)
        return minpoly
    
    def matrix_jordan_form(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        jordan_blocks = []
        remaining_matrix = matrix
        while remaining_matrix:
            eigenvalues = matrix_eigenvalues(remaining_matrix)
            for eig in eigenvalues:
                eig_block = [[eig if i == j else 0 for j in range(n)] for i in range(n)]
                for k in range(n):
                    if remaining_matrix[k][k] == eig:
                        eig_block[k][k + 1] = 1
                        break
                jordan_blocks.append(eig_block)
                remaining_matrix = matrix_subtraction(remaining_matrix, eig_block)
        return jordan_blocks
    
    def matrix_subtraction(A, B):
        m, n = len(A), len(A[0])
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                result[i][j] = A[i][j] - B[i][j]
        return result
    
    def matrix_transpose(matrix):
        m, n = len(matrix), len(matrix[0])
        result = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                result[j][i] = matrix[i][j]
        return result
    
    def matrix_conjugate_transpose(matrix):
        m, n = len(matrix), len(matrix[0])
        result = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                result[j][i] = complex_conjugate(matrix[i][j])
        return result
    
    def complex_conjugate(z):
        if isinstance(z, complex):
            return z.conjugate()
        else:
            return z
    
    def matrix_trace(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        trace = 0
        for i in range(n):
            trace += matrix[i][i]
        return trace
    
    def matrix_determinant(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * matrix_determinant(submatrix)
        return det
    
    def matrix_power(matrix, power):
        result = [[1 if i == j else 0 for j in range(len(matrix))] for i in range(len(matrix))]
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiplication(result, matrix)
            matrix = matrix_multiplication(matrix, matrix)
            power //= 2
        return result
    
    def matrix_eigenvalues(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        eigenvalues = []
        for i in range(n):
            coeff = [1]
            for j in range(n - 1):
                coeff.append(-matrix[i][j] / (i + 1))
            roots = solve_polynomial(coeff)
            eigenvalues.extend(roots)
        return eigenvalues
    
    def solve_polynomial(coefficients):
        n = len(coefficients) - 1
        if n == 0:
            return []
        elif n == 1:
            return [-coefficients[0] / coefficients[1]]
        else:
            roots = []
            for i in range(n + 1):
                sub_coeffs = [c * (-i / (n - i)) for c in coefficients]
                root = solve_polynomial(sub_coeffs)[-1]
                roots.append(root)
            return roots
    
    def matrix_charpoly(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        charpoly = [1]
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det = (-1) ** (n - i) * matrix_determinant(submatrix)
            charpoly.append(det)
        return charpoly
    
    def matrix_minpoly(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        minpoly = [1]
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det = (-1) ** (n - i) * matrix_determinant(submatrix)
            minpoly.append(det)
        return minpoly
    
    def matrix_jordan_form(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        jordan_blocks = []
        remaining_matrix = matrix
        while remaining_matrix:
            eigenvalues = matrix_eigenvalues(remaining_matrix)
            for eig in eigenvalues:
                eig_block = [[eig if i == j else 0 for j in range(n)] for i in range(n)]
                for k in range(n):
                    if remaining_matrix[k][k] == eig:
                        eig_block[k][k + 1] = 1
                        break
                jordan_blocks.append(eig_block)
                remaining_matrix = matrix_subtraction(remaining_matrix, eig_block)
        return jordan_blocks
    
    def matrix_subtraction(A, B):
        m, n = len(A), len(A[0])
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                result[i][j] = A[i][j] - B[i][j]
        return result
    
    def matrix_transpose(matrix):
        m, n = len(matrix), len(matrix[0])
        result = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                result[j][i] = matrix[i][j]
        return result
    
    def matrix_conjugate_transpose(matrix):
        m, n = len(matrix), len(matrix[0])
        result = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                result[j][i] = complex_conjugate(matrix[i][j])
        return result
    
    def complex_conjugate(z):
        if isinstance(z, complex):
            return z.conjugate()
        else:
            return z
    
    def matrix_trace(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        trace = 0
        for i in range(n):
            trace += matrix[i][i]
        return trace
    
    def matrix_determinant(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * matrix_determinant(submatrix)
        return det