# https://jroatch.xyz/2011/blog/polarium-password-encoding

octets = []
# The tile data always consists of 8x8 bits. 0 is white and 1 is black. octet 0 is the topmost row, and bit 0 is the leftmost column. All 64 tiles are packed from left to right, top to bottom. The tile data is always 8x8 bits even if the width and height is smaller.
octets.insert(0, 0x00)
octets.insert(1, 0x3C)
octets.insert(2, 0x42)
octets.insert(3, 0x95)
octets.insert(4, 0x21)
octets.insert(5, 0x29)
octets.insert(6, 0x22)
octets.insert(7, 0x1C)
# Start hint Y and start hint X
octets.insert(8, 0x52)
# End hint Y and end hint X
octets.insert(9, 0x45)
# The Width and Height defines a window of the tile data that's used. Usually the bits left outside this window is changed to the default checkerboard pattern, but they can be anything.
# There's some trickiness comparing hint coordinates with Width and Height. Hint coordinates include the implied border around the whole puzzle, and starts at 0. Width and Height is the portion of tiles that are included in the puzzle and starts at 1. So for a puzzle that has a width of 5 and a height of 2 the coordinates range from (0,0) to (6,3) seeing the whole board as 7 by 4.
octets.insert(10, 0x88)
# The checksum is the sum of octets 0 through 10 module 256.
octets.insert(11, sum(octets) % 256)

# The way that Polarium [DS] codes octets to characters is that is takes 4 octets at a time, interprets them as three 32-bit little-endian unsigned integers, converts them to decimal, 0 fills them to 10 characters, and then reverses those characters.
password = [''.join(list(reversed('{:010d}'.format(int.from_bytes(list(x), byteorder='little', signed=False))))) for x in zip(*[iter(octets)]*4)]

height = octets[10] & 0xF0 >> 4
width = octets[10] & 0x0F
print("Tiles:")
for i in range(0, height):
    print("{:0{width}b}".format(octets[i], width=width))
print("Start hints: {:x}".format(octets[8]))
print("End hints: {:x}".format(octets[9]))
print("Size: {:x}".format(octets[10]))
print("Checksum: {:x}".format(octets[11]))

print("Password:")
for line in password:
    print(line)

