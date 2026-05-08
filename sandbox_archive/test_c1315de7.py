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

def mobius_transform(f):
    n = int(math.log2(len(f)))
    for k in range(1, n + 1):
        sign = (-1) ** (k % 2)
        for i in range(n - k + 1):
            f[i] += sign * f[i + k]
    return f

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = -A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_acc0_circuit(s, d):
        circuit = []
        for _ in range(d - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, s - 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(input_values[i] for i in inputs)
            elif gate_type == 'OR':
                result = any(input_values[i] for i in inputs)
            else:
                raise ValueError("Invalid gate type")
            stack.append(result)
        return stack[0]
    
    def anf_to_catalecticant_matrix(anf, n):
        k = n // 2
        m = math.comb(n, k)
        M = [[0] * m for _ in range(m)]
        for S in range(m):
            for T in range(m):
                if not (S & T):
                    U = S | T
                    M[S][T] = anf[U]
        return M
    
    def gf2_rank(matrix):
        return gaussian_elimination(matrix)
    
    n_values = [8, 10, 12]
    results = []
    for n in n_values:
        s_values = [n, 3 * n, 9 * n]
        d_values = [2, 3]
        for s in s_values:
            for d in d_values:
                circuit = generate_acc0_circuit(s, d)
                input_values = [random.randint(0, 1) for _ in range(n)]
                output = evaluate_circuit(circuit, input_values)
                anf = [output] + [0] * (2 ** n - 1)
                mobius_anf = mobius_transform(anf)
                M = anf_to_catalecticant_matrix(mobius_anf, n)
                MCR = gf2_rank(M)
                results.append((n, s, d, MCR))
    
    random_truth_table = [random.randint(0, 1) for _ in range(2 ** 8)]
    mobius_random_truth_table = mobius_transform(random_truth_table)
    M_random_truth_table = anf_to_catalecticant_matrix(mobius_random_truth_table, 8)
    MCR_random_truth_table = gf2_rank(M_random_truth_table)
    
    MAJ_n_truth_table = [1 if i >= 4 else 0 for i in range(2 ** 8)]
    mobius_MAJ_n_truth_table = mobius_transform(MAJ_n_truth_table)
    M_MAJ_n_truth_table = anf_to_catalecticant_matrix(mobius_MAJ_n_truth_table, 8)
    MCR_MAJ_n_truth_table = gf2_rank(M_MAJ_n_truth_table)
    
    mean_MCR_acc0 = sum(MCR for _, _, _, MCR in results) / len(results)
    std_MCR_acc0 = math.sqrt(sum((MCR - mean_MCR_acc0) ** 2 for _, _, _, MCR in results) / len(results))
    support_fraction = sum(1 for _, _, _, MCR in results if MCR <= (s + 1) ** (2 * d)) / len(results)
    
    random_truth_table_support = MCR_random_truth_table >= 0.5 * math.comb(8, 4)
    MAJ_n_support = MCR_MAJ_n_truth_table == 1
    
    if support_fraction < 0.8:
        return {
            "metric_name": "MCR",
            "metric_value": mean_MCR_acc0,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "support_fraction < 0.8"
        }
    
    if not random_truth_table_support:
        return {
            "metric_name": "MCR",
            "metric_value": mean_MCR_acc0,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "random truth table does not support"
        }
    
    if MAJ_n_support:
        return {
            "metric_name": "MCR",
            "metric_value": mean_MCR_acc0,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "MAJ_n does not support"
        }
    
    return {
        "metric_name": "MCR",
        "metric_value": mean_MCR_acc0,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_MCR_acc0 = sum(r["metric_value"] for r in results) / len(results)
    std_MCR_acc0 = math.sqrt(sum((r["metric_value"] - mean_MCR_acc0) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_MCR_acc0} std={std_MCR_acc0} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_MCR_acc0} std={std_MCR_acc0} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "support_fraction < 0.8"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")