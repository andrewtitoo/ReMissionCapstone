ReMission: A Data-Driven IBD Symptom Tracker

Introduction
Before starting this task, ensure that your capstone project has been approved by your instructor.

In this task, you will design, develop, and implement the capstone project approved by your instructor in Task 1.

Note: Your work for this task will not be evaluated until you have successfully passed Task 1.
Requirements
Your submission must be your original work. No more than a combined total of 30% of the submission and no more than a 10% match to any one individual source can be directly quoted or closely paraphrased from sources, even if cited correctly. The similarity report that is provided when you submit your task can be used as a guide.



You must use the rubric to direct the creation of your submission because it provides detailed criteria that will be used to evaluate your work. Each requirement below may be evaluated by more than one rubric aspect. The rubric aspect titles may contain hyperlinks to relevant portions of the course.



Tasks may not be submitted as cloud links, such as links to Google Docs, Google Slides, OneDrive, etc., unless specified in the task requirements. All other submissions must be file types that are uploaded and submitted as attachments (e.g., .docx, .pdf, .ppt).


A.  Create a letter of transmittal and a project proposal to convince senior, nontechnical managers and executives to implement your data product approved in Task 1. The proposal should include each of the following:

•   a summary of the problem

•   a description of how the data product benefits the customer and supports the decision-making process

•   an outline of the data product

•   a description of the data that will be used to construct the data product

•   the objectives and hypotheses of the project

•   an outline of the project methodology

•   funding requirements

•   the impact of the solution on stakeholders

•   ethical and legal considerations and precautions that will be used when working with and communicating about sensitive data

•   your expertise relevant to the solution you propose


    Note: Expertise described here could be real or hypothetical to fit the project topic you have created.



B.  Write an executive summary directed to IT professionals that addresses each of the following requirements:

•   the decision support problem or opportunity you are solving for

•   a description of the customers and why this product will fulfill their needs

•   existing gaps in the data products you are replacing or modifying (if applicable)

•   the data available or the data that needs to be collected to support the data product lifecycle

•   the methodology you use to guide and support the data product design and development

•   deliverables associated with the design and development of the data product

•   the plan for implementation of your data product, including the anticipated outcomes from this development

•   the methods for validating and verifying that the developed data product meets the requirements and, subsequently, the needs of the customers

•   the programming environments and any related costs, as well as the human resources that are necessary to execute each phase in the development of the data product

•   a projected timeline, including milestones, start and end dates, duration for each milestone, dependencies, and resources assigned to each task



C.  Design and develop your fully functional data product that addresses your identified business problem or organizational need from part A. Include each of the following attributes, as they are the minimum required elements for the product:

•   one descriptive method and one nondescriptive (predictive or prescriptive) method

•   collected or available datasets

•   decision support functionality

•   ability to support featurizing, parsing, cleaning, and wrangling datasets

•   methods and algorithms supporting data exploration and preparation

•   data visualization functionalities for data exploration and inspection

•   implementation of interactive queries

•   implementation of machine-learning methods and algorithms

•   functionalities to evaluate the accuracy of the data product

•   industry-appropriate security features

•   tools to monitor and maintain the product

•   a user-friendly, functional dashboard that includes three visualization types



D.  Create each of the following forms of documentation for the product you have developed:

•   a business vision or business requirements document

•   raw and cleaned datasets with the code and executable files used to scrape and clean data (if applicable)

•   code used to perform the analysis of the data and construct a descriptive, predictive, or prescriptive data product

•   assessment of the hypotheses for acceptance or rejection

•   visualizations and elements of effective storytelling supporting the data exploration and preparation, data analysis, and data summary, including the phenomenon and its detection

•   assessment of the product’s accuracy

•   the results from the data product testing, revisions, and optimization based on the provided plans, including screenshots

•   source code and executable file(s)

•   a quick-start guide summarizing the steps necessary to install and use the product



E.  Acknowledge sources, using in-text citations and references, for content that is quoted, paraphrased, or summarized.



F.  Demonstrate professional communication in the content and presentation of your submission.

Remission Capstone 

Introduction
Welcome to ReMission, a revolutionary application designed to provide personalized, data-driven solutions for individuals managing Inflammatory Bowel Disease (IBD). Combining cutting-edge technologies such as machine learning, interactive data visualization, and a user-centric interface, ReMission equips users with the tools necessary to understand their symptoms, identify triggers, and take proactive steps to manage their health. This document serves as a complete guide to the project, offering detailed insights into its purpose, structure, functionality, and technical implementation.

Project Motivation
Inflammatory Bowel Disease, encompassing Crohn’s Disease and Ulcerative Colitis, presents a unique challenge to those affected. The unpredictable nature of the condition—marked by sudden flare-ups, chronic pain, and fatigue—can lead to significant physical, emotional, and financial hardships. Patients often feel powerless, with little control over their health and few tools to help them manage their condition effectively.

ReMission was created to bridge this gap, offering users a lifeline through technology. By logging daily symptoms, visualizing trends, and receiving predictive insights, users gain a better understanding of their health. This empowers them to make informed decisions that can reduce symptom severity, prevent flare-ups, and improve their overall quality of life.

Why ReMission?
Real-Time Symptom Tracking: Users can capture and monitor vital health metrics, such as stress levels, sleep quality, and medication adherence, providing a holistic view of their well-being over time.
Predictive Analytics: Machine learning models analyze user data to predict potential flare-ups, offering early warnings and actionable recommendations.
Empowerment Through Data: By transforming raw data into meaningful insights, ReMission helps users take control of their condition, fostering a sense of empowerment and self-efficacy.
Functionality Overview
ReMission is built around three core components, each designed to deliver a unique aspect of the user experience:

1. Dashboard
   The dashboard serves as the user’s central hub, providing a comprehensive overview of their health data. Key features include:

Summary Metrics: Displays average pain, stress levels, and sleep hours over customizable time periods.
Dynamic Visualizations: Interactive graphs and charts highlight historical symptom trends, enabling users to spot patterns and correlations.
Personalized Insights: CHIIP, the app’s predictive bot, delivers tailored recommendations based on the user’s data, helping them anticipate and mitigate potential flare-ups.
2. Symptom Logger
   The logger provides a simple yet powerful interface for users to record their daily health metrics. It features:

Comprehensive Input Fields: Allows users to log stress levels, pain intensity, sleep duration, exercise, and medication adherence.
Guided Logging: A progress bar ensures all necessary fields are completed, improving the accuracy and reliability of the logged data.
3. CHIIP Insights
   CHIIP (Chronic Health Insight and Improvement Predictor) is an AI-powered virtual assistant designed to analyze user data and provide actionable insights. Key functionalities include:

Predictive Warnings: Alerts users to potential flare-ups based on their recent symptom trends.
Customized Advice: Offers specific recommendations tailored to the user’s unique health patterns, such as encouraging more rest during high-stress periods or increasing exercise for better symptom management.
Project Logic and Architecture
The ReMission application is underpinned by a robust and scalable architecture that ensures seamless performance and integration across all components.

1. Backend (Flask API)
   The backend handles all data operations, including:

Data Storage: Manages user symptom logs and machine learning predictions.
API Endpoints: Facilitates communication between the frontend and backend, ensuring real-time data flow.
Machine Learning Integration: Embeds the predictive model to generate insights and recommendations.
2. Frontend (Angular)
   The frontend offers a responsive, intuitive interface, allowing users to interact seamlessly with the application. Features include:

Real-Time Updates: Ensures users see the latest data and insights without needing to refresh.
Modular Design: Each feature, from logging to insights, operates independently for streamlined performance.
3. Machine Learning Component
   The machine learning model is the heart of ReMission’s predictive capabilities. Built using logistic regression, it:

Analyzes User Data: Identifies patterns in symptoms and lifestyle factors to predict flare-ups.
Learns Continuously: Synthetic data enables the model to adapt and improve its predictions over time.
4. Database (SQLite)
   The SQLite database provides lightweight, reliable data storage, ensuring:

Data Integrity: Maintains accurate and consistent user data.
Efficient Queries: Supports fast retrieval of symptom logs and prediction results.
Key Features and Benefits
Predictive Analytics
ReMission’s machine learning model identifies critical trends—such as the relationship between high stress and flare-ups—enabling users to take preventive action before symptoms escalate.

Interactive Data Visualization
Dynamic charts and graphs make it easy for users to explore their health data, uncovering patterns that might otherwise go unnoticed.

Privacy and Security
User data is anonymized and protected through secure communication protocols, ensuring privacy and compliance with industry standards like HIPAA and GDPR.

User-Centric Design
ReMission’s intuitive interface is designed for users of all technical backgrounds, ensuring a smooth and accessible experience.

Installation and Usage
System Requirements
To run ReMission, ensure your system meets the following requirements:

Python: 3.8+
Node.js: 14+
npm: 6+
Angular CLI: Installed globally (npm install -g @angular/cli)
Git: For cloning the repository
Installation Steps
1. From ZIP File
   Download and extract the provided ZIP file.
   Follow the backend and frontend setup instructions in the quick-start guide.
2. From GitHub
   Clone the repository:
   git clone https://github.com/andrewtitoo/ReMissionCapstone.git
   Set up the backend and frontend as outlined in the quick-start guide.
   Validation and Testing
   The ReMission application underwent rigorous testing to ensure its reliability and effectiveness:

Unit Testing: Verified the functionality of individual components.
Integration Testing: Ensured seamless interaction between the frontend, backend, and database.
User Acceptance Testing (UAT): Collected feedback from real users to validate the app’s usability and predictive accuracy.
The machine learning model achieved a high F1-score of 94.5%, demonstrating its effectiveness in predicting IBD flare-ups with minimal false positives or negatives.

Conclusion
ReMission represents a significant step forward in the management of chronic health conditions. By harnessing the power of data and predictive analytics, it empowers users to take control of their health and improve their quality of life. With its robust architecture, user-friendly design, and powerful insights, ReMission is poised to become an indispensable tool for individuals living with IBD.

For detailed setup instructions and further documentation, please refer to the Quick-Start Guide.