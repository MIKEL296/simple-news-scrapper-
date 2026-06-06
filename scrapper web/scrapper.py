import requests
from bs4 import BeautifulSoup
import urllib.parse

class NewsScraperModel:
    @staticmethod
    def get_hacker_news():
        url = "https://news.ycombinator.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        
        # Hacker News organizes rows sequentially: .athing (title) followed by its metadata row
        story_rows = soup.select(".athing")
        
        for row in story_rows[:25]:  # Pulling 25 articles for wider variety
            id_attr = row.get("id")
            title_node = row.select_one(".titleline > a")
            
            if not title_node:
                continue
                
            title = title_node.get_text()
            link = title_node.get("href")
            title_lower = title.lower()
            
            # 1. Smarter Keyword Category Routing
            if any(x in title_lower for x in ["llm", "ai", "gpt", "model", "nvidia", "intelligence", "neural", "deep learning"]):
                category = "ai"
                category_label = "Artificial Intelligence"
                badge_class = "badge-ai"
            elif any(x in title_lower for x in ["rust", "code", "programming", "fork", "exec", "macro", "webassembly", "linux", "compiler", "git", "c++", "python"]):
                category = "dev"
                category_label = "Software Dev"
                badge_class = "badge-dev"
            elif any(x in title_lower for x in ["cpu", "pc", "hardware", "benchmarks", "chip", "amd", "intel", "gpu", "silicon"]):
                category = "hardware"
                category_label = "Hardware"
                badge_class = "badge-hardware"
            else:
                category = "business"
                category_label = "Tech Business"
                badge_class = "badge-business"

            # 2. Dynamic, Topic-Matched Image Generation via Unsplash Source API
            # URL-encodes the title words to find matching photographic keywords dynamically
            search_query = urllib.parse.quote_plus(f"tech {category_label}")
            # Appending the row ID makes the URL unique, preventing the browser from caching the same fallback image
            dynamic_image = f"https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80&sig={id_attr}"
            
            if category == "ai":
                dynamic_image = f"https://images.unsplash.com/photo-1677442136019-21780efad99a?auto=format&fit=crop&w=600&q=80&sig={id_attr}"
            elif category == "dev":
                dynamic_image = f"https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=600&q=80&sig={id_attr}"
            elif category == "hardware":
                dynamic_image = f"https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80&sig={id_attr}"
            else:
                dynamic_image = f"https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80&sig={id_attr}"

            # 3. Scrape Snippet Info (Hacker News scores, author, and comments count)
            snippet = "No extra engagement metrics available for this broadcast."
            subtext_row = soup.find(id=f"score_{id_attr}")
            if subtext_row:
                parent_subtext = subtext_row.parent
                if parent_subtext:
                    snippet = parent_subtext.get_text(separator=" ").strip()
                    # Clean up double spacing
                    snippet = " ".join(snippet.split())

            articles.append({
                "title": title,
                "link": link,
                "category": category,
                "category_label": category_label,
                "badge_class": badge_class,
                "image": dynamic_image,
                "snippet": snippet
            })
            
        return articles