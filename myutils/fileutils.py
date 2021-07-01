import errno
import os


def write_string_to_file(filename, string):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        # for c
        f.write(string)
        f.close()


def initialize_with_empty_file(filename):
    write_string_to_file(filename, '')
