from crewai.flow.flow import Flow, start, listen
import time
from litellm import completion

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



class CityFunFacts(Flow):
    

    @start()
    def get_fact(self):
        result=completion(
            model="gemini/gemini-1.5-flash",
            api_key=GEMINI_API_KEY,
            messages=[{"content":"return any random city name of Pakistan", "role": "user"}],
        )

        city=result['choices'][0]['message']['content']
        print(city)
        return city
        
    
    @listen(get_fact)
    def generate_fun_fact(self,city_name):
        result=completion(
        model="gemini/gemini-1.5-flash",
        api_key=API_Key,
        messages=[{"content":f"write some fun facts about the {city_name} city.", "role": "user"}]
        )

        fun_fact=result['choices'][0]['message']['content']
        print(city_name)
        self.state ['fun_fact']= fun_fact

    @listen(generate_fun_fact)
    def save_fun_fact(self):
         with open('fun_fact.md', 'w') as file:
              file.write(self.state['fun_fact'])
              return self.state['fun_fact']
         



        
def kickoff():
    obj=CityFunFacts()
    result=obj.kickoff()
    print(result)
