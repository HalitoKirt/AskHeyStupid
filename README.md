# AskHeyStupid
A playful website for asking a question, in return you will get a dumb-dumb answer.  Not all AI has to be smart.  Powered by AWS, this project follows AWS Well-Architected Framework and AWS Security Best Practices. 
---

## Architecture

-- Browser → CloudFront → S3 → API Gateway → Lambda → Amazon Bedrock

---

## Security

- HTTPS enforced via CloudFront
- Origin Access Control (OAC)
- IAM least-privilege roles
- Controlled API exposure via API Gateway
  
---

## Key Features

- Serverless architecture (no infrastructure management)
- AI-powered responses (Bedrock + Claude)
- Secure, production-style AWS design
- CDN-backed global delivery via CloudFront
- Clean separation of frontend and backend

---

## Design Decisions

- This design was implemented over Amplify to display core AWS security and building skills.  Amplify, fully managed, would have been easier and faster
- Integrated Amazon Bedrock (Claude) with controlled prompt design to manage response output.  This application goes against their natural training of factual, grounded,          context aware and relevant responses.  Prompting consisted of repeating of words like “dumb”, “useless” and “not relevant” to help counter it natural responses.  Also, raised   the temp for more creativity
- Ask Hey Stupid originally explored a Bedrock Agent path. During testing, I found that direct Bedrock integration was a better fit for controlling response behavior and          reducing complexity. That change made the solution more secure, more efficient, and easier to operate.  

---

## Why This Project Matters

This project demonstrates:

- Real-world cloud architecture design
- Secure integration of AI services in AWS
- Understanding of serverless application patterns
- Ability to build, deploy, and troubleshoot production-style systems

---

## Challenges

- Resolved CORS preflight failures
- Debugged API Gateway routing issues
- Managed IAM permissions across services

---

## Future Improvements

- Add merch and accept payments
- Add authentication (Amazon Cognito) for customers
- Enhance prompt engineering for stricter response control
- Expand frontend UI/UX

---

## Author

Built by Randall  
Cloud Security Engineer focused on securing AI-powered AWS workloads.

---

## 🔗 Live Demo 

visit www.askheystupid.com for stupid fun. 

