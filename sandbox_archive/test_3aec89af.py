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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def generate_3_regular_graph(n):
        G = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in edges and (j, i) not in edges:
                    G[i].append(j)
                    G[j].append(i)
                    edges.add((i, j))
                    break
        return G
    
    def is_connected(G):
        visited = [False] * len(G)
        stack = [0]
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                for u in G[v]:
                    if not visited[u]:
                        stack.append(u)
        return all(visited)
    
    def spectral_gap(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        d = [len(neighbors) for neighbors in G]
        for i, neighbors in enumerate(G):
            for j in neighbors:
                A[i][j] = 1 / math.sqrt(d[i] * d[j])
        lambda_max = max(eigenvalue(A) for eigenvalue in eigenvalues(A))
        lambda_min = min(eigenvalue(A) for eigenvalue in eigenvalues(A))
        return (lambda_max - lambda_min) / (2 * n)
    
    def eigenvalues(M):
        n = len(M)
        if n == 1:
            return [M[0][0]]
        M = [[M[i][j] for j in range(n)] for i in range(n)]
        det = determinant(M)
        if det == 0:
            raise ValueError("Matrix is singular")
        eigenvals = []
        for k in range(1, n):
            A_k = [[sum(M[i][j] * M[j][k] for j in range(k)) for i in range(n)] for k in range(n)]
            det_A_k = determinant(A_k)
            eigenvals.append(det_A_k / det)
        return eigenvals
    
    def determinant(M):
        n = len(M)
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * M[0][j] * determinant(submatrix)
        return det
    
    def generate_01_charge(G):
        n = len(G)
        charge = [random.choice([0, 1]) for _ in range(n)]
        if sum(charge) % 2 == 0:
            charge[random.randint(0, n - 1)] ^= 1
        return charge
    
    def dhar_burning(G, c, q):
        n = len(G)
        q_reduced = [c[i] for i in range(n)]
        queue = [q]
        while queue:
            v = queue.pop()
            if q_reduced[v] > 0:
                q_reduced[v] -= 1
                for u in G[v]:
                    q_reduced[u] += 1
                    if q_reduced[u] == 2:
                        queue.append(u)
        return sum(q_reduced) - n
    
    def luo_algorithm(G, c):
        n = len(G)
        r = 0
        while True:
            q = random.choice(range(n))
            q_reduced = [c[i] for i in range(n)]
            queue = [q]
            while queue:
                v = queue.pop()
                if q_reduced[v] > 0:
                    q_reduced[v] -= 1
                    for u in G[v]:
                        q_reduced[u] += 1
                        if q_reduced[u] == 2:
                            queue.append(u)
            r += sum(q_reduced) - n
            if r >= len(G):
                return r
    
    def tseitin_formula(G, c):
        n = len(G)
        clauses = []
        for i in range(n):
            clauses.extend([[i * n + j + 1, -(i * n + k + 1)] for j, k in enumerate(G[i]) if j < k])
            clauses.append([-(i * n + j + 1) for j in G[i]])
            clauses.append([i * n + j + 1 for j in G[i]])
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
                value = False
            else:
                value = True
            assignment[literal] = value
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(new_clauses, assignment)
        pure_literal = next((l for l in range(1, max(clause) + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            value = True
            if -pure_literal in assignment:
                value = False
            assignment[pure_literal] = value
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(new_clauses, assignment)
        literal = random.choice([l for l in range(1, max(clause) + 1) if l not in assignment and -l not in assignment])
        value = True
        if -literal in assignment:
            value = False
        assignment[literal] = value
        new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
        new_clauses_false = [c for c in clauses if literal in c or -literal in c]
        return dpll(new_clauses_true, assignment) or dpll(new_clauses_false, assignment)
    
    def run_dpll(clauses):
        assignment = {}
        return dpll(clauses, assignment)
    
    n_values = [8, 10, 12, 14]
    results = []
    for n in n_values:
        for _ in range(30):
            G = generate_3_regular_graph(n)
            if not is_connected(G) or spectral_gap(G) < 0.15:
                continue
            c = generate_01_charge(G)
            r_BN = dhar_burning(G, c, 0)
            D = len(G) - r_BN
            Tseitin_G_c = tseitin_formula(G, c)
            L = run_dpll(Tseitin_G_c)
            W = max(len(clause) for clause in Tseitin_G_c if any(literal in assignment for literal in clause))
            results.append({
                "n": n,
                "D": D,
                "L": L,
                "W": W
            })
    
    mean_L_over_D = sum(result["L"] / result["D"] for result in results) / len(results)
    std_L_over_D = math.sqrt(sum((result["L"] / result["D"] - mean_L_over_D) ** 2 for result in results) / len(results))
    mean_W_over_D = sum(result["W"] / result["D"] for result in results) / len(results)
    std_W_over_D = math.sqrt(sum((result["W"] / result["D"] - mean_W_over_D) ** 2 for result in results) / len(results))
    
    support_fraction_L = sum(1 for result in results if (0.33 <= result["L"] / result["D"] <= 3) and (0.33 <= result["W"] / result["D"] <= 3)) / len(results)
    
    if support_fraction_L >= 0.8:
        return {
            "metric_name": "support_fraction",
            "metric_value": support_fraction_L,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = next((result for result in results if not (0.33 <= result["L"] / result["D"] <= 3) and (0.33 <= result["W"] / result["D"] <= 3)), None)
        return {
            "metric_name": "support_fraction",
            "metric_value": support_fraction_L,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"n={counterexample['n']}, D={counterexample['D']}, L={counterexample['L']}, W={counterexample['W']}"
        }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = generate_primes(30)
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=0 support_fraction=1")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next((result for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={counterexample['n']}, D={counterexample['D']}, L={counterexample['L']}, W={counterexample['W']}\" first_failing_seed={seeds[results.index(counterexample)]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")