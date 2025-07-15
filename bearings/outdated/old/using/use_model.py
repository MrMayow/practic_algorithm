import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib  # Для загрузки scaler'а

# === 1. Загрузка новых данных ===
new_df = pd.read_csv("test_ball_defect.csv")  # только колонка 'vibration'
vibration = new_df['vibration'].values
print(vibration)
# === 2. Формирование окон (200 точек каждое) ===
window_size = 200
X_new = []
for i in range(0, len(vibration) - window_size, window_size):
    window = vibration[i:i+window_size]
    X_new.append(window)

X_new = np.array(X_new)  # (samples, 200)

# === 3. Загрузка scaler'а и нормализация ===
scaler = joblib.load("scaler.save")  # тот же, что использовался при обучении
X_new = scaler.transform(X_new)

# === 4. Преобразование формы ===
X_new = X_new.reshape((X_new.shape[0], X_new.shape[1], 1))

# === 5. Загрузка модели ===

from tensorflow.keras.models import load_model
model = load_model("bearing_fault_model.h5")

# === 6. Предсказание ===
predictions = model.predict(X_new)

# === 7. Интерпретация ===
for i, p in enumerate(predictions):
    result = "DEFECT" if p >= 0.5 else "NO DEFECT"
    print(f"Window {i}: {result} (Confidence: {p[0]:.2f})")
