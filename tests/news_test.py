import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep, FallingEdge
from cocotb_bus.drivers import BusDriver
from cocotb_coverage.coverage import CoverCross, CoverPoint, coverage_db
from cocotb_bus.monitors import BusMonitor
import random
import constraint
import os


@CoverPoint("top.current_state",
            xf=lambda x, y: x,
            bins=['ST0', 'ST5', 'ST10', 'ST15', 'ST20']
            )
@CoverPoint("top.next_state",
            xf=lambda x, y: y,
            bins=['ST0', 'ST5', 'ST10', 'ST15', 'ST20']
            )
@CoverCross("top.state.cross",
            items=["top.current_state", "top.next_state"],
            ign_bins=[('ST0', 'ST15'), ('ST0', 'ST20'),
                      ('ST5', 'ST0'), ('ST5', 'ST20'),
                      ('ST10', 'ST0'), ('ST10', 'ST5'),
                      ('ST15', 'ST5'), ('ST15', 'ST10'),
                      ('ST15', 'ST15'), ('ST15', 'ST20'),
                      ('ST20', 'ST5'), ('ST20', 'ST10'),
                      ('ST20', 'ST15'), ('ST20', 'ST20')]
            )
def states_cover(st, ns):
    """
    Cover group encompassing all potential 
    transitions between the current state and the next state.
    """
    pass


class coin_generator:
    """
    A class to represent coin generator which used to be inserted into the news stand vending machine
    """

    def __init__(self):
        """
        Initialize a new constrain random problem with allowed range
        """
        self.p = constraint.Problem()
        self.p.addVariable('coin', [0, 1, 2])

    def solve(self):
        """
        Solve the constraint random problem
        """
        self.solutions = self.p.getSolutions()

    def get(self):
        """
        Get the solution to the constraint random problem

        Returns: random choice
        """
        return random.choice(self.solutions)


class input_driver(BusDriver):
    """
    "A class designed to model the insertion of coins into
     the newsstand vending machine."
    """
    _signals = ['coin']

    def __init__(self, dut, name, clock):
        """
        Create a new bus driver object and assign the system clock
        value to its clock attribute.
        """
        BusDriver.__init__(self, dut, name, clock)
        self.clock = clock

    async def _driver_send(self, value, sync=True):
        """
        drive a coin into the dut at rising edge of a clock.
        Wait until the current time step no longer has any further delta steps. 
        """
        await RisingEdge(self.clock)
        self.bus.coin.value = value
        await ReadOnly()
        await FallingEdge(self.clock)
        await NextTimeStep()


class scb(BusMonitor):
    """
    This class implements a system scoreboard for a news stand vending machine.
    It validates the machine's output in each state,
    ensuring it dispenses the correct quantity of newspapers and accurately calculates any change required.
    """
    _signals = ['coin', 'newspaper', 'change']

    async def _monitor_recv(self):
        """
        Monitor receiver, compare dut current state and outputs with the scb golden model.
        """
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
            states_cover(state, next_state)
            await falling_edge
            await read_only
            assert outputs[state]['newspaper'] == newspaper.integer, "newspaper stand outputs do not match expected"


@cocotb.test()
async def news_test(dut):

    # Build the tb components
    coindrv = input_driver(dut, 'vif', dut.clock)
    scb(dut, 'vif', dut.clock)

    # Create coins stimuli
    coingen = coin_generator()
    coingen.solve()

    # Reset the DUT
    coindrv.append(0)
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    dut.reset.value = 0
    await RisingEdge(dut.clock)

    # Insert coins into news paper vend machine
    for i in range(50):
        await FallingEdge(dut.clock)
        coin_sel = coingen.get()
        coindrv.append(coin_sel['coin'])

    # Sets the coverage xml file
    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_file = os.path.join(
        os.getenv('RESULT_PATH', "./"), 'coverage.xml')
    coverage_db.export_to_xml(filename=coverage_file)
