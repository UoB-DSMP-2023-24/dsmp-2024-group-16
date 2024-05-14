import numpy as np
import pandas as pd
from arch import arch_model

# 加载数据
data = pd.read_csv('Tapes\Tape.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
data['log_return'] = np.log(data['Close'] / data['Close'].shift(1))
data.dropna(inplace=True)

# 使用AIC和BIC信息准则来选择最佳的p和q值
best_aic = np.inf
best_bic = np.inf
best_order = (0, 0)
best_model = None

# 考虑的p和q范围
p_range = range(1, 4)  # p从1到3
q_range = range(1, 4)  # q从1到3

for p in p_range:
    for q in q_range:
        try:
            model = arch_model(data['log_return'], p=p, q=q, vol='Garch')
            model_fit = model.fit(disp='off')
            aic = model_fit.aic
            bic = model_fit.bic

            # 检查是否是更好的模型（更低的AIC或BIC）
            if aic < best_aic:
                best_aic = aic
                best_order = (p, q)
                best_model = model_fit

            if bic < best_bic:
                best_bic = bic
                best_order = (p, q)
                best_model = model_fit

        except Exception as e:
            print(f"Failed to fit GARCH({p},{q}) model: {str(e)}")

# 输出最佳模型的结果
print(f"Best Model Order: p={best_order[0]}, q={best_order[1]}")
print(best_model.summary())
