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
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment[literal] = literal > 0
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
        
        literal = random.choice(cnf)[0]
        assignment[literal] = True
        if dpll(cnf, assignment):
            return True
        assignment[literal] = False
        if dpll(cnf, assignment):
            return True
        return False
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-lit in clauses[i] and lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                        new_clause = [lit for lit in set(clauses[i]) | set(clauses[j]) if lit != -lit]
                        if len(new_clause) > width:
                            width = len(new_clause)
                        if not new_clause:
                            return float('inf')
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return width
    
    def vector_space_representation(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        vectors = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    vectors[lit][lit] += 1
                else:
                    vectors[-lit][-lit] -= 1
        return vectors
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            b[i] /= factor
            for j in range(i + 1, n):
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= M[i][j] * x[j]
        return x
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = matrix[:]
        r = 0
        for i in range(n):
            if r < m:
                max_row = r
                for j in range(r + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[r], A[max_row] = A[max_row], A[r]
                if A[r][i]:
                    for j in range(n):
                        A[r][j] /= A[r][i]
                    b[r] /= A[r][i]
                    for j in range(r + 1, m):
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[r][k]
                        b[j] -= factor * b[r]
                    r += 1
        return r
    
    def dimension_of_representation(vectors):
        n = len(vectors)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if vectors[i][j]:
                    A[i][j] = 1
        return rank(A)
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-lit in clauses[i] and lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                        new_clause = [lit for lit in set(clauses[i]) | set(clauses[j]) if lit != -lit]
                        if len(new_clause) > width:
                            width = len(new_clause)
                        if not new_clause:
                            return float('inf')
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return width
    
    def vector_space_representation(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        vectors = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    vectors[lit][lit] += 1
                else:
                    vectors[-lit][-lit] -= 1
        return vectors
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            b[i] /= factor
            for j in range(i + 1, n):
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= M[i][j] * x[j]
        return x
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = matrix[:]
        r = 0
        for i in range(n):
            if r < m:
                max_row = r
                for j in range(r + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[r], A[max_row] = A[max_row], A[r]
                if A[r][i]:
                    for j in range(n):
                        A[r][j] /= A[r][i]
                    b[r] /= A[r][i]
                    for j in range(r + 1, m):
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[r][k]
                        b[j] -= factor * b[r]
                    r += 1
        return r
    
    def dimension_of_representation(vectors):
        n = len(vectors)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if vectors[i][j]:
                    A[i][j] = 1
        return rank(A)
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-lit in clauses[i] and lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                        new_clause = [lit for lit in set(clauses[i]) | set(clauses[j]) if lit != -lit]
                        if len(new_clause) > width:
                            width = len(new_clause)
                        if not new_clause:
                            return float('inf')
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return width
    
    def vector_space_representation(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        vectors = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    vectors[lit][lit] += 1
                else:
                    vectors[-lit][-lit] -= 1
        return vectors
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            b[i] /= factor
            for j in range(i + 1, n):
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= M[i][j] * x[j]
        return x
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = matrix[:]
        r = 0
        for i in range(n):
            if r < m:
                max_row = r
                for j in range(r + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[r], A[max_row] = A[max_row], A[r]
                if A[r][i]:
                    for j in range(n):
                        A[r][j] /= A[r][i]
                    b[r] /= A[r][i]
                    for j in range(r + 1, m):
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[r][k]
                        b[j] -= factor * b[r]
                    r += 1
        return r
    
    def dimension_of_representation(vectors):
        n = len(vectors)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if vectors[i][j]:
                    A[i][j] = 1
        return rank(A)
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-lit in clauses[i] and lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                        new_clause = [lit for lit in set(clauses[i]) | set(clauses[j]) if lit != -lit]
                        if len(new_clause) > width:
                            width = len(new_clause)
                        if not new_clause:
                            return float('inf')
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return width
    
    def vector_space_representation(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        vectors = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    vectors[lit][lit] += 1
                else:
                    vectors[-lit][-lit] -= 1
        return vectors
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            b[i] /= factor
            for j in range(i + 1, n):
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= M[i][j] * x[j]
        return x
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = matrix[:]
        r = 0
        for i in range(n):
            if r < m:
                max_row = r
                for j in range(r + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[r], A[max_row] = A[max_row], A[r]
                if A[r][i]:
                    for j in range(n):
                        A[r][j] /= A[r][i]
                    b[r] /= A[r][i]
                    for j in range(r + 1, m):
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[r][k]
                        b[j] -= factor * b[r]
                    r += 1
        return r
    
    def dimension_of_representation(vectors):
        n = len(vectors)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if vectors[i][j]:
                    A[i][j] = 1
        return rank(A)
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-lit in clauses[i] and lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                        new_clause = [lit for lit in set(clauses[i]) | set(clauses[j]) if lit != -lit]
                        if len(new_clause) > width:
                            width = len(new_clause)
                        if not new_clause:
                            return float('inf')
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return width
    
    def vector_space_representation(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        vectors = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    vectors[lit][lit] += 1
                else:
                    vectors[-lit][-lit] -= 1
        return vectors
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            b[i] /= factor
            for j in range(i + 1, n):
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= M[i][j] * x[j]
        return x
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = matrix[:]
        r = 0
        for i in range(n):
            if r < m:
                max_row = r
                for j in range(r + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[r], A[max_row] = A[max_row], A[r]
                if A[r][i]:
                    for j in range(n):
                        A[r][j] /= A[r][i]
                    b[r] /= A[r][i]
                    for j in range(r + 1, m):
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[r][k]
                        b[j] -= factor * b[r]
                    r += 1