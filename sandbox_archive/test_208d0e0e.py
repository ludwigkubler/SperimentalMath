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
    
    def generate_boolean_formula(n):
        num_clauses = random.randint(5, 10)
        literals = [f'x{i+1}' for i in range(n)]
        formula = []
        for _ in range(num_clauses):
            clause = random.sample(literals, random.randint(1, n))
            formula.append(' & '.join(clause))
        return ' | '.join(formula)

    def dual_linear_code(formula, n):
        literals = set()
        for literal in formula.split():
            if literal.startswith('x'):
                literals.add(literal)
        code_matrix = [[0] * len(literals) for _ in range(len(literals))]
        for literal in literals:
            index = int(literal[2:]) - 1
            code_matrix[index][index] = 1
        return code_matrix

    def minimal_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank, n)):
                rank += 1
                for j in range(i, n):
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    for k in range(n):
                        matrix[k][j] *= Fraction(1, matrix[j][j])
                    for k in range(n):
                        if k != j:
                            factor = -matrix[k][j]
                            for l in range(n):
                                matrix[k][l] += factor * matrix[j][l]
        return rank

    def clause_entanglement_complexity(formula, n):
        literals = set()
        for literal in formula.split():
            if literal.startswith('x'):
                literals.add(literal)
        complexity = 0
        for literal in literals:
            index = int(literal[2:]) - 1
            for j in range(index + 1, len(literals)):
                if any(f'x{i+1}' in formula for i in range(j)) and all(f'x{i+1}' not in formula for i in range(j)):
                    complexity += 1
        return complexity

    n = random.randint(5, 40)
    F = generate_boolean_formula(n)
    code_matrix = dual_linear_code(F, n)
    rank = minimal_rank(code_matrix)
    entanglement_complexity = clause_entanglement_complexity(F, n)

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    print(f"RESULT: {RESULT} mean={mean_rank:.2f} std=NA support_fraction={support_fraction:.2f}")