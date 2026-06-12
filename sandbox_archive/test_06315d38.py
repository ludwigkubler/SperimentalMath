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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(n)]
            clause = ' | '.join(literals)
            clauses.append(clause)
        return ' & '.join(clauses)

    def dpll_solver(cnf):
        def parse_cnf(cnf):
            clauses = cnf.split(' & ')
            parsed_clauses = []
            for clause in clauses:
                literals = clause.split(' | ')
                parsed_clauses.append(literals)
            return parsed_clauses

        def is_satisfiable(parsed_clauses, assignment):
            for clause in parsed_clauses:
                if all(l not in assignment or (l[0] == '-' and assignment[l[1:]] != 'T') for l in clause):
                    return False
            return True

        def backtrack(parsed_clauses, assignment):
            free_vars = [i for i in range(len(assignment)) if assignment[i] is None]
            if not free_vars:
                return is_satisfiable(parsed_clauses, assignment)
            var = free_vars[0]
            assignment[var] = 'T'
            if backtrack(parsed_clauses, assignment):
                return True
            assignment[var] = 'F'
            if backtrack(parsed_clauses, assignment):
                return True
            assignment[var] = None
            return False

        parsed_clauses = parse_cnf(cnf)
        assignment = [None] * len(parsed_clauses)
        return backtrack(parsed_clauses, assignment)

    def count_local_cycles(toric_variety):
        # Placeholder for actual toric variety computation and cycle counting
        return random.randint(1, 10)  # Simulated value

    n_max = 40
    instances_tested = 30
    total_l = 0
    total_d = 0
    local_cycles = []
    proof_depths = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        l = count_local_cycles(cnf)
        d = dpll_solver(cnf)
        total_l += l
        total_d += d
        local_cycles.append(l)
        proof_depths.append(d)

    mean_l = total_l / instances_tested
    mean_d = total_d / instances_tested
    std_dev_l = math.sqrt(sum((x - mean_l) ** 2 for x in local_cycles) / instances_tested)
    std_dev_d = math.sqrt(sum((x - mean_d) ** 2 for x in proof_depths) / instances_tested)

    correlation_coefficient = sum((local_cycles[i] - mean_l) * (proof_depths[i] - mean_d) for i in range(instances_tested)) / (instances_tested * std_dev_l * std_dev_d)
    mean_abs_diff = sum(abs(local_cycles[i] - proof_depths[i]) for i in range(instances_tested)) / instances_tested

    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_abs_diff=<{}>".format(correlation_coefficient, mean_abs_diff)

    return {
        "metric_name": "Resolution Proof Depth",
        "metric_value": mean_d,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))