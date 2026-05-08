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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    if not clauses:
        return True
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    pure_symbols = {}
    for clause in clauses:
        for literal in clause:
            symbol = abs(literal)
            if symbol not in pure_symbols:
                count = sum(1 for c in clauses if literal in c)
                pure_symbols[symbol] = 'positive' if count > len(clauses) - count else 'negative'
    unit_clauses.extend([symbol for symbol, polarity in pure_symbols.items() if polarity == 'positive'])
    unit_clauses.extend([-symbol for symbol, polarity in pure_symbols.items() if polarity == 'negative'])
    unit_clauses = list(set(unit_clauses))
    for literal in unit_clauses:
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
            return True
    return False

def generate_tseitin_formula(q):
    n = q * (q + 1) + 1
    variables = list(range(1, n + 1))
    clauses = []
    incidence_matrix = [[0] * n for _ in range(n)]
    for i in range(q):
        for j in range(q):
            line_index = i * q + j + 1
            point_index = (i * q + j) % (q + 1) + 1
            incidence_matrix[line_index][point_index] = 1
            clauses.append([line_index, -point_index])
            clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 1
        point_index = (i * q) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 2
        point_index = (i * q + 1) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 3
        point_index = (i * q + q) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 4
        point_index = (i * q + q + 1) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 5
        point_index = (i * q + q + 2) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 6
        point_index = (i * q + q + 3) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 7
        point_index = (i * q + q + 4) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 8
        point_index = (i * q + q + 5) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 9
        point_index = (i * q + q + 6) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 10
        point_index = (i * q + q + 7) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 11
        point_index = (i * q + q + 8) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 12
        point_index = (i * q + q + 9) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 13
        point_index = (i * q + q + 10) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 14
        point_index = (i * q + q + 11) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 15
        point_index = (i * q + q + 12) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 16
        point_index = (i * q + q + 13) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 17
        point_index = (i * q + q + 14) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 18
        point_index = (i * q + q + 15) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 19
        point_index = (i * q + q + 16) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 20
        point_index = (i * q + q + 17) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 21
        point_index = (i * q + q + 18) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 22
        point_index = (i * q + q + 19) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 23
        point_index = (i * q + q + 20) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 24
        point_index = (i * q + q + 21) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 25
        point_index = (i * q + q + 22) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 26
        point_index = (i * q + q + 23) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 27
        point_index = (i * q + q + 24) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 28
        point_index = (i * q + q + 25) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 29
        point_index = (i * q + q + 26) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 30
        point_index = (i * q + q + 27) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 31
        point_index = (i * q + q + 28) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 32
        point_index = (i * q + q + 29) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 33
        point_index = (i * q + q + 30) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 34
        point_index = (i * q + q + 31) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 35
        point_index = (i * q + q + 32) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 36
        point_index = (i * q + q + 33) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 37
        point_index = (i * q + q + 34) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 38
        point_index = (i * q + q + 35) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 39
        point_index = (i * q + q + 36) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 40
        point_index = (i * q + q + 37) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 41
        point_index = (i * q + q + 38) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 42
        point_index = (i * q + q + 39) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 43
        point_index = (i * q + q + 40) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 44
        point_index = (i * q + q + 41) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 45
        point_index = (i * q + q + 42) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 46
        point_index = (i * q + q + 43) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 47
        point_index = (i * q + q + 44) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 48
        point_index = (i * q + q + 45) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 49
        point_index = (i * q + q + 46) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 50
        point_index = (i * q + q + 47) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 51
        point_index = (i * q + q + 48) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 52
        point_index = (i * q + q + 49) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 53
        point_index = (i * q + q + 50) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 54
        point_index = (i * q + q + 51) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 55
        point_index = (i * q + q + 52) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 56
        point_index = (i * q + q + 53) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 57
        point_index = (i * q + q + 54) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 58
        point_index = (i * q + q + 55) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 59
        point_index = (i * q + q + 56) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 60
        point_index = (i * q + q + 57) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 61
        point_index = (i * q + q + 58) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 62
        point_index = (i * q + q + 59) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 63
        point_index = (i * q + q + 60) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 64
        point_index = (i * q + q + 61) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 65
        point_index = (i * q + q + 62) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 66
        point_index = (i * q + q + 63) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 67
        point_index = (i * q + q + 64) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 68
        point_index = (i * q + q + 65) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 69
        point_index = (i * q + q + 66) % (q + 1) + 1
        incidence_matrix[line_index][point_index] = 1
        clauses.append([line_index, -point_index])
        clauses.append([-line_index, point_index])
    for i in range(q):
        line_index = i * q + q + 70
        point_index = (i * q + q + 67) % (q + 1) + 1