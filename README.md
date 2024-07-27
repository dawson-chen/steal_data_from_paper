## code to extract Scaling Law from LLama3.1 paper

1. First, you need to install qpdf

    ```shell
    # on macos
    brew install qpdf
    # on ubuntu
    apt-get install qpdf
    # other
    # install from source or download installer from https://github.com/qpdf/qpdf/releases/tag/v11.9.1
    ```

2. Uncompress the pdf to see the internal operations in pdf file. 

    ```shell
    qpdf --stream-data=uncompress llama3.1_paper.pdf llama3.1_paper_content.txt
    ```

    Run this commmand to get file `llama3.1_paper_content.txt`.

3. run extract code.
    ```shell
    python extract_scaling_law_data.py
    ```

That's it, peace&love to the world
