#!/usr/bin/env python3

from litex import RemoteClient

wb = RemoteClient()
wb.open()

# Trigger a reset of the SoC
#wb.regs.ctrl_reset.write(1)

# Dump all CSR registers of the SoC
#for name, reg in wb.regs.__dict__.items():
#    print("0x{:08x} : 0x{:08x} {}".format(reg.addr, reg.read(), name))

wb.write(0x40000000, 0xdeadbeef)
wb.write(0x40000000 + 4 * 4, 0xdeadbeef)
wb.write(0x40000000 + 4 * 4 * 2, 0xdeadbeef)
wb.write(0x40000000 + 4 * 4 * 3, 0xdeadbeef)
print('0x0: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 0x0 * 4, 4 * 4)]))

wb.regs.generator_reset.write(1)
wb.regs.generator_reset.write(0)

wb.regs.generator_base.write(0x0)
wb.regs.generator_end.write(0x8)
wb.regs.generator_length.write(32)

wb.regs.generator_start.write(1)
while True:
    if wb.regs.generator_done.read():
        break
    else:
        import time
        time.sleep(1 / 1e6) # 1us

print('0x0: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 0x0 * 4, 4*4)]))

wb.close()
