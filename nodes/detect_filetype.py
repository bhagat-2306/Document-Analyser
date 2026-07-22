from utils.file_utils import get_file_extension


def detect_filetype(state):

    extension = get_file_extension(state["file_path"])

    state["file_type"] = extension

    return state