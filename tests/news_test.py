import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep, FallingEdge
from cocotb_bus.drivers import BusDriver
from cocotb_coverage.coverage import CoverCross, CoverPoint, coverage_db
from cocotb_bus.monitors import BusMonitor
import os
import random


class InputDriver(BusDriver):
    _signals = ['coin']

    def __init__(self, dut, name, clock):
        BusDriver.__init__(self, dut, name, clock)
        self.clock = clock

    async def _driver_send(self, value, sync=True):
        await RisingEdge(self.clock)
        self.bus.coin.value = value
        await ReadOnly()
        await RisingEdge(self.clock)
        await NextTimeStep()


class NewsStandSB(BusMonitor):
    _signals = ['coin', 'newspaper', 'change']

    async def _monitor_recv(self):
        rising_edge = RisingEdge(self.clock)
        falling_edge = FallingEdge(self.clock)
        read_only = ReadOnly()
        states = {
            'ST0': {0: 'ST0', 1: 'ST5', 2: 'ST10'},
            'ST5': {0: 'ST5', 1: 'ST10', 2: 'ST15'},
            'ST10': {0: 'ST10', 1: 'ST15', 2: 'ST20'},
            'ST15': {0: 'ST0', 1: 'ST0', 2: 'ST0'},
            'ST20': {0: 'ST0', 1: 'ST0', 2: 'ST0'},
        }
        outputs = {
            'ST0': {'newspaper': 0, 'change': 0},
            'ST5': {'newspaper': 0, 'change': 0},
            'ST10': {'newspaper': 0, 'change': 0},
            'ST15': {'newspaper': 1, 'change': 0},
            'ST20': {'newspaper': 1, 'change': 1},
        }

        next_state = 'ST0'
        await RisingEdge(self.clock)
        while True:
            await rising_edge
            await read_only
            state = next_state
            coin = self.bus.coin.value
            newspaper = self.bus.newspaper.value
            change = self.bus.change.value
            next_state = states.get(state, {}).get(coin.integer, None)
            self.log.info(
                f'coin: {coin.integer}, state: {state}, next_state: {next_state}, newspaper: {newspaper}, change: {change}')
            await falling_edge
            await read_only
            assert outputs[state]['newspaper'] == newspaper.integer, "newspaper stand outputs do not match expected"



@cocotb.test()
async def news_test(dut):
    coindrv = InputDriver(dut, 'vif', dut.clock)
    coindrv.append(0)
    await Timer(1, 'ns')
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    dut.reset.value = 0
    await RisingEdge(dut.clock)
    NewsStandSB(dut, 'vif', dut.clock)
    await RisingEdge(dut.clock)
    coindrv.append(1)
    await RisingEdge(dut.clock)
    coindrv.append(2)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
