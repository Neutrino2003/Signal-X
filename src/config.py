
import os

# Data Constants
SEQ_LENGTH = 16
IMG_HEIGHT = 90
IMG_WIDTH = 75
IMG_SIZE = (IMG_HEIGHT, IMG_WIDTH)
BATCH_SIZE = 16
NUM_CLASSES = 27

# Paths
# Defaulting to the path found in the legacy notebook, but this should be updated by the user
DATASET_ROOT = "/mnt/MainDrive/Codes/Deep Learning/Gesture_control/3D_CNN+Lstm/archive_2"
TRAIN_DIR = os.path.join(DATASET_ROOT, "Train")
VAL_DIR = os.path.join(DATASET_ROOT, "Validation")
TEST_DIR = os.path.join(DATASET_ROOT, "Test")

TRAIN_CSV = os.path.join(DATASET_ROOT, "Train.csv")
VAL_CSV = os.path.join(DATASET_ROOT, "Validation.csv")
TEST_CSV = os.path.join(DATASET_ROOT, "Test.csv")

# Training Constants
EPOCHS = 20
LEARNING_RATE = 0.0001
