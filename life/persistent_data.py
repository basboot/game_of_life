import pickle
import os.path

PERSISTENT_DATA_FILE = "results.pk"

def save_data(results, max_n):
    data = {"results": results, "max_n": max_n}
    file = open(PERSISTENT_DATA_FILE, 'wb')
    pickle.dump(data, file)
    file.close()


def load_data():
    # Create data file if not exists
    if not os.path.isfile(PERSISTENT_DATA_FILE):
        # initial data
        save_data({}, 0)

        
    file = open(PERSISTENT_DATA_FILE, 'rb')
    data = pickle.load(file)
    file.close()
    return data["results"], data["max_n"]