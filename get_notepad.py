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
        with open(full_file_path, 'rb') as file:
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

    def get_file_data(self, full_file_path: str) -> str:
        full_file = self.get_file_content(full_file_path)
        pattern = b"\x01\x00\x00\x00"
        #pattern = b"\x00t\x00e"
        #data_start = full_file[full_file.index(pattern)+5:-5]
        data_start = full_file[full_file.index(pattern)+6:-5]
        print(data_start)
        # for data in data_start:
        #     print(data)
        print(data_start.decode('utf-16'))


def main():
    getnote = GetNotepad()
    file = r"C:\Users\jesse\AppData\Local\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\TabState\a1ebe41d-2862-4f3a-881e-299125f61e10.bin"
   # files = getnote.get_all_files()
   # for file in files:
    #     #print(getnote.get_file_name(file))
    #     # print(getnote.get_issaved(file))
    print(getnote.get_file_name(file))
    getnote.get_file_data(file)

    # file = getnote.get_file_content("C:\\Users\\jesse\\AppData\\Local\\Packages\\Microsoft.WindowsNotepad_8wekyb3d8bbwe\\LocalState\\TabState\\02cd1a99-c190-4b10-854b-f9321717d3da.bin")
    #
    # print(file.decode('utf-16'))
    # getnote.get_file_name("C:\\Users\\jesse\\AppData\\Local\\Packages\\Microsoft.WindowsNotepad_8wekyb3d8bbwe\\LocalState\\TabState\\02cd1a99-c190-4b10-854b-f9321717d3da.bin")


if __name__ == "__main__":
    main()
