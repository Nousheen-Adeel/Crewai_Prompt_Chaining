import tkinter as tk
from tkinter import scrolledtext, ttk
from litellm import completion
import os
from dotenv import load_dotenv
from crewai.flow.flow import Flow, start, listen

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class LatestNewsBot(Flow):
    
    @start()
    def get_news_category(self):
        """Fetches a random category if none is selected."""
        categories = ["World", "Politics", "Sports", "Technology", "Business", "Entertainment", "Health"]
        return categories[0]  # Default: World News

    @listen(get_news_category)
    def fetch_latest_news(self, category):
        """Fetches the latest hot news from the world based on category."""
        prompt = f"Give me the most trending and latest news in the world related to {category}. Make it short and engaging."
        
        result = completion(
            model="gemini/gemini-1.5-pro",
            api_key=GEMINI_API_KEY,
            messages=[{"content": prompt, "role": "user"}]
        )

        news = result['choices'][0]['message']['content']
        print(news)
        self.state['latest_news'] = news

    @listen(fetch_latest_news)
    def save_news(self):
        """Saves the latest news to a file."""
        with open('latest_news.md', 'w') as file:
            file.write(self.state['latest_news'])
        return self.state['latest_news']


def kickoff():
    """Fetches the selected category and displays news in the GUI."""
    selected_category = category_var.get()
    if not selected_category:
        selected_category = "World"  # Default category

    obj = LatestNewsBot()
    result = obj.kickoff()
    
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"\n📰 {selected_category} News: {result}\n")
    output_text.config(state=tk.DISABLED)
    output_text.yview(tk.END)


# GUI setup
root = tk.Tk()
root.title("🌍 Global Hot News Chatbot")
root.geometry("550x450")
root.configure(bg="#1E1E1E")  # Dark theme

# Heading
heading_label = tk.Label(root, text="🔥 Get the Hottest Latest News!", font=("Arial", 16, "bold"), fg="white", bg="#1E1E1E")
heading_label.pack(pady=10)

# Dropdown for selecting news category
category_var = tk.StringVar()
category_label = tk.Label(root, text="Select News Category:", font=("Arial", 12), fg="white", bg="#1E1E1E")
category_label.pack()
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=["World", "Politics", "Sports", "Technology", "Business", "Entertainment", "Health"])
category_dropdown.pack(pady=5)
category_dropdown.current(0)  # Default to "World"

# Fetch News Button
fetch_button = tk.Button(root, text="📢 Get Latest News", command=kickoff, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
fetch_button.pack(pady=5)

# Output Box (Scrollable)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, font=("Arial", 12), bg="#BBDEFB", fg="black")
output_text.pack(padx=10, pady=10)
output_text.config(state=tk.DISABLED)

# Run the App
root.mainloop()
