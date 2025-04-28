import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pickle

# Load cleaned data
df = pd.read_csv(r'L:\Guvi\Project 4\cleaned_data.csv')

# Label Encode 'name'
name_encoder = LabelEncoder()
df['name_encoded'] = name_encoder.fit_transform(df['name'])

# Save the Label Encoder
with open('name_encoder.pkl', 'wb') as file:
    pickle.dump(name_encoder, file)

# One-Hot Encode 'city' and 'cuisine'
categorical_cols = ['city', 'cuisine']
ohe_encoder = OneHotEncoder(sparse_output=False)

encoded_features = ohe_encoder.fit_transform(df[categorical_cols])

# Create DataFrame for One-Hot encoded features
encoded_df = pd.DataFrame(encoded_features, columns=ohe_encoder.get_feature_names_out(categorical_cols))

# Drop original 'name', 'city', 'cuisine'
df_encoded = df.drop(columns=['name', 'city', 'cuisine'])

# Combine everything
final_encoded_df = pd.concat([df_encoded.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

# Save One-Hot Encoder
with open('encoder.pkl', 'wb') as file:
    pickle.dump(ohe_encoder, file)

# Save final encoded data
final_encoded_df.to_csv('encoded_data.csv', index=False)

print("Completed encoding process")
