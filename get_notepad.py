import json
import os
import glob


class GetNotepad:
    def __init__(self) -> None:
        self.environ_path = os.environ['LOCALAPPDATA']
        self.np_cache_path = "Packages\\Microsoft.WindowsNotepad_8wekyb3d8bbwe\\LocalState\\TabState\\"
        self.np_cache_path_full = os.path.join(self.environ_path, self.np_cache_path)

    def get_all_files(self) -> list:
        '''
        Filters all files to *.bin removing ".0.bin", ".0.1.bin", ".1.bin".
        :return:
        selected_files (the filtered list of files)
        '''
        selected_files = []

        all_files = glob.glob(os.path.join(self.np_cache_path_full, "*.bin*"))
        for file in all_files:
            if file.endswith(".0.bin") or file.endswith(".1.bin"):
                continue
            selected_files.append(file)

        return selected_files

    def get_file_content(self, full_file_path: str) -> bytes:
        '''
        Read the file and prepare it in a variable
        :param full_file_path:
        :return:
        Full file contents in binary mode.
        '''
        with open(full_file_path, 'br') as file:
            return file.read()

    def get_file_name(self, full_file_path: str) -> str:
        '''
        Returns a file name or prints an error message if issaved
        :param full_file_path:
        :return:
        Returns the extracted and decoded file name otherwise prints an error message.
        '''
        # byte 4
        try:
            if self.get_issaved(full_file_path):
                full_file = self.get_file_content(full_file_path)
                file_name_size = full_file[4] * 2

                return full_file[5:5 + file_name_size].decode("utf-16")
        except:
            print(f"Could not get filename for {full_file_path=}")

    def get_issaved(self, full_file_path: str) -> bool:
        '''
        Determines whether a tab in Notepad is saved to a file.
        :param full_file_path:
        :return:
        issaved: bool
        '''
        full_file = self.get_file_content(full_file_path)
        issaved = bool(full_file[3])
        if type(issaved is bool):
            return issaved

    def get_file_data(self, full_file_path: str) -> str:
        '''
        Slices the .bin to extract only the user content data.
        :param full_file_path:
        :return:
        Returns the data as a string
        '''
        full_file = self.get_file_content(full_file_path)
        pattern = b"\x01\x00\x00\x00"

        data_start = full_file.index(pattern)
        parsed_full = full_file[data_start + 6:-5]

        # try: parse > 255 bytes if exception reduce byte start length
        # encode to utf8 to capture the full content - decode with utf16 prints only last line
        try:
            parsed_full_encode = parsed_full.decode('utf-16le').encode('utf8')
        except:
            parsed_full = full_file[data_start + 5: -5]
            parsed_full_encode = parsed_full.decode('utf-16le').encode('utf8')

        return str(parsed_full_encode)


def main() -> None:
    getnote = GetNotepad()
    np_dictionary = {}
    i = 0

    files = getnote.get_all_files()
    for file in files:
        np_dictionary["filename" + str(i).zfill(4)] = getnote.get_file_name(file)

        # workaround (print on decode only prints last line of data from utf16)
        np_dictionary["data" + str(i).zfill(4)] = getnote.get_file_data(file).strip("b'")

        i += 1

    x = json.dumps(np_dictionary)
    print(x)


if __name__ == "__main__":
    main()
