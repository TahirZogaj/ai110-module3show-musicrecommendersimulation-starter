# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge holding a scorecard. The user describes their taste with four answers: their favorite genre, their favorite mood, how energetic they want the music to be (on a scale from 0 to 1), and whether they like acoustic sounds.

The judge then looks at every song in the catalog, one at a time, and hands out points:

- **Same genre as the user's favorite:** 2 points. This is the biggest reward, because genre is the clearest sign of "this is my kind of music."
- **Same mood as the user's favorite:** 1 point.
- **Energy close to what the user wants:** up to 1 point. A perfect match earns the full point, and the further away the song's energy is, the fewer points it gets. A calm-music fan isn't rewarded for loud songs just because they are loud; what matters is being *close* to the target.
- **Acoustic sound that fits the user's preference:** up to half a point. If the user likes acoustic music, more acoustic songs earn more; if not, less acoustic songs earn more.

A perfect song scores 4.5. While handing out points, the judge also writes down *why* (for example, "genre match +2.0"), so every recommendation comes with an explanation.

Once every song has a score, the songs are lined up from highest to lowest, and the top five become the recommendations.

**Changes from the starter logic:** the starter code returned the first few songs in the file without judging them. I added the point system above, the energy-closeness rule, the acoustic preference, and the written reasons. Tempo, danceability and valence are loaded but not scored: in this dataset tempo and danceability rise and fall with energy, so counting them would reward the same thing several times.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
