def heap_push(heap, item):
    heap.append(item)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i][0] < heap[parent][0]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break

def heap_pop(heap):
    if len(heap) == 1:
        return heap.pop()
    root = heap[0]
    heap[0] = heap.pop()
    i = 0
    size = len(heap)
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < size and heap[left][0] < heap[smallest][0]:
            smallest = left
        if right < size and heap[right][0] < heap[smallest][0]:
            smallest = right
        if smallest != i:
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
        else:
            break
    return root

def build_min_heap(freq_list):
    heap = []
    for item in freq_list:
        heap_push(heap, item)
    return heap

def count_frequencies(data):
    freq = {}
    for char in data:
        if char not in freq:
            freq[char] = 0
        freq[char] += 1
    return freq

def sort_frequencies(freq):
    freq_list = [(count, char) for char, count in freq.items()]
    freq_list.sort(key=lambda x: x[0])
    return freq_list

def build_tree(freq_list):
    heap = build_min_heap(freq_list)
    while len(heap) > 1:
        left = heap_pop(heap)
        right = heap_pop(heap)
        combined = (left[0] + right[0], (left, right))
        heap_push(heap, combined)
    return heap[0]

def generate_codes(tree, prefix="", codes=None):
    if codes is None:
        codes = {}
    if isinstance(tree[1], str):
        codes[tree[1]] = prefix
    else:
        generate_codes(tree[1][0], prefix + "0", codes)
        generate_codes(tree[1][1], prefix + "1", codes)
    return codes

def encode_data(data, codes):
    encoded = ""
    for char in data:
        encoded += codes[char]
    return encoded

def decode_data(encoded, tree):
    decoded = ""
    node = tree
    for bit in encoded:
        if bit == "0":
            node = node[1][0]
        else:
            node = node[1][1]
        if isinstance(node[1], str):
            decoded += node[1]
            node = tree
    return decoded

def compress(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()
    freq = count_frequencies(data)
    freq_list = sort_frequencies(freq)
    tree = build_tree(freq_list)
    codes = generate_codes(tree)
    encoded = encode_data(data, codes)
    byte_array = bytearray()
    buffer = ""
    for bit in encoded:
        buffer += bit
        if len(buffer) == 8:
            byte_array.append(int(buffer, 2))
            buffer = ""
    if buffer:
        byte_array.append(int(buffer.ljust(8, "0"), 2))
    with open(output_file, "wb") as f:
        f.write(len(freq).to_bytes(2, "big"))
        for char, count in freq.items():
            f.write(char.encode("utf-8"))
            f.write(count.to_bytes(4, "big"))
        f.write(byte_array)

def decompress(input_file, output_file):
    with open(input_file, "rb") as f:
        freq_size = int.from_bytes(f.read(2), "big")
        freq = {}
        for _ in range(freq_size):
            char = f.read(1).decode("utf-8")
            count = int.from_bytes(f.read(4), "big")
            freq[char] = count
        encoded_data = f.read()
    bit_string = ""
    for byte in encoded_data:
        bit_string += f"{byte:08b}"
    freq_list = sort_frequencies(freq)
    tree = build_tree(freq_list)
    decoded = decode_data(bit_string.strip("0"), tree)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(decoded)

def main():
    print("1 - Kompresja")
    print("2 - Dekompresja")
    choice = input("Wybierz: ")
    if choice == "1":
        input_file = input("Plik wejściowy: ")
        output_file = input("Plik wyjściowy: ")
        compress(input_file, output_file)
        print("Kompresja zakończona.")
    elif choice == "2":
        input_file = input("Plik skompresowany: ")
        output_file = input("Plik wyjściowy: ")
        decompress(input_file, output_file)
        print("Dekompresja zakończona.")
    else:
        print("Nieprawidłowa opcja.")

if __name__ == "__main__":
    main()
