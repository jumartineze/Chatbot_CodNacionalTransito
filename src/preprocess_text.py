import os

def is_all_caps(line):
    """
    Check if a line is in all uppercase (after stripping).
    """
    return line.strip().isupper()



def join_lines(current_line, next_line):
    """
    Determine whether the current line should be joined with the next one.
    """
    return (
        is_all_caps(current_line) or
        is_all_caps(next_line) or
        current_line.endswith('.') or
        len(current_line.strip()) == 0 or
        next_line[:1].isupper() or
        next_line.replace('"', '')[:1].isupper()
    )



def preprocess_text_lines(lines):
    """
    Clean and join lines based on rules to improve structure and readability.
    """
    processed_lines = []
    for i, current_line in enumerate(lines):
        current_line = current_line.strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''

        if join_lines(current_line, next_line):
            processed_lines.append(current_line + '\n')
        else:
            processed_lines.append(current_line + ' ')
    return processed_lines



def preprocess_file(input_path, output_dir="data"):
    """
    Read a text file, process its lines to remove unwanted breaks, and save the result.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_preprocessed.txt")

    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    cleaned_text = ''.join(preprocess_text_lines(lines))

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(cleaned_text)



if __name__ == "__main__":
    input_path = "data/ley-769-de-2002-codigo-nacional-de-transito.txt"
    preprocess_file(input_path)
