import gurobipy as gp
from gurobipy import GRB
import numpy as np

costs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]*10  # 0.1*i for i in range(0,11)]
valuations = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# costs = [np.random.normal(0.5, 0.3) for _ in range(20)]
# valuations = [np.random.uniform(0.5, 0.3) for _ in range(30)]
commission = 0.1
p_range = 0.1

S = len(costs)
B = len(valuations)


## model
m = gp.Model()

x = m.addVars(S, B, vtype=GRB.CONTINUOUS, lb=0, ub=1)
p = m.addVars(S, B, vtype=GRB.CONTINUOUS, lb=0, ub=1)
pmin = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1)
pmax = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1)
z_s = m.addVars(S, B, vtype=GRB.BINARY)
z_b = m.addVars(S, B, vtype=GRB.BINARY)
z_pmin = m.addVars(S, B, vtype=GRB.BINARY)
z_pmax = m.addVars(S, B, vtype=GRB.BINARY)


M = 10

m.setObjective(gp.quicksum(x[s, b] * p[s, b] for s in range(S) for b in range(B)) * commission, GRB.MAXIMIZE)

for s in range(S):
    for b in range(B):
        m.addConstr(x[s, b] <= 1/(S*B))

        m.addConstr(x[s, b] <= z_s[s, b] * M)
        m.addConstr(x[s, b] <= z_b[s, b] * M)

        m.addConstr(costs[s] - p[s, b] * (1 - commission) <= M * (1 - z_s[s, b]))
        m.addConstr(p[s, b] - valuations[b] <= M * (1 - z_b[s, b]))

        m.addConstr(pmax - pmin == p_range)
        #m.addConstr(p[s, b] == costs[s] * (1 + commission))
        m.addConstr(x[s, b] <= z_pmin[s, b] * M)
        m.addConstr(x[s, b] <= z_pmax[s, b] * M)
        m.addConstr(pmin - p[s, b] <= M * (1 - z_pmin[s, b]))
        m.addConstr(p[s, b] - pmax <= M * (1 - z_pmax[s, b]))

m.optimize()

print('Price: ', pmin.x, pmax.x)

def printing():
    print('Price: ', pmin.x, pmax.x)
    for b in range(B):
        print(f"Buyer {b} with valuation {valuations[b]}")
        print(f"c: {'  | '.join(['%.1f' % round(costs[s],2) for s in range(S)])}")
        print(f"x: {' | '.join(['%.2f' % round(x[s,b].x,2) for s in range(S)])}")
        print(f"p: {' | '.join(['%.2f' % round(p[s, b].x, 2) for s in range(S)])}")
