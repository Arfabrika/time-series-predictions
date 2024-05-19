import pandas as pd

class OutDataTable:
    def __init__(self, colNames, fileName = 'out.csv', sortColumn = '') -> None:
        self.sortColumn = (colNames[0] if sortColumn == '' else sortColumn)
        self.tbl = pd.DataFrame(columns = colNames)
        self.fileName = fileName
        self.tmparr = [' - '] * len(colNames)

    def write(self):
        self.tbl.loc[len(self.tbl.index )] = self.tmparr
        self.tmparr = [' - '] * len(self.tbl.columns)

    def add(self, vals, inds = []):
        for i in range(len(inds)):
            self.tmparr[inds[i]] = vals[i]

    def save(self):
        self.tbl = self.tbl.sort_values(self.sortColumn)
        writer = pd.ExcelWriter(self.fileName, engine='xlsxwriter')
        self.tbl.to_excel(writer, sheet_name='algos', index=False)

        # set auto column width
        for column in self.tbl:
            column_length = max(self.tbl[column].astype(str).map(len).max(), len(column)) + 1
            col_idx = self.tbl.columns.get_loc(column)
            writer.sheets['algos'].set_column(col_idx, col_idx, column_length)
        writer.close()

    def makeIndsArr(self, colNames):
        arr = []
        for name in colNames:
            arr.append(self.tbl.columns.get_loc(name))
        return arr