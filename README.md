# Viable_tumor_cell_density
# Step_1 Prepare images
Place your pathology images in the directory data/σ=6/xxx=test/xxx/ori

Place your ground truth images in the directory data/σ=6/xxx=test/xxx/likeli

# Step_2 Model training
Please open the model_train.ipynb, and run the cell sequentially.
Then, the training of the model begins, and the weights are stored when the F-measure for the validation data is best.

※The weights of our results are available in the release section. 
Please download the file best_F_xxx.pth and place it in the directory data/σ=6/xxx=test/weight_F/nuclei_sarcoma.

# Step_2 Model evaluation
Please open the prediction.ipynb, and run the cell sequentially.
Then, the detection performance of the model is evaluated.
