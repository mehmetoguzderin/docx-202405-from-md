PYTHON_BIN=python3
if ! command -v $PYTHON_BIN &> /dev/null
then
    PYTHON_BIN=python
fi

$PYTHON_BIN /docx-202405-from-md/src-to-img.py /data

$PYTHON_BIN /docx-202404-from-md/docx-202404-from-md.py /data
