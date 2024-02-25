import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("./datasets/programming languages.csv")
data["Date"] = pd.to_datetime(data["Date"])

plt.figure(figsize=(14, 8))
# for col in data:
#     if col == 'Date':
#         continue
#     plt.plot(data["Date"], data[col], label=col)
plt.plot(data["Date"], data["Rust"], label="Rust")
# plt.plot(data["Date"], data["Python"], label="Python")
# plt.plot(data["Date"], data["JavaScript"], label="JavaScript")
# plt.plot(data["Date"], data["Java"], label="Java")
plt.legend()
plt.title("Popularity of languages")
plt.xlabel("Year")
plt.ylabel("Mean popularity in %")
plt.show()
# print(data["Date"].iloc[0], data["Date"].iloc[-1])