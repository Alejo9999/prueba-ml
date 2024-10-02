from app.file_reader.read_file import read_csv
from io import StringIO

def test_read_csv():
    csv_file = StringIO("MLA,123\nMLB,456")
    items = read_csv(csv_file)
    assert len(items) == 2
    assert items[0]["site"] == "MLA"
    assert items[0]["id"] == 123
