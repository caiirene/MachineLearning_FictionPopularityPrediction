# Predictive Machine Learning Model for Online Fiction Clicks

## Project Overview
This project develops a machine learning model to predict the click rates of online novels. Our final model is documented in the Jupyter Notebook titled `CleanJinjiangModel.ipynb`.

## Key Performance Metrics
The model's performance was evaluated using k-fold cross-validation, resulting in the following metrics:
- **Average Mean Squared Error (MSE)**: 8,404,515.651321704
- **Average R²**: 0.8357806345931185

## Important Files
1. **JinjiangBooks.csv**: Raw data scraped from the Jinjiang website, containing information on 15,500 books.
2. **QidianBooks.csv**: Raw data scraped from the Qidian website, including details on 1,000 books.
3. **processed_data.csv**: Preprocessed data from Jinjiang, ready for model training.
4. **CleanJinjiangModel.ipynb**: Notebook containing the final model's training process. To retrieve data for the report's tables, run the code blocks in this notebook.
5. **JinjiangModel.ipynb**: Comprehensive notebook with all code used for data analysis and model building. The content is extensive and unstructured, but it provides a complete overview of the project's methodology.

## Final Model Training
The final model training process can be found in the second to last code block of `CleanJinjiangModel.ipynb`.

## Usage
To work with this project, clone the repository and ensure you have Jupyter Notebook installed. Open `CleanJinjiangModel.ipynb` to access the finalized training procedures and `JinjiangModel.ipynb` for a more detailed exploration of the data and preliminary modeling steps.

