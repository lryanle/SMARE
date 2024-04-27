<p align="center">
    <img src="./frontend/public/logos/smare.png" alt="Statefarm SMARE" style="width:384px;"/>
</p>
<hr><br>

<p align="center">
    <img src="https://img.shields.io/website?url=https%3A%2F%2Fsmare.lryanle.com&up_message=Online&up_color=%2357F287&down_message=Offline&down_color=E74C3C&style=for-the-badge&logo=https%3A%2F%2Fsmare.lryanle.com%2F_next%2Fimage%3Furl%3D%252Flogos%252Fsmare.png%26w%3D384%26q%3D75&logoColor=%23e1261c&label=smare.lryanle.com&color=2ecc71&link=https%3A%2F%2Fsmare.lryanle.com" alt="SMARE Website" />
    <img src="https://img.shields.io/github/commit-activity/t/lryanle/SMARE?style=for-the-badge" alt="GitHub commits" />
    <img src="https://img.shields.io/github/issues-pr/lryanle/SMARE?style=for-the-badge" alt="GitHub pull request" />
    <img src="https://img.shields.io/github/issues/lryanle/SMARE?style=for-the-badge" alt="GitHub issues" />
    <img src="https://img.shields.io/github/repo-size/lryanle/SMARE?style=for-the-badge" alt="GitHub Repo Size" />
    <img src="https://img.shields.io/github/license/lryanle/SMARE?style=for-the-badge" alt="Github License" />
</p>

<p align="center">The Social Marketplace Automotive Risk Engine (SMARE) Project. This project aims to detect supicious listings and potential instances of insurance fraud posted on the most popular social marketplace sites, such as Craigslist and Facebook Marketplace. In partnership between Statefarm and UTA CSE Senior Design. View the live deployment at <a href="https://smare.lryanle.com" target="_blank">smare.lryanle.com</a>.</p>

## 🔍 Table of Contents

* [💻 Stack](#stack)

* [📝 Project Summary](#project-summary)

* [⚙️ Setting Up](#setting-up)

* [🚀 Run Locally](#run-locally)

* [🙌 Contributors](#contributors)

* [📄 License](#license)

## 💻 Stack

- [**frontend**](frontend)
  - [Next](https://nextjs.org/): A React framework for building web applications with server-side rendering.
  - [Typescript](https://www.typescriptlang.org/): Typed superset of JavaScript that compiles to plain JavaScript.
  - [shadcn/ui](https://github.com/shadcn/ui): A UI library for React, built using Tailwind CSS.
  - [Tailwind](https://tailwindcss.com/): Utility-first CSS framework for rapidly building custom designs.
  - [Prisma](https://www.prisma.io/): Next-generation ORM for Node.js and TypeScript.
  - [Nextauth](https://next-auth.js.org/): Authentication for Next.js.
  - [Framer Motion](https://www.framer.com/motion/): A React library to power animations.
  - [Lucide](https://lucide.dev/): Open-source icon library.
  - [Rechart](https://recharts.org/en-US/): A composable charting library built on React components.
  - [Remark](https://remark.js.org/): A Markdown processor powered by plugins part of the unified collective.
  - [SWR](https://swr.vercel.app/): React Hooks library for data fetching.
  - [zod](https://github.com/colinhacks/zod): TypeScript-first schema validation with static type inference.
- [**backend**](backend)
  - [Selenium](https://www.selenium.dev/): A suite of tools for automating web browsers.
  - [BS4 (Beautiful Soup)](https://www.crummy.com/software/BeautifulSoup/): A Python library for pulling data out of HTML and XML files.
  - [Pymongo](https://pymongo.readthedocs.io/en/stable/): Python driver for MongoDB.
  - [Pandas](https://pandas.pydata.org/): A fast, powerful, flexible, and easy-to-use open-source data analysis and manipulation tool.
  - [Imblearn](https://imbalanced-learn.org/stable/): Python library to tackle the problem of imbalanced datasets.
  - [Loguru](https://github.com/Delgan/loguru): A Python logging library that aims to make life easier for developers.
  - [OpenAI API](https://openai.com/): A generative AI API.

## 📝 Project Summary

- [**frontend**](frontend): Contains the frontend application with various components and settings.
  - [**frontend/app**](app): The main page for the client-/customer-facing portion of our SaaS. Main feature is a dashboard to present information retreived from our pipeline.
  - [**frontend/app/api**](api): Our middleware to retrieve, process, and present information from our DB to the web application.
- [**backend**](backend): Houses backend logic including cleaners, models, scrapers, and utilities.
  - [**backend/src/cleaners**](cleaners): Contains all functionality related to cleaning data in the backend pipeline.
  - [**backend/src/models**](models): Contains our 6 models to score and help flag social marketplace listings that are suspicious.
  - [**backend/src/cleaners**](scrapes): Retrieves data from various social media marketplaces and places them in our data pipeline flow.
  - [**backend/src/utilities**](utilities): Utilities for all backend-related processes such as logging and our custom DB adapter.
- [**documentation**](documentation): Contains project documentation including sprint reports and charters.

## ⚙️ Setting Up

### Database Access

Make a copy of the ``.env.example`` file and make the following changes.

1. remove ``.example`` from the extension

2. Paste the username and password provided in MongoDB Atlas (if you should have access but do not, please contact @waseem-polus)
  
3. Paste the connection URL provided provided in MongoDB Atlas. Include the password and username fields using ``${VARIABLE}`` syntax to embed the value of the variable

### Run Scrapers locally
**Prerequisites**
- python3
- pipenv

**Installing dependencies**  
Navigate to ``scrapers/`` and open the virtual environment using
```bash
pipenv shell
```
Then install dependencies using
```bash
pipenv install
```

**Scraper Usage**  
To create build a **production-ready** Docker Image use
```bash
pipenv run build
```
To create build a **development** Docker Image use
```bash
pipenv run dev
```

If there is an existing smarecontainer, run the following:
```bash
pipenv run stop
```

To run a docker container "smarecontainer" use (Note: delete any containers with the same name before running)
```bash
pipenv run cont
```
then
```bash
# Scrape Craigsist homepage
pipenv run craigslist

# Scrape Facebook Marketplace homepage
pipenv run facebook
```

## 🙌 Contributors

<table style="border:1px solid #404040;text-align:center;width:100%">
<tr><td style="width:14.29%;border:1px solid #404040;" width="130px" valign="top" align="center">
        <a href="https://github.com/waseem-polus" spellcheck="false" align="center">
          <img src="https://avatars.githubusercontent.com/u/69316929?v=4?s=100" width="100px;" alt="waseem-polus"/>
          <br />
          <b>Waseem Polus</b>
        </a>
      </td><td style="width:14.29%;border:1px solid #404040;" width="130px" valign="top" align="center">
        <a href="https://github.com/lryanle" spellcheck="false" align="center">
          <img src="https://avatars.githubusercontent.com/u/31494954?v=4?s=100" width="100px;" alt="lryanle"/>
          <br />
          <b>Ryan Lahlou</b>
        </a>
      </td><td style="width:14.29%;border:1px solid #404040;" width="130px" valign="top" align="center">
        <a href="https://github.com/temitayoaderounmu" spellcheck="false" align="center">
          <img src="https://avatars.githubusercontent.com/u/91757922?v=4?s=100" width="100px;" alt="temitayoaderounmu"/>
          <br />
          <b>Temitayo Aderounmu</b>
        </a>
      </td><td style="width:14.29%;border:1px solid #404040;" width="130px" valign="top" align="center">
        <a href="https://github.com/athiya26" spellcheck="false" align="center">
          <img src="https://avatars.githubusercontent.com/u/123428427?v=4?s=100" width="100px;" alt="athiya26"/>
          <br />
          <b>Athiya Manoj</b>
        </a>
      </td><td style="width:14.29%;border:1px solid #404040;" width="130px" valign="top" align="center">
        <a href="https://github.com/Yeabgezz" spellcheck="false" align="center">
          <img src="https://avatars.githubusercontent.com/u/90985279?v=4?s=100" width="100px;" alt="Yeabgezz"/>
          <br />
          <b>Yeabsra Gebremeskel</b>
        </a>
      </td></tr></table>


## 📊 Statistics

![Metrics](/github-metrics.svg)
![Pagespeed](/metrics.plugin.pagespeed.svg)
[![SMAREScreenShot](/metrics.plugin.screenshot.svg)](https://smare.lryanle.com/)

## 📄 License

This project is licensed under the **MIT License** - see the [**MIT License**](https://github.com/lryanle/SMARE/blob/main/LICENSE) file for details.
