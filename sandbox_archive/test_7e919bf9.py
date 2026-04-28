# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from collections import defaultdict

def is_unsat(F):
    n = max(abs(l) for clause in F for l in clause)
    assignment = [None] * (n + 1)
    
    def propagate():
        changed = True
        while changed:
            changed = False
            for i in range(1, n + 1):
                if assignment[i] is None:
                    pos = any(l > 0 and assignment[l] == 1 for l in clause)
                    neg = any(l < 0 and assignment[-l] == -1 for l in clause)
                    if pos and not neg:
                        assignment[i] = 1
                        changed = True
                    elif not pos and neg:
                        assignment[i] = -1
                        changed = True
    
    propagate()
    
    for clause in F:
        if all(assignment[l] == (l > 0) * 2 - 1 for l in clause):
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    m_values = [math.floor(4.5 * n) for n in n_values]
    
    results = []
    for n, m in zip(n_values, m_values):
        count_unsat = 0
        count_random = 0
        total_leaves = 0
        
        for _ in range(30):
            F = []
            while True:
                clause = [random.randint(-n, -1), random.randint(1, n)]
                if len(set(clause)) == 2 and all(abs(l) not in F for l in clause):
                    F.append(tuple(sorted(clause)))
                    break
            if is_unsat(F):
                count_unsat += 1
                leaves = 0
                g_F = [0] * (1 << n)
                for i in range(1 << n):
                    assignment = [((i >> j) & 1) * 2 - 1 for j in range(n)]
                    if is_unsat([list(clause)] + F, assignment):
                        leaves += 1
                        g_F[i] = 1
                total_leaves += leaves
                k = int(math.log2(m + 1))
                T_k = sum(g_F[i]**2 for i in range(1 << n) if bin(i).count('1') > k)
                log_L = math.log2(leaves + 1)
                max_hat_g_emptyset = max(abs(sum(g_F[i] * (1 << j) for i in range(1 << n))) for j in range(n))
                conjecture_holds = log_L <= 4 * (1 + T_k * 2**n) / max(1, max_hat_g_emptyset * 2**n)
                ratio = log_L / (1 + T_k * 2**n / max(1, max_hat_g_emptyset * 2**n))
                results.append({
                    "metric_name": "log2(L+1)",
                    "metric_value": log_L,
                    "instances_tested": 1,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": "" if conjecture_holds else f"Ratio out of bounds: {ratio}"
                })
        
        for _ in range(30):
            F = []
            while len(F) < m:
                clause = [random.randint(-n, -1), random.randint(1, n)]
                if len(set(clause)) == 2 and all(abs(l) not in F for l in clause):
                    F.append(tuple(sorted(clause)))
            if is_unsat(F):
                count_random += 1
                leaves = 0
                g_F = [0] * (1 << n)
                for i in range(1 << n):
                    assignment = [((i >> j) & 1) * 2 - 1 for j in range(n)]
                    if is_unsat([list(clause)] + F, assignment):
                        leaves += 1
                        g_F[i] = 1
                total_leaves += leaves
                k = int(math.log2(m + 1))
                T_k = sum(g_F[i]**2 for i in range(1 << n) if bin(i).count('1') > k)
                log_L = math.log2(leaves + 1)
                max_hat_g_emptyset = max(abs(sum(g_F[i] * (1 << j) for i in range(1 << n))) for j in range(n))
                ratio = log_L / (1 + T_k * 2**n / max(1, max_hat_g_emptyset * 2**n))
                results.append({
                    "metric_name": "log2(L+1)",
                    "metric_value": log_L,
                    "instances_tested": 1,
                    "conjecture_holds": ratio >= 0.05 and ratio <= 4,
                    "counterexample": "" if ratio >= 0.05 and ratio <= 4 else f"Ratio out of bounds: {ratio}"
                })
    
    mean_log_L = sum(result["metric_value"] for result in results) / len(results)
    std_log_L = math.sqrt(sum((result["metric_value"] - mean_log_L)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_log_L": mean_log_L,
        "std_log_L": std_log_L,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_log_L = sum(result["mean_log_L"] for result in results) / len(results)
    std_log_L = math.sqrt(sum((result["mean_log_L"] - mean_log_L)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.6) / len(results)
    
    if all(result["support_fraction"] >= 0.6 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_log_L} std={std_log_L} support_fraction={support_fraction}")
    elif sum(1 for result in results if result["support_fraction"] < 0.6) / len(results) <= 0.2:
        print("RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE not enough evidence to confirm or refute the conjecture")