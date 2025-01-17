import tempfile

from stbl.stbl import STBLFile


def test_stblfile(path_stbl):
    stblfile = STBLFile()
    stblfile.read(path_stbl)

    assert stblfile.header.signature == b'STBL'
    assert stblfile.header.version == 5
    assert stblfile.header.entry_num == 6
    assert stblfile.header.checksum == 152

    assert stblfile.entries[0].instance_id == 0xC728CF53
    assert stblfile.entries[0].length == 15
    assert stblfile.entries[0].text == 'Touchable Grass'
    assert stblfile.entries[1].instance_id == 0x5F241919
    assert stblfile.entries[1].length == 30
    assert stblfile.entries[1].text == 'It\'s grass that you can touch.'
    assert stblfile.entries[2].instance_id == 0x7CA1A310
    assert stblfile.entries[2].length == 11
    assert stblfile.entries[2].text == 'Touch Grass'
    assert stblfile.entries[3].instance_id == 0x9786BDDC
    assert stblfile.entries[3].length == 12
    assert stblfile.entries[3].text == '(From Grass)'
    assert stblfile.entries[4].instance_id == 0xFF405357
    assert stblfile.entries[4].length == 65
    assert stblfile.entries[4].text == '{0.SimFirstName} touched grass and finally understand everything.'
    assert stblfile.entries[5].instance_id == 0xCEA90473
    assert stblfile.entries[5].length == 13
    assert stblfile.entries[5].text == 'Touched Grass'

    entries = stblfile.find_entries(0xCEA90473)

    assert len(entries) == 1
    assert entries[0].instance_id == 0xCEA90473
    assert entries[0].length == 13
    assert entries[0].text == 'Touched Grass'

    assert stblfile.find_entries(0x12345678) == []

    assert stblfile.validate()

    with tempfile.NamedTemporaryFile() as f:
        stblfile.write(f.name)

        new_file = STBLFile()
        new_file.read(f.name)

        assert new_file.validate()
        assert new_file.header.entry_num == 6
        assert new_file.header.checksum == 152
