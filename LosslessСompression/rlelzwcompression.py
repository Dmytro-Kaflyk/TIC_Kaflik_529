import math
import matplotlib.pyplot as plt

def encode_rle(sequence):
    if not sequence:
        return []
    encoded = []
    count = 1
    prev = sequence[0]
    for ch in sequence[1:]:
        if ch == prev:
            count += 1
        else:
            encoded.append((count, prev))
            count = 1
            prev = ch
    encoded.append((count, prev))
    return encoded

def decode_rle(sequence):
    result = []
    for count, ch in sequence:
        result.append(ch * count)
    return "".join(result)

def encode_lzw(data):
    dictionary = {chr(i): i for i in range(65536)}
    current = ""
    result = []
    size = 0
    with open("results_rle_lzw.txt", "a", encoding="utf-8") as file:
        for c in data:
            new_str = current + c
            if new_str in dictionary:
                current = new_str
            else:
                code = dictionary[current]
                element_bits = 16 if code < 65536 else math.ceil(math.log2(len(dictionary)))
                size += element_bits
                file.write(f"Code: {code}, Element: {current}, Bits: {element_bits}\n")
                result.append(code)
                dictionary[new_str] = len(dictionary)
                current = c
        code = dictionary[current]
        element_bits = 16 if code < 65536 else math.ceil(math.log2(len(dictionary)))
        size += element_bits
        file.write(f"Code: {code}, Element: {current}, Bits: {element_bits}\n")
        result.append(code)
        file.write(f"Закодована LZW послідовність: {''.join(map(str, result))} \n")
        file.write(f"Розмір закодованої LZW послідовності: {size} bits \n\n")
    return result, size

def decode_lzw(sequence):
    dictionary = {i: chr(i) for i in range(65536)}
    result = ""
    previous = None
    with open("results_rle_lzw.txt", "a", encoding="utf-8") as file:
        for code in sequence:
            if code in dictionary:
                current = dictionary[code]
                result += current
                if previous is not None:
                    dictionary[len(dictionary)] = previous + current[0]
                previous = current
            else:
                current = previous + previous[0]
                result += current
                dictionary[len(dictionary)] = current
                previous = current
        file.write(f"Декодована LZW послідовність: {result}\n")
        file.write(f"Розмір декодованої LZW послідовності: {len(result)*16} bits\n\n")
    return result

def entropy(sequence):
    from collections import Counter
    n = len(sequence)
    freq = Counter(sequence)
    ent = 0
    for count in freq.values():
        p = count / n
        ent -= p * math.log2(p)
    return ent

def compression_ratio(original_len, compressed_bits):
    return round((original_len * 16) / compressed_bits, 2)

def process_sequences_with_metrics(sequences):
    results = []
    with open("results_rle_lzw.txt", "w", encoding="utf-8") as file:
        for idx, seq in enumerate(sequences, 1):
            file.write(f"Послідовність {idx}: {seq}\n\n")
            encoded_rle = encode_rle(seq)
            decoded_rle = decode_rle(encoded_rle)
            compression_ratio_rle = compression_ratio(len(seq), sum(count * 16 for count, _ in encoded_rle))
            file.write(f"RLE закодована послідовність: {encoded_rle}\n")
            file.write(f"RLE декодована послідовність: {decoded_rle}\n")
            file.write(f"Розмір RLE закодованої послідовності: {sum(count * 16 for count, _ in encoded_rle)} bits\n")
            file.write(f"Коефіцієнт стиснення RLE: {compression_ratio_rle}\n\n")
            encoded_lzw, size_lzw = encode_lzw(seq)
            decoded_lzw = decode_lzw(encoded_lzw)
            compression_ratio_lzw = compression_ratio(len(seq), size_lzw)
            file.write(f"LZW закодована послідовність: {encoded_lzw}\n")
            file.write(f"LZW декодована послідовність: {decoded_lzw}\n")
            file.write(f"Розмір LZW закодованої послідовності: {size_lzw} bits\n")
            file.write(f"Коефіцієнт стиснення LZW: {compression_ratio_lzw}\n\n")
            ent = entropy(seq)
            results.append([round(ent, 2), compression_ratio_rle, compression_ratio_lzw])
    return results

def plot_results(results):
    N = len(results)
    fig, ax = plt.subplots(figsize=(14/1.54, N/1.54))
    headers = ['Ентропія', 'КС RLE', 'КС LZW']
    rows = [f'Послідовність {i+1}' for i in range(N)]
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=rows,
                     loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    plt.savefig("results_table.png")
    plt.show()

if __name__ == "__main__":
    sequences_to_process = [
        "аааааааab",
        "11102140",
        "abcdefgabcdefg",
        "ааабббвввггг",
        "ababababab",
        "1111111111111111",
        "abcabcabcabc",
        "zzzzzzzzzzzzzzzz"
    ]
    results = process_sequences_with_metrics(sequences_to_process)
    plot_results(results)
