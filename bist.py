#!/usr/bin/env python3

from litex import RemoteClient
import time

wb = RemoteClient()
wb.open()

# --------------------------------------------------------------------

# Test patterns: 4 (words) x 32 (bits)
pattern = 0xffffffffffffffffffffffffffffffff
#pattern = 0x00000000000000000000000000000000
#pattern = 0xa5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5
#pattern = 0x5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a
#pattern = 0xaaaaaaaa55555555aaaaaaaa55555555
#pattern = 0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#pattern = 0x55555555555555555555555555555555

# Disable bulk write
wb.regs.bulk_wr_enabled.write(0)

# Reset
wb.regs.bulk_wr_reset.write(1)
wb.regs.bulk_wr_reset.write(0)

# Configure
wb.regs.bulk_wr_address.write(0x00000000) # Without offset
wb.regs.bulk_wr_dataword.write(pattern)
# Arty-A7: 256 MiB DDR3 memory divided by 4 bytes per word and 4 words per write
wb.regs.bulk_wr_count.write(int(256 * 1024 * 1024 / 4 / 4) - 1)

# Enable bulk write
wb.regs.bulk_wr_enabled.write(1)
# Wait until done
while not wb.regs.bulk_wr_done.read():
    time.sleep(1 / 1e6) # 1us
# Stop bulk write
wb.regs.bulk_wr_enabled.write(0)

# Dump last words of the memory
print('bulk: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 0x0 * 4, 12)]))
#for m in [(int(256 * 1024 * 1024 / 4) - 1 - 4), (int(256 * 1024 * 1024 / 4) - 1)]:
#    print('0x{:08x}: 0x{:08x}'.format(0x40000000 + m * 4, wb.read(0x40000000 + m * 4, 1)[0] ))

# ----------- test bist ----------
wb.regs.generator_reset.write(1)
wb.regs.generator_reset.write(0)

wb.regs.generator_base.write(0x0)
wb.regs.generator_end.write(1 * 4) # words (n * 4)
wb.regs.generator_length.write(1 * 16) # bytes (n * 4 * 4)
wb.regs.generator_random.write(0)

wb.regs.generator_start.write(1)
wb.regs.generator_start.write(0)

while not wb.regs.generator_done.read():
    time.sleep(1 / 1e6)

print('bist_counter: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 0x0 * 4, 12)]))

# ----------- test lfsr bist ----------
wb.regs.generator_reset.write(1)
wb.regs.generator_reset.write(0)
wb.regs.generator_base.write(0x0)
wb.regs.generator_end.write(4)
wb.regs.generator_random.write(1)
wb.regs.generator_length.write(16)
wb.regs.generator_start.write(1)
wb.regs.generator_start.write(0)

# ----------- test lfsr bist ----------
wb.regs.generator_reset.write(1)
wb.regs.generator_reset.write(0)

# whole memory
wb.regs.generator_base.write(0x0)
wb.regs.generator_end.write(256 * 1024 * 1024 // 4)

# random data (lfsr)
wb.regs.generator_random.write(1)

# fill whole memory
wb.regs.generator_length.write(256 * 1024 * 1024)

wb.regs.generator_start.write(1)
wb.regs.generator_start.write(0)

while not wb.regs.generator_done.read():
    time.sleep(1 / 1e6)

print('bist_random_base: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 0x0 * 4, 4 * 4)]))
print('bist_random_end: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + (256 * 1024 * 1024) - (4 * 4 * 4), (4 * 4))]))

# --------------------------------------------------------------------
#import random
#offset = random.Random(42).randrange(0x0, 256 * 1024 * 1024 - 32) # FIXME: Corner case
#print('offset: ' + str(offset) + ', expecting: ' + str((offset//16) * 16))
#wb.write(0x40000000 + offset, wb.read(0x40000000 + offset) ^ 0x000010000)
# --------------------------------------------------------------------

# Disable bulk read
#wb.regs.bulk_rd_enabled.write(0)

# Reset
#wb.regs.bulk_rd_reset.write(1)
#wb.regs.bulk_rd_reset.write(0)

# Configure
#wb.regs.bulk_rd_address.write(0x00000000) # Without offset
#wb.regs.bulk_rd_dataword.write(pattern)
# Arty-A7: 256 MiB DDR3 memory divided by 4 bytes per word and 4 words per write
#wb.regs.bulk_rd_count.write(int(256 * 1024 * 1024 / 4 / 4) - 1)

#wb.regs.bulk_rd_enabled.write(1)
# Wait until done
#while not wb.regs.bulk_rd_done.read():
#    time.sleep(1 / 1e6) # 1us
# Stop bulk write
#wb.regs.bulk_rd_enabled.write(0)
#time.sleep(100 / 1e3)

# --------------------
#ptr = wb.regs.bulk_rd_pointer.read()
#assert(ptr == (offset//16 + 1))
#print('pointer: 0x{:08x} : {:d}'.format(ptr, (ptr-1) * 4 * 4))

wb.close()
