from source.algorithms.algos import Algos

class Session:
    def __init__(self, data, learn_size, **kwargs) -> None:
        self.data = data
        self.learn_size = int(len(self.data) * learn_size)
        self.algos = Algos(self.learn_size, "Time", "...")


    def runAlgo(self, cur_algo, params, edit_algo_params, **kwargs):
        if edit_algo_params:
            cur_edit_algo = getattr(self.algos, edit_algo_params['name'])
            try:
                cur_result = cur_edit_algo(self.data, edit_algo_params['params'], cur_algo, params, kwargs)
            except Exception as e:
                print(f"Error in edit algo block: {str(e)}")
                cur_result = {"metrics": {"MSE": float("inf")}}
        else:
            try:
                cur_result = cur_algo(self.data, params, **kwargs)
            except Exception as e:
                print(f"Error: {str(e)}")
                cur_result = {"metrics": {"MSE": float("inf")}}
        return cur_result


    def makePrediction(self, inputData):
        result = []
        # Проверка на стационарность

        # total_best_result = {"metrics": {"MSE": float("inf")}}
        # total_best_win_params = {}

        algos = inputData.get("algos", {})

        for algo_name, algo_params in algos.items():
            params = algo_params.get("params", None)
            # Параметр, будет ли рисоваться график
            isPlot = algo_params.get("isPlot", False)
            if params is None:
                params_list = self.algos.makeParamsList(algo_name, len(self.data) - self.learn_size)
            else:
                params_list = [params]
            edit_algo_params = algo_params.get("editAlgo", None)

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
            for params in params_list:
                if len(window_params) > 0:
                    cur_result = self.runAlgo(cur_algo, params, edit_algo_params,
                                              window_params=window_params, isPlot=isPlot)
                    if cur_result["metrics"]["MSE"] < best_result["metrics"]["MSE"]:
                        best_result = cur_result
                        best_win_params = window_params
                        best_algo_params = params
                else:
                    # Проверка, надо ли обучать алгоритм на всей обучающей выборке
                    if not algo_params.get("fullTrain", False):
                        for window_size in range(int(len(self.data) * 0.1), self.learn_size, 2):
                            for start_pos in range(0, self.learn_size - window_size, window_size):
                                window_params = {
                                    "start_pos": start_pos,
                                    "stop_pos": start_pos + window_size
                                }
                                print(f"Model params in win: {params}, Windows params are: size = {window_size}; {window_params['start_pos']} - {window_params['stop_pos']}")

                                cur_result = self.runAlgo(cur_algo, params, edit_algo_params,
                                              window_params=window_params, isPlot=isPlot)
                                if cur_result["metrics"]["MSE"] < best_result["metrics"]["MSE"]:
                                    best_result = cur_result
                                    best_win_params = window_params
                                    best_algo_params = params

                    # Проверка алгоритма на всем временном ряду
                    print(f"Windows params are: size = {self.learn_size}")
                    print(f"Model params in full: {params}")
                    cur_result = self.runAlgo(cur_algo, params, edit_algo_params,
                                              window_params=window_params, isPlot=isPlot)
                    if cur_result["metrics"]["MSE"] < best_result["metrics"]["MSE"]:
                        best_result = cur_result
                        best_win_params = {"start_pos": 0, "stop_pos": self.algos.learn_size}
                        best_algo_params = params
                    window_params = {}
            # Сохранение лучшего результата внутри алгоритма
            result.append(best_result)
            print("Best window params", best_win_params)
            print("Best algo params:", best_algo_params)

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

        self.algos.outtbl.save()
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