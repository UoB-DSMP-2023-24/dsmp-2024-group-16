import numpy as np
import pandas as pd
from arch import arch_model

# 加载数据
data = pd.read_csv('Tapes/Tape.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 计算日对数收益率
data['log_return'] = np.log(data['Close'] / data['Close'].shift(1))

# 删除任何NaN值
data = data.dropna()

# 指定GARCH模型
am = arch_model(data['log_return'], vol='Garch', p=1, q=1)

# 拟合模型
res = am.fit(update_freq=5)

# 显示拟合结果
print(res.summary())

# 预测未来的波动率
forecasts = res.forecast(horizon=30)
print(forecasts.variance[-1:])  # 输出最后一天的5天波动率预测

# 假设 'res' 是您的GARCH模型的拟合结果
summary_str = res.summary().as_text()
forecasts_str = str(res.forecast(horizon=30).variance.iloc[-1])

# 将结果整合到一个字符串中
export_text = summary_str + "\n\nForecasts:\n" + forecasts_str

# 指定导出的文件路径
output_file_path = 'GARCH_Model_Results.txt'

# 写入到txt文件
with open(output_file_path, 'w') as file:
    file.write(export_text)

print(f'Results saved to {output_file_path}')

