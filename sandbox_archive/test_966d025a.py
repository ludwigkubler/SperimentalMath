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
    
    def generate_k_sat_instance(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def incidence_algebra(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        algebra = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in clause:
                for j in clause:
                    if i != 0 and j != 0:
                        algebra[abs(i) - 1][abs(j) - 1] += 1
        return algebra
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def p_adic_metric_complexity(algebra):
        n = len(algebra)
        max_value = max(max(row) for row in algebra)
        if max_value == 0:
            return 0
        return math.log2(max_value + 1)
    
    def clause_tree_width(clauses):
        n = len(set(abs(x) for x in sum(clauses, [])))
        tree_width = 0
        for i in range(n):
            neighbors = [j for j in range(n) if algebra[i][j] > 0]
            tree_width = max(tree_width, len(neighbors))
        return tree_width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate