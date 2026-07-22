import easyocr

reader = easyocr.Reader(['en'], gpu=False)


def extract_image(state):

    result = reader.readtext(state["file_path"])

    text = ""

    for r in result:

        text += r[1] + "\n"

    state["raw_text"] = text

    return state