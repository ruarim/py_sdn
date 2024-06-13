"""
This script demonstrates and compares the different simulators

- Image Source Method (ISM) order 17
- Ray Tracing (RT) only
- Hybrid ISM/RT with ISM order 17
- Hybrid ISM/RT with ISM order 3

It compares the theoretical and measured RT60 and the computation times.

We can observe that the order 17 is not sufficient when using only the ISM.
RT is able to simulate the whole tail.
Also, the RT60 of ISM is not completely consistent with the Hybrid method as it
doesn't include scattering. Scattering reduces the length of the reverberent tail.
"""

from __future__ import print_function

import time

import matplotlib.pyplot as plt
import numpy as np

import pyroomacoustics as pra

from config import WALL_ABSORPTION, ROOM_DIMS, SOURCE_LOC, MIC_LOC, FS
from evaluation.plot import plot_signal

np.random.seed(0)

# room dimension
room_dim = ROOM_DIMS

# Create the shoebox
materials = pra.make_materials(
    ceiling=(WALL_ABSORPTION, 0.0),
    floor=(WALL_ABSORPTION, 0.0),
    east=(WALL_ABSORPTION, 0.0),
    west=(WALL_ABSORPTION, 0.0),
    north=(WALL_ABSORPTION, 0.0),
    south=(WALL_ABSORPTION, 0.0),
)

def make_params(orders):
    return {f"ISM{order}": {"max_order": order, "ray_tracing": False} for order in orders}

def make_room(config):
    """
    A short helper function to make the room according to config
    """

    shoebox = (
        pra.ShoeBox(
            room_dim,
            materials=materials,
            # materials=pra.Material.make_freq_flat(0.07),
            fs=FS,
            max_order=config["max_order"],
            ray_tracing=config["ray_tracing"],
            air_absorption=True,
            use_rand_ism=False, # reduce sweeping echos - important for auralisation
            max_rand_disp=0.05,
        )
        .add_source(SOURCE_LOC)
        .add_microphone(MIC_LOC)
    )

    return shoebox


def chrono(f, *args, **kwargs):
    """
    A short helper function to measure running time
    """
    t = time.perf_counter()
    ret = f(*args, **kwargs)
    runtime = time.perf_counter() - t
    return runtime, ret


def simulate_room_ISM(normalise=False, orders=[17], xlim=None):
    rirs = {}
    params = make_params(orders)
    
    for name, config in params.items():
        print("Simulate: ", name)

        shoebox = make_room(config)

        rt60_sabine = shoebox.rt60_theory(formula="sabine")
        rt60_eyring = shoebox.rt60_theory(formula="eyring")

        # run separately the different parts of the simulation
        t_ism, _ = chrono(shoebox.image_source_model)
        t_rt, _  = chrono(shoebox.ray_tracing)
        t_rir, _ = chrono(shoebox.compute_rir)

        rir = shoebox.rir[0][0].copy()
        rirs[name] = rir

        if normalise: rir = rir / np.max(rir)
        
        plot_signal(rir, title=f'PyRoomAcoustics RIR: DIMS{ROOM_DIMS} ORDER: {config["max_order"]}', xlim=xlim)

        plt.figure(2)
        rt60 = shoebox.measure_rt60(plot=False, decay_db=60)
        
        print(f"  RT60:")
        print(f"    - Eyring   {rt60_eyring:.3f} s")
        print(f"    - Sabine   {rt60_sabine:.3f} s")
        print(f"    - Measured {rt60[0, 0]:.3f} s")

        print("  Computation:")
        print(f"    - ISM  {t_ism:.6f} s")
        print(f"    - RIR  {t_rir:.6f} s")
        print(f"    Total: {t_ism + t_rt + t_rir:.6f} s")
        print()

    return rir