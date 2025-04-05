import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

# Створення нейромережі для бінарної класифікації
model_classification = Sequential([
    Dense(64, activation='relu', input_shape=(10,)),  # Вхідний шар
    Dense(32, activation='relu'),                     # Прихований шар
    Dense(1, activation='sigmoid')                    # Вихідний шар (бінарна класифікація)
])

# Компільовуємо модель
model_classification.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Виведення структури моделі
model_classification.summary()
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Генерація синтетичних даних
X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Навчання нейромережі класифікації
model_classification.fit(X_train, y_train, epochs=20, batch_size=10, validation_data=(X_test, y_test))

# Оцінка результатів
loss, accuracy = model_classification.evaluate(X_test, y_test)
print(f"Точність моделі класифікації: {accuracy:.2f}")

# Приклад зміни оптимізатора:
# model_classification.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])

# ===== Приклад моделі LSTM для регресії =====

# Побудова моделі LSTM для регресії
model_regression = Sequential([
    LSTM(50, activation='relu', return_sequences=True, input_shape=(10, 1)),
    LSTM(50, activation='relu'),
    Dense(1)
])

# Компільовуємо модель регресії
model_regression.compile(optimizer='adam', loss='mse')

# Підготовка даних для LSTM (потрібно змінити форму даних)
X_train_reshaped = X_train.reshape(-1, 10, 1)

# Навчання моделі регресії
# model_regression.fit(X_train_reshaped, y_train, epochs=20, batch_size=16)
# Закоментовано, щоб не виконувати обидві моделі одночасно