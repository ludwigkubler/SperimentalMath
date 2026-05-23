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
    
    def generate_expander_graph(n):
        G = {}
        for i in range(n):
            G[i] = set()
        for _ in range(2 * n - 1):
            u, v = random.sample(range(n), 2)
            G[u].add(v)
            G[v].add(u)
        return G
    
    def generate_tseitin_formula(G):
        clauses = []
        literals = {}
        for i in G:
            literals[i] = (random.choice(['A', 'B']), random.choice([True, False]))
            if literals[i][1]:
                clauses.append([(literals[i][0], i)])
            else:
                clauses.append([(-literals[i][0], i)])
        for u in G:
            for v in G[u]:
                a = (random.choice(['A', 'B']), random.choice([True, False]))
                b = (random.choice(['A', 'B']), random.choice([True, False]))
                c = (random.choice(['A', 'B']), random.choice([True, False]))
                literals[(u, v)] = (a[0], b[0], c[0])
                clauses.append([(literals[(u, v)][0], u), (-literals[(u, v)][1], v)])
                clauses.append([(-literals[(u, v)][0], v), (literals[(u, v)][1], u)])
                clauses.append([(-literals[(u, v)][2], u), (-literals[(u, v)][2], v)])
        return clauses
    
    def compute_quandle_representation(G):
        quandles = {}
        for i in G:
            quandles[i] = set()
        for u in G:
            for v in G[u]:
                if (u, v) not in quandles and (v, u) not in quandles:
                    quandles[(u, v)] = random.choice(['A', 'B'])
                    quandles[(v, u)] = quandles[(u, v)]
        return quandles
    
    def compute_rank(quandle):
        n = len(quandle)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in quandle:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            rank = 0
            for i in range(n):
                pivot_row = -1
                for j in range(rank, m):
                    if A[j][i]:
                        pivot_row = j
                        break
                if pivot_row == -1:
                    continue
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                for j in range(n):
                    if j != i and A[pivot_row][j]:
                        factor = Fraction(A[j][i], A[pivot_row][i])
                        for k in range(n):
                            A[j][k] -= factor * A[pivot_row][k]
            return rank
        
        return gaussian_elimination(matrix)
    
    def compute_resolution_proof_length(clauses):
        assignment = {}
        
        def dpll(clauses, assignment, Q, V):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal[0] in assignment and assignment[literal[0]] != literal[1]:
                    return False
                assignment[literal[0]] = literal[1]
                clauses = [c for c in clauses if not any(v in assignment or (assignment[v] == 'T' and v in Q and Q[v] != c[0]) for v in c)]
            pure_literal = next((v for v in V if sum(1 for c in clauses if v in c) - sum(1 for c in clauses if -v in c) == 1), None)
            if pure_literal:
                assignment[pure_literal] = True
                clauses = [c for c in clauses if not any(v in assignment or (assignment[v] == 'T' and v in Q and Q[v] != c[0]) for v in c)]
            return dpll(clauses, assignment, Q, V)
        
        return len(clauses) if not dpll(clauses, assignment, {}, range(len(clauses))) else 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_expander_graph(n)
    F = generate_tseitin_formula(G)
    
    quandle_representations = [compute_quandle_representation(G) for _ in range(30)]
    ranks = [compute_rank(qr) for qr in quandle_representations]
    proof_lengths = [compute_resolution_proof_length(F) for _ in range(30)]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_proof_length = sum(proof_lengths) / len(proof_lengths)
    support_fraction = sum(1 for rank, length in zip(ranks, proof_lengths) if length >= 2 ** math.floor(rank)) / len(ranks)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "support_fraction < 0.8"
    
    return {
        "metric_name": "Rank vs DPLL Length",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    mean_length = sum(r["instances_tested"] * r["metric_value"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support_fraction < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")