import matplotlib.pyplot as plt

def makePlot(x, y, x_ext, y_ext, x_pred, y_pred, learnBoarder, title='', pred_ci = None):
    plt.plot(x, y, label='input data')
    plt.plot(x_ext, y_ext, label='model')
    if max(y_ext) > 100 or (pred_ci is not None and max(abs(pred_ci.iloc[:, 0])) > 100):
        plt.ylim(0, 100)
    plt.plot(x_pred, y_pred, label='prediction')
    plt.axvline(x = x[learnBoarder], label = 'training border', color='r')
    if pred_ci is not None:
        plt.fill_between(pred_ci.index,
            pred_ci.iloc[:, 0],
            pred_ci.iloc[:, 1], color='k', alpha=.2)
    plt.legend()
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Mean popularity in %")
    plt.show()