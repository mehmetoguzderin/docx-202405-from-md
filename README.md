## Prerequisites

* Docker

## Usage

1. Navigate to the directory containing the Markdown file.
2. Run the following command:

   ```
   docker run -v $PWD/:/data --rm ghcr.io/mehmetoguzderin/docx-202405-from-md:main
   ```

3. The generated Word file and diagrams will be saved in the same directory.
