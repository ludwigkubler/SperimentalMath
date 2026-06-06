# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                cnf.append(clause)
        return cnf
    
    def quadratic_form(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]
        matrix = gaussian_elimination(matrix)
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], matrix[i][i])
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
        return x
    
    def linear_independence(matrix):
        return rank(matrix) == len(matrix)
    
    def quadratic_form_matrix(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]
        matrix = gaussian_elimination(matrix)
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], matrix[i][i])
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
        return x
    
    def linear_independence(matrix):
        return rank(matrix) == len(matrix)
    
    def quadratic_form_matrix(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]
        matrix = gaussian_elimination(matrix)
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], matrix[i][i])
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
        return x
    
    def linear_independence(matrix):
        return rank(matrix) == len(matrix)
    
    def quadratic_form_matrix(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]
        matrix = gaussian_elimination(matrix)
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], matrix[i][i])
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
        return x
    
    def linear_independence(matrix):
        return rank(matrix) == len(matrix)
    
    def quadratic_form_matrix(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]
        matrix = gaussian_elimination(matrix)
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], matrix[i][i])
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
        return x
    
    def linear_independence(matrix):
        return rank(matrix) == len(matrix)
    
    def quadratic_form_matrix(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]
        matrix = gaussian_elimination(matrix)
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], matrix[i][i])
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
        return x
    
    def linear_independence(matrix):
        return rank(matrix) == len(matrix)
    
    def quadratic_form_matrix(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]
        matrix = gaussian_elimination(matrix)
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], matrix[i][i])
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
        return x
    
    def linear_independence(matrix):
        return rank(matrix) == len(matrix)
    
    def quadratic_form_matrix(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    Q[i-1][i-1] += 1
        return Q
    
    def min_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i+1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A * A
    
    def frege_proof_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        r = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(r, n)):
                r += 1
        return r
    
    def solve_system(matrix, b):
        n = len(matrix)
        x = [Fraction(0) for _ in range(n)]