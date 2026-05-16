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
    
    def matching_polynomial(G):
        n = len(G)
        dp = [[0] * (1 << n) for _ in range(n)]
        dp[0][0] = 1
        for i in range(1, n):
            for mask in range(1 << n):
                if not (mask & (1 << i)):
                    continue
                for j in range(i):
                    if G[i][j] and (mask & (1 << j)) == 0:
                        dp[i][mask] += dp[j][mask ^ (1 << i)]
        return sum(dp[n-1])

    def mahler_measure(mu_G):
        roots = [r.real for r in np.roots(mu_G)]
        M = 1
        for r in roots:
            if abs(r) >= 1:
                M *= abs(r)
        return M

    def dpll_refutation_tree_size(G, c):
        n = len(G)
        clauses = []
        for i in range(n):
            clauses.append([2*i+1, -2*(i+1)])
        for i in range(n):
            if c[i] == 0:
                clauses.append([-2*i-1])
            else:
                clauses.append([2*i+1])

        def unit_propagation(clauses, assignment):
            changed = True
            while changed:
                changed = False
                for clause in clauses:
                    if len(clause) == 1:
                        literal = clause[0]
                        if literal > 0 and not assignment[literal-1]:
                            assignment[literal-1] = True
                            changed = True
                        elif literal < 0 and assignment[-literal-1]:
                            assignment[-literal-1] = False
                            changed = True
            return assignment

        def dpll(clauses, assignment):
            if not clauses:
                return len(assignment)
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                return float('inf')
            literal = unit_clauses[0][0]
            assignment[literal-1] = True
            result = dpll(clauses, assignment)
            if result < float('inf'):
                return result
            assignment[literal-1] = False
            assignment[-literal-1] = True
            return dpll(clauses, assignment)

        assignment = [False] * (2*n)
        return dpll(clauses, assignment)

    n_values = {8, 10, 12, 14, 16}
    total_instances = 0
    valid_instances = 0
    counterexample = ""

    for n in n_values:
        for _ in range(30):
            G = [[False] * n for _ in range(n)]
            degree_sum = 0
            while degree_sum != 2*n:
                u, v = random.sample(range(n), 2)
                if not G[u][v]:
                    G[u][v] = True
                    G[v][u] = True
                    degree_sum += 2

            c = [random.choice([0, 1]) for _ in range(n)]
            mu_G = matching_polynomial(G)
            M = mahler_measure(mu_G)

            T = dpll_refutation_tree_size(G, c)
            total_instances += 1

            if T >= M / 2:
                valid_instances += 1
            else:
                counterexample = f"Graph: {G}, Charge: {c}, Tree Size: {T}, Mahler Measure: {M}"

    return {
        "metric_name": "DPLL Refutation Tree Size",
        "metric_value": total_instances,
        "instances_tested": total_instances,
        "conjecture_holds": valid_instances / total_instances >= 0.95,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")