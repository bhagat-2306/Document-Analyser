from utils.text_cleaner import clean_text


def preprocess(state):

    cleaned_text = clean_text(state["raw_text"])

    state["cleaned_text"] = cleaned_text

    return state