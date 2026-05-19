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
    
    def generate_3cnf(n, m):
        cnf = []
        for _ in range(m):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
            clause = ' ∨ '.join(literals)
            cnf.append(clause)
        return ' ∧ '.join(cnf)

    def is_unsatisfiable(cnf):
        # Simple random-walk + DPLL probe
        for _ in range(60):
            assignment = {i: random.choice([True, False]) for i in range(1, n+1)}
            stack = [assignment]
            while stack:
                current_assignment = stack.pop()
                if all(eval(clause, current_assignment) for clause in cnf.split(' ∧ ')):
                    return True
                unassigned_var = next((i for i in range(1, n+1) if i not in current_assignment), None)
                if unassigned_var is None:
                    break
                stack.append({**current_assignment, unassigned_var: True})
                stack.append({**current_assignment, unassigned_var: False})
        return False

    def walsh_transform(p_F, S):
        n = len(p_F)
        p_hat_S = 0
        for C in cnf.split(' ∧ '):
            if all(lit in S for lit in C.split()):
                polarity = 1
                for lit in C.split():
                    if '~' in lit:
                        polarity *= -1
                p_hat_S += polarity * (2 ** (-len(C.split())))
        return p_hat_S

    def compute_T(F):
        n = len(p_F)
        T = 0
        for i in range(1, n+1):
            for S in combinations(range(1, n+1), min(i, 3)):
                if all(lit in S for lit in F.split()):
                    p_hat_S = walsh_transform(F, S)
                    T += math.sqrt(p_hat_S ** 2)
        return T

    def dpll(cnf):
        stack = []
        assignment = {}
        while True:
            if is_unsatisfiable(cnf):
                return len(stack)
            unassigned_var = next((i for i in range(1, n+1) if i not in assignment), None)
            if unassigned_var is None:
                break
            stack.append(unassigned_var)
            assignment[unassigned_var] = True
            cnf = cnf.replace(f'x{unassigned_var}', '').replace(f'~x{unassigned_var}', '')
        return len(stack)

    def combinations(iterable, r):
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)

    n_values = [16, 20, 24, 28, 32]
    alpha_values = [4.0, 4.5, 5.0]
    total_instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    log_values = []
    T_values = []

    for n in n_values:
        for alpha in alpha_values:
            m = math.ceil(alpha * n)
            cnf = generate_3cnf(n, m)
            if is_unsatisfiable(cnf):
                T_F = compute_T(cnf)
                B_F = dpll(cnf)
                log_value = math.log2(1 + B_F)
                T_over_sqrt_m = T_F / math.sqrt(m)
                log_values.append(log_value)
                T_values.append(T_over_sqrt_m)
                if log_value < 0.10 * T_over_sqrt_m:
                    conjecture_holds = False
                    counterexample = f"n={n}, alpha={alpha}, m={m}"
                    break
            total_instances_tested += 1

    correlation = sum((log_values[i] - mean_log) * (T_values[i] - mean_T) for i in range(len(log_values))) / len(log_values)
    mean_log = sum(log_values) / len(log_values)
    mean_T = sum(T_values) / len(T_values)

    return {
        "metric_name": "log_2(1+B(F)) vs T(F)/√m",
        "metric_value": correlation,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    mean_log = sum(result["metric_value"] for result in results) / len(results)
    std_log = math.sqrt(sum((result["metric_value"] - mean_log) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_log} std={std_log} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")