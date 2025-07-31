
# **Real-Time Email Delivery Checker**

A web application for **real-time email delivery checking**.  
Designed for teams that need to quickly verify whether emails land in **Inbox**, **Spam**, or are **Not Found**, with detailed analytics and user management.

---

## **Features**

### **1. Authentication**
- **Secure login** with no public registration.  
- **Single-device login only** to prevent unauthorized access.  

### **2. User Management**
- Admin can **create and manage multiple users**.  
- All user data stored in **MySQL** for easy management and scalability.  

### **3. Email Delivery Checker**
- Connect up to **10 Gmail accounts** via **App Passwords**.  
- **Search** by sender **name** or **email** across multiple connected mailboxes.  
- **Real-time results** categorized as:  
  - **Inbox**  
  - **Spam**  
  - **Not Found**  

### **4. Analytics**
- **Visual percentage boxes** displaying **Inbox vs Spam delivery rates** (0–100%).  
- Dynamic updates based on recent checks.  

### **5. Powerful Search**
- **Comprehensive search bar** to filter results by sender name or email.  
- Instant results for **Inbox**, **Spam**, and **Not Found** categories.  

### **6. Design**
- UI built following a **carefully crafted design** for clarity and usability.  
- Responsive layout for desktop and mobile users.  

---

## **Tech Stack**
- **Frontend:** Vue 3 + Vite + Tailwind (with dark/light mode support)  
- **Backend & Email Processing:** Python 3.10 (IMAP + real-time parsing)
- **Server:** Ubuntu 24.04, Nginx, Supervisor  
- **Database:** MySQL  

---

## **Use Cases**
- Verify whether emails are landing in **Inbox or Spam**.  
- **Track delivery performance** across multiple accounts.  
- **Audit & troubleshoot** email campaigns quickly.  



---

