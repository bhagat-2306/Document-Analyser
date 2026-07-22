from pathlib import Path

from config import UPLOAD_DIR


def load_document(state):
    uploaded_file = state.get('uploaded_file')
    file_path = state.get('file_path')

    if uploaded_file is not None:
        save_path = UPLOAD_DIR / uploaded_file.name
        with open(save_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        state['file_path'] = str(save_path)
        state['uploaded_file'] = None

    elif file_path:
        state['file_path'] = str(Path(file_path))

    else:
        raise ValueError('No document was provided to load.')

    return state
