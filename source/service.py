from source.algorithms.algos import Algos

class Session:
    def __init__(self, data, learn_size, **kwargs) -> None:
        self.data = data
        self.learn_size = int(len(self.data) * learn_size)
        self.algos = Algos(self.learn_size, "Time", "...")


    def makePrediction(self, inputData):
        result = []
        # Проверка на стационарность

        # total_best_result = {"metrics": {"MSE": float("inf")}}
        # total_best_win_params = {}

        algos = inputData.get("algos", {})

        for algo_name, algo_params in algos.items():
            if algo_params.get("params", None) is None:
                print("No params, autochoice (in future)")
                continue
            
            # Поиск оптимального размера окна и его местоположения
            # TODO предоставить пользователю выбор из реализованных метрик
            best_result = {"metrics": {"MSE": float("inf")}}
            best_win_params = {}
            try:
                cur_algo = getattr(self.algos, algo_name)
            except Exception as e:
                print(f"Error in getting algorithm: {e}")
                continue
            window_params = algo_params.get("window_params", {})

            # Проверка на наличие пользовательского обучающего интервала
            if len(window_params) > 0:
                best_result = cur_algo(self.data, algo_params["params"], window_params = window_params)
                best_win_params = window_params
            else:
                if not algo_params.get("fullTrain", False):
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
                    best_win_params = {"start_pos": 0, "stop_pos": self.algos.learn_size}

            # Сохранение лучшего результата внутри алгоритма
            result.append(best_result)
            print("Best window params", best_win_params)

            # Поиск лучшего алгоритма - вынести логику поиска лучшего на фронт?
            # if best_result["metrics"]["MSE"] < total_best_result["metrics"]["MSE"]:
            #     total_best_result = best_result
            #     total_best_win_params = best_win_params

        # Применение усредненного алгоритма
        if inputData.get("needAvg", False):
            # Сбор данных от других алгоритмов (только для прогноза!)
            algdata = []
            for res in result:
                algdata.append(res['pred'][self.algos.learn_size:])
            cur_result = self.algos.averange(self.data, algdata)

        return result
        # return {
        #     "result": result,
        #     "best": best_result
        #     }

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