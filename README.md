# AI-Powered Search Bar with Django

Welcome to the **AI-Powered Search Bar** project! This repository contains a Django-based web application that integrates advanced AI functionalities to provide dynamic search capabilities and intelligent recommendations. Leveraging a combination of modern frontend and backend technologies, this project showcases how to build a feature-rich search interface enhanced by AI assistants.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [AI Assistants](#ai-assistants)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Dynamic Search Interface:** Real-time search with instant results using HTMX.
- **AI-Powered Recommendations:** Intelligent shoe recommendations based on user queries.
- **Interactive Chat with Database:** Conversational AI that interacts with the shoe database for detailed information.
- **Responsive UI:** Modern and responsive design using TailwindCSS and DaisyUI.
- **Markdown Support:** Rich text descriptions and AI responses rendered in Markdown.
- **Secure Input Handling:** Sanitization of user inputs to prevent security vulnerabilities.

## Technologies Used

### Frontend

- **HTMX:** [htmx.org](https://htmx.org/) for dynamic HTML interactions.
- **Hyperscript:** [hyperscript.org](https://hyperscript.org/) for enhanced frontend scripting.
- **TailwindCSS:** [Tailwind CSS](https://tailwindcss.com/) for utility-first CSS styling.
- **DaisyUI:** [daisyui.com](https://daisyui.com/) for TailwindCSS components.
- **MDEditor:** [django-mdeditor](https://github.com/pylixm/django-mdeditor) for Markdown editing.

### Backend

- **Django:** [Django](https://www.djangoproject.com/) as the primary web framework.
- **Django AI Assistant:** [django-ai-assistant](https://pypi.org/project/django-ai-assistant/) for integrating AI functionalities.
- **Langchain:** [langchain-core](https://pypi.org/project/langchain-core/) and [langchain-community](https://pypi.org/project/langchain-community/) for AI workflows.
- **Bleach:** [bleach](https://pypi.org/project/bleach/) for sanitizing user inputs.
- **Markdownify:** [django-markdownify](https://pypi.org/project/django-markdownify/) for rendering Markdown content.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.8+**
- **Node.js and npm** (for managing frontend dependencies)
- **Git** installed on your machine

## Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-search-bar.git
cd ai-search-bar
```

### 2. Set Up Virtual Environment

Create and activate a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

- **Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

### 3. Install Python Dependencies

Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

**Note:** Ensure `requirements.txt` includes all necessary packages:

```plaintext
django
django-htmx
django-ai-assistant
bleach
django-tailwind
daisyui
django-mdeditor
langchain-core
langchain-community
django-markdownify
scikit-learn
```

### 4. Install Frontend Dependencies

Navigate to the TailwindCSS directory and install Node.js dependencies.

```bash
cd theme/static/static_src/
npm install
npm install -D daisyui@latest
```

### 5. Configure TailwindCSS

Ensure `tailwind.config.js` is set up correctly with DaisyUI plugins.

```js
module.exports = {
  content: [
    // Add paths to your templates and static files
    "../**/templates/**/*.html",
    "./**/*.js",
  ],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('daisyui'),
  ],
}
```

### 6. Apply Migrations

Set up the database by running migrations.

```bash
cd ../../../
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

Create a superuser account to access the Django admin interface.

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials.

### 8. Collect Static Files

Collect static files for production.

```bash
python manage.py collectstatic
```

## Configuration

### Environment Variables

Create a `.env` file in the project root to manage environment-specific settings. Include any necessary API keys or secret settings.

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Django Settings

Ensure `settings.py` includes all necessary configurations:

- **Installed Apps:**

  ```python
  INSTALLED_APPS = [
      # ... other installed apps
      'django.contrib.staticfiles',
      'tailwind',
      'theme',
      'search_app',
      'django_ai_assistant',
      'mdeditor',
      'markdownify',
      'django_htmx',
  ]
  ```

- **Templates Directory:**

  ```python
  TEMPLATES = [
      {
          "BACKEND": "django.template.backends.django.DjangoTemplates",
          "DIRS": [
              BASE_DIR / "templates",
              BASE_DIR / "search_app/templates/search_app",
          ],
          # ... other settings
      }
  ]
  ```

- **Static Files:**

  ```python
  STATIC_URL = '/static/'
  STATIC_ROOT = BASE_DIR / 'staticfiles'
  STATICFILES_DIRS = [
      BASE_DIR / "theme/static",
  ]
  ```

## Running the Application

Start the Django development server to run the application locally.

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to access the AI-Powered Search Bar.

## Usage

### Accessing the Admin Interface

1. Navigate to `http://127.0.0.1:8000/admin/`.
2. Log in using the superuser credentials you created earlier.
3. Add `CollectableShoe` entries and their corresponding `ShoeDescription` using the admin interface.

### Performing Searches

- Use the search bar on the homepage to enter queries related to the available shoes.
- The AI Assistants will process your input to provide relevant search results and recommendations.
- Click on "Ask AI" to engage in a conversational query about the shoes.

## AI Assistants

This project utilizes three AI Assistants to enhance search functionality:

### 1. AISearchAssistant

- **Role:** Routes user queries to the appropriate AI Assistant based on the context.
- **Functionality:** Determines whether to use `ShoeRecommendationAssistant` or `RAGShoeAssistant`.

### 2. ShoeRecommendationAssistant

- **Role:** Provides recommendations based on specific details like brand, model, price, and artist.
- **Functionality:** Fetches and formats shoe data to present to the user.

### 3. RAGShoeAssistant

- **Role:** Offers background information and general knowledge about collectable shoes using a Retrieval-Augmented Generation (RAG) approach.
- **Functionality:** Utilizes `Langchain` and `TFIDFRetriever` to access and retrieve relevant shoe descriptions.

### Setting Up AI Assistants

1. **Create `ai_Assistant.py` in `search_app/`:**

   ```python
   # [Insert the ai_Assistant.py content here]
   ```

2. **Install Required Packages:**

   ```bash
   pip install langchain-community langchain-core scikit-learn
   ```

3. **Configure AI Assistants:**

   Ensure that the AI Assistants are correctly defined and integrated within the Django project. The assistants handle query routing and response generation based on user inputs.

## Contributing

Contributions are welcome! Follow these steps to contribute to the project:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your message here"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to reach out if you encounter any issues or have suggestions for improvements. Happy coding!
