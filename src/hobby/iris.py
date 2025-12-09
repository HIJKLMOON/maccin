# 鸢尾花种类分类机器学习项目
# 目标：根据花萼长度、花萼宽度、花瓣长度、花瓣宽度预测鸢尾花的种类

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 1. 加载数据集
def load_data():
    """加载鸢尾花数据集并转换为DataFrame"""
    iris = load_iris()
    # 创建DataFrame
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['species'] = iris.target
    # 将数字标签转换为花的名称
    df['species_names'] = df['species'].apply(lambda x: iris.target_names[x])
    return df, iris

# 2. 数据探索与可视化
def explore_data(df):
    # """探索数据集的基本信息和分布"""
    # print("数据集基本信息：")
    # print(df.info())
    # print("\n数据集统计描述：")
    # print(df.describe())
    # print("\n各类别数量分布：")
    # print(df['species_names'].value_counts())
    
    # 绘制特征两两之间的散点图
    plt.figure(figsize=(12, 8))
    sns.pairplot(df, hue='species_names', markers=['o', 's', 'D'])
    plt.suptitle('鸢尾花特征两两散点图', y=1.02)
    plt.show()
    
    # 绘制箱线图查看特征分布
    plt.figure(figsize=(12, 6))
    for i, column in enumerate(df.columns[:4]):
        plt.subplot(2, 2, i+1)
        sns.boxplot(x='species_names', y=column, data=df)
        plt.title(f'{column}在不同种类中的分布')
    plt.tight_layout()
    plt.show()

# 3. 数据预处理
def preprocess_data(df, iris):
    # """准备训练和测试数据"""
    # 特征和标签
    X = df[iris.feature_names]  # 特征：花萼长度、花萼宽度、花瓣长度、花瓣宽度
    y = df['species']           # 标签：0, 1, 2 分别代表三种鸢尾花
    
    # 划分训练集和测试集（70%训练，30%测试）
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # 特征标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

# 4. 模型训练与评估
def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    # """训练多种分类模型并评估性能"""
    # 定义要使用的模型
    models = {
        'K近邻分类器': KNeighborsClassifier(n_neighbors=5),
        '支持向量机': SVC(kernel='rbf', gamma='scale'),
        '决策树': DecisionTreeClassifier(max_depth=3, random_state=42),
        '随机森林': RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    # 训练并评估每个模型
    results = {}
    for name, model in models.items():
        print(f"\n----- {name} -----")
        
        # 训练模型
        model.fit(X_train, y_train)
        
        # 预测
        y_pred = model.predict(X_test)
        
        # 评估
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = accuracy
        print(f"准确率: {accuracy:.4f}")
        
        # 混淆矩阵
        print("\n混淆矩阵:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        # 分类报告
        print("\n分类报告:")
        print(classification_report(y_test, y_pred))
        
        # 交叉验证
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        print(f"交叉验证准确率: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    # 比较所有模型的准确率
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), results.values())
    plt.ylim(0.8, 1.0)
    plt.title('不同模型的准确率比较')
    plt.ylabel('准确率')
    for i, v in enumerate(results.values()):
        plt.text(i, v + 0.01, f'{v:.4f}', ha='center')
    plt.show()
    
    # 返回表现最好的模型
    best_model_name = max(results, key=results.get)
    best_model = models[best_model_name]
    print(f"\n表现最好的模型是: {best_model_name}, 准确率: {results[best_model_name]:.4f}")
    
    return best_model

# 5. 使用最佳模型进行预测
def predict_new_samples(best_model, scaler, iris):
    """使用训练好的最佳模型预测新样本"""
    print("\n----- 新样本预测 -----")
    # 定义新样本 (花萼长度, 花萼宽度, 花瓣长度, 花瓣宽度)
    new_samples = [
        [5.1, 3.5, 1.4, 0.2],  # 预期是山鸢尾(setosa)
        [6.2, 2.9, 4.3, 1.3],  # 预期是变色鸢尾(versicolor)
        [7.3, 2.9, 6.3, 1.8]   # 预期是维吉尼亚鸢尾(virginica)
    ]
    
    # 对新样本进行标准化
    new_samples_scaled = scaler.transform(new_samples)
    
    # 预测
    predictions = best_model.predict(new_samples_scaled)
    prediction_names = [iris.target_names[p] for p in predictions]
    
    # 显示结果
    for sample, name in zip(new_samples, prediction_names):
        print(f"样本 {sample} 预测为: {name}")

# 主函数
def main():
    # 加载数据
    df, iris = load_data()
    
    # 数据探索
    explore_data(df)
    
    # 数据预处理
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df, iris)
    
    # 模型训练与评估
    best_model = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # 预测新样本
    predict_new_samples(best_model, scaler, iris)

if __name__ == "__main__":
    main()
    