import os
import subprocess
import tempfile
import sys


def find_mermaid_trio_and_svg_files(directory):
    mermaid_files = []
    trio_files = []
    svg_files = []

    for root, dirs, files in os.walk(directory):
        if "src" in dirs:
            src_dir = os.path.join(root, "src")
            for file in os.listdir(src_dir):
                if file.endswith(".mermaid"):
                    mermaid_files.append(os.path.join(src_dir, file))
                elif file.endswith(".trio.json"):
                    trio_files.append(os.path.join(src_dir, file))
                elif file.endswith(".svg"):
                    svg_files.append(os.path.join(src_dir, file))

    return mermaid_files, trio_files, svg_files


def convert_mermaid_to_png(mermaid_file):
    directory, filename = os.path.split(mermaid_file)
    base_filename = os.path.splitext(filename)[0]

    src_directory = os.path.dirname(directory)
    img_directory = os.path.join(src_directory, "img")
    os.makedirs(img_directory, exist_ok=True)

    png_file = os.path.join(img_directory, f"{base_filename}.mermaid.png")

    command = f"mmdc --puppeteerConfigFile /docx-202405-from-md/puppeteer.json -i {mermaid_file} -o {png_file} -s 16 -b white"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {mermaid_file} to PNG: {e}")


def convert_trio_to_png(trio_file):
    directory, filename = os.path.split(trio_file)
    base_filename = os.path.splitext(filename)[0]

    src_directory = os.path.dirname(directory)
    img_directory = os.path.join(src_directory, "img")
    os.makedirs(img_directory, exist_ok=True)

    png_file = os.path.join(img_directory, f"{base_filename}.trio.png")

    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as temp_svg_file:
        temp_svg_path = temp_svg_file.name

    command = f"roger trio --trio {trio_file} -o {temp_svg_path}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {trio_file} to SVG: {e}")
        return

    command = f"inkscape {temp_svg_path} --export-filename={png_file} --export-background=white --export-background-opacity=1.0 --export-dpi=600"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {temp_svg_path} to PNG: {e}")
    finally:
        os.remove(temp_svg_path)


def convert_svg_to_png(svg_file):
    directory, filename = os.path.split(svg_file)
    base_filename = os.path.splitext(filename)[0]

    src_directory = os.path.dirname(directory)
    img_directory = os.path.join(src_directory, "img")
    os.makedirs(img_directory, exist_ok=True)

    png_file = os.path.join(img_directory, f"{base_filename}.svg.png")

    command = f"inkscape {svg_file} --export-filename={png_file} --export-background=white --export-background-opacity=1.0 --export-dpi=600"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {svg_file} to PNG: {e}")


def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."

    mermaid_files, trio_files, svg_files = find_mermaid_trio_and_svg_files(directory)

    if not mermaid_files and not trio_files and not svg_files:
        print("No .mermaid, .trio.json, or .svg files found in the repository.")
    else:
        for file in mermaid_files:
            convert_mermaid_to_png(file)
        for file in trio_files:
            convert_trio_to_png(file)
        for file in svg_files:
            convert_svg_to_png(file)


if __name__ == "__main__":
    main()
