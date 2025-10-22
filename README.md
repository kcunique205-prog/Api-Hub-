<div align="center">

# 🔮 ApiHub - Your Gateway to Free APIs & Code 🔮

**A dynamic web application built with Flask and Python, integrated with a Telegram bot for secure user access. Discover and use a curated collection of free APIs and source codes.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-2.x-green?style=for-the-badge&logo=flask" alt="Flask Version">
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram" alt="Telegram Bot">
  <img src="https://img.shields.io/badge/Deployment-Render-brightgreen?style=for-the-badge&logo=render" alt="Deployed on Render">
</p>

![ApiHub Showcase](https://i.imgur.com/8a1b2c3.png) 
*A live preview of the ApiHub interface.*

</div>

---

## ✨ Features

ApiHub sirf ek project nahi, ek complete developer toolkit hai.

-   🔐 **Secure Telegram Authentication:** Users get a one-time access code from a Telegram bot to enter the site.
-   🚀 **Dynamic Frontend:** A beautiful, responsive, and modern UI with dark mode support.
-   ⚙️ **Powerful Admin Panel:**
    -   View live site statistics (`Total Visits`, `Active Users`).
    -   Add new APIs and source codes directly from the UI.
    -   Secure login for admin-only access.
-   ⚡ **Blazing Fast & Smooth:** Optimized for performance with a clean and intuitive user experience.
-   🔍 **Search & Filter:** Easily find what you're looking for with instant search and category filters.
-   ☁️ **Cloud Ready:** Designed to be deployed seamlessly on cloud platforms like Render.

---

## 🛠️ Tech Stack

| Component         | Technology                                                                                                                              |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend**       | <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white" alt="Flask"> |
| **Frontend**      | <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white" alt="HTML5"> <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white" alt="CSS3"> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black" alt="JavaScript"> |
| **Bot**           | <img src="https://img.shields.io/badge/pyTelegramBotAPI-0088cc?style=flat&logo=telegram" alt="pyTelegramBotAPI">                            |
| **Deployment**    | <img src="https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white" alt="Render"> <img src="https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white" alt="Gunicorn"> |
| **Icons**         | <img src="https://img.shields.io/badge/Feather-FFFFFF?style=flat&logo=feather" alt="Feather Icons">                                       |

---

## 🚀 Getting Started & Deployment

Deploying your own instance of ApiHub is easy. Follow these steps to get it live on Render.

### 1. Fork & Setup GitHub Repository

-   **Fork** this repository to your own GitHub account.
-   Ensure your repository has the following structure:
    ```
    /
    ├── app.py
    ├── requirements.txt
    └── templates/
        ├── index.html
        └── access_page.html
    ```

### 2. Create a Telegram Bot

-   Go to **@BotFather** on Telegram.
-   Create a new bot using the `/newbot` command.
-   You will get a **Bot Token**. Save it.
-   Get your personal **Telegram User ID** from a bot like `@userinfobot`.

### 3. Deploy on Render

1.  Click the button below to deploy directly to Render:

    [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

2.  Connect your GitHub repository.
3.  In the **Environment** section, add the following environment variables:
    -   **`BOT_TOKEN`**: Your Telegram bot token.
    -   **`ADMIN_TELEGRAM_ID`**: Your personal Telegram user ID.
    -   **`SECRET_KEY`**: A long, random string for Flask sessions (e.g., `your_super_secret_key_12345`).

4.  Set the **Start Command** to:
    ```sh
    gunicorn "app:app"
    ```
5.  Click **"Create Web Service"**. Your app will be live in a few minutes!

---

## 🤖 Bot Commands

Interact with your ApiHub instance directly from Telegram.

-   `/start` or `/getcode` - Generates a new 6-digit access code for the website.
-   `/stats` - (Admin Only) Fetches and displays the current website statistics.

---

## 👨‍💻 Developer

-   **Author:** Diwas
-   **Telegram:** [@nepalxd](https://t.me/nepalxd)

<div align="center">

**Made with ❤️ and a lot of Python.**

</div>
