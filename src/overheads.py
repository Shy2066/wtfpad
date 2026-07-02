import os
import sys
import numpy as np

from parser import parse


def latency(trace):
    if len(trace) < 2:
        return 0.0
    return trace[-1].timestamp - trace[0].timestamp


def bandwidth(trace):
    total_bytes = sum([abs(p.length) for p in trace])
    lat = latency(trace)
    if lat == 0.0:
        return 0.0
    return 1.0 * total_bytes / lat


def bandwidth_ovhd_ratio(new, old):
    """带宽比值：new / old"""
    bw_old = bandwidth(old)
    if bw_old == 0.0:
        return 0.0
    return bandwidth(new) / bw_old


def bandwidth_ovhd_increase(new, old):
    """带宽开销（增长率）：(new - old) / old"""
    bw_old = bandwidth(old)
    if bw_old == 0.0:
        return 0.0
    return (bandwidth(new) - bw_old) / bw_old


def latency_ovhd(new, old):
    lat_old = latency(old)
    if lat_old == 0.0:
        return 0.0
    return latency(new) / lat_old


def main():
    bandwidth_ratios, bandwidth_overheads, latencies = [], [], []

    original_files, simulated_files = sys.argv[1], sys.argv[2]

    for fname in os.listdir(original_files):
        original_trace = parse(os.path.join(original_files, fname))
        simulated_trace = parse(os.path.join(simulated_files, fname))

        bw_ratio = bandwidth_ovhd_ratio(simulated_trace, original_trace)
        bw_over = bandwidth_ovhd_increase(simulated_trace, original_trace)
        lat_ovhd = latency_ovhd(simulated_trace, original_trace)

        bandwidth_ratios.append(bw_ratio)
        bandwidth_overheads.append(bw_over)
        latencies.append(lat_ovhd)

    print("Bandwidth ratio (median):",
          np.median([b for b in bandwidth_ratios if b > 0.0]))

    print("Bandwidth overhead (median increase %):",
          np.median([b for b in bandwidth_overheads if b > 0.0]))

    print("Latency overhead (median):",
          np.median([l for l in latencies if l > 0.0]))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(-1)