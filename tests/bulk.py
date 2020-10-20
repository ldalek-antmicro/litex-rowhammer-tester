#!/usr/bin/env python3

import unittest

from migen import *

#from litedram.common import *
#from litedram.frontend.bist import *

#class xTestStringMethods(unittest.TestCase):
#
#    def test_upper(self):
#        self.assertEqual('foo'.upper(), 'FOO')
#
#    def test_isupper(self):
#        self.assertTrue('FOO'.isupper())
#        self.assertFalse('Foo'.isupper())
#
#    def test_split(self):
#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
#        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)


#from importlib.machinery import SourceFileLoader
#litedram_test_common = SourceFileLoader("test.common", "litedram/test/common.py").load_module()
#litedram_test_bist   = SourceFileLoader("test.bist", "litedram/test/test_bist.py").load_module()

from arty import BaseSoC

class TestArty(unittest.TestCase):
    def test_counter(self):
        pass

        #class DUT(Module):
        #    def __init__(self):
        #        self.write_port = LiteDRAMNativeWritePort(address_width=32, data_width=32)
        #        self.submodules.generator = LiteDRAMBISTGenerator(self.write_port)

        #def main_generator(dut, mem):
        #    generator = litedram_test_bist.GenCheckCSRDriver(dut.generator)

        #    class my_checker:
        #        def __init__(self):
        #            pass

        #        def reset(self):
        #            pass

        #        def configure(self, base, length, end=None, random_addr=None, random_data=None):
        #            pass

        #        def run(self):
        #            pass

        #    #checker = my_checker()
        #    #yield from litedram_test_bist.TestBIST.bist_test(None, generator, checker, mem)

        #dut = DUT()
        #mem = litedram_test_common.DRAMMemory(32, 48)

        #generators = [
        #    main_generator(dut, mem),
        #    mem.write_handler(dut.write_port),
        #]
        #run_simulation(dut, generators)

        class Namespace:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

        args = Namespace(sim=False,
                         etherbone=False,
                         ddrphy=False,
                         leds=True,
                         pattern=False,
                         bulk=False)
        soc = BaseSoC(args=args)
