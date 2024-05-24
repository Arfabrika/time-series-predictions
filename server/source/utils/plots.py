import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
import io
import base64

def makePlot(x, y, y_model, pred_ind, pred_ci = None, **kwargs):
    plt.plot(x, y, label='input data')
    start_ind = kwargs.get('start_ind', 0)
    stop_ind = kwargs.get('stop_ind', 0)
    only_predict = kwargs.get('only_predict', False)
    if not only_predict:
        plt.plot(x[start_ind:], y_model, label='model')

    # set scale limit (need add smth for prediction tunnel?)
    plt.ylim(top=max(y) * 1.3)
    plt.ylim(bottom=(min(y) // 2))
    # if max(y_ext) > 100 or (pred_ci is not None and max(abs(pred_ci.iloc[:, 0])) > 100):
    #     plt.ylim(0, 100)
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
    # plt.show()
    # in future
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    base64Plot = base64.b64encode(my_stringIObytes.read()).decode()
    plt.cla()
    return base64Plot

def autocorrelationPlot(y):
    plot_acf(y)
    plt.show()