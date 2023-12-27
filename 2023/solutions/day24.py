from collections import defaultdict
import re
from random import sample
from time import time

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day24.txt", "r")
    input = [i.strip() for i in file.readlines()]

    def gi(line):
        return list(map(int, re.findall(r"-?\d+", line)))

    hail = []
    L = 200000000000000
    R = 400000000000000
    def get_path(pos, vel):
        if vel == 0: return -1, -1
        # L <= x + vt
        lt = max(0, (L - pos) / vel)
        rt = max(0, (R - pos) / vel)
        if lt <= rt and vel >= 0: return lt, rt
        elif lt >= rt and vel < 0: return rt, lt
        return -1, -1

    good = []
    for line in input:
        pos, vel = line.split(" @ ")
        pos = gi(pos)
        vel = gi(vel)
        px, py, pz = pos
        vx, vy, vz = vel
        X = get_path(px, vx)
        Y = get_path(py, vy)
        hail.append((pos, vel))
        if X[0] == -1 or Y[0] == -1:
            continue
        T = max(X[0], Y[0]), min(X[1], Y[1])
        if T[0] <= T[1]:
            good.append(((px + vx * T[0], py + vy * T[0]), (px + vx * T[1], py + vy * T[1])))

    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    def intersect(A, B, C, D):
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    part1 = 0
    for ind, (L1, R1) in enumerate(good):
        for ind1, (L2, R2) in enumerate(good):
            if ind <= ind1: break
            part1 += intersect(L1, R1, L2, R2)

    SAMPLE_LIM = 3
    sampled = sample(hail, SAMPLE_LIM)
    def solve_start(dim, v1, v2, A, B):
        """The derivation (dim=0, v1=vx, v2=vy):
        Collision equation:
        s_x + t * v_x = p_x + t * vel_x
        For each component:
        s_x = t * (vel_x - v_x) + p_x
        s_y = t * (vel_y - v_y) + p_y
        s_z = t * (vel_z - v_z) + p_z
        Isolating and equating for time t:
        (s_x - p_x) / (vel_x - v_x) = (s_y - p_y) / (vel_y - v_y)
        Isolating s_x and doing the same for hailstone 2 (B):
        s_x = p_x1 + (s_y - p_y1) * (vel_x1 - v_x) / (vel_y1 - v_y)
        s_x = p_x2 + (s_y - p_y2) * (vel_x2 - v_x) / (vel_y2 - v_y)
        Equating based off of start x:
        p_x1 + (s_y - p_y1) * (vel_x1 - v_x) / (vel_y1 - v_y) = p_x2 + (s_y - p_y2) * (vel_x2 - v_x) / (vel_y2 - v_y)
        Solving for s_y:
        dvx1 = vel_x1 - v_x, dvx2 = vel_x2 - v_x, dvy1 = vel_y1 - v_y, dvy2 = vel_y2 - v_y
        (p_x1 - p_x2) * dvy2 * dvy1 + (s_y - p_y1) * dvx1 * dvy2 - (s_y - p_y2) * dvx2 * dvy1 = 0
        (p_x1 - p_x2) * dvy2 * dvy1 - p_y1 * dvx1 * dvy2 + p_y2 * dvx2 * dvy1 = s_y * (dvx2 * dvy1 - dvx1 * dvy2)
        (...) / (dvx2 * dvy1 - dvx1 * dvy2) = s_y"""
        nx = (dim + 1) % 3  # Generalize to the other dimensions
        pA, vA = A
        pB, vB = B
        dv11, dv12 = vA[dim] - v1, vB[dim] - v1
        dv21, dv22 = vA[nx] - v2, vB[nx] - v2
        s_num = (pA[dim] - pB[dim]) * dv22 * dv21 - pA[nx] * dv11 * dv22 + pB[nx] * dv12 * dv21
        s_denum = dv12 * dv21 - dv11 * dv22
        return None if s_denum == 0 or s_num % s_denum != 0 else s_num // s_denum

    def solve_xy():
        for vx in range(-500, 500):
            for vy in range(-500, 500):
                s_y = None
                for ind in range(SAMPLE_LIM):
                    res = solve_start(0, vx, vy, sampled[ind - 1], sampled[ind])
                    if res == None: break
                    if s_y != None and s_y != res: break
                    s_y = res
                else:
                    # Solve for s_x using the information we know
                    # s_x = t * (vel_x - v_x) + p_x
                    # s_y = t * (vel_y - v_y) + p_y
                    for pos, vel in hail:
                        if vy == vel[1]: continue
                        s_x = (s_y - pos[1]) * (vel[0] - vx) // (vel[1] - vy) + pos[0]
                        return s_x, s_y, vx, vy
        assert False

    s_x, s_y, vx, vy = solve_xy()
    # Solve for s_z
    for vz in range(-500, 500):
        s_z = None
        for ind in range(SAMPLE_LIM):
            res = solve_start(1, vy, vz, sampled[ind - 1], sampled[ind])
            if res == None: break
            if s_z != None and s_z != res: break
            s_z = res
        else:
            return part1, s_x + s_y + s_z

if __name__ == "__main__":
    print(main())

"""
Review:
- part 1 was ok, at least the math was manageable
- part 2 was a disaster, i dont know how to use z3 and was extremely slow
    - i also didnt like it, so heres algebra bash + velocity bruteforce to solve part 2 
"""