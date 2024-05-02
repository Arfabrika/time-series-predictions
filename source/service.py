from source.algorithms.algos import Algos

class Session:
    def __init__(self, data, learn_size, **kwargs) -> None:
        self.data = data
        self.learn_size = int(len(self.data) * learn_size)
        self.algos = Algos(self.learn_size, "Time", "...")


    """
    algos - словарь, имеет следующую структуру:
    {
        "params": [...] - массив параметров или None, если параметры считаем автоматически
        "isPlot": true/false - отображаем ли график
    }
    """
    def makePrediction(self, algos):
        result = []
        # Проверка на стационарность


        for algo_name, algo_params in algos.items():
            if algo_params.get("params", None) is None:
                print("No params, autochoice (in future)")
                continue
            
            # Поиск оптимального размера окна и его местоположения
            best_result = {"metrics": {"MSE": float("inf")}}
            best_win_params = {}
            try:
                cur_algo = getattr(self.algos, algo_name)
            except Exception as e:
                print(f"Error in getting algorithm: {e}")
                continue

            for window_size in range(int(len(self.data) * 0.1), self.learn_size, 2):
                for start_pos in range(0, self.learn_size - window_size, window_size):
                    window_params = {
                        "start_pos": start_pos,
                        "stop_pos": start_pos + window_size
                    }
                    cur_result = cur_algo(self.data, algo_params["params"], window_params = window_params)
                    print(f"Windows params are: size = {window_size}; {window_params['start_pos']} - {window_params['stop_pos']}")
                    if cur_result["metrics"]["MSE"] < best_result["metrics"]["MSE"]:
                        best_result = cur_result
                        best_win_params = window_params

            # Проверка алгоритма на всем временном ряду
            cur_result = cur_algo(self.data, algo_params["params"])
            print(f"Windows params are: size = {self.learn_size}")
            if cur_result["metrics"]["MSE"] < best_result["metrics"]["MSE"]:
                best_result = cur_result
                #best_win_params = window_params

            # Сохранение лучшего результата
            result.append(best_result)
            print("Best window params", best_win_params)
        return result

"""
Решение проблемы двух запросов
def send_request():
    payload = {"param_1": "value_1", "param_2": "value_2"}
    files = {
        'json': (None, json.dumps(payload), 'application/json'),
        'file': (os.path.basename(file), open(file, 'rb'), 'application/octet-stream')
    }

    r = requests.post(url, files=files)
    print(r.content)
"""