from dataclasses import dataclass
from functools import reduce
from struct import pack, unpack


@dataclass
class STBLHeader:
    signature: bytes
    version: int
    entry_num: int
    checksum: int


@dataclass
class STBLEntry:
    instance_id: int
    length: int
    text: str


class STBLFile:
    header: STBLHeader
    entries: list

    @staticmethod
    def parse_header(f):
        f.seek(0)
        data = unpack('<4schI6sI', f.read(21))
        return STBLHeader(
            signature=data[0],
            version=data[1],
            entry_num=data[3],
            checksum=data[5]
        )

    @staticmethod
    def parse_entries(f):
        entries = []

        f.seek(21)

        while True:
            buf = f.read(7)

            if not buf:
                break

            data = unpack('<IcH', buf)
            entries.append(
                STBLEntry(
                    instance_id=data[0],
                    length=data[2],
                    text=(unpack('%ds' % data[2], f.read(data[2]))[0]).decode('utf-8')
                )
            )

        return entries

    def __init__(self):
        self.entries = []

    def read(self, filename):
        f = open(filename, 'rb')

        self.header = STBLFile.parse_header(f)
        self.entries = STBLFile.parse_entries(f)

        f.close()

    def write(self, filename):
        f = open(filename, 'wb')
        f.write(pack('<4schIihI', b'STBL', b'\x05', 0, len(self.entries), 0, 0, self.calculate_checksum()))

        for entry in self.entries:
            f.write(pack('<IcH', entry.instance_id, b'\x00', entry.length))
            f.write(bytes(entry.text, 'utf-8'))

        f.close()

    def calculate_checksum(self):
        return reduce(lambda value, entry: value + entry.length, self.entries, 0) + len(self.entries)

    def validate(self):
        result = self.header.signature == b'STBL'
        result = result and self.header.version == b'\x05'
        result = result and self.header.entry_num == len(self.entries)

        result = result and self.header.checksum == self.calculate_checksum()

        return result

    def find_entry(self, instance_id):
        result = list(filter(lambda e: e.instance_id == instance_id, self.entries))

        if len(result) > 1:
            raise Exception('Instance ID "%d" is not unique.' % instance_id)

        if len(result) == 1:
            return result[0]
        else:
            return None
