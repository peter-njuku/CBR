# Basic CBR System with no imports

# Store cases in a file
DATABASE_FILE = "cases.txt"

# Levenshtein Distance for string similarity (no imports)
def levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0 for _ in range(len_s2 + 1)] for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        for j in range(len_s2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[len_s1][len_s2]

# Load cases from the database file
def load_cases():
    cases = []
    try:
        with open(DATABASE_FILE, "r") as file:
            for line in file:
                symptoms, disease, treatment = line.strip().split("|")
                cases.append({"symptoms": symptoms, "disease": disease, "treatment": treatment})
    except FileNotFoundError:
        pass
    return cases

# Save a new case to the database
def save_case(symptoms, disease, treatment):
    with open(DATABASE_FILE, "a") as file:
        file.write(f"{symptoms}|{disease}|{treatment}\n")

# Find the most similar case
def find_most_similar_case(user_symptoms, cases):
    best_match = None
    best_distance = float("inf")

    for case in cases:
        distance = levenshtein_distance(user_symptoms, case["symptoms"])
        if distance < best_distance:
            best_distance = distance
            best_match = case

    return best_match, best_distance

# Menu system
def menu():
    while True:
        print("\n=== Case-Based Reasoning (CBR) System ===")
        print("1. Add a new case")
        print("2. Query for a similar case")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            symptoms = input("Enter symptoms: ").strip()
            disease = input("Enter diagnosed disease: ").strip()
            treatment = input("Enter recommended treatment: ").strip()
            save_case(symptoms, disease, treatment)
            print("Case added successfully!")
        elif choice == "2":
            user_symptoms = input("Enter symptoms to query: ").strip()
            cases = load_cases()
            if not cases:
                print("No cases in the database. Add cases first!")
            else:
                best_match, distance = find_most_similar_case(user_symptoms, cases)
                if best_match:
                    print("\n--- Most Similar Case ---")
                    print(f"Symptoms: {best_match['symptoms']}")
                    print(f"Disease: {best_match['disease']}")
                    print(f"Treatment: {best_match['treatment']}")
                    print(f"Similarity (Edit Distance): {distance}")
                else:
                    print("No similar cases found.")
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    menu()
