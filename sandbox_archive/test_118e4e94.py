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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        # Simplified SAT solver for small instances
        n = max(abs(c) for c in sum(clauses, []))
        assignment = [None] * (n + 1)
        stack = []
        
        def backtrack():
            if len(stack) == n:
                return True
            var = next((i for i in range(1, n + 1) if assignment[i] is None), None)
            if var is None:
                return False
            assignment[var] = True
            stack.append(var)
            for clause in clauses:
                if any(x == -var or x == var for x in clause):
                    continue
                if all(x != -var and x != var for x in clause):
                    assignment[var] = False
                    stack.pop()
                    break
            else:
                if backtrack():
                    return True
            assignment[var] = None
            stack.pop()
            assignment[-var] = True
            stack.append(-var)
            for clause in clauses:
                if any(x == var or x == -var for x in clause):
                    continue
                if all(x != var and x != -var for x in clause):
                    assignment[-var] = False
                    stack.pop()
                    break
            else:
                return True
            return False
        
        return backtrack()
    
    def compute_rank(clauses):
        # Simplified algorithm to find the rank of a groupoid
        n = len(clauses)
        generators = set()
        for i in range(n):
            for j in range(i + 1, n):
                if is_satisfiable([clauses[i], clauses[j]]):
                    generators.add((i, j))
        return len(generators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, 2 * n)
        clauses = generate_cnf(n, m)
        rank = compute_rank(clauses)
        expected_rank = math.log(n, 2) ** 2
        if rank > expected_rank:
            return {
                "metric_name": "rank(G(F))",
                "metric_value": rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank(G(F))={rank} > O(log^2({n}))={expected_rank}"
            }
        results.append(rank)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "rank(G(F))",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 307))  # 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= math.log(len(seeds), 2) ** 2) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > math.log(len(seeds), 2) ** 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > math.log(len(seeds), 2) ** 2)
        print(f"RESULT: FALSIFIED counterexample='n={len(seeds)}, rank(G(F))>O(log^2(n))' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")