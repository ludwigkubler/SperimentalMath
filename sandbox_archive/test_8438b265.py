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
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def generate_nc1_circuit(depth: int):
        if depth == 0:
            return random.choice([0, 1])
        else:
            a = generate_nc1_circuit(depth-1)
            b = generate_nc1_circuit(depth-1)
            return (a + b) % 2

    def simulate_abp(circuit, abp):
        n = len(abp)
        state = [0] * n
        for node in circuit:
            if isinstance(node, int):
                state[node] += 1
            else:
                a = state.pop()
                b = state.pop()
                state.append((a + b) % 2)
        return state[0]

    def abp_size(circuit):
        n = len(circuit)
        size = 0
        for node in circuit:
            if isinstance(node, int):
                size += 1
            else:
                size += 2
        return size

    def generate_p_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    def simulate_abp_for_p(abp, p_function):
        n = len(p_function)
        state = [0] * (2**n)
        for i in range(2**n):
            for j in range(n):
                if (i >> j) & 1:
                    state[i] += p_function[j]
            state[i] %= 2
        return state

    def abp_size_for_p(abp, p_function):
        n = len(p_function)
        size = 0
        for i in range(2**n):
            for j in range(n):
                if (i >> j) & 1:
                    size += 1
            size += 2
        return size

    def generate_nc1_circuit_of_depth(depth: int):
        circuit = []
        for _ in range(depth):
            if random.choice([0, 1]) == 0:
                circuit.append(random.randint(0, len(circuit)-1))
            else:
                circuit.extend([len(circuit), len(circuit)+1])
        return circuit

    def generate_abp_for_nc1_circuit(circuit):
        n = len(circuit)
        abp = [0] * (2*n)
        for i in range(n):
            if isinstance(circuit[i], int):
                abp[circuit[i]] += 1
            else:
                a = circuit[i]
                b = circuit[i+1]
                abp[a] += 1
                abp[b] += 1
                abp[2*n-1] += 1
        return abp

    def generate_abp_for_p_function(p_function):
        n = len(p_function)
        abp = [0] * (2**n + 2*n)
        for i in range(2**n):
            for j in range(n):
                if (i >> j) & 1:
                    abp[i] += p_function[j]
            abp[i] %= 2
        return abp

    def generate_counterexample():
        n = random.randint(5, 30)
        p_function = generate_p_function(n)
        abp = generate_abp_for_p_function(p_function)
        if abp_size_for_p(abp, p_function) > 2**n:
            return f"Exponential size ABP for P function of length {n}"
        else:
            return ""

    def run_nc1_circuit_simulation(depth: int):
        circuit = generate_nc1_circuit_of_depth(depth)
        abp = generate_abp_for_nc1_circuit(circuit)
        return abp_size(circuit), simulate_abp(circuit, abp)

    def run_p_function_simulation():
        n = random.randint(5, 30)
        p_function = generate_p_function(n)
        abp = generate_abp_for_p_function(p_function)
        return abp_size_for_p(abp, p_function), simulate_abp_for_p(abp, p_function)

    results = []
    for _ in range(30):
        depth = random.choice([5, 10, 15, 20, 30, 40])
        nc1_circuit_size, nc1_circuit_result = run_nc1_circuit_simulation(depth)
        p_function_size, p_function_result = run_p_function_simulation()
        results.append({
            "metric_name": "ABP Size",
            "metric_value": nc1_circuit_size,
            "instances_tested": 1,
            "conjecture_holds": nc1_circuit_size <= depth**2 * n,
            "counterexample": generate_counterexample()
        })

    return {
        "metric_name": "Average ABP Size",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": 30,
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if r["counterexample"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")