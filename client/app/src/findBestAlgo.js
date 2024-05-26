export function findBestAlgo(data) {
    var bestInd = 0
    var bestMSE = Infinity
    data.result.map((item, index) => {
        if (item.metrics.MSE < bestMSE) {
            bestMSE = item.metrics.MSE;
            bestInd = index
        }
    })
    return bestInd
}