"""Doc."""
from multiprocessing import Process, Manager
from autosk import run

t = {
    'Survived': 'target',
    'Age': 'predictor'
}

if __name__ == '__main__':
    manager = Manager()
    return_dict = manager.dict()
    p = Process(target=run, args=('titanic.csv', t, return_dict))
    p.start()
    p.join()
    print(return_dict)
