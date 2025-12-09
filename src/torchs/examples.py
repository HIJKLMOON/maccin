import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import ToTensor # 图像转张量
from torchvision.datasets import MNIST # 内置数据集

from pathlib import Path

root_path = Path(__file__).parent / "dataset"

train_dataset = MNIST(root=root_path, train=True, transform=ToTensor(), download=True)
test_dataset = MNIST(root=root_path, train=False, transform=ToTensor(), download=True)

train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        # 1. 定义层：全连接层（Linear(in_features, out_features)）
        self.fc1 = nn.Linear(784, 256)  # 输入层→隐藏层1
        self.fc2 = nn.Linear(256, 128)  # 隐藏层1→隐藏层2
        self.fc3 = nn.Linear(128, 10)   # 隐藏层2→输出层（10类）
        # 2. 激活函数：引入非线性（如ReLU）
        self.relu = nn.ReLU()

    def forward(self, x):
        # 定义前向传播：数据流经各层的顺序
        x = x.view(-1, 784)  # 展平图像：(batch_size, 1, 28, 28) → (batch_size, 784)
        x = self.relu(self.fc1(x))  # 隐藏层1 + 激活
        x = self.relu(self.fc2(x))  # 隐藏层2 + 激活
        x = self.fc3(x)  # 输出层（无需激活，损失函数会处理）
        return x

# 1. 初始化网络（若有GPU可移至GPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNet().to(device)

# 2. 损失函数：分类任务用交叉熵损失
criterion = nn.CrossEntropyLoss()

# 3. 优化器：用Adam优化，学习率lr=0.001
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 5  # 训练轮次（遍历全部数据的次数）

for epoch in range(num_epochs):
    model.train()  # 切换为训练模式（启用Dropout、BatchNorm等）
    running_loss = 0.0  # 记录本轮损失
    
    # 遍历训练集的每个批次
    for i, (images, labels) in enumerate(train_loader):
        # 数据移至GPU/CPU
        images, labels = images.to(device), labels.to(device)
        
        # 前向传播：计算模型预测值
        outputs = model(images)
        
        # 计算损失：预测值与真实标签的差距
        loss = criterion(outputs, labels)
        
        # 反向传播+参数更新：
        optimizer.zero_grad()  # 清空上一轮梯度（避免累积）
        loss.backward()        # 反向传播计算梯度
        optimizer.step()       # 优化器更新网络参数
        
        # 累计损失
        running_loss += loss.item() * images.size(0)
    
    # 计算本轮平均损失
    epoch_loss = running_loss / len(train_dataset)
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}')

model.eval()  # 切换为评估模式（禁用Dropout、固定BatchNorm）
correct = 0
total = 0

# 测试时不计算梯度（节省内存、加速）
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)  # 取预测概率最大的类别
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

# 计算测试准确率
accuracy = 100 * correct / total
print(f'Test Accuracy: {accuracy:.2f}%')
    