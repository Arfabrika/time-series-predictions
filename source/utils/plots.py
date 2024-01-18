import matplotlib.pyplot as plt

def makePlot(x, y, y_ext, x_pred, y_pred, title='', pred_ci = None, xname = 'X', yname = 'Y'):
    plt.plot(x, y, label='input data')
    plt.plot(x, y_ext, label='model')

    # set scale limit (need add smth for prediction tunnel?)
    plt.ylim(top=max(y) * 1.3)
    plt.ylim(bottom=(min(y) // 2))
    # if max(y_ext) > 100 or (pred_ci is not None and max(abs(pred_ci.iloc[:, 0])) > 100):
    #     plt.ylim(0, 100)
    plt.plot(x_pred, y_pred, label='prediction')
    plt.axvline(x = x[x == x_pred.iloc[0]], label = 'training border', color='r')
    #plt.scatter(x, y, label='input data points')
    if pred_ci is not None:
        plt.fill_between(pred_ci.index,
            pred_ci.iloc[:, 0],
            pred_ci.iloc[:, 1], color='k', alpha=.2)
    plt.legend()
    plt.title(title)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.show()