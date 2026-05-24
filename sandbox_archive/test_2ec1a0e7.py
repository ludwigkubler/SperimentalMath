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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            literals = set()
            while len(literals) < 2:
                literal = random.randint(1, n * 2)
                if literal <= n:
                    literals.add(-literal)
                else:
                    literals.add(literal - n)
            clause = ' '.join(str(l) for l in literals) + ' 0'
            cnf.append(clause)
        return '\n'.join(cnf)

    def indicator_matrix(cnf):
        lines = cnf.split('\n')
        m = len(lines)
        n = max(abs(int(lit)) for line in lines for lit in line.split()[:-1])
        I = [[0] * n for _ in range(m)]
        for i, line in enumerate(lines):
            literals = [int(lit) for lit in line.split()[:-1]]
            for lit in literals:
                if 1 <= abs(lit) <= n:
                    I[i][abs(lit) - 1] = 1
        return I

    def minimal_rank(I):
        m, n = len(I), len(I[0])
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(m):
                if I[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                rank += 1
                for j in range(m):
                    if j != pivot_row:
                        factor = Fraction(I[j][i], I[pivot_row][i])
                        for k in range(n):
                            I[j][k] -= factor * I[pivot_row][k]
        return rank

    def dpll_proof_width(cnf):
        # Placeholder function, actual implementation needed
        return random.randint(10, 100)  # Dummy value

    n_values = [10, 15, 20, 30, 40]
    m_values = [n // 2 for n in n_values]

    results = []
    for n, m in zip(n_values, m_values):
        cnf = generate_cnf(n, m)
        I = indicator_matrix(cnf)
        rank = minimal_rank(I)
        proof_width = dpll_proof_width(cnf)
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "proof_width": proof_width
        })

    if not results:
        return {
            "metric_name": "minimal_rank_over_dpll",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }

    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_proof_width = sum(result["proof_width"] for result in results) / len(results)

    return {
        "metric_name": "minimal_rank_over_dpll",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": False,
        "counterexample": f"mean_rank={mean_rank}, mean_proof_width={mean_proof_width}"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank={result['metric_value']}, mean_proof_width={result['counterexample']}\" first_failing_seed={first_failing_seed}")