from flask import Flask, jsonify
from flask_cors import CORS
from qiskit_machine_learning.datasets import ad_hoc_data
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

# Uncomment below for local dev
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/test', methods=['GET'])
def test():
    adhoc_dimension = 2
    train_features, train_labels, test_features, test_labels, adhoc_total = ad_hoc_data(
        training_size=20,
        test_size=5,
        n=adhoc_dimension,
        gap=0.3,
        plot_data=False,
        one_hot=False,
        include_sample_total=True,
    )

    # Generate the plot, display it locally, and capture it as a base64 encoded PNG image
    image_base64 = plot_dataset(train_features, train_labels, test_features, test_labels, adhoc_total)
    
    # Detailed explanation for the user about the dataset and model
    explanation = (
        "In this experiment, we are using an ad hoc dataset consisting of two classes in a 2D space. "
        "The dataset is generated using Qiskit’s ad_hoc_data function. In a typical quantum machine learning workflow, "
        "we would build a quantum classifier (using, for example, a variational quantum circuit) to separate these classes. "
        "Here, the plot shows the training data (blue squares and red circles) and the testing data (colored points with contrasting outlines) "
        "over a background that represents the entire dataset. "
        "This visualization helps us understand how the quantum model would be trained and how it might generalize to new data."
    )
    
    return jsonify({
        "message": explanation,
        "plot_image": image_base64
    })

def plot_features(ax, features, labels, class_label, marker, face, edge, label):
    ax.scatter(
        features[np.where(labels[:] == class_label), 0],
        features[np.where(labels[:] == class_label), 1],
        marker=marker,
        facecolors=face,
        edgecolors=edge,
        label=label,
    )

def plot_dataset(train_features, train_labels, test_features, test_labels, adhoc_total):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_ylim(0, 2 * np.pi)
    ax.set_xlim(0, 2 * np.pi)
    
    # Plot the background heatmap using adhoc_total
    ax.imshow(
        np.asmatrix(adhoc_total).T,
        interpolation="nearest",
        origin="lower",
        cmap="RdBu",
        extent=[0, 2 * np.pi, 0, 2 * np.pi],
    )
    
    # Plot training and testing features for both classes
    plot_features(ax, train_features, train_labels, 0, "s", "w", "b", "A train")
    plot_features(ax, train_features, train_labels, 1, "o", "w", "r", "B train")
    plot_features(ax, test_features, test_labels, 0, "s", "b", "w", "A test")
    plot_features(ax, test_features, test_labels, 1, "o", "r", "w", "B test")
    
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    ax.set_title("Ad hoc dataset")
    
    # Show the plot locally (this will open a window with the plot)
    plt.show()
    
    # After closing the plot window, save the figure to an in-memory buffer
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    
    # Encode the image in base64 for returning in the JSON response
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the figure to free up resources
    return img_base64

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
