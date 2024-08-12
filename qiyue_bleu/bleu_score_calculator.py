import pandas as pd
import sacrebleu

# Load the CSV file
result_df = pd.read_csv('C:/Users/Qiyue/OneDrive/桌面/测评/result.csv', encoding='ISO-8859-1')

# Load the Excel file
test_df = pd.read_excel('C:/Users/Qiyue/OneDrive/桌面/测评/test 1.xlsx', sheet_name=0)

# Handle potential NaN values in the datasets
result_df['SageMaker Result'] = result_df['SageMaker Result'].fillna('')
test_df['referral_content'] = test_df['referral_content'].fillna('')

# Calculate BLEU scores
bleu_scores = []
for i in range(len(result_df)):
    candidate = result_df.loc[i, "SageMaker Result"]
    reference = test_df.loc[i, "referral_content"]
    score = sacrebleu.sentence_bleu(candidate, [reference])
    bleu_scores.append(score.score)

# Create a DataFrame to display the results
bleu_df = pd.DataFrame({
    "Filename": result_df["Filename"],
    "BLEU Score": bleu_scores
})

# Print the DataFrame
print(bleu_df)

# Save the DataFrame to a CSV file
bleu_df.to_csv('C:/Users/Qiyue/OneDrive/桌面/测评/bleu_scores.csv', index=False)