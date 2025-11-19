YOLOv8 PPE Detector (Streamlit Web App)
A real-time Personal Protective Equipment (PPE) Detection system for automated safety monitoring in industrial environments.

Live Application
This application is deployed and hosted publicly.

https://ppe-detector-web-app.streamlit.app/

Key Features
1. 14-Class Detection: Detects both required safety gear (Hardhat, Gloves, Safety Vest) and violations (NO-Hardhat, NO-Gloves, NO-Mask).

2. Real-Time Ready: Utilizes YOLOv8s for fast inference on uploaded images and videos.

3. Interactive Demo: A Streamlit frontend allows users to upload files and adjust the Confidence Threshold.

## 💻 Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Model** | **YOLOv8s** | Core object detection engine. |
| **Frontend** | **Streamlit** | User interface and web application hosting. |
| **Deployment** | **Streamlit Cloud** | Hosts the public web app. |
| **Model Access** | **Google Drive + `gdown`** | Securely downloads the large `best.pt` file during deployment. |



Project Demo Screenshot












<img width="500" height="500" alt="PPE_Result1" src="https://github.com/user-attachments/assets/3d7d22e6-7af6-499a-86e3-e10d57b3d246" />











<img width="500" height="500" alt="PPE_Result2" src="https://github.com/user-attachments/assets/2355e34c-1ec3-4619-a424-a2bda4b7b269" />




<img width="500" height="500" alt="PPE_Result3" src="https://github.com/user-attachments/assets/e255114b-ac65-4df5-843b-b08a0a03fa43" />

























