import os
import glob


class GetNotepad:
    def __init__(self) -> None:
        self.environ_path = os.environ['LOCALAPPDATA']
        self.np_cache_path = "Packages\\Microsoft.WindowsNotepad_8wekyb3d8bbwe\\LocalState\\TabState\\"
        self.np_cache_path = os.path.join(self.environ_path, self.np_cache_path)

    def get_all_files(self) -> list:
        '''
        Filters all files to *.bin removing ".0.bin", ".0.1.bin", ".1.bin".
        :return:
        selected_files (the filtered list of files)
        '''
        selected_files = []

        all_files = glob.glob(os.path.join(self.np_cache_path, "*.bin*"))
        for file in all_files:
            if file.endswith(".0.bin") or file.endswith(".1.bin"):
                continue
            selected_files.append(file)

        return selected_files

    def get_file_content(self, full_file_path: str) -> bytes:
        with open(full_file_path, 'br') as file:
            return file.read()

    def get_file_name(self, full_file_path: str) -> str | None:
        # byte 4
        try:
            if self.get_issaved(full_file_path):
                full_file = self.get_file_content(full_file_path)
                file_name_size = full_file[4] * 2

                return full_file[5:5 + file_name_size].decode("utf-16")
        except:
            print(f"Could not get filename for {full_file_path=}")

    def get_issaved(self, full_file_path: str) -> bool:
        full_file = self.get_file_content(full_file_path)
        issaved = bool(full_file[3])
        if type(issaved is bool):
            return issaved

    def get_file_data(self, full_file_path: str) -> bytes:
        full_file = self.get_file_content(full_file_path)
        pattern = b"\x01\x00\x00\x00"

        data_start = full_file.index(pattern)
        parsed_full = full_file[data_start + 6:-5]

        try:
            parsed_full_encode = parsed_full.decode('utf-16le').encode('utf8')
        except:
            parsed_full = full_file[data_start + 5: -5]
            parsed_full_encode = parsed_full.decode('utf-16le').encode('utf8')

        return parsed_full_encode


def main():
    getnote = GetNotepad()

    files = getnote.get_all_files()
    for file in files:
        print(getnote.get_file_name(file))
        print(getnote.get_issaved(file))
        print(getnote.get_file_data(file))


if __name__ == "__main__":
    main()
