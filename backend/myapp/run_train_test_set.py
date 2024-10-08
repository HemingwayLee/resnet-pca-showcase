import os
import glob
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from matplotlib.font_manager import FontProperties
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

model = ResNet50(weights='imagenet')

vectors = []
results = []
for fp in glob.glob("images/*.jpg"):
    img = image.load_img(fp, target_size=(224, 224))
    
    # image.array_to_img(img).show()

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    # print('Predicted:', decode_predictions(preds, top=3)[0])

    filename, file_extension =os.path.splitext(os.path.basename(fp))
    print(filename)

    results.append({"name": filename, "vector": preds})
    vectors.append(preds[0])

    
pca = PCA(n_components=2)
X = pca.fit_transform(np.array(vectors))

# This is for train set
plt.scatter(X[:, 0], X[:, 1], color="red")

# This is for test set
for i, res in enumerate(results):
    # c = "red" if i % 2 == 0 else "blue" 
    # plt.scatter(X[i, 0], X[i, 1], color=c)
    if i % 2 == 0:
        plt.scatter(X[i, 0], X[i, 1], color="blue")

# plt.show()
plt.savefig("foo.jpg")
