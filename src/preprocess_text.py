import os

# -------------------------------------
# Helper Functions
# -------------------------------------

def is_all_caps(line):
    """
    Returns True if the line is fully uppercase, ignoring whitespace.
    Useful for detecting headers or article titles.
    """
    return line.strip().isupper()

def join_lines(current_line, next_line):
    """
    Determines whether the current_line should be joined with next_line.
    This logic aims to remove unnecessary line breaks while preserving structure.
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
    Iterates through the lines of a text and joins or separates them based
    on formatting rules, improving the structure and flow of the content.
    """
    processed_lines = []

    for i, current_line in enumerate(lines):
        current_line = current_line.strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''

        # Decide whether to join lines or add a line break
        if join_lines(current_line, next_line):
            processed_lines.append(current_line + '\n')
        else:
            processed_lines.append(current_line + ' ')

    return processed_lines

# -------------------------------------
# Main Preprocessing Function
# -------------------------------------

def preprocess_file(input_path, output_dir="data"):
    """
    Loads a text file, preprocesses its content to clean formatting issues
    (like unwanted line breaks), and writes the result to a new file.
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

# -------------------------------------
# Entry Point (Script Execution)
# -------------------------------------

if __name__ == "__main__":
    input_path = "data/ley-769-de-2002-codigo-nacional-de-transito.txt"
    preprocess_file(input_path)
