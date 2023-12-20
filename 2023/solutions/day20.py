from math import lcm

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day20.txt", "r")
    input = [i.strip() for i in file.readlines()]

    # no time, cleaning this up later
    modules = {}
    states = {}
    broadcast_items = []
    for line in input:
        a, b = line.split(" -> ")
        b = b.strip().split(", ")
        if "broadcast" in line:
            broadcast_items = b
        elif a[0] == "%":
            modules[a[1:]] = "%", b
            states[a[1:]] = 0
        else:
            modules[a[1:]] = "&", b
            states[a[1:]] = {}

    for key, (t, b) in modules.items():
        for lab in b:
            if lab in modules and modules[lab][0] == "&":
                states[lab][key] = 0

    def apply(lab, pulse, prev):
        if lab not in modules:
            return False, 0
        t, nxt = modules[lab]
        if t == "%":
            if pulse == 1: return False, 0
            if states[lab] == 0:
                states[lab] = 1
                return True, 1
            states[lab] = 0
            return True, 0
        states[lab][prev] = pulse
        return True, 0 if all(i == 1 for i in states[lab].values()) else 1

    prev_high = {}
    cycles = {}
    low = high = 0
    for button_iter in range(1, 10 ** 5):
        queue = []
        low += 1 + len(broadcast_items)
        for lab in broadcast_items:
            queue.append((lab.strip(), 0, "broadcast"))
        for lab, pt, prev in queue:
            res, pulse = apply(lab, pt, prev)
            if res:
                # I have a headache so im just going to hardcode this in
                if lab in "dc rv vp cq" and pulse == 1:
                    if lab in prev_high:
                        if lab not in cycles:
                            diff = button_iter - prev_high[lab]
                            cycles[lab] = diff
                            if len(cycles) == 4:
                                part2 = 1
                                for val in cycles.values():
                                    part2 = lcm(part2, val)
                                return part1, part2
                    else:
                        prev_high[lab] = button_iter
                t, nxt = modules[lab]
                for nx_lab in nxt:
                    if pulse:
                        high += 1
                    else:
                        low += 1
                    queue.append((nx_lab, pulse, lab))
        if button_iter == 1000:
            part1 = low * high

if __name__ == "__main__":
    print(main())

"""
Review:
- part 1 was a pretty big reading disaster
    - didnt put the pulse count in the correct spot and lost a good chunk because of that
- part 2 was an even bigger disaster
    - i knew cycles were going to be a thing after inspecting the input
    - ...but did not realize i should be doing the check while pulses were doing their thing
    - i spent all my time checking the states after the button push completed and got nowhere with that T_T
    
i have no proper setup for the next 4 days, and will be on an airplane flying back to canada for the last day
so im probably not getting any more points (:
"""