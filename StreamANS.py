# Entropy Coding Algorithm: Asymmetric Numeral System
# Citation: https://zhuanlan.zhihu.com/p/688390177


class StreamANS:
    def __init__(self, symbols: list[str], frequencies: list[int], bitwidth: int):
        if sum(frequencies) != 2 ** bitwidth:  # Need to satisfy the sum of all frequencies equal to 2^bitwidth
            raise ValueError("The sum of all frequencies must be equal to 2^bitwidth")
        self.symbols = symbols
        self.frequencies = frequencies
        self.bitwidth = bitwidth  # Maximum bit width of register

        self.mask = (1 << bitwidth) - 1  # Mask code
        self.dic_length = len(symbols)  # Character type
        self.state = 0  # The current compressed number, initially 0

    def encode(self, data: str) -> list[int]:
        compress = []
        for symbol in data:
            index = self.symbols.index(symbol)  # The index of the current symbol
            if self.state >> self.bitwidth >= self.frequencies[index]:
                compress.append(self.state & self.mask)  # Take out the last 'bitwidth' bits of state
                self.state >>= self.bitwidth  # Update state
                pass
            self.state = (self.state // self.frequencies[index] << self.bitwidth) + self.state % self.frequencies[
                index] + sum(self.frequencies[0: index])  # ANS encoding algorithm
            pass
        while self.state != 0:  # Process the rest
            compress.append(self.state & self.mask)
            self.state >>= self.bitwidth
            pass
        return compress

    def decode(self, data_length: int, compressed: list[int]) -> str:
        decompressed = ''
        while compressed and self.state >> self.bitwidth == 0:  # Set the initial state for decoding
            self.state = (self.state << self.bitwidth) | compressed.pop()
        for i in range(data_length):  # Decoding requires the length of the original message
            remainder = self.state & self.mask
            index = 0
            while remainder >= self.frequencies[index]:
                remainder -= self.frequencies[index]
                index += 1
            decompressed += self.symbols[index]
            self.state = (self.state >> self.bitwidth) * self.frequencies[index] + remainder  # ANS decoding algorithm
            if compressed and (self.state >> self.bitwidth) == 0:
                self.state = (self.state << self.bitwidth) | compressed.pop()
            pass
        return decompressed[::-1]


if __name__ == "__main__":
    datas = "CABCAA"
    symbols = ['A', 'B', 'C']
    frequencies = [7, 3, 6]
    sans = StreamANS(symbols=symbols, frequencies=frequencies, bitwidth=4)
    compressed_data = sans.encode(data=datas)
    print("Compressed data: {}".format(compressed_data))
    decompressed_data = sans.decode(data_length=len(datas), compressed=compressed_data)
    print("Decompressed data: {}".format(decompressed_data))
