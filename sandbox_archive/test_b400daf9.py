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
    
    def generate_ac0_circuit(n, d):
        circuit = []
        for _ in range(d):
            layer = [random.choice(['AND', 'OR'])]
            for _ in range(n):
                if layer[-1] == 'AND':
                    layer.append(random.choice([True, False]))
                else:
                    layer.append(random.choice([True, False]))
            circuit.append(layer)
        return circuit
    
    def simulate_circuit(circuit, n):
        inputs = list(itertools.product([0, 1], repeat=n))
        outputs = []
        for input in inputs:
            current_input = input
            for layer in circuit:
                if layer[0] == 'AND':
                    result = all(current_input[i] == layer[i + 1] for i in range(n))
                else:
                    result = any(current_input[i] == layer[i + 1] for i in range(n))
                current_input = [result]
            outputs.append(result)
        return outputs
    
    def hamming_weight(x):
        return bin(x).count('1')
    
    def g_f(k, truth_table, n):
        return sum(truth_table[sum(inputs)] for inputs in itertools.combinations(range(n), k)) / math.comb(n, k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)
                b.append(1/3 - g_f(j, truth_table, n))
            return linprog_c(A, b, k)
        
        def linprog_c(A, b, k):
            x0 = [0] * (k + 1)
            while True:
                result = scipy.optimize.linprog([c for c in A], bounds=[(-math.inf, math.inf)] * (k + 1), method='simplex')
                if result.success and objective_function(result.x) <= 1/3:
                    return k
                k += 1
        
        k = 0
        while True:
            k = linprog_c(k)
    
    def compute_ψ_sym(truth_table, n):
        def objective_function(q):
            return max(abs(q[j] - g_f(j, truth_table, n)) for j in range(n + 1))
        
        def linprog_c(k):
            A = []
            b = []
            for j in range(n + 1):
                row = [0] * (k + 1)
                row[j] = 1
                A.append(row)
                b.append(g_f(j, truth_table, n) - 1/3)
                A.append(row)