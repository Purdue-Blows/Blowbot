import os

src_directory = "/home/xanmankey/Programming/Misc/BlowBot/blowbot/src"
test_directory = "/home/xanmankey/Programming/Misc/BlowBot/blowbot/tests"

for root, dirs, files in os.walk(src_directory):
    relative_path = os.path.relpath(root, src_directory)
    test_path = os.path.join(test_directory, relative_path)
    os.makedirs(test_path, exist_ok=True)
    for file in files:
        test_file_path = os.path.join(test_path, "test_" + file)
        open(test_file_path, "w").close()
