import torch
import torch.nn as nn
import joblib

# Định nghĩa lớp MLP
class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return out

# Hàm để tải mô hình đã lưu
def load_model(model_path, input_size=6, hidden_size=64, num_classes=2):
    model = MLP(input_size, hidden_size, num_classes)
    model.load_state_dict(torch.load(model_path, weights_only=True))  # Sử dụng weights_only=True
    model.eval()
    return model

# Hàm để tải scaler
def load_scaler(scaler_path):
    return joblib.load(scaler_path)
