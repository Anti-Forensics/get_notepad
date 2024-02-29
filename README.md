This application will dump the notepad tab cache to json format. Notepad caches your data until the tab within Notepad.exe has been closed.

Among much data, the notepad cache is used to store filenames (if saved) and tab content data. This means that your notes may be fully recoverable.

Just run the program on a windows 11 machine or integrate the class into your own project. This program outputs json format.

Example output:

.\get_notepad.exe  
    {"filename0000": null, "data0000": "asdfasdff", "filename0001": null, "data0001": "test23", "filename0002": null, "data0002": "test\\rtest\\rtest\\rtest4\\r\\rtest5  "}  