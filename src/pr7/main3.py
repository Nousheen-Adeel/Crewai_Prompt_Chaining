import tkinter as tk
from tkinter import scrolledtext, ttk
from litellm import completion
import os
from dotenv import load_dotenv
from crewai.flow.flow import Flow, start, listen

# Load API Keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class TravelGuideBot(Flow):

    @start()
    def get_destination(self):
        """Returns selected or default travel destination."""
        return self.state.get("destination", "Hunza Valley")

    @listen(get_destination)
    def fetch_travel_info(self, destination):
        """Fetches travel guide details for the selected destination."""
        prompt = f"Give me a detailed travel guide for {destination} in Pakistan. Include places to visit, food, and best time to go."

        result = completion(
            model="gemini/gemini-1.5-pro",
            api_key=GEMINI_API_KEY,
            messages=[{"content": prompt, "role": "user"}]
        )

        self.state['travel_info'] = result['choices'][0]['message']['content']

    @listen(fetch_travel_info)
    def save_guide(self):
        """Saves the travel guide details to a file."""
        with open('travel_guide.md', 'w') as file:
            file.write(self.state['travel_info'])

def kickoff():
    """Fetches selected destination details and updates GUI."""
    selected_destination = destination_var.get()
    
    obj = TravelGuideBot()
    obj.state["destination"] = selected_destination  # Store destination
    obj.kickoff()

    # Update travel guide text
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"\n🌍 Travel Guide for {selected_destination}:\n\n{obj.state['travel_info']}\n")
    output_text.config(state=tk.DISABLED)
    output_text.yview(tk.END)

# GUI Setup
root = tk.Tk()
root.title("✈️ PAKISTAN TRAVEL GUIDE")
root.geometry("600x500")
root.configure(bg="#1E1E1E")

# Heading
tk.Label(root, text="🌍 DISCOVER PAKISTAN'S BEST TRAVEL SPOTS!", font=("Arial", 16, "bold"), fg="white", bg="#1E1E1E").pack(pady=10)

# Destination List
destinations = [
    "Hunza Valley", "Fairy Meadows", "Skardu", "Murree", "Kumrat Valley",
    "Naran", "Kaghan", "Swat Valley", "Neelum Valley", "Shogran",
    "Ratti Gali Lake", "Malam Jabba", "Gorakh Hill", "Sajikot Waterfall", "Deosai Plains",
    "Khunjerab Pass", "Hingol National Park", "Gwadar", "Ormara Beach", "Ziarat"
]

# Dropdown
destination_var = tk.StringVar()
tk.Label(root, text="SELECT TRAVEL DESTINATION:", font=("Arial", 12, "bold"), fg="white", bg="#1E1E1E").pack()
destination_dropdown = ttk.Combobox(root, textvariable=destination_var, values=destinations, font=("Arial", 12, "bold"))
destination_dropdown.pack(pady=5)
destination_dropdown.current(0)

# Fetch Button
tk.Button(root, text="📌 GET TRAVEL GUIDE", command=kickoff, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

# Output Box
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10, font=("Arial", 12, "bold"), bg="#BBDEFB", fg="black")
output_text.pack(padx=10, pady=10)
output_text.config(state=tk.DISABLED)

# Run App
root.mainloop()
