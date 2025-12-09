# import sklearn as sk
# import numpy as np
# fruit_label	fruit_name	fruit_subtype	mass	width	height	color_score

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
def getData():
    data_fruit = pd.read_csv(r"fruit_data_with_colors.txt", sep='\t')
    data = data_fruit[['mass', 'width', 'height', 'color_score']]
    target = data_fruit['fruit_name']
    
    x_train, x_test, y_train, y_test = train_test_split(
        data, target,
        test_size=0.3,
        random_state=42,
        shuffle=True,
        stratify=target
    )
    teeData = {
        'mass': [192, 200],
        'width': [8.4, 7.3],
        'height': [7.3, 10.5],
        'color_score': [0.55, 0.72]
    }
    tee = pd.DataFrame(teeData)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(x_train)
    tee_scaled = scaler.transform(tee)
    target_scaled = scaler.transform(x_test)
    
    knnVar = KNeighborsClassifier(n_neighbors=5)
    knnVar.fit(data_scaled, y_train)
    
    result = knnVar.predict(target_scaled)
    teeResult = knnVar.predict(tee_scaled)
    accuracy = knnVar.score(target_scaled, y_test)
    
    print(f"预测结果：{result}\n精确率：{accuracy}\ntee预测结果：{teeResult}")
if __name__ == "__main__":
    getData()