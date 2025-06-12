# 🌿♻️🍱 Image Classifier: Plant / Waste / Food

A multi-domain image classification project powered by Convolutional Neural Networks (CNN) and TensorFlow/Keras. This app can classify images into one of three categories:

- 🌿 Plant (e.g., poisonous vs. non-poisonous)
- ♻️ Waste (e.g., organic, recyclable, hazardous)
- 🍱 Food (e.g., healthy vs. unhealthy)

The model is deployed with a clean, interactive UI using **Streamlit**, making it accessible for both educational and practical uses.

---

## 🚀 Features

- 📸 Upload any image to get instant predictions
- 🧠 Trained on CNN using TensorFlow/Keras
- 🌐 Web-based interface built with Streamlit
- 📊 Simple and extensible multi-class output
- 🤝 Open-source and beginner-friendly code structure

---

## 📁 Project Structure
1. **Structure**
   ```bash
   image-classifier/
   ├── data/ # Training/validation datasets (organized per class)
   ├── models/ # Trained model files (saved in HDF5/TF format)
   ├── notebooks/ # Jupyter Notebooks for EDA and model training
   ├── streamlit_app/ # Streamlit app files
   │ ├── app.py
   │ └── utils.py
   ├── requirements.txt
   └── README.md
   
---

## 🔧 Tech Stack

- **Python 3.10+**
- **TensorFlow / Keras** for image classification
- **Streamlit** for building the web app
- **Pandas & NumPy** for data handling
- **Matplotlib / Seaborn** for visualizations

---

## 🧪 Dataset

The dataset should be organized into separate folders for each category under the `data/` directory, e.g.:

1. **Structure on data**
   ```bash
   data/
   ├── plant/
   │ ├── poisonous/
   │ └── non_poisonous/
   ├── waste/
   │ ├── organic/
   │ ├── recyclable/
   │ └── hazardous/
   ├── food/
   │ ├── healthy/
   │ └── unhealthy/

You can use or adapt publicly available datasets like:
- [Kaggle Plant Seedlings](https://www.kaggle.com/c/plant-seedlings-classification)
- [Garbage Classification](https://www.kaggle.com/datasets/mostafaabla/garbage-classification)
- [Food-101](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/)

---

## 🖥️ How to Run the App Locally

1. **Clone this repository**
   ```bash
   [git clone https://github.com/yourusername/image-classifier.git](https://github.com/rhaffle87/AI-Garbage-Classifier.git)
   cd image-classifier
   
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
3. **Clone this repository**
   ```bash
   python notebooks/train_model.py

4. **Clone this repository**
   ```bash
   streamlit run streamlit_app/app.py

## 🔧 Output
| Input Image                                | Prediction         |
| ------------------------------------------ | ------------------ |
| ![sample](https://via.placeholder.com/100) | `Recyclable Waste` |
| ![sample](https://via.placeholder.com/100) | `Unhealthy Food`   |
| ![sample](https://via.placeholder.com/100) | `Poisonous Plant`  |

## 🤝 Contributing
We welcome contributions! Whether you're fixing bugs, improving performance, or adding new categories—your help is appreciated.
1. Fork this repo
2. Create your feature branch (git checkout -b feature/new-class)
3. Commit your changes (git commit -am 'Add new classifier')
4. Push to the branch (git push origin feature/new-class)
5. Open a Pull Request

## 📚 Related Repositories
- 🔗 davidsandberg/facenet – image embeddings
- 🔗 MLH-Fellowship/plant-disease-detector – plant disease detection

## ✨ Acknowledgements
- TensorFlow/Keras Documentation
- Streamlit Community
- Open datasets from Kaggle and UCI
