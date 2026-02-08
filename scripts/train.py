
import os
import argparse
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

from src import config
from src.data.loader import load_dataset_metadata, data_generator
from src.models.cnn_lstm import build_enhanced_inception_lstm_model

def train(args):
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load Metadata
    print("Loading metadata...")
    train_df = load_dataset_metadata(config.TRAIN_CSV, max_samples=args.max_samples)
    val_df = load_dataset_metadata(config.VAL_CSV, max_samples=args.max_samples)
    
    # Generators
    print("Creating data generators...")
    train_gen = data_generator(
        train_df, 
        config.TRAIN_DIR, 
        config.BATCH_SIZE, 
        config.SEQ_LENGTH, 
        config.IMG_SIZE, 
        config.NUM_CLASSES,
        use_mediapipe=args.use_mediapipe
    )
    
    val_gen = data_generator(
        val_df, 
        config.VAL_DIR, 
        config.BATCH_SIZE, 
        config.SEQ_LENGTH, 
        config.IMG_SIZE, 
        config.NUM_CLASSES,
        use_mediapipe=args.use_mediapipe
    )
    
    # Model
    print("Building model...")
    model = build_enhanced_inception_lstm_model(
        config.NUM_CLASSES, 
        config.SEQ_LENGTH, 
        config.IMG_SIZE
    )
    
    if args.summary:
        model.summary()
        
    # Callbacks
    checkpoint_path = os.path.join(args.output_dir, "best_model.keras")
    callbacks = [
        ModelCheckpoint(checkpoint_path, monitor='val_accuracy', save_best_only=True, verbose=1),
        EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True, verbose=1)
    ]
    
    # Train
    print("Starting training...")
    steps_per_epoch = len(train_df) // config.BATCH_SIZE
    validation_steps = len(val_df) // config.BATCH_SIZE
    
    history = model.fit(
        train_gen,
        steps_per_epoch=steps_per_epoch,
        validation_data=val_gen,
        validation_steps=validation_steps,
        epochs=args.epochs,
        callbacks=callbacks
    )
    
    # Save final
    final_path = os.path.join(args.output_dir, "final_model.h5")
    model.save(final_path)
    print(f"Training complete. Model saved to {final_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Gesture Recognition Model")
    parser.add_argument("--epochs", type=int, default=config.EPOCHS, help="Number of epochs")
    parser.add_argument("--output_dir", type=str, default="outputs", help="Output directory")
    parser.add_argument("--max_samples", type=int, default=None, help="Limit samples for debugging")
    parser.add_argument("--use_mediapipe", action="store_true", help="Use MediaPipe for hand ROI")
    parser.add_argument("--summary", action="store_true", help="Show model summary")
    
    args = parser.parse_args()
    train(args)
