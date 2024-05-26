import matplotlib.pyplot as plt
import numpy as np
import io
import datetime
import base64

def makePlot(x, y, y_model, pred_ind, pred_ci = None, **kwargs):
    def makeOnePlot(x, y, y_model, pred_ind, pred_ci, **kwargs):
        
        start_ind = kwargs.get('start_ind', 0)
        stop_ind = kwargs.get('stop_ind', 0)
        only_predict = kwargs.get('only_predict', False)
        isFull = kwargs.get('isFull', False)
        if not isFull:
            plt.figure(figsize=(8, 6))
        plt.plot(x, y, label='input data')
        if not only_predict:
            plt.plot(x[start_ind:], y_model, label='model')

        plt.ylim(top=max(y) * 1.3)
        plt.ylim(bottom=(min(y) // 2))
        if not only_predict:
            plt.plot(x[pred_ind:], y_model[pred_ind - start_ind:], label='prediction')
        else:
            plt.plot(x[pred_ind:], y_model, label='prediction')
        plt.axvline(x = x[x == x[pred_ind]], label = 'test border', color='r')
        plt.vlines([x[x == x[stop_ind]], x[x == x[start_ind]]], ymin=min(y) // 2,
                ymax=max(y) * 1.3, color='y', label = 'learn border', linestyle='dashed')
        #plt.scatter(x, y, label='input data points')
        if pred_ci is not None:
            plt.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
        plt.legend()
        plt.title(kwargs.get('title', kwargs.get("name", "Prediction")))
        plt.xlabel(kwargs.get('xname', 'X'))
        plt.ylabel(kwargs.get('yname', 'Y'))
        if isFull: 
            plt.get_current_fig_manager().full_screen_toggle()
        else:
            # Hardcode for metro dataset
            plt.xticks(np.arange(min(x), max(x) + datetime.timedelta(days=10), (x[1] - x[0]) * (len(y) // 5)))

        my_stringIObytes = io.BytesIO()
        plt.savefig(my_stringIObytes, format='jpg')
        my_stringIObytes.seek(0)
        base64Plot = base64.b64encode(my_stringIObytes.read()).decode()
        plt.cla()
        return base64Plot

    plots = []
    kwargs['isFull'] = False
    plots.append(makeOnePlot(x, y, y_model, pred_ind, pred_ci, **kwargs))
    kwargs['isFull'] = True
    plots.append(makeOnePlot(x, y, y_model, pred_ind, pred_ci, **kwargs))
    return plots
