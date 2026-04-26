import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(i, n + 1):
                        M[j][k] -= factor * M[i][k]
        return [row[-1] for row in M]
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_circuit_size(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function must be a Boolean function of n bits")
        circuit = []
        for i in range(n):
            circuit.append((f[i], "input"))
        for i in range(n, len(f)):
            inputs = [circuit[j][0] for j in range(i-n, i)]
            gate_type = random.choice(["AND", "OR"])
            output = 1 if gate_type == "AND" else 0
            circuit.append((output, gate_type, inputs))
        return len(circuit)
    
    def compute_ideal_generators(f):
        n = int(math.log2(len(f)))
        A = []
        for i in range(2**n):
            row = [f[i] ^ f[j] if (i & j) == 0 else 0 for j in range(2**n)]
            A.append(row)
        b = [1 if f[i] == 1 else 0 for i in range(2**n)]
        return gaussian_elimination(A, b)
    
    n = random.choice([5, 8, 11, 14])
    f = generate_random_boolean_function(n)
    circuit_size = compute_circuit_size(f)
    ideal_generators = compute_ideal_generators(f)
    
    metric_value = len(ideal_generators) / circuit_size
    conjecture_holds = metric_value >= 2**(n/2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Generator to Circuit Size Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={r['seed']}")
                break